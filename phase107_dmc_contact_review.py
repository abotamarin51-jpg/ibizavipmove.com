"""Review the English DMC-to-Contact context, without sending enquiries or Analytics."""
from __future__ import annotations

import argparse
from datetime import datetime
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
from threading import Thread
from urllib.parse import urlsplit
from zoneinfo import ZoneInfo

ORIGIN = 'https://ibizavipmove.com'
DMC = '/destination-management-ibiza/'
PRIVATE = '/private-client-services-ibiza/'
TRAVEL = '/luxury-travel-concierge-ibiza/'
CONTACT = '/contact/?service=dmc'
PRIVATE_CONTACT = '/contact/?service=private-client'
TRAVEL_CONTACT = '/contact/?service=travel-concierge'
SERVICE = 'Destination Management'
PRIVATE_SERVICE = 'Private Client Services'
TRAVEL_SERVICE = 'Luxury Travel Concierge'
QUERIES = {'', 'service=dmc', 'service=chauffeur', 'service=invalid', 'service=dmc&service=chauffeur',
           'service=private-client', 'service=private-client&service=dmc',
           'service=private-client&service=private-client', 'service=travel-concierge',
           'service=travel-concierge&service=dmc', 'service=travel-concierge&service=travel-concierge'}
STATIC_TYPES = {'script', 'stylesheet', 'font', 'image'}
SUFFIXES = {'.js', '.css', '.woff', '.woff2', '.ttf', '.svg', '.jpg', '.jpeg', '.png', '.webp', '.avif', '.ico'}
GEOMETRY = """el => {
 const r=el.getBoundingClientRect(),top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
 return {width:r.width,height:r.height,left:r.left,right:r.right,top:r.top,bottom:r.bottom,
 inside:r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1,
 unobstructed:top===el||el.contains(top),overflow:document.documentElement.scrollWidth>innerWidth+1};
}"""


def allowed(url, method, kind, origin):
    u, base = urlsplit(url), urlsplit(origin)
    if method != 'GET' or u.username or u.password:
        return False
    if (u.scheme, u.netloc) == (base.scheme, base.netloc):
        if kind == 'document':
            return (u.path in {DMC, PRIVATE, TRAVEL} and not u.query) or (u.path == '/contact/' and u.query in QUERIES)
        return kind in STATIC_TYPES and Path(u.path).suffix.lower() in SUFFIXES
    return (u.scheme == 'https' and u.port in (None, 443)
            and u.hostname in {'fonts.googleapis.com', 'fonts.gstatic.com'}
            and kind in {'stylesheet', 'font'})


def self_test():
    cases = [(ORIGIN+DMC,'GET','document',True), (ORIGIN+CONTACT,'GET','document',True),
             (ORIGIN+PRIVATE,'GET','document',True), (ORIGIN+PRIVATE_CONTACT,'GET','document',True),
             (ORIGIN+TRAVEL,'GET','document',True), (ORIGIN+TRAVEL_CONTACT,'GET','document',True),
             (ORIGIN+'/assets/premium.js?v=11','GET','script',True),
             (ORIGIN+'/contact/?name=test','GET','document',False),
             (ORIGIN+'/contact/','POST','document',False),
             (ORIGIN+'/collect','POST','fetch',False),
             ('https://wa.me/34600703303','GET','document',False),
             ('https://www.google-analytics.com/g/collect','POST','ping',False),
             ('https://www.googletagmanager.com/gtag/js','GET','script',False),
             ('https://ibizavipmove.com.example.net/contact/','GET','document',False),
             ('https://user:pass@ibizavipmove.com/contact/','GET','document',False),
             ('https://fonts.gstatic.com/a.woff2','GET','font',True)]
    for url, method, kind, expected in cases:
        assert allowed(url,method,kind,ORIGIN) == expected, (url,method,kind)
    print(f'PASS: DMC request policy, {len(cases)} offline cases')


def ready(page):
    page.wait_for_function('Boolean(window.IVMCookieConsent)', timeout=7000)
    page.evaluate('window.IVMCookieConsent.reject()')
    page.evaluate('document.fonts.ready')


