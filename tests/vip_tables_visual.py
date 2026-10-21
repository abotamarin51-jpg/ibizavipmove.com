"""Review the generated VIP Tables page without contacting third parties or Analytics."""
from __future__ import annotations

from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
from threading import Thread
from urllib.parse import urlsplit

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

CANONICAL = 'https://ibizavipmove.com/vip-tables-club-access-ibiza/'
PATH = '/vip-tables-club-access-ibiza/'
WA_PATH = '/34600703303'
PLACEHOLDERS = (
    '[URL DE UNA IMAGEN PROPIA, 1200x630]',
    '[MISMA IMAGEN]',
    '[FECHA]',
    '[YYYY-MM-DD]',
    '[CONFIRMAR: deja solo los venues donde realmente puedes solicitar mesas]',
    '[OPCIONAL: añade aquí rangos reales y actuales solo si puedes respaldarlos.',
)
GEOMETRY = """el=>{const r=el.getBoundingClientRect();const top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
return {left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height,
focused:document.activeElement===el,unobstructed:top===el||el.contains(top),
overflow:document.documentElement.scrollWidth>innerWidth+1}}"""


def verify_image(path: Path) -> None:
    with Image.open(path) as image:
        variance = ImageStat.Stat(image.convert('RGB')).var
        assert max(variance) > 1, f'Blank or uniform screenshot: {path.name}'


def visible(page, selector: str, expected: bool) -> None:
    page.wait_for_function("""([selector,expected])=>{const el=document.querySelector(selector);if(!el)return false;
      const s=getComputedStyle(el),r=el.getBoundingClientRect();const state=s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>0&&r.width>0&&r.height>0;
      return state===expected;}""", arg=[selector, expected], timeout=7000)


def actionable(locator) -> dict:
    locator.scroll_into_view_if_needed()
    locator.focus()
    locator.click(trial=True, timeout=7000)
    geometry = locator.evaluate(GEOMETRY)
    assert geometry['focused'] and geometry['unobstructed'], geometry
    assert not geometry['overflow'], geometry
    assert geometry['left'] >= -1 and geometry['top'] >= -1, geometry
    assert geometry['right'] <= locator.page.viewport_size['width'] + 1, geometry
    assert geometry['bottom'] <= locator.page.viewport_size['height'] + 1, geometry
    assert geometry['width'] >= 24 and geometry['height'] >= 24, geometry
    return geometry


