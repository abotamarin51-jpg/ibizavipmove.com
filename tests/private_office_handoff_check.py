"""Browser gate for the English Private Office handoff; never send contact or Analytics."""
from __future__ import annotations

import argparse
from datetime import datetime
from functools import partial
import hashlib
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import sys
from threading import Thread
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from phase179_enhance import BRIEF, CANONICAL, CONTACT, MESSAGE, WA, WA_HREF, enhance_html

ORIGIN = 'https://ibizavipmove.com'
PAGE = '/private-office/'
STATIC_TYPES = {'script', 'stylesheet', 'font', 'image'}
STATIC_SUFFIXES = {'.js', '.css', '.woff', '.woff2', '.ttf', '.svg', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.ico'}
GEOMETRY = """el=>{const r=el.getBoundingClientRect(),t=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
return {width:r.width,height:r.height,inside:r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1,
unobstructed:t===el||el.contains(t),overflow:document.documentElement.scrollWidth>innerWidth+1,focused:document.activeElement===el}}"""


def permitted(url: str, method: str, kind: str, origin: str) -> bool:
    parsed, base = urlsplit(url), urlsplit(origin)
    if method != 'GET' or parsed.username or parsed.password:
        return False
    if (parsed.scheme, parsed.netloc) == (base.scheme, base.netloc):
        if kind == 'document':
            return parsed.path == PAGE and not parsed.query
        return kind in STATIC_TYPES and Path(parsed.path).suffix.lower() in STATIC_SUFFIXES
    return (parsed.scheme == 'https' and parsed.port in (None, 443)
            and parsed.hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'}
            and kind in {'stylesheet', 'font'})


def self_test() -> None:
    sample = (
        f'<html lang="en"><head><link rel="canonical" href="{CANONICAL}"></head><body>'
        '<main id="main-content"><section class="page-hero">'
        '<h1>Ibiza concierge support for family offices and personal assistants.</h1>'
        f'<a class="btn gold" href="{WA}">Start a private brief</a></section>'
        '<section class="ivm-b2b-cta"><h2>Place Ibiza under one point of contact.</h2>'
        f'<p>Send the dates.</p><a class="btn ghost" href="{WA}">WhatsApp 24/7</a>'
        '</section></main></body></html>'
    )
    changed = enhance_html(sample)
    assert changed.count(WA_HREF) == 2
    assert changed.count('data-ivm179="contact"') == 1
    assert changed.count('data-ivm179="brief"') == 1
    assert enhance_html(changed) == changed
    invalid = [
        sample.replace('lang="en"', 'lang="fr"'),
        sample.replace(CANONICAL, ORIGIN + '/partners/'),
        sample.replace('class="btn gold"', 'class="other"'),
        sample.replace('class="btn ghost"', 'class="other"'),
        sample.replace('</main>', sample.split('<main id="main-content">', 1)[1].split('</main>', 1)[0] + '</main>'),
        sample.replace('Start a private brief', 'Changed label'),
        sample.replace(WA, 'https://wa.me/111', 1),
    ]
    for html in invalid:
        try:
            enhance_html(html)
        except ValueError:
            pass
        else:
            raise AssertionError('Unexpected or ambiguous Private Office markup accepted')
    cases = [
        (ORIGIN + PAGE, 'GET', 'document', True),
        (ORIGIN + '/assets/premium.js?v=12', 'GET', 'script', True),
        ('https://fonts.gstatic.com/font.woff2', 'GET', 'font', True),
        (WA_HREF, 'GET', 'document', False),
        ('https://www.google-analytics.com/g/collect', 'POST', 'fetch', False),
        (ORIGIN + PAGE + '?test=1', 'GET', 'document', False),
        ('https://ibizavipmove.com.example.com' + PAGE, 'GET', 'document', False),
    ]
    for url, method, kind, expected in cases:
        assert permitted(url, method, kind, ORIGIN) == expected
    print(f'PASS: Phase 179 browser self-test — idempotence, 7 markup negatives and {len(cases)} request-policy cases')


def review(root: Path, output: Path, production: bool = False) -> dict:
    from playwright.sync_api import sync_playwright

    root, output = root.resolve(), output.resolve()
    assert not output.is_relative_to(root), 'Evidence cannot enter website output'
    output.mkdir(parents=True, exist_ok=True)
    server = None
    origin = ORIGIN
    if not production:
        assert (root / PAGE.strip('/') / 'index.html').is_file()
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
        Thread(target=server.serve_forever, daemon=True).start()
        origin = f'http://127.0.0.1:{server.server_port}'

    chrome = next((shutil.which(name) for name in (
        'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'
    ) if shutil.which(name)), None)
    report = {
        'checkedAt': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
        'sourceCommit': os.environ.get('GITHUB_SHA'),
        'mode': 'production_unmodified' if production else 'built_artifact',
        'page': ORIGIN + PAGE, 'status': 'NOT_RUN', 'results': [],
        'limitations': ['Chromium emulation, not physical Safari or native WhatsApp.',
                        'No message, form, call or Analytics request sent.'],
    }
    try:
        assert chrome, 'Installed Chrome/Chromium required'
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=chrome, headless=True)
            report['browser'] = browser.version
            try:
                for mode, width, height in (('desktop', 1366, 768), ('mobile', 390, 844)):
                    result = {'mode': mode, 'viewport': [width, height], 'errors': [], 'missing': [], 'blocked': [], 'actions': []}
                    report['results'].append(result)
                    context = browser.new_context(viewport={'width': width, 'height': height},
                        is_mobile=mode == 'mobile', has_touch=mode == 'mobile',
                        service_workers='block', accept_downloads=False)
                    def route_request(route):
                        request = route.request
                        if permitted(request.url, request.method, request.resource_type, origin):
                            route.continue_()
                        else:
                            parsed = urlsplit(request.url)
                            result['blocked'].append({'host': parsed.hostname, 'path': parsed.path,
                                                      'type': request.resource_type, 'method': request.method})
                            route.abort()
                    context.route('**/*', route_request)
                    context.route_web_socket('**/*', lambda ws: ws.close())
                    context.add_init_script("""window.__ivmReviewed=[];
                    document.addEventListener('click',e=>{const a=e.target.closest&&e.target.closest('a[data-ivm179="office"]');
                    if(a){e.preventDefault();window.__ivmReviewed.push(a.href)}},true);""")
                    page = context.new_page()
                    page.on('pageerror', lambda error: result['errors'].append(str(error)))
                    page.on('response', lambda response: result['missing'].append(
                        {'url': response.url, 'status': response.status})
                        if response.status >= 400 and urlsplit(response.url).netloc == urlsplit(origin).netloc else None)
                    try:
                        response = page.goto(origin + PAGE, wait_until='load', timeout=30000)
                        assert response and response.status == 200
                        result['httpStatus'] = response.status
                        result['htmlSha256'] = hashlib.sha256(response.body()).hexdigest()
                        page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=7000)
                        page.evaluate('window.IVMCookieConsent.reject()')
                        page.evaluate('document.fonts.ready')
                        assert page.locator('link[rel="canonical"]').get_attribute('href') == CANONICAL
                        assert page.locator('h1').count() == 1
                        assert page.locator('h1').inner_text().strip() == 'Ibiza concierge support for family offices and personal assistants.'
                        brief = page.locator('[data-ivm179="brief"]')
                        assert brief.count() == 1 and all(term in brief.inner_text() for term in (
                            'guest count', 'time zone', 'approve requests', 'Identity documents', 'bank details'))
                        form = page.locator('main a[data-ivm179="contact"]')
                        assert form.count() == 1 and form.get_attribute('href') == CONTACT
                        links = page.locator('main a[data-ivm179="office"]')
                        assert links.count() == 2
                        assert sorted(links.all_inner_texts()) == ['Start a private brief', 'WhatsApp 24/7']
                        assert links.evaluate_all('els=>els.map(a=>a.getAttribute("href"))') == [WA_HREF, WA_HREF]
                        assert all(urlsplit(href).path == '/34600703303' for href in
                                   page.locator('a[href^="https://wa.me/"]').evaluate_all('els=>els.map(a=>a.href)'))
                        for locator in [links.nth(0), links.nth(1), form]:
                            locator.evaluate("el=>el.scrollIntoView({block:'center',inline:'center'})")
                            locator.focus()
                            locator.click(trial=True, timeout=7000)
                            geometry = locator.evaluate(GEOMETRY)
                            assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'], geometry
                            assert geometry['focused'] and geometry['width'] >= 24 and geometry['height'] >= 24, geometry
                            result['actions'].append({'label': locator.inner_text().strip(), 'geometry': geometry})
                        if not production:
                            for locator in (links.nth(0), links.nth(1)):
                                locator.click()
                                locator.focus(); page.keyboard.press('Enter')
                            assert page.evaluate('window.__ivmReviewed') == [WA_HREF, WA_HREF, WA_HREF, WA_HREF]
                            assert page.url == origin + PAGE
                        screenshot = output / f'private-office-{mode}.png'
                        page.screenshot(path=str(screenshot), full_page=True)
                        assert screenshot.stat().st_size > 10000
                        assert not result['errors'] and not result['missing'], result
                        result['status'] = 'PASS'
                    finally:
                        context.close()
            finally:
                browser.close()
        report['status'] = 'PASS'
    except Exception as error:
        report.update(status='FAILED_OR_BLOCKED', error=f'{type(error).__name__}: {error}')
        raise
    finally:
        if server:
            server.shutdown(); server.server_close()
        (output / 'private-office-report.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        print('PRIVATE_OFFICE_HANDOFF_REPORT ' + json.dumps(report), flush=True)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production', action='store_true')
    parser.add_argument('--self-test', action='store_true')
    parser.add_argument('--root', type=Path, default=Path('_site'))
    parser.add_argument('--output', type=Path,
                        default=Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-private-office-review')
    args = parser.parse_args()
    self_test()
    if not args.self_test:
        review(args.root, args.output, args.production)
