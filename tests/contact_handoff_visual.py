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
from private_office_handoff_check import review as review_private_office
from private_office_handoff_check import self_test as self_test_private_office
from vip_tables_visual import review as review_vip_tables

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


def review_home_vip_link(page, origin, mode, width, height, output):
    """Check the internal Home link; never activate a contact destination."""
    response = page.goto(origin + '/', wait_until='load', timeout=15000)
    assert response and response.status == 200
    page.evaluate('document.fonts.ready')
    assert page.evaluate("document.fonts.check('16px Manrope')"), 'Home font did not load'
    link = page.locator('a[href="/vip-services-ibiza/"]').filter(has_text='VIP hospitality requests')
    assert link.count() == 1, 'Expected exactly one Home VIP hospitality link'
    assert link.inner_text() == 'VIP hospitality requests'
    assert link.locator('..').inner_text() == 'We coordinate chauffeur transport, villas, yachts, aviation, VIP hospitality requests and security around each stay.'
    assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com/'
    # Avoid sampling geometry midway through the site's normal smooth scrolling.
    link.evaluate('e => e.scrollIntoView({block: "center", behavior: "instant"})')
    page.wait_for_function('''() => {
        let e = document.querySelector('a[href="/vip-services-ibiza/"]');
        for (; e; e = e.parentElement) {
            const s = getComputedStyle(e);
            if (s.display === 'none' || s.visibility !== 'visible' || Number(s.opacity) < .99) return false;
        }
        return true;
    }''', timeout=5000)
    link.focus()
    page.keyboard.press('Tab')
    page.keyboard.press('Shift+Tab')
    link.evaluate('e => e.scrollIntoView({block: "center", behavior: "instant"})')
    state = link.evaluate('''e => {
        const s = getComputedStyle(e);
        const rects = [...e.getClientRects()].filter(r => r.width && r.height);
        return {focused: document.activeElement === e,
            focusVisible: e.matches(':focus-visible'), outline: s.outlineStyle, outlineWidth: s.outlineWidth,
            underline: s.textDecorationLine.includes('underline'), color: s.color,
            inheritedColor: s.color === getComputedStyle(e.parentElement).color,
            overflow: document.documentElement.scrollWidth > innerWidth + 1,
            visibleRects: rects.length,
            rects: rects.map(r => ({left:r.left, top:r.top, right:r.right, bottom:r.bottom})),
            bounded: rects.every(r => r.left >= 0 && r.top >= 0 && r.right <= innerWidth && r.bottom <= innerHeight),
            unobstructed: rects.every(r => { const t = document.elementFromPoint(r.x+r.width/2, r.y+r.height/2); return t === e || e.contains(t); })};
    }''')
    screenshot = output / f'home-vip-link-{mode}.png'
    page.screenshot(path=str(screenshot))
    verify_image(screenshot, (width, height))
    assert state['focused'] and state['focusVisible'] and state['outline'] != 'none' and state['outlineWidth'] != '0px', state
    assert state['underline'] and state['inheritedColor'], state
    assert state['visibleRects'] and state['bounded'] and state['unobstructed'] and not state['overflow'], state
    with page.expect_navigation(wait_until='load', timeout=15000) as navigation:
        page.keyboard.press('Enter')
    assert navigation.value and navigation.value.status == 200
    assert page.url == origin + '/vip-services-ibiza/'
    assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com/vip-services-ibiza/'
    assert page.locator('h1').count() == 1
    assert page.locator('a[href^="https://wa.me/34600703303"]').count() > 0
    assert page.locator('a[href="tel:+34600703303"]').count() > 0
    assert page.locator('a[href="mailto:partnership@ibizavipmove.com"]').count() > 0
    assert page.locator('a[href="/contact/?service=vip-services"]').count() == 2
    page.evaluate('document.fonts.ready')
    target_image = output / f'home-vip-target-{mode}.png'
    page.screenshot(path=str(target_image))
    verify_image(target_image, (width, height))
    return {'mode': mode, 'viewport': [width, height], 'linkState': state,
        'keyboardNavigation': 'passed', 'destinationHttp': navigation.value.status,
        'contactTargets': 'preserved; not activated', 'homeScreenshot': screenshot.name,
        'targetScreenshot': target_image.name}


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
                        assert button.count() == 1, 'Expected exactly one form submit button'
                        assert (button.text_content() or '').strip() == LABEL, 'Button source label changed'
                        assert button.inner_text().strip().casefold() == LABEL.casefold(), 'Visible button label changed'
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
                        report.setdefault('homeVipLink', []).append(
                            review_home_vip_link(page, origin, mode, width, height, output)
                        )
                        assert not errors and not missing, {'scriptErrors': errors, 'missingLocalResources': missing}
                        print(f'PASS: Home VIP link, keyboard navigation and nonblank screenshots: {mode}')
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
    self_test_private_office()
    review_private_office(
        Path('_site'),
        Path(os.environ['RUNNER_TEMP']) / 'ivm-contact-review' / 'private-office',
    )
    review_vip_tables(
        Path('_site'),
        Path(os.environ['RUNNER_TEMP']) / 'ivm-contact-review' / 'vip-tables',
    )
