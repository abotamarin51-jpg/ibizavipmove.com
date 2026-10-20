"""Check two German event WhatsApp drafts; never send messages or Analytics."""
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
from urllib.parse import parse_qs, urlsplit
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from phase178_enhance import DE_EVENT_DRAFT, DE_EVENT_HREF, DE_EVENT_WA, event_whatsapp_html

ORIGIN = 'https://ibizavipmove.com'
PAGE = '/de/private-events-ibiza/'
STATIC = {'script', 'stylesheet', 'font', 'image'}
EXTENSIONS = {'.js', '.css', '.woff', '.woff2', '.ttf', '.svg', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.ico'}


def permitted(url, method, kind, origin):
    u, base = urlsplit(url), urlsplit(origin)
    if method != 'GET' or u.username or u.password:
        return False
    if (u.scheme, u.netloc) == (base.scheme, base.netloc):
        if kind == 'document':
            return u.path == PAGE and not u.query
        return kind in STATIC and Path(u.path).suffix.lower() in EXTENSIONS
    return (u.scheme == 'https' and u.port in (None, 443)
            and u.hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'}
            and kind in {'stylesheet', 'font'})


def self_test():
    head = '<html lang="de"><link rel="canonical" href="' + ORIGIN + PAGE + '">'
    anchors = ''.join(f'<a class="btn {s}" href="{DE_EVENT_WA}">Private Event anfragen</a>' for s in ('gold', 'dark'))
    sample = head + '<main>' + anchors + '</main><a href="' + DE_EVENT_WA + '">WhatsApp</a></html>'
    changed = event_whatsapp_html(sample)
    assert changed.count(DE_EVENT_HREF) == 2
    assert changed.replace(DE_EVENT_HREF, DE_EVENT_WA) == sample
    assert event_whatsapp_html(changed) == changed
    assert parse_qs(urlsplit(DE_EVENT_HREF).query) == {'text': [DE_EVENT_DRAFT]}
    assert urlsplit(DE_EVENT_HREF).path == '/34600703303'
    invalid = [sample.replace('lang="de"', 'lang="fr"'), sample.replace(ORIGIN + PAGE, ORIGIN + '/de/services/'),
               sample.replace('class="btn gold"', 'class="other"'), sample + anchors,
               sample.replace(DE_EVENT_WA, 'https://wa.me/111', 1),
               sample.replace('Private Event anfragen', 'Unexpected label', 1), changed + anchors]
    for text in invalid:
        try:
            event_whatsapp_html(text)
        except ValueError:
            pass
        else:
            raise AssertionError('Unexpected or ambiguous CTA accepted')
    cases = [(ORIGIN+PAGE, 'GET', 'document', True), (ORIGIN+'/collect', 'POST', 'fetch', False),
             (DE_EVENT_HREF, 'GET', 'document', False), ('https://www.google-analytics.com/g/collect', 'GET', 'image', False),
             ('https://www.googletagmanager.com/gtag/js', 'GET', 'script', False),
             (ORIGIN+'/assets/premium.js?v=12', 'GET', 'script', True),
             (ORIGIN+PAGE+'?name=example', 'GET', 'document', False),
             ('https://ibizavipmove.com.example.com'+PAGE, 'GET', 'document', False)]
    for url, method, kind, expected in cases:
        assert permitted(url, method, kind, ORIGIN) == expected
    print('PASS: draft encoding, exact two-link delta, idempotence, 7 markup negatives and 8 network-policy cases')


def review(root, output, production=False):
    from playwright.sync_api import sync_playwright
    root, output = root.resolve(), output.resolve()
    assert not output.is_relative_to(root), 'Evidence cannot enter website output'
    output.mkdir(parents=True, exist_ok=True)
    report = {'checkedAt': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
              'verificationSourceCommit': os.environ.get('GITHUB_SHA'),
              'mode': 'production_unmodified' if production else 'built_artifact',
              'page': ORIGIN+PAGE, 'status': 'NOT_RUN', 'results': [],
              'limitations': ['Chromium viewport emulation, not physical Safari or native WhatsApp.',
                             'No message, form, call or Analytics request sent; no commercial outcome measured.']}
    server = None
    origin = ORIGIN
    if not production:
        assert (root/PAGE.strip('/')/'index.html').is_file()
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Quiet, directory=str(root)))
        Thread(target=server.serve_forever, daemon=True).start()
        origin = f'http://127.0.0.1:{server.server_port}'
    chrome = next((shutil.which(x) for x in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser') if shutil.which(x)), None)
    try:
        assert chrome, 'Installed Chrome/Chromium required'
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=chrome, headless=True)
            try:
                for mode, width, height in [('desktop',1366,768), ('mobile',390,844), ('mobile-small',360,800)]:
                    result = {'mode': mode, 'errors': [], 'missing': [], 'blocked': 0, 'buttons': []}
                    report['results'].append(result)
                    context = browser.new_context(viewport={'width':width,'height':height}, is_mobile=mode!='desktop',
                                                  has_touch=mode!='desktop', service_workers='block', accept_downloads=False)
                    def route_request(route):
                        req = route.request
                        if permitted(req.url, req.method, req.resource_type, origin):
                            route.continue_()
                        else:
                            result['blocked'] += 1
                            route.abort()
                    context.route('**/*', route_request)
                    context.route_web_socket('**/*', lambda ws: ws.close())
                    context.add_init_script("""window.__ivmReviewedLinks=[];
                      document.addEventListener('click', e=>{const a=e.target.closest&&e.target.closest('a');
                      if(a&&a.href.startsWith('https://wa.me/')){e.preventDefault();window.__ivmReviewedLinks.push(a.href);}},true);""")
                    page = context.new_page()
                    page.on('pageerror', lambda e: result['errors'].append(str(e)))
                    page.on('response', lambda r: result['missing'].append({'url':r.url,'status':r.status})
                            if r.status>=400 and urlsplit(r.url).netloc==urlsplit(origin).netloc else None)
                    page.on('requestfailed', lambda r: result['missing'].append({'url':r.url,'failure':r.failure})
                            if urlsplit(r.url).netloc==urlsplit(origin).netloc and permitted(r.url,r.method,r.resource_type,origin) else None)
                    try:
                        response = page.goto(origin+PAGE, wait_until='load', timeout=30000)
                        assert response and response.status == 200
                        result['httpStatus'] = response.status
                        result['htmlSha256'] = hashlib.sha256(response.body()).hexdigest()
                        page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=7000)
                        page.evaluate('window.IVMCookieConsent.reject()')
                        page.evaluate('document.fonts.ready')
                        assert page.locator('html').get_attribute('lang') == 'de'
                        assert page.locator('link[rel="canonical"]').get_attribute('href') == ORIGIN+PAGE
                        assert page.locator('h1').count() == 1
                        assert page.locator('main a.btn[href^="https://wa.me/"]').count() == 2
                        assert all(h == DE_EVENT_WA for h in page.locator('a[href^="https://wa.me/"]').evaluate_all(
                            'els=>els.filter(a=>!a.closest("main")).map(a=>a.getAttribute("href"))'))
                        for style in ('gold','dark'):
                            link = page.locator('main a.btn.'+style+'[href^="https://wa.me/"]')
                            assert link.count()==1 and link.get_attribute('href')==DE_EVENT_HREF
                            assert link.text_content().strip()=='Private Event anfragen'
                            link.scroll_into_view_if_needed()
                            link.focus()
                            link.click(trial=True, timeout=7000)
                            geometry = link.evaluate("""el=>{const r=el.getBoundingClientRect(),t=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
                             return {width:r.width,height:r.height,inside:r.left>=0&&r.right<=innerWidth&&r.top>=0&&r.bottom<=innerHeight,
                                     unobstructed:t===el||el.contains(t),overflow:document.documentElement.scrollWidth>innerWidth+1};}""")
                            assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'], geometry
                            assert geometry['width']>=24 and geometry['height']>=24
                            page.screenshot(path=str(output/f'{mode}-{style}.png'))
                            if not production:
                                link.click()
                                link.focus(); page.keyboard.press('Enter')
                                assert page.evaluate('window.__ivmReviewedLinks.slice(-2)')==[DE_EVENT_HREF,DE_EVENT_HREF]
                                assert page.url==origin+PAGE
                            result['buttons'].append({'style':style,'draftCorrect':True,'geometry':geometry})
                        assert not result['errors'] and not result['missing'], result
                        result['status']='PASS'
                    finally:
                        context.close()
            finally:
                browser.close()
        report['status']='PASS'
    except Exception as err:
        report.update(status='FAILED_OR_BLOCKED', error=f'{type(err).__name__}: {err}')
        raise
    finally:
        if server:
            server.shutdown(); server.server_close()
        (output/'de-event-report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('DE_EVENT_WHATSAPP_REPORT '+json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--production',action='store_true')
    p.add_argument('--self-test',action='store_true')
    p.add_argument('--root',type=Path,default=Path('_site'))
    p.add_argument('--output',type=Path,default=Path(os.environ.get('RUNNER_TEMP','/tmp'))/'ivm-dmc-context-review'/'de-event')
    args=p.parse_args()
    self_test()
    if not args.self_test:
        review(args.root,args.output,args.production)
