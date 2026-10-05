from pathlib import Path
from html import unescape
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
    // Failure-only snapshot; no text, form values, contact activation or network.
    try{
      const snapshot=(selector)=>{
        const el=document.querySelector(selector);
        if(!el)return {present:false};
        const s=getComputedStyle(el),r=el.getBoundingClientRect();
        return {
          present:true,visible:visible(el),inside:inside(el),hidden:el.hidden,
          rect:{left:r.left,top:r.top,right:r.right,bottom:r.bottom,width:r.width,height:r.height},
          style:{display:s.display,visibility:s.visibility,opacity:s.opacity,position:s.position,
            top:s.top,right:s.right,bottom:s.bottom,left:s.left,transform:s.transform,
            overflow:s.overflow,contentVisibility:s.contentVisibility}
        };
      };
      document.body.setAttribute('data-phase174-diagnostics',JSON.stringify({
        viewport:{innerWidth,innerHeight,outerWidth,outerHeight,devicePixelRatio,scrollX,scrollY,
          visualWidth:window.visualViewport?.width,visualHeight:window.visualViewport?.height},
        readyState:document.readyState,
        state:{
          contactAccessHidden:document.body.classList.contains('ivm-contact-access-hidden'),
          menuOpen:document.body.classList.contains('menu-open'),
          consentOpen:Boolean(document.querySelector('.ivm-consent:not([hidden])')),
          consentApi:Boolean(window.IVMCookieConsent),
          editing:Boolean(document.activeElement?.matches?.('input,textarea,select,[contenteditable="true"]'))
        },
        desktop:snapshot('.ivm-whatsapp-float'),mobile:snapshot('.mobile-bar'),
        body:snapshot('body'),root:snapshot('html')
      }));
    }catch(_){
      document.body.setAttribute('data-phase174-diagnostics','Diagnostic collection failed');
    }
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
            error_attr = 'data-phase174-error="'
            start = result.stdout.find(error_attr)
            if start != -1:
                start += len(error_attr)
                end = result.stdout.find('"', start)
                print('Phase 174 browser error:', result.stdout[start:end if end != -1 else None])
            else:
                tail = result.stdout[-4000:]
                print(tail)
            diagnostic_attr = 'data-phase174-diagnostics="'
            diagnostic_start = result.stdout.find(diagnostic_attr)
            if diagnostic_start != -1:
                diagnostic_start += len(diagnostic_attr)
                diagnostic_end = result.stdout.find('"', diagnostic_start)
                diagnostic_value = result.stdout[diagnostic_start:diagnostic_end if diagnostic_end != -1 else None]
                print('Phase 174 browser diagnostics:', unescape(diagnostic_value)[:8000])
            raise SystemExit(f'Phase 174 browser gate failed for {mode}')
        print(f'Phase 174 browser PASS: {mode} {size}')

