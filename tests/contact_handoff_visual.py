"""Review built English Contact without sending briefs or Analytics requests."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
import json
import os
import shutil

from PIL import Image, ImageStat
from playwright.sync_api import sync_playwright

LABEL = 'Continue to WhatsApp'
HELPER = 'Opens WhatsApp with your details. Review the message and press Send there.'


def verify_image(path, size=None):
    with Image.open(path) as image:
        if size is not None and image.size != size:
            raise AssertionError(f'Unexpected screenshot dimensions: {image.size}')
        variance = ImageStat.Stat(image.convert('RGB')).var
        if max(variance) <= 1:
            raise AssertionError(f'Blank or uniform screenshot: {path.name}')
        return variance


def main():
    root = Path('_site').resolve()
    output = (Path(os.environ['RUNNER_TEMP']) / 'ivm-contact-review').resolve()
    assert (root / 'contact/index.html').is_file(), 'Built Contact page missing'
    assert not output.is_relative_to(root), 'Evidence must not enter the website'
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
    report = {'commit': os.environ.get('GITHUB_SHA'), 'results': []}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=chrome, headless=True)
            report['browser'] = browser.version
            try:
                for mode, width, height in (('desktop', 1366, 768), ('mobile', 390, 844)):
                    context = browser.new_context(
                        viewport={'width': width, 'height': height},
                        is_mobile=mode == 'mobile', has_touch=mode == 'mobile',
                        service_workers='block',
                    )
                    denied = []
                    errors = []
                    missing = []

                    def allow_local_only(route):
                        request = route.request
                        static_font = (urlsplit(request.url).hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'}
                            and request.method == 'GET' and request.resource_type in {'stylesheet', 'font'})
                        # Only existing static fonts may leave localhost; contact and Analytics requests are denied.
                        if request.url.startswith(origin + '/') or static_font:
                            route.continue_()
                        else:
                            denied.append(route.request.resource_type)
                            route.abort()

                    context.route('**/*', allow_local_only)
                    try:
                        page = context.new_page()
                        page.on('pageerror', lambda error: errors.append(str(error)))
                        page.on('response', lambda response: missing.append(response.url)
                                if response.status >= 400 and response.url.startswith(origin + '/') else None)
                        response = page.goto(origin + '/contact/', wait_until='load', timeout=15000)
                        assert response and response.status == 200
                        page.evaluate('document.fonts.ready')
                        assert page.evaluate("document.fonts.check('16px Manrope')"), 'Site font did not load'
                        page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=5000)
                        page.evaluate('window.IVMCookieConsent.reject()')
                        button = page.locator('#conciergeForm button[type="submit"]')
                        assert button.count() == 1 and button.inner_text() == LABEL
                        assert page.get_by_text(HELPER, exact=False).count() == 1
                        button.scroll_into_view_if_needed()
                        button.focus()
                        page.wait_for_function("""() => {
                            let el = document.querySelector('#conciergeForm button[type="submit"]');
                            for (; el; el = el.parentElement) {
                                const s = getComputedStyle(el);
                                if (s.display === 'none' || s.visibility !== 'visible' || Number(s.opacity) < .99) return false;
                            }
                            return true;
                        }""", timeout=5000)
                        geometry = button.evaluate("""b => {
                            const r = b.getBoundingClientRect();
                            const top = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
                            return {left:r.left, top:r.top, right:r.right, bottom:r.bottom,
                              width:r.width, height:r.height, focused:document.activeElement===b,
                              unobstructed:top===b || b.contains(top),
                              overflow:document.documentElement.scrollWidth > innerWidth + 1};
                        }""")
                        assert geometry['focused'] and geometry['unobstructed'], geometry
                        assert not geometry['overflow'], geometry
                        assert geometry['left'] >= 0 and geometry['top'] >= 0, geometry
                        assert geometry['right'] <= width and geometry['bottom'] <= height, geometry
                        assert geometry['width'] >= 24 and geometry['height'] >= 24, geometry
                        assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com/contact/'
                        assert page.locator('h1').count() == 1
                        targets = page.evaluate("""() => ({
                            wa:[...document.querySelectorAll('a[href^="https://wa.me/"]')].map(a=>new URL(a.href).pathname),
                            tel:[...document.querySelectorAll('a[href^="tel:"]')].map(a=>a.getAttribute('href'))
                        })""")
                        assert targets['wa'] and set(targets['wa']) == {'/34600703303'}
                        assert targets['tel'] and set(targets['tel']) == {'tel:+34600703303'}
                        assert not errors and not missing, {'scriptErrors': errors, 'missingLocalResources': missing}
                        screenshot = output / f'contact-{mode}.png'
                        page.screenshot(path=str(screenshot))
                        variance = verify_image(screenshot, (width, height))
                        full = output / f'contact-{mode}-full.png'
                        page.screenshot(path=str(full), full_page=True)
                        verify_image(full)
                        report['results'].append({'mode': mode, 'viewport': [width, height],
                            'geometry': geometry, 'variance': variance, 'blockedExternalRequests': len(denied),
                            'javascriptErrors': errors, 'missingLocalResources': missing,
                            'label': LABEL, 'helper': HELPER, 'contactTargets': targets})
                        print(f'PASS: Contact handoff, focus, bounds and nonblank screenshots: {mode}')
                    finally:
                        context.close()
            finally:
                browser.close()
    except Exception as error:
        report['error'] = str(error)
        raise
    finally:
        server.shutdown()
        server.server_close()
        (output / 'report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
