"""Review the built Destination Management snippet in desktop and mobile Chromium."""
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

EXPECTED_TITLE = 'Luxury DMC & Destination Management Ibiza | Ibiza VIP Move'
EXPECTED_DESC = 'Luxury destination management in Ibiza for travel advisors, family offices and concierge firms coordinating transport, villas, yachts and guest logistics.'
CANONICAL = 'https://ibizavipmove.com/destination-management-ibiza/'


def verify_image(path, size):
    with Image.open(path) as image:
        if image.size != size:
            raise AssertionError(f'Unexpected screenshot dimensions: {image.size}')
        if max(ImageStat.Stat(image.convert('RGB')).var) <= 1:
            raise AssertionError(f'Blank or uniform screenshot: {path.name}')


def main():
    root = Path('_site').resolve()
    output = (Path(os.environ['RUNNER_TEMP']) / 'ivm-destination-review').resolve()
    assert (root / 'destination-management-ibiza/index.html').is_file(), 'Destination page missing'
    assert not output.is_relative_to(root), 'Review evidence must remain outside website artifact'
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
                        is_mobile=mode == 'mobile',
                        has_touch=mode == 'mobile',
                        service_workers='block',
                    )
                    denied = []
                    errors = []
                    missing = []

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
                        response = page.goto(
                            origin + '/destination-management-ibiza/',
                            wait_until='load',
                            timeout=15000,
                        )
                        assert response and response.status == 200
                        if page.evaluate('Boolean(window.IVMCookieConsent)'):
                            page.evaluate('window.IVMCookieConsent.reject()')

                        assert page.title() == EXPECTED_TITLE
                        assert page.locator('meta[name="description"]').get_attribute('content') == EXPECTED_DESC
                        assert page.locator('link[rel="canonical"]').get_attribute('href') == CANONICAL
                        assert page.locator('h1').count() == 1

                        summary = page.locator('section.page-hero p').first
                        assert summary.inner_text().strip() == EXPECTED_DESC
                        summary.scroll_into_view_if_needed()
                        assert summary.is_visible()

                        cta = page.get_by_role('link', name='Start a private brief')
                        assert cta.count() == 1 and cta.is_visible()

                        geometry = summary.evaluate("""el => {
                            const r = el.getBoundingClientRect();
                            return {
                                left: r.left, right: r.right, top: r.top, bottom: r.bottom,
                                width: r.width, height: r.height,
                                overflow: document.documentElement.scrollWidth > innerWidth + 1
                            };
                        }""")
                        assert not geometry['overflow'], geometry
                        assert geometry['width'] > 0 and geometry['height'] > 0, geometry
                        assert geometry['left'] >= -1 and geometry['right'] <= width + 1, geometry
                        assert not errors and not missing, {
                            'javascriptErrors': errors,
                            'missingLocalResources': missing,
                        }

                        screenshot = output / f'destination-{mode}.png'
                        page.screenshot(path=str(screenshot))
                        verify_image(screenshot, (width, height))
                        report['results'].append({
                            'mode': mode,
                            'viewport': [width, height],
                            'geometry': geometry,
                            'blockedExternalRequests': len(denied),
                            'javascriptErrors': errors,
                            'missingLocalResources': missing,
                            'title': EXPECTED_TITLE,
                            'description': EXPECTED_DESC,
                        })
                        print(f'PASS: Destination snippet visible without overflow: {mode}')
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
