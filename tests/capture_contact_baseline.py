"""Capture the approved Contact document and its already-requested static assets.
Only diagnosis; no website mutation and no outbound contact/Analytics request.
"""
import hashlib
import json
import os
from pathlib import Path
from playwright.sync_api import sync_playwright
from production_whatsapp_review import ORIGIN, allowed_request

out = Path(os.environ['RUNNER_TEMP']) / 'ivm-production-contact-review' / 'contact-baseline'
out.mkdir(parents=True, exist_ok=True)
manifest = {}
with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='chrome', headless=True)
    context = browser.new_context(viewport={'width':390, 'height':844}, is_mobile=True, has_touch=True, service_workers='block')
    context.route('**/*', lambda route: route.continue_() if allowed_request(route.request.url, route.request.method, route.request.resource_type) else route.abort())
    context.route_web_socket('**/*', lambda ws: ws.close())
    page = context.new_page()
    def capture(response):
        request = response.request
        if not allowed_request(request.url, request.method, request.resource_type):
            return
        if response.status != 200:
            return
        body = response.body()
        name = hashlib.sha256(response.url.encode()).hexdigest()
        (out / name).write_bytes(body)
        manifest[response.url] = {'file':name, 'contentType':response.headers.get('content-type','application/octet-stream'), 'sha256':hashlib.sha256(body).hexdigest()}
    page.on('response', capture)
    page.goto(ORIGIN+'/contact/', wait_until='load')
    page.wait_for_function('Boolean(window.IVMCookieConsent)')
    page.evaluate('window.IVMCookieConsent.reject()')
    page.evaluate('document.fonts.ready')
    page.locator('.menu-btn').click()
    diag = page.evaluate("""() => {
      const elements = ['.site-header','.menu-btn','.mobile-menu','body','main'].map(selector=>{
        const el=document.querySelector(selector),s=getComputedStyle(el),r=el.getBoundingClientRect();
        return {selector,class:el.className,inline:el.getAttribute('style'),position:s.position,zIndex:s.zIndex,transform:s.transform,opacity:s.opacity,isolation:s.isolation,rect:{top:r.top,bottom:r.bottom,left:r.left,right:r.right}};
      });
      const rules=[];
      function scan(items){for(const rule of items){
        if(rule.selectorText && /site-header|menu-btn|mobile-menu/.test(rule.selectorText) && (rule.style.zIndex||rule.style.position||rule.style.transform))rules.push(rule.cssText);
        if(rule.cssRules)scan(rule.cssRules);
      }}
      for(const sheet of document.styleSheets){try{scan(sheet.cssRules);}catch(_){}}
      return {url:location.href,scrollY,bodyClass:document.body.className,elements,rules};
    }""")
    (out/'diagnostic.json').write_text(json.dumps(diag,indent=2))
    print('CONTACT_MENU_DIAGNOSTIC '+json.dumps(diag),flush=True)
    page.screenshot(path=str(out/'menu-before.png'))
    context.close()
    browser.close()
(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
print('BASELINE_CAPTURE_COMPLETE '+str(len(manifest)),flush=True)
