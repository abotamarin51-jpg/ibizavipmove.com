from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
import os
import shutil
import subprocess
import sys
import time

ROOT = Path('_site').resolve()
INDEX = ROOT / 'index.html'
PROBE = ROOT / '__phase174_probe.html'
assert INDEX.is_file(), 'Built homepage missing'

chrome = next((shutil.which(name) for name in (
    'google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'
) if shutil.which(name)), None)
assert chrome, 'No Chromium/Chrome executable available for Phase 174 browser gate'

probe_script = r"""
<script>
(async()=>{
  const wait=(ms)=>new Promise(r=>setTimeout(r,ms));
  const mode=new URLSearchParams(location.search).get('mode')||'desktop';
  const expectedWa='https://wa.me/34600703303';
  const expectedTel='tel:+34600703303';
  const fail=(m)=>{throw new Error(m)};
  const visible=(el)=>{
    if(!el)return false;
    const s=getComputedStyle(el),r=el.getBoundingClientRect();
    return s.display!=='none'&&s.visibility!=='hidden'&&Number(s.opacity)!==0&&r.width>0&&r.height>0;
  };
  const inside=(el)=>{
    const r=el.getBoundingClientRect();
    return r.left>=-1&&r.top>=-1&&r.right<=innerWidth+1&&r.bottom<=innerHeight+1;
  };

  try{
    await wait(180);
    if(window.IVMCookieConsent)window.IVMCookieConsent.reject();
    await wait(100);

    const bar=document.querySelector('.mobile-bar');
    const float=document.querySelector('.ivm-whatsapp-float');
    if(!bar||!float)fail('Contact access elements missing');

    const links=[...bar.querySelectorAll('a')];
    if(links.length!==2)fail('Mobile bar must keep exactly two actions');
    const tel=links.find(a=>a.href.startsWith(expectedTel));
    const wa=links.find(a=>a.href.startsWith(expectedWa));
    if(!tel||!wa)fail('Approved mobile targets changed');
    if(!wa.querySelector('svg.ivm-whatsapp-icon'))fail('Mobile WhatsApp icon missing');
    if(!float.href.startsWith(expectedWa))fail('Desktop WhatsApp target changed');
    if(!float.querySelector('svg.ivm-whatsapp-icon'))fail('Desktop WhatsApp icon missing');
    if(!/WhatsApp Concierge/i.test(float.textContent))fail('Desktop CTA label missing');

    if(mode==='desktop'){
      if(innerWidth<=600)fail('Desktop viewport not applied');
      if(!visible(float)||!inside(float))fail('Desktop WhatsApp CTA not visible inside viewport');
      if(visible(bar))fail('Mobile bar visible on desktop');
    }else{
      if(innerWidth>600)fail('Mobile viewport not applied');
      if(!visible(bar)||!inside(bar))fail('Mobile bar not visible inside viewport');
      if(visible(float))fail('Desktop WhatsApp CTA visible on mobile');

      document.body.classList.add('menu-open');
      await wait(60);
      if(visible(bar))fail('Mobile bar overlaps open menu');
      document.body.classList.remove('menu-open');
      await wait(60);
      if(!visible(bar))fail('Mobile bar did not return after menu close');

      const input=document.createElement('input');
      document.body.appendChild(input);
      input.focus();
      await wait(60);
      if(visible(bar))fail('Mobile bar remains visible while form control is focused');
      input.blur();
      input.remove();
      await wait(80);
      if(!visible(bar))fail('Mobile bar did not return after focus ended');
    }

    if(window.IVMCookieConsent){
      window.IVMCookieConsent.open();
      await wait(80);
      const target=mode==='desktop'?float:bar;
      if(visible(target))fail('Contact access overlaps cookie dialog');
      window.IVMCookieConsent.reject();
      await wait(80);
      if(!visible(target))fail('Contact access did not return after cookie dialog closed');
    }

    document.documentElement.setAttribute('data-phase174',mode+'-pass');
  }catch(err){
    document.documentElement.setAttribute('data-phase174',mode+'-fail');
    document.body.setAttribute('data-phase174-error',String(err&&err.message||err));
  }
})();
</script>
"""

html = INDEX.read_text(encoding='utf-8')
assert '</body>' in html.lower(), 'Homepage body close missing'
PROBE.write_text(html.replace('</body>', probe_script + '</body>'), encoding='utf-8')

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

old_cwd = Path.cwd()
os.chdir(ROOT)
server = ThreadingHTTPServer(('127.0.0.1', 0), Quiet)
thread = Thread(target=server.serve_forever, daemon=True)
thread.start()
port = server.server_address[1]

try:
    for mode, size in (('desktop', '1366,768'), ('mobile', '390,844')):
        url = f'http://127.0.0.1:{port}/__phase174_probe.html?mode={mode}'
        cmd = [
            chrome,
            '--headless=new',
            '--disable-gpu',
            '--no-sandbox',
            '--disable-dev-shm-usage',
            '--hide-scrollbars',
            '--host-resolver-rules=MAP * 0.0.0.0, EXCLUDE localhost, EXCLUDE 127.0.0.1',
            f'--window-size={size}',
            '--virtual-time-budget=2600',
            '--dump-dom',
            url,
        ]
        result = subprocess.run(cmd, text=True, capture_output=True, timeout=45)
        if result.returncode != 0:
            print(result.stderr[-2000:])
            raise SystemExit(f'Chrome failed for {mode}: {result.returncode}')
        marker = f'data-phase174="{mode}-pass"'
        if marker not in result.stdout:
            tail = result.stdout[-4000:]
            print(tail)
            raise SystemExit(f'Phase 174 browser gate failed for {mode}')
        print(f'Phase 174 browser PASS: {mode} {size}')
finally:
    server.shutdown()
    server.server_close()
    os.chdir(old_cwd)
    try:
        PROBE.unlink()
    except FileNotFoundError:
        pass
