"""Review the three new club pages at desktop/mobile sizes without sending enquiries."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import sys
from threading import Thread
from urllib.parse import parse_qs, urlsplit

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from phase190_club_guides import CLUBS, ROOT, route


def main():
    output = Path(os.environ['RUNNER_TEMP']) / 'ivm-club-review'
    output.mkdir(parents=True, exist_ok=True)
    chrome = next((shutil.which(n) for n in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser') if shutil.which(n)), None)
    assert chrome, 'Runner Chrome/Chromium required'

    class Quiet(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(ROOT.resolve())))
    Thread(target=server.serve_forever, daemon=True).start()
    origin = f'http://127.0.0.1:{server.server_port}'
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=chrome, headless=True)
            for mode, width, height in (('desktop', 1366, 768), ('mobile', 390, 844)):
                context = browser.new_context(viewport={'width': width, 'height': height}, is_mobile=mode == 'mobile', has_touch=mode == 'mobile', service_workers='block')
                def local_and_fonts_only(request):
                    url = request.request.url
                    is_font = urlsplit(url).hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'} and request.request.method == 'GET' and request.request.resource_type in {'stylesheet', 'font'}
                    if url.startswith(origin + '/') or is_font:
                        request.continue_()
                    else:
                        request.abort()
                context.route('**/*', local_and_fonts_only)
                for club in CLUBS:
                    page = context.new_page()
                    errors, missing = [], []
                    page.on('pageerror', lambda error: errors.append(str(error)))
                    page.on('response', lambda response: missing.append(response.url) if response.url.startswith(origin + '/') and response.status >= 400 else None)
                    response = page.goto(origin + route(club), wait_until='networkidle')
                    assert response.status == 200
                    page.evaluate('document.fonts.ready')
                    assert page.locator('h1').inner_text() == club['name'] + ' VIP tables.'
                    assert page.locator('h1').is_visible()
                    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), 'Horizontal overflow'
                    for cta in page.locator('[data-ivm190="brief"]').all():
                        cta.scroll_into_view_if_needed()
                        cta.focus()
                        cta.click(trial=True)
                        rect = cta.bounding_box()
                        assert rect and rect['height'] >= 44 and rect['x'] >= -1 and rect['x'] + rect['width'] <= width + 1
                        href = urlsplit(cta.get_attribute('href'))
                        assert href.netloc == 'wa.me' and href.path == '/34600703303'
                        assert club['name'] in parse_qs(href.query)['text'][0], 'Club context lost after JS initialization'
                    summary = page.locator('details summary').first
                    summary.click()
                    assert page.locator('details').first.get_attribute('open') is not None
                    assert page.locator('details p').first.is_visible()
                    for section in page.locator('main section').all():
                        section.scroll_into_view_if_needed()
                    page.screenshot(path=str(output / f'{club["slug"]}-{mode}-full.png'), full_page=True)
                    page.evaluate('window.scrollTo(0,0)')
                    page.screenshot(path=str(output / f'{club["slug"]}-{mode}-hero.png'))
                    assert not errors and not missing, {'errors': errors, 'missing': missing}
                    results.append({'route': route(club), 'viewport': mode, 'status': 'pass'})
                    page.close()
                context.close()
            browser.close()
    finally:
        server.shutdown()
    (output / 'report.json').write_text(json.dumps({'commit': os.getenv('GITHUB_SHA'), 'results': results, 'external_contact_requests': 'blocked; CTA trials only'}, indent=2))
    print('PASS: Club guides — all three pages at desktop/mobile widths; visible content, editable FAQ, actionable contextual CTAs, no missing local assets or page errors')


if __name__ == '__main__':
    main()