def review(root: Path, output: Path) -> dict:
    root = root.resolve()
    output = output.resolve()
    assert (root / PATH.strip('/') / 'index.html').is_file(), 'Generated VIP Tables page missing'
    assert not output.is_relative_to(root), 'Evidence must not enter website output'
    output.mkdir(parents=True, exist_ok=True)
    chrome = next((shutil.which(name) for name in (
        'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'
    ) if shutil.which(name)), None)
    assert chrome, 'Existing runner Chrome/Chromium is required'

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    report = {
        'commit': os.environ.get('GITHUB_SHA'),
        'page': CANONICAL,
        'mode': 'built_artifact',
        'results': [],
        'limitations': [
            'Chromium viewport emulation, not physical Safari or native WhatsApp.',
            'No message, form, call or Analytics request is sent.',
            'Bracketed owner confirmations intentionally remain unresolved.',
        ],
    }
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=chrome, headless=True)
            report['browser'] = browser.version
            try:
                for mode, width, height in (('desktop', 1366, 768), ('mobile', 390, 844)):
                    context = browser.new_context(
                        viewport={'width': width, 'height': height},
                        is_mobile=mode == 'mobile', has_touch=mode == 'mobile',
                        service_workers='block', accept_downloads=False,
                    )
                    blocked = []
                    errors = []
                    missing = []

                    def allow_local_only(route):
                        request = route.request
                        parsed = urlsplit(request.url)
                        static_font = (
                            parsed.hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'}
                            and request.method == 'GET'
                            and request.resource_type in {'stylesheet', 'font'}
                        )
                        if request.url.startswith(origin + '/') or static_font:
                            route.continue_()
                        else:
                            blocked.append({
                                'host': parsed.hostname, 'path': parsed.path,
                                'method': request.method, 'type': request.resource_type,
                            })
                            route.abort()

                    context.route('**/*', allow_local_only)
                    context.route_web_socket('**/*', lambda ws: ws.close())
                    try:
                        page = context.new_page()
                        page.on('pageerror', lambda error: errors.append(str(error)))
                        page.on('response', lambda response: missing.append({
                            'url': response.url, 'status': response.status,
                        }) if response.status >= 400 and response.url.startswith(origin + '/') else None)
                        response = page.goto(origin + PATH, wait_until='load', timeout=30000)
                        assert response and response.status == 200
                        page.evaluate('document.fonts.ready')
                        assert page.evaluate("document.fonts.check('16px Manrope')"), 'Site font did not load'
                        page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=7000)
                        page.evaluate('window.IVMCookieConsent.reject()')

                        assert page.locator('link[rel="canonical"]').get_attribute('href') == CANONICAL
                        assert page.locator('h1').count() == 1
                        assert page.locator('h1').inner_text().strip() == 'VIP tables and club access in Ibiza, arranged privately.'
                        assert page.locator('table').count() == 2
                        assert page.locator('details').count() == 8
                        assert page.locator('nav.ivm-language-links a').count() == 1
                        assert page.locator('nav.ivm-language-links a').get_attribute('aria-current') == 'page'
                        source = page.content()
                        for marker in PLACEHOLDERS:
                            assert marker in source, f'Missing unresolved marker: {marker}'

                        main_wa = page.locator('main a[href^="https://wa.me/"]')
                        assert main_wa.count() == 3
                        paths = main_wa.evaluate_all('els=>els.map(a=>new URL(a.href).pathname)')
                        assert set(paths) == {WA_PATH}
                        actions = []
                        for locator in (main_wa.nth(0), main_wa.nth(1), main_wa.nth(2), page.locator('nav.ivm-language-links a')):
                            actions.append({'label': locator.inner_text().strip(), 'geometry': actionable(locator)})

                        wrappers = page.locator('div[style*="overflow-x:auto"]')
                        assert wrappers.count() == 2
                        page_width_ok = not page.evaluate('document.documentElement.scrollWidth > innerWidth + 1')
                        assert page_width_ok, 'Page creates horizontal viewport overflow'
                        table_metrics = wrappers.evaluate_all("""els=>els.map(el=>({
                          clientWidth:el.clientWidth,scrollWidth:el.scrollWidth,
                          tableWidth:el.querySelector('table').getBoundingClientRect().width
                        }))""")

                        bar = page.locator('.mobile-bar')
                        floating = page.locator('.ivm-whatsapp-float')
                        assert bar.count() == 1 and floating.count() == 1
                        target = '.mobile-bar' if mode == 'mobile' else '.ivm-whatsapp-float'
                        other = '.ivm-whatsapp-float' if mode == 'mobile' else '.mobile-bar'
                        visible(page, target, True)
                        visible(page, other, False)
                        if mode == 'mobile':
                            menu = page.locator('.menu-btn')
                            menu.click()
                            visible(page, '.mobile-menu', True)
                            visible(page, '.mobile-bar', False)
                            menu.click()
                            visible(page, '.mobile-bar', True)

                        page.evaluate('window.IVMCookieConsent.open()')
                        visible(page, target, False)
                        page.evaluate('window.IVMCookieConsent.reject()')
                        visible(page, target, True)

                        assert not errors and not missing, {
                            'javascriptErrors': errors, 'missingLocalResources': missing,
                        }
                        screenshot = output / f'vip-tables-{mode}.png'
                        page.screenshot(path=str(screenshot), full_page=True)
                        assert screenshot.stat().st_size > 10000
                        verify_image(screenshot)
                        result = {
                            'mode': mode, 'viewport': [width, height], 'httpStatus': response.status,
                            'actions': actions, 'tables': table_metrics, 'viewportOverflow': not page_width_ok,
                            'blockedExternalRequests': blocked, 'javascriptErrors': errors,
                            'missingLocalResources': missing, 'screenshot': screenshot.name,
                            'status': 'PASS',
                        }
                        report['results'].append(result)
                        print(f'PASS: VIP Tables page browser review: {mode}')
                    finally:
                        context.close()
            finally:
                browser.close()
        report['status'] = 'PASS'
    except Exception as error:
        report['status'] = 'FAILED_OR_BLOCKED'
        report['error'] = f'{type(error).__name__}: {error}'
        raise
    finally:
        server.shutdown()
        server.server_close()
        (output / 'vip-tables-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    return report


if __name__ == '__main__':
    review(
        Path('_site'),
        Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-vip-tables-review',
    )