# Phase 175 — verify the German event handoff visually as well as in the DOM.
P175_SOURCE = ROOT / 'de' / 'privatkoch-villa-staff-ibiza' / 'index.html'
P175_PROBE = P175_SOURCE.with_name('__phase175_visual_probe.html')
assert P175_SOURCE.is_file(), 'Phase 175 German source missing'
assert (ROOT / 'de' / 'private-events-ibiza' / 'index.html').is_file(), 'Phase 175 German event target missing'
p175_script = r"""
<script>
window.addEventListener('load', async () => {
  const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
  try {
    if (window.IVMCookieConsent) window.IVMCookieConsent.reject();
    await wait(240);
    const cards = document.querySelectorAll('a[href="/de/private-events-ibiza/"]');
    if (cards.length !== 1) throw Error('Expected exactly one event card');
    const card = cards[0];
    if (card.querySelector('strong')?.textContent !== 'Eventkoordination & private Events') throw Error('Wrong event-card label');
    card.scrollIntoView({behavior:'instant', block:'center'});
    card.focus({preventScroll:true});
    await wait(120);
    const r = card.getBoundingClientRect(), s = getComputedStyle(card);
    if (document.activeElement !== card || s.display === 'none' || s.visibility === 'hidden' || Number(s.opacity) === 0) throw Error('Event card is not visible/focusable');
    if (r.width <= 0 || r.height <= 0 || r.left < -1 || r.top < -1 || r.right > innerWidth + 1 || r.bottom > innerHeight + 1) throw Error('Event card is outside viewport');
    if (document.documentElement.scrollWidth > innerWidth + 1 || card.scrollWidth > card.clientWidth + 1) throw Error('Horizontal overflow or clipped card');
    const wa = [...document.querySelectorAll('a[href^="https://wa.me/"]')];
    const tel = [...document.querySelectorAll('a[href^="tel:"]')];
    if (!wa.length || !tel.length || wa.some(a => new URL(a.href).pathname !== '/34600703303') || tel.some(a => a.getAttribute('href') !== 'tel:+34600703303')) throw Error('Approved contact target changed');
    document.documentElement.setAttribute('data-phase175-visual', 'pass');
  } catch (err) {
    document.documentElement.setAttribute('data-phase175-visual', 'fail');
    document.body.setAttribute('data-phase175-visual-error', String(err.message || err));
  }
}, {once:true});
</script>
"""
p175_html = P175_SOURCE.read_text(encoding='utf-8')
assert p175_html.count('</body>') == 1, 'Phase 175 German body close mismatch'
P175_PROBE.write_text(p175_html.replace('</body>', p175_script + '</body>'), encoding='utf-8')
shots = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-browser-review'
shots.mkdir(parents=True, exist_ok=True)
image_python = Path(os.environ.get('RUNNER_TEMP', '/tmp')) / 'ivm-image-tools' / 'bin' / 'python'
assert image_python.is_file(), 'Pillow validation environment missing'

for mode, size in (('desktop', '1366,768'), ('mobile', '390,844')):
    url = f'http://127.0.0.1:{port}/de/privatkoch-villa-staff-ibiza/__phase175_visual_probe.html'
    base_cmd = [
        chrome,
        '--headless=new',
        '--disable-gpu',
        '--no-sandbox',
        '--disable-dev-shm-usage',
        '--hide-scrollbars',
        '--run-all-compositor-stages-before-draw',
        '--host-resolver-rules=MAP * 0.0.0.0, EXCLUDE localhost, EXCLUDE 127.0.0.1',
        f'--window-size={size}',
        '--virtual-time-budget=2600',
    ]
    dom_result = subprocess.run(base_cmd + ['--dump-dom', url], text=True, capture_output=True, timeout=45)
    if dom_result.returncode != 0 or 'data-phase175-visual="pass"' not in dom_result.stdout:
        print(dom_result.stderr[-2000:])
        raise SystemExit(f'Phase 175 German DOM visual gate failed for {mode}')
    shot = shots / f'validated-german-event-card-{mode}.png'
    shot_result = subprocess.run(base_cmd + [f'--screenshot={shot}', url], text=True, capture_output=True, timeout=45)
    if shot_result.returncode != 0:
        print(shot_result.stderr[-2000:])
        raise SystemExit(f'Phase 175 German screenshot command failed for {mode}')
    expected = tuple(map(int, size.split(',')))
    image_check = subprocess.run([
        str(image_python), '-c',
        "from PIL import Image,ImageStat; import sys; "
        "im=Image.open(sys.argv[1]).convert('RGB'); exp=tuple(map(int,sys.argv[2].split(','))); "
        "var=sum(ImageStat.Stat(im).var); colors=len(set(im.resize((64,64)).getdata())); "
        "print(f'image={im.size} variance={var:.3f} sampled_colors={colors}'); "
        "raise SystemExit(0 if im.size==exp and var>10 and colors>=8 else 2)",
        str(shot), size,
    ], text=True, capture_output=True, timeout=30)
    print(image_check.stdout.strip())
    if image_check.returncode != 0:
        print(image_check.stderr[-2000:])
        raise SystemExit(f'Phase 175 German screenshot is blank or invalid for {mode}')
    print(f'Phase 175 visual PASS: {mode} {size}')

finally:
    server.shutdown()
    server.server_close()
    os.chdir(old_cwd)
    for probe in (PROBE, P175_PROBE):
        try:
            probe.unlink()
        except FileNotFoundError:
            pass
