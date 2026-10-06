"""Deterministic browser gate for the published WhatsApp access pattern."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
import shutil

from playwright.sync_api import sync_playwright

ROOT = Path('_site').resolve()
assert (ROOT / 'index.html').is_file(), 'Built homepage missing'

EXPECTED_WA = 'https://wa.me/34600703303'
EXPECTED_TEL = 'tel:+34600703303'
VISIBLE_JS = """el => {
    if (!el) return false;
    const s = getComputedStyle(el), r = el.getBoundingClientRect();
    return s.display !== 'none' && s.visibility !== 'hidden' &&
        Number(s.opacity) !== 0 && r.width > 0 && r.height > 0;
}"""
INSIDE_JS = """el => {
    const r = el.getBoundingClientRect();
    return r.left >= -1 && r.top >= -1 &&
        r.right <= innerWidth + 1 && r.bottom <= innerHeight + 1;
}"""


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def wait_state(page, selector, should_be_visible, label):
    page.wait_for_function(
        """([selector, expected]) => {
            const el = document.querySelector(selector);
            if (!el) return false;
            const s = getComputedStyle(el), r = el.getBoundingClientRect();
            const visible = s.display !== 'none' && s.visibility !== 'hidden' &&
                Number(s.opacity) !== 0 && r.width > 0 && r.height > 0;
            return visible === expected;
        }""",
        [selector, should_be_visible],
        timeout=5000,
    )
    state = page.locator(selector).evaluate(VISIBLE_JS)
    if state != should_be_visible:
        raise AssertionError(f'{label}: expected visible={should_be_visible}, got {state}')


def main():
    chrome = next((shutil.which(name) for name in (
        'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'
    ) if shutil.which(name)), None)
    assert chrome, 'No Chromium/Chrome executable available for Phase 174 browser gate'

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=chrome, headless=True)
            try:
                for mode, width, height in (('desktop', 1366, 768), ('mobile', 390, 844)):
                    context = browser.new_context(
                        viewport={'width': width, 'height': height},
                        is_mobile=mode == 'mobile',
                        has_touch=mode == 'mobile',
                        service_workers='block',
                    )
                    errors = []
                    missing = []
                    denied = []

                    def allow_local_only(route):
                        request = route.request
                        host = urlsplit(request.url).hostname
                        static_font = (
                            host in {'fonts.googleapis.com', 'fonts.gstatic.com'}
                            and request.method == 'GET'
                            and request.resource_type in {'stylesheet', 'font'}
                        )
                        if request.url.startswith(origin + '/') or static_font:
                            route.continue_()
                        else:
                            denied.append(request.url)
                            route.abort()

                    context.route('**/*', allow_local_only)
                    try:
                        page = context.new_page()
                        page.on('pageerror', lambda error: errors.append(str(error)))
                        page.on(
                            'response',
                            lambda response: missing.append(response.url)
                            if response.status >= 400 and response.url.startswith(origin + '/')
                            else None,
                        )
                        response = page.goto(origin + '/', wait_until='load', timeout=15000)
                        assert response and response.status == 200
                        page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=5000)
                        page.evaluate('window.IVMCookieConsent.reject()')

                        bar = page.locator('.mobile-bar')
                        floating = page.locator('.ivm-whatsapp-float')
                        assert bar.count() == 1 and floating.count() == 1, 'Contact access elements missing'

                        links = bar.locator('a')
                        assert links.count() == 2, 'Mobile bar must keep exactly two actions'
                        hrefs = links.evaluate_all("els => els.map(a => a.getAttribute('href'))")
                        assert EXPECTED_TEL in hrefs, 'Approved mobile telephone target changed'
                        assert any((href or '').startswith(EXPECTED_WA) for href in hrefs), 'Approved mobile WhatsApp target changed'
                        assert bar.locator('svg.ivm-whatsapp-icon').count() == 1, 'Mobile WhatsApp icon missing'
                        assert (floating.get_attribute('href') or '').startswith(EXPECTED_WA), 'Desktop WhatsApp target changed'
                        assert floating.locator('svg.ivm-whatsapp-icon').count() == 1, 'Desktop WhatsApp icon missing'
                        assert 'whatsapp concierge' in floating.inner_text().casefold(), 'Desktop CTA label missing'

                        if mode == 'desktop':
                            assert page.evaluate('innerWidth') > 600, 'Desktop viewport not applied'
                            wait_state(page, '.ivm-whatsapp-float', True, 'desktop WhatsApp CTA')
                            assert floating.evaluate(INSIDE_JS), 'Desktop WhatsApp CTA not inside viewport'
                            wait_state(page, '.mobile-bar', False, 'desktop mobile bar')
                        else:
                            assert page.evaluate('innerWidth') <= 600, 'Mobile viewport not applied'
                            wait_state(page, '.mobile-bar', True, 'mobile contact bar')
                            assert bar.evaluate(INSIDE_JS), 'Mobile bar not inside viewport'
                            wait_state(page, '.ivm-whatsapp-float', False, 'mobile desktop CTA')

                            page.evaluate("document.body.classList.add('menu-open')")
                            wait_state(page, '.mobile-bar', False, 'mobile bar with open menu')
                            page.evaluate("document.body.classList.remove('menu-open')")
                            wait_state(page, '.mobile-bar', True, 'mobile bar after menu close')

                            page.evaluate("""() => {
                                const input = document.createElement('input');
                                input.id = 'phase174-focus-probe';
                                document.body.appendChild(input);
                                input.focus();
                            }""")
                            wait_state(page, '.mobile-bar', False, 'mobile bar with focused control')
                            page.evaluate("""() => {
                                const input = document.getElementById('phase174-focus-probe');
                                input.blur();
                                input.remove();
                            }""")
                            wait_state(page, '.mobile-bar', True, 'mobile bar after focus ended')

                        page.evaluate('window.IVMCookieConsent.open()')
                        target = '.ivm-whatsapp-float' if mode == 'desktop' else '.mobile-bar'
                        wait_state(page, target, False, 'contact access with cookie dialog')
                        page.evaluate('window.IVMCookieConsent.reject()')
                        wait_state(page, target, True, 'contact access after cookie dialog close')

                        assert not errors and not missing, {
                            'javascriptErrors': errors,
                            'missingLocalResources': missing,
                        }
                        print(
                            f'Phase 174 browser PASS: {mode} {width},{height}; '
                            f'blocked external requests={len(denied)}'
                        )
                    finally:
                        context.close()
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()


if __name__ == '__main__':
    main()
