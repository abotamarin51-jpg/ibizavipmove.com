"""Read-only browser review of the three approved Ibiza VIP Move production pages.

No website build/deploy, form submission, outbound contact or Analytics request.
Screenshots/JSON are review evidence, not proof of customers or native iOS handoff.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import shutil
from datetime import datetime
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ORIGIN = 'https://ibizavipmove.com'
PAGES = ('/', '/private-office/', '/contact/')
PHONE = 'tel:+34600703303'
WA_PATH = '/34600703303'
FONT_HOSTS = {'fonts.googleapis.com', 'fonts.gstatic.com'}
STATIC_TYPES = {'stylesheet', 'script', 'image', 'font'}
STATIC_SUFFIXES = {'.css', '.js', '.png', '.jpg', '.jpeg', '.webp', '.avif', '.svg', '.ico', '.woff', '.woff2', '.ttf'}
VISIBLE = """el => {
  if (!el) return false;
  const s = getComputedStyle(el), r = el.getBoundingClientRect();
  return s.display !== 'none' && s.visibility !== 'hidden' &&
         Number(s.opacity) > 0 && r.width > 0 && r.height > 0;
}"""
GEOMETRY = """el => {
  const r = el.getBoundingClientRect();
  const top = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
  return {left:r.left, top:r.top, right:r.right, bottom:r.bottom,
    width:r.width, height:r.height,
    inside:r.left>=-1 && r.top>=-1 && r.right<=innerWidth+1 && r.bottom<=innerHeight+1,
    unobstructed:top===el || el.contains(top),
    overflow:document.documentElement.scrollWidth>innerWidth+1};
}"""


def allowed_request(url: str, method: str, resource_type: str) -> bool:
    """Allow only approved HTTPS documents/static assets and existing static fonts."""
    u = urlsplit(url)
    if method != 'GET' or u.scheme != 'https' or u.username or u.password or u.port not in (None, 443):
        return False
    if u.hostname == 'ibizavipmove.com':
        if resource_type == 'document':
            return u.path in PAGES and not u.query
        return resource_type in STATIC_TYPES and Path(u.path).suffix.lower() in STATIC_SUFFIXES
    return u.hostname in FONT_HOSTS and resource_type in {'stylesheet', 'font'}


def policy_self_test() -> None:
    cases = [
        (ORIGIN+'/', 'GET', 'document', True),
        (ORIGIN+'/private-office/', 'GET', 'document', True),
        (ORIGIN+'/contact/', 'GET', 'document', True),
        (ORIGIN+'/assets/premium.js?v=11', 'GET', 'script', True),
        (ORIGIN+'/assets/premium.css?v=11', 'GET', 'stylesheet', True),
        (ORIGIN+'/assets/logo.svg', 'GET', 'image', True),
        ('https://fonts.googleapis.com/css2?family=Manrope', 'GET', 'stylesheet', True),
        ('https://fonts.gstatic.com/font.woff2', 'GET', 'font', True),
        ('https://wa.me/34600703303', 'GET', 'document', False),
        ('https://www.google-analytics.com/g/collect', 'POST', 'ping', False),
        ('https://www.googletagmanager.com/gtag/js?id=test', 'GET', 'script', False),
        (ORIGIN+'/collect.gif', 'GET', 'image', False),
        (ORIGIN+'/api/submit', 'POST', 'fetch', False),
        (ORIGIN+'/contact/', 'POST', 'document', False),
        (ORIGIN+'/contact/?name=test', 'GET', 'document', False),
        (ORIGIN+'/assets/premium.js', 'GET', 'fetch', False),
        ('https://ibizavipmove.com.example.net/', 'GET', 'document', False),
        ('https://user:password@ibizavipmove.com/', 'GET', 'document', False),
        ('https://ibizavipmove.com:444/', 'GET', 'document', False),
        ('http://ibizavipmove.com/', 'GET', 'document', False),
        ('tel:+34600703303', 'GET', 'document', False),
        ('mailto:partnership@ibizavipmove.com', 'GET', 'document', False),
        ('https://fonts.googleapis.com/collect', 'POST', 'fetch', False),
    ]
    for url, method, kind, expected in cases:
        assert allowed_request(url, method, kind) == expected, (url, method, kind)
    print(f'POLICY SELF-TEST PASS: {len(cases)} cases; no network used')


def wait_visibility(page, selector: str, expected: bool) -> None:
    page.wait_for_function("""([selector,expected])=>{
      const el=document.querySelector(selector); if(!el)return false;
      const s=getComputedStyle(el),r=el.getBoundingClientRect();
      const visible=s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)>0&&r.width>0&&r.height>0;
      return visible===expected;
    }""", arg=[selector, expected], timeout=7000)


def actionable(locator) -> dict:
    # Trial performs visibility/stability/hit-target checks, but never dispatches a click.
    locator.click(trial=True, timeout=7000)
    geometry = locator.evaluate(GEOMETRY)
    assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'], geometry
    assert geometry['width'] >= 24 and geometry['height'] >= 24, geometry
    return geometry


def navigation_link(page, target: str):
    candidates = []
    for link in page.locator('a[href]').all():
        href = link.get_attribute('href') or ''
        parsed = urlsplit(href)
        if parsed.path != target or parsed.query or (parsed.netloc and parsed.netloc != 'ibizavipmove.com'):
            continue
        if link.is_visible():
            text = link.inner_text().lower()
            candidates.append((('brief' in text or 'request' in text), link))
    assert candidates, f'No visible internal link to {target}'
    return sorted(candidates, key=lambda item: item[0], reverse=True)[0][1]


def run_review(output: Path, inline_crops: bool, candidate_css: Path | None = None, baseline_css: Path | None = None) -> dict:
    from playwright.sync_api import sync_playwright
    replacement = None
    if candidate_css is not None or baseline_css is not None:
        assert candidate_css is not None and baseline_css is not None
        old = baseline_css.read_bytes()
        new = candidate_css.read_bytes()
        delta = b'\n/* Keep the Contact close control above its existing mobile-menu overlay. */\n@media(max-width:900px){body.ivm-private-desk.menu-open .site-header{position:fixed;z-index:100}}\n'
        assert hashlib.sha1(b'blob '+str(len(old)).encode()+b'\0'+old).hexdigest() == '1ea3da7ba7fcac84e7a97dd37a6c52600061a432', 'Unreviewed baseline CSS'
        assert new == old + delta, 'Candidate CSS change is outside the reviewed minimal fix'
        replacement = (old, new)
    output.mkdir(parents=True, exist_ok=True)
    chrome = next((shutil.which(x) for x in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser') if shutil.which(x)), None)
    assert chrome, 'No installed Chrome/Chromium executable'
    report = {'testedAt': datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
              'origin': ORIGIN, 'sourceCommit': os.environ.get('GITHUB_SHA'),
              'reviewMode': 'candidate_css_response_override' if replacement else 'production_unmodified',
              'scope': list(PAGES), 'modes': [], 'status': 'NOT_RUN',
              'limitations': ['Chromium viewport emulation, not a physical iPhone/Safari test.',
                              'Contact actions use trial clicks; no form is submitted or message sent.',
                              'No site change, new deployment, indexation or commercial outcome is implied.']}
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=chrome, headless=True)
            report['browserVersion'] = browser.version
            try:
                for mode, width, height in [('desktop',1366,768), ('mobile',390,844)]:
                    result = {'mode':mode, 'viewport':[width,height], 'pages':[], 'denied':[],
                              'httpErrors':[], 'networkErrors':[], 'javascriptErrors':[], 'assets':{}, 'inlineStyles':{}, 'candidateOverrides':[]}
                    report['modes'].append(result)
                    context = browser.new_context(viewport={'width':width,'height':height},
                        is_mobile=(mode=='mobile'),has_touch=(mode=='mobile'),
                        service_workers='block',accept_downloads=False)

                    def route_read_only(route):
                        req = route.request
                        if allowed_request(req.url,req.method,req.resource_type):
                            if replacement and urlsplit(req.url).hostname == 'ibizavipmove.com' and req.resource_type == 'stylesheet':
                                response = route.fetch(max_redirects=0, timeout=15000)
                                assert response.status == 200, 'Candidate stylesheet source did not return 200'
                                body = response.body()
                                old, new = replacement
                                if old in body:
                                    assert body.count(old) == 1, 'Ambiguous baseline stylesheet content'
                                    body = body.replace(old, new, 1)
                                    result['candidateOverrides'].append({'url':req.url,'sourceSha256':hashlib.sha256(old).hexdigest(),'candidateSha256':hashlib.sha256(new).hexdigest()})
                                route.fulfill(response=response, body=body)
                            else:
                                route.continue_()
                        else:
                            u=urlsplit(req.url)
                            result['denied'].append({'host':u.hostname,'path':u.path,'type':req.resource_type,'method':req.method})
                            route.abort()

                    context.route('**/*',route_read_only)
                    context.route_web_socket('**/*',lambda ws: ws.close())
                    page = context.new_page()
                    page.set_default_timeout(7000)
                    page.on('pageerror', lambda error: result['javascriptErrors'].append(str(error)))
                    page.on('requestfailed', lambda req: result['networkErrors'].append({'url':req.url,'failure':req.failure})
                        if allowed_request(req.url,req.method,req.resource_type) else None)

                    def observe_response(response):
                        req=response.request
                        if allowed_request(req.url,req.method,req.resource_type):
                            if response.status >= 400:
                                result['httpErrors'].append({'url':response.url,'status':response.status})
                            if (urlsplit(response.url).path == '/assets/premium.js' or
                                (urlsplit(response.url).hostname == 'ibizavipmove.com' and req.resource_type == 'stylesheet')):
                                body=response.body()
                                result['assets'][urlsplit(response.url).path] = {
                                  'url':response.url,'status':response.status,'bytes':len(body),
                                  'sha256':hashlib.sha256(body).hexdigest(),
                                  'iconMarkerPresent':b'ivm-whatsapp-icon' in body,
                                  'floatingMarkerPresent':b'ivm-whatsapp-float' in body}
                    page.on('response',observe_response)
                    try:
                        response=page.goto(ORIGIN+'/',wait_until='load',timeout=30000)
                        for index,path in enumerate(PAGES):
                            if index:
                                link=navigation_link(page,path)
                                with page.expect_navigation(wait_until='load',timeout=30000) as nav:
                                    link.click()
                                response=nav.value
                            assert response and response.status==200, f'HTTP status for {path}'
                            assert page.url==ORIGIN+path, f'Unexpected navigation: {page.url}'
                            page.wait_for_function('Boolean(window.IVMCookieConsent)',timeout=7000)
                            page.evaluate('window.IVMCookieConsent.reject()')
                            page.evaluate('document.fonts.ready')
                            assert page.evaluate("document.fonts.check('16px Manrope')"), 'Manrope not loaded'
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+path
                            assert page.locator('h1').count()==1
                            # Production may bundle CSS or inline it; inspect what the document actually uses.
                            for style in page.locator('style').all():
                                text=style.text_content() or ''
                                if 'ivm-whatsapp-icon' in text and 'ivm-whatsapp-float' in text:
                                    digest=hashlib.sha256(text.encode('utf-8')).hexdigest()
                                    result['inlineStyles'][digest]={'document':path,'bytes':len(text.encode('utf-8'))}
                            bar=page.locator('.mobile-bar'); floating=page.locator('.ivm-whatsapp-float')
                            assert bar.count()==1 and floating.count()==1, 'Duplicate or missing contact controls'
                            assert bar.locator('a').count()==2
                            assert bar.locator('svg.ivm-whatsapp-icon').count()==1
                            assert floating.locator('svg.ivm-whatsapp-icon').count()==1
                            assert 'whatsapp concierge' in floating.inner_text().lower()
                            wa=bar.locator('a[href^="https://wa.me/"]')
                            tel=bar.locator('a[href^="tel:"]')
                            assert wa.count()==1 and tel.count()==1
                            for a in [wa,floating]:
                                u=urlsplit(a.get_attribute('href') or '')
                                assert u.scheme=='https' and u.netloc=='wa.me' and u.path==WA_PATH
                            assert tel.get_attribute('href')==PHONE
                            target='.mobile-bar' if mode=='mobile' else '.ivm-whatsapp-float'
                            other='.ivm-whatsapp-float' if mode=='mobile' else '.mobile-bar'
                            wait_visibility(page,target,True); wait_visibility(page,other,False)
                            active=wa if mode=='mobile' else floating
                            data={'path':path,'status':response.status,'action':actionable(active)}
                            if mode=='mobile':
                                data['telephone']=actionable(tel)
                                page.locator('.menu-btn').click()
                                wait_visibility(page,target,False)
                                assert page.locator('.mobile-menu').is_visible()
                                page.screenshot(path=str(output/f'{mode}-{index}-menu.png'))
                                page.locator('.menu-btn').click()
                                wait_visibility(page,target,True)
                            page.evaluate('window.IVMCookieConsent.open()')
                            wait_visibility(page,target,False)
                            page.screenshot(path=str(output/f'{mode}-{index}-cookies.png'))
                            page.evaluate('window.IVMCookieConsent.reject()')
                            wait_visibility(page,target,True)
                            if path=='/contact/':
                                field=page.locator('#conciergeForm input:not([type="hidden"])').first
                                field.focus()
                                wait_visibility(page,target,False)
                                page.screenshot(path=str(output/f'{mode}-{index}-field-focus.png'))
                                field.blur()
                                wait_visibility(page,target,True)
                                button=page.locator('#conciergeForm button[type="submit"]')
                                assert button.inner_text().strip().lower()=='continue to whatsapp'
                                data['formButton']=actionable(button)
                                data['formSubmitted']=False
                            else:
                                page.evaluate('window.scrollTo(0,0)')
                            page.screenshot(path=str(output/f'{mode}-{index}.png'))
                            if path=='/':
                                clip={'x':max(0,width-430),'y':height-120,'width':min(430,width),'height':120}
                                image=page.screenshot(path=str(output/f'{mode}-cta.jpg'),type='jpeg',quality=60,clip=clip)
                                data['cropSha256']=hashlib.sha256(image).hexdigest()
                                if inline_crops:
                                    print('IVM_CTA_CROP '+mode+' '+base64.b64encode(image).decode('ascii'),flush=True)
                            result['pages'].append(data)
                            print('PRODUCTION_PAGE_REVIEW '+json.dumps({'mode':mode,**data}),flush=True)
                        assert not result['httpErrors'] and not result['networkErrors'] and not result['javascriptErrors'], 'See resource/JavaScript errors in report'
                        script=result['assets'].get('/assets/premium.js')
                        assert script and script['status']==200 and script['iconMarkerPresent'] and script['floatingMarkerPresent'], 'Production premium.js markers missing'
                        contact_css=[asset for path,asset in result['assets'].items()
                                     if path.endswith('.css') and asset['status']==200
                                     and asset['iconMarkerPresent'] and asset['floatingMarkerPresent']]
                        assert contact_css or result['inlineStyles'], 'No served or inline stylesheet containing both contact markers'
                        if replacement:
                            assert result['candidateOverrides'], 'Candidate fix was never exercised'
                        result['status']='PASS'
                    except Exception as error:
                        result['status']='FAIL'; result['error']=str(error)
                        try: page.screenshot(path=str(output/f'{mode}-failure.png'))
                        except Exception: pass
                        raise
                    finally:
                        context.close()
            finally:
                browser.close()
        report['status']='PASS'
    except Exception as error:
        report['status']='FAILED_OR_BLOCKED'; report['error']=str(error)
        raise
    finally:
        (output/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('PRODUCTION_REVIEW_REPORT '+json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--self-test',action='store_true')
    parser.add_argument('--inline-crops',action='store_true')
    parser.add_argument('--candidate-css',type=Path)
    parser.add_argument('--baseline-css',type=Path)
    parser.add_argument('--output',type=Path,default=Path('production-contact-review'))
    args=parser.parse_args()
    policy_self_test()
    if not args.self_test:
        run_review(args.output,args.inline_crops,args.candidate_css,args.baseline_css)