def review(production=False):
    from playwright.sync_api import sync_playwright
    from PIL import Image, ImageStat
    output = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-dmc-context-review'
    output.mkdir(parents=True, exist_ok=True)
    root = Path('_site').resolve()
    assert not output.resolve().is_relative_to(root), 'Evidence cannot enter website output'
    server = None
    origin = ORIGIN
    if not production:
        assert (root/'contact/index.html').is_file()
        class Quiet(SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        server = ThreadingHTTPServer(('127.0.0.1',0), partial(Quiet,directory=str(root)))
        Thread(target=server.serve_forever,daemon=True).start()
        origin = f'http://127.0.0.1:{server.server_port}'
    report = {'testedAt':datetime.now(ZoneInfo('Europe/Madrid')).isoformat(),
              'commit':os.environ.get('GITHUB_SHA'), 'mode':'production_unmodified' if production else 'built_artifact',
              'pages':[DMC,CONTACT,PRIVATE,PRIVATE_CONTACT,TRAVEL,TRAVEL_CONTACT], 'results':[], 'status':'NOT_RUN',
              'limitations':['Chromium viewport emulation, not physical iPhone/Safari.',
                             'No form submission, outbound contact or Analytics request; no commercial outcome measured.']}
    chrome = next((shutil.which(x) for x in ('google-chrome','google-chrome-stable','chromium','chromium-browser') if shutil.which(x)), None)
    try:
        assert chrome, 'Installed Chrome/Chromium required'
        with sync_playwright() as pw:
            browser = pw.chromium.launch(executable_path=chrome,headless=True)
            report['browser'] = browser.version
            try:
                for mode,width,height in [('desktop',1366,768),('mobile',390,844)]:
                    result = {'mode':mode,'viewport':[width,height],'journeys':[],'errors':[],'missing':[],'blocked':0}
                    report['results'].append(result)
                    context = browser.new_context(viewport={'width':width,'height':height},
                        is_mobile=mode=='mobile',has_touch=mode=='mobile',service_workers='block',accept_downloads=False)
                    def route_request(route):
                        req=route.request
                        if allowed(req.url,req.method,req.resource_type,origin):
                            route.continue_()
                        else:
                            result['blocked']+=1
                            route.abort()
                    context.route('**/*',route_request)
                    context.route_web_socket('**/*',lambda ws:ws.close())
                    page=context.new_page()
                    page.on('pageerror',lambda err:result['errors'].append(str(err)))
                    page.on('requestfailed',lambda req:result['missing'].append({'url':req.url,'failure':req.failure})
                        if allowed(req.url,req.method,req.resource_type,origin) else None)
                    page.on('response',lambda res:result['missing'].append({'url':res.url,'status':res.status})
                        if res.status>=400 and allowed(res.url,res.request.method,res.request.resource_type,origin) else None)
                    try:
                        # Exercise both existing contextual CTA links, without contacting a third party.
                        for index in range(2):
                            res=page.goto(origin+DMC,wait_until='load',timeout=30000)
                            assert res and res.status==200
                            ready(page)
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+DMC
                            links=page.locator('main a[href="'+CONTACT+'"]')
                            assert links.count()==2, 'Both existing DMC links must preserve context'
                            label=links.nth(index).inner_text()
                            with page.expect_navigation(wait_until='load',timeout=30000) as navigation:
                                links.nth(index).click()
                            assert navigation.value and navigation.value.status==200
                            assert page.url==origin+CONTACT
                            ready(page)
                            select=page.locator('#fService')
                            assert select.input_value()==SERVICE, 'DMC service was not carried into Contact'
                            assert select.locator('option[value="'+SERVICE+'"]').count()==1
                            assert page.locator('#fClientType').input_value()=='', 'Profile must not be inferred'
                            assert page.locator('#fClientType option').count()==7
                            assert page.locator('#fName').input_value()==page.locator('#fPhone').input_value()==''
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+'/contact/'
                            assert page.locator('h1').count()==1 and select.get_attribute('required') is not None
                            assert select.locator('xpath=..').evaluate("el=>el.tagName==='LABEL'")
                            targets=page.locator('a[href^="https://wa.me/"]').evaluate_all('els=>els.map(a=>new URL(a.href).pathname)')
                            assert targets and set(targets)=={'/34600703303'}
                            assert set(page.locator('a[href^="tel:"]').evaluate_all('els=>els.map(a=>a.getAttribute("href"))'))=={'tel:+34600703303'}
                            select.focus()
                            select.click(trial=True,timeout=7000)
                            geometry=select.evaluate(GEOMETRY)
                            assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'],geometry
                            assert geometry['height']>=24 and geometry['width']>=24
                            screenshot=output/f'{mode}-service-{index}.png'
                            page.screenshot(path=str(screenshot))
                            with Image.open(screenshot) as im:
                                assert im.size==(width,height) and max(ImageStat.Stat(im.convert('RGB')).var)>1
                            # Choosing another service/profile stays possible and does not navigate or send.
                            select.select_option(label='Full Concierge')
                            page.locator('#fClientType').select_option('travel_advisor')
                            select.blur()
                            assert select.input_value()=='Full Concierge'
                            assert page.url==origin+CONTACT
                            result['journeys'].append({'link':label,'selectedService':SERVICE,'editable':True,
                                'profileInitiallyEmpty':True,'geometry':geometry,'formSubmitted':False})
                        # Verify three Private Client pathways retain the selected service without inferring identity.
                        for index in range(3):
                            res=page.goto(origin+PRIVATE,wait_until='load',timeout=30000)
                            assert res and res.status==200
                            ready(page)
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+PRIVATE
                            links=page.locator('main a[href="'+PRIVATE_CONTACT+'"]')
                            assert links.count()==3, 'Three existing Private Client form links must keep context'
                            label=links.nth(index).inner_text()
                            with page.expect_navigation(wait_until='load',timeout=30000) as navigation:
                                links.nth(index).click()
                            assert navigation.value and navigation.value.status==200
                            assert page.url==origin+PRIVATE_CONTACT
                            ready(page)
                            select=page.locator('#fService')
                            assert select.input_value()==PRIVATE_SERVICE, 'Private Client service context lost'
                            assert select.locator('option[value="'+PRIVATE_SERVICE+'"]').count()==1
                            assert page.locator('#fClientType').input_value()=='', 'Do not infer a client role'
                            assert page.locator('#fName').input_value()==page.locator('#fPhone').input_value()==''
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+'/contact/'
                            select.focus()
                            select.click(trial=True,timeout=7000)
                            geometry=select.evaluate(GEOMETRY)
                            assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'],geometry
                            assert geometry['height']>=24 and geometry['width']>=24
                            screenshot=output/f'{mode}-private-client-{index}.png'
                            page.screenshot(path=str(screenshot))
                            with Image.open(screenshot) as im:
                                assert im.size==(width,height) and max(ImageStat.Stat(im.convert('RGB')).var)>1
                            select.select_option(label='Full Concierge')
                            assert select.input_value()=='Full Concierge'
                            result['journeys'].append({'link':label,'selectedService':PRIVATE_SERVICE,
                                'editable':True,'profileInitiallyEmpty':True,'geometry':geometry,'formSubmitted':False})
                        # The two existing Luxury Travel form CTAs retain the actual requested service.
                        for index in range(2):
                            res=page.goto(origin+TRAVEL,wait_until='load',timeout=30000)
                            assert res and res.status==200
                            ready(page)
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+TRAVEL
                            links=page.locator('main a[href="'+TRAVEL_CONTACT+'"]')
                            assert links.count()==2, 'Travel page requires two contextual form CTAs'
                            label=links.nth(index).inner_text()
                            with page.expect_navigation(wait_until='load',timeout=30000) as navigation:
                                links.nth(index).click()
                            assert navigation.value and navigation.value.status==200
                            assert page.url==origin+TRAVEL_CONTACT
                            ready(page)
                            select=page.locator('#fService')
                            assert select.input_value()==TRAVEL_SERVICE, 'Luxury Travel context lost'
                            assert select.locator('option[value="'+TRAVEL_SERVICE+'"]').count()==1
                            assert page.locator('#fClientType').input_value()=='', 'Visitor role cannot be inferred'
                            assert page.locator('#fName').input_value()==page.locator('#fPhone').input_value()==''
                            assert page.locator('link[rel="canonical"]').get_attribute('href')==ORIGIN+'/contact/'
                            assert page.locator('h1').count()==1 and select.get_attribute('required') is not None
                            select.focus()
                            select.click(trial=True,timeout=7000)
                            geometry=select.evaluate(GEOMETRY)
                            assert geometry['inside'] and geometry['unobstructed'] and not geometry['overflow'],geometry
                            assert geometry['height']>=24 and geometry['width']>=24
                            screenshot=output/f'{mode}-travel-{index}.png'
                            page.screenshot(path=str(screenshot))
                            with Image.open(screenshot) as im:
                                assert im.size==(width,height) and max(ImageStat.Stat(im.convert('RGB')).var)>1
                            select.select_option(label='Full Concierge')
                            assert select.input_value()=='Full Concierge'
                            result['journeys'].append({'link':label,'selectedService':TRAVEL_SERVICE,
                                'editable':True,'profileInitiallyEmpty':True,'geometry':geometry,'formSubmitted':False})
                        for query,expected in [('', ''),('service=invalid',''),('service=dmc&service=chauffeur',''),
                                               ('service=chauffeur','Private Chauffeur & Transportation'),
                                               ('service=private-client',PRIVATE_SERVICE),
                                               ('service=private-client&service=dmc',''),
                                               ('service=private-client&service=private-client',''),
                                               ('service=travel-concierge',TRAVEL_SERVICE),
                                               ('service=travel-concierge&service=dmc',''),
                                               ('service=travel-concierge&service=travel-concierge','')]:
                            page.goto(origin+'/contact/'+('?' + query if query else ''),wait_until='load',timeout=30000)
                            ready(page)
                            assert page.locator('#fService').input_value()==expected, ('Unexpected preselection',query)
                        assert not result['errors'] and not result['missing'], result
                        result['status']='PASS'
                        print('DMC_CONTEXT_PASS '+json.dumps(result),flush=True)
                    except Exception:
                        page.screenshot(path=str(output/f'{mode}-failure.png'))
                        raise
                    finally:
                        context.close()
            finally:
                browser.close()
        report['status']='PASS'
    except Exception as err:
        report['status']='FAILED_OR_BLOCKED';report['error']=str(err)
        raise
    finally:
        if server:
            server.shutdown();server.server_close()
        (output/'report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print('DMC_CONTEXT_REPORT '+json.dumps(report),flush=True)
    return report


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--production',action='store_true')
    parser.add_argument('--self-test',action='store_true')
    args=parser.parse_args()
    self_test()
    if not args.self_test:
        review(args.production)
