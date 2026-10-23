"""Keep explicit VIP Services intent on the existing English Contact form.

This is an idempotent, bounded change to two existing generated HTML files.
"""
from pathlib import Path

VIP = Path('_site/vip-services-ibiza/index.html')
CONTACT = Path('_site/contact/index.html')
PARAM = '/contact/?service=vip-services'
SERVICE = 'VIP Services'
OLD_LINKS = (
    '<a class="text-link" href="/contact/">Request private support →</a>',
    '<a class="btn dark" href="/contact/">Start your brief</a>',
)
NEW_LINKS = tuple(link.replace('href="/contact/"', f'href="{PARAM}"') for link in OLD_LINKS)
EXISTING_OPTION = '<option value="Personal Concierge">Personal Concierge</option>'
OPTION = '<option value="VIP Services">VIP Services</option>'
SCRIPT = '''<script id="ivm-vip-services-form-context">(()=>{
  const apply=()=>{
    if(document.documentElement.lang!=='en'||location.pathname!=='/contact/')return;
    const values=new URLSearchParams(location.search).getAll('service');
    if(values.length!==1||values[0]!=='vip-services')return;
    const select=document.getElementById('fService');
    if(select&&!select.value&&[...select.options].some(o=>o.value==='VIP Services')){
      select.value='VIP Services';
    }
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});
  else apply();
})();</script>'''


def require(ok, message):
    if not ok:
        raise SystemExit('VIP Services contact context: ' + message)


def identity(vip, contact):
    require('<html lang="en"' in vip and '<html lang="en"' in contact, 'English only')
    require('<link rel="canonical" href="https://ibizavipmove.com/vip-services-ibiza/"' in vip,
            'VIP Services canonical changed')
    require('<link rel="canonical" href="https://ibizavipmove.com/contact/"' in contact,
            'Contact canonical changed')
    require('name="robots" content="index,follow' in vip and 'name="robots" content="index,follow' in contact,
            'unexpected robots directive')
    for marker in ('ivm-dmc-form-context', 'ivm-private-client-form-context',
                   'ivm-travel-concierge-form-context', 'ivm-lifestyle-management-form-context',
                   'ivm-personal-concierge-form-context'):
        require(contact.count('id="'+marker+'"') == 1, 'previous guard missing: '+marker)
    for dest in ('https://wa.me/34600703303','tel:+34600703303','partnership@ibizavipmove.com'):
        require(dest in vip and dest in contact, 'approved contact route missing: '+dest)


def audit():
    vip=VIP.read_text(encoding='utf-8')
    contact=CONTACT.read_text(encoding='utf-8')
    identity(vip,contact)
    require(all(vip.count(new)==1 and old not in vip for old,new in zip(OLD_LINKS,NEW_LINKS)),
            'exactly two reviewed VIP form CTAs required')
    require(contact.count(OPTION)==1 and contact.count(EXISTING_OPTION)==1,
            'service choice missing or duplicated')
    require(contact.count(SCRIPT)==1 and contact.count('id="ivm-vip-services-form-context"')==1,
            'VIP guard missing or duplicated')
    require(vip.count('<h1')==1 and contact.count('<h1')==1,
            'unexpected heading change')
    print('PASS: VIP Services exact contact handoff, approved contacts and SEO identity preserved')


def enhance():
    require(VIP.is_file() and CONTACT.is_file(),'VIP or Contact page missing')
    vip=VIP.read_text(encoding='utf-8')
    contact=CONTACT.read_text(encoding='utf-8')
    identity(vip,contact)
    installed=(all(vip.count(new)==1 for new in NEW_LINKS) and OPTION in contact and SCRIPT in contact)
    if installed:
        audit()
        return
    require(all(vip.count(old)==1 and new not in vip for old,new in zip(OLD_LINKS)),
            'existing VIP CTA drift or ambiguity')
    require(contact.count(EXISTING_OPTION)==1 and OPTION not in contact,
            'unexpected English Contact option inventory')
    require('id="ivm-vip-services-form-context"' not in contact and contact.count('</body>')==1,
            'unexpected Contact body/guard')
    revised_vip=vip
    for old,new in zip(OLD_LINKS,NEW_LINKS):
        revised_vip=revised_vip.replace(old,new,1)
    revised_contact=contact.replace(EXISTING_OPTION,EXISTING_OPTION+OPTION,1).replace(
        '</body>',SCRIPT+'</body>',1)
    require(revised_vip.split('</head>',1)[0]==vip.split('</head>',1)[0]
            and revised_contact.split('</head>',1)[0]==contact.split('</head>',1)[0],
            'SEO head/metadata drift')
    require(revised_vip.count('<a ')==vip.count('<a ')
            and revised_contact.count('<a ')==contact.count('<a '),
            'unexpected link markup change')
    VIP.write_text(revised_vip,encoding='utf-8')
    CONTACT.write_text(revised_contact,encoding='utf-8')
    audit()


if __name__ == '__main__':
    enhance()
