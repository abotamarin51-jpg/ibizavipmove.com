"""Retain an explicit Luxury Lifestyle Management selection in the existing EN private form.

Only the pre-existing Lifestyle page and Contact form are edited, never outgoing messages.
"""
from pathlib import Path

LIFESTYLE = Path('_site/luxury-lifestyle-management-ibiza/index.html')
CONTACT = Path('_site/contact/index.html')
PARAM = '/contact/?service=lifestyle-management'
SERVICE = 'Luxury Lifestyle Management'
OLD_LINKS = (
    '<a class="text-link" href="/contact/">Request private support →</a>',
    '<a class="btn dark" href="/contact/">Start your brief</a>',
    '<a class="btn dark" href="/contact/">Private brief</a>',
)
NEW_LINKS = tuple(link.replace('href="/contact/"', f'href="{PARAM}"') for link in OLD_LINKS)
EXISTING_OPTION = '<option value="Luxury Travel Concierge">Luxury Travel Concierge</option>'
OPTION = '<option value="Luxury Lifestyle Management">Luxury Lifestyle Management</option>'
SCRIPT = '''<script id="ivm-lifestyle-management-form-context">(()=>{
  const apply=()=>{
    if(document.documentElement.lang!=='en'||location.pathname!=='/contact/')return;
    const values=new URLSearchParams(location.search).getAll('service');
    if(values.length!==1||values[0]!=='lifestyle-management')return;
    const select=document.getElementById('fService');
    if(select&&!select.value&&[...select.options].some(o=>o.value==='Luxury Lifestyle Management')){
      select.value='Luxury Lifestyle Management';
    }
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});
  else apply();
})();</script>'''


def require(ok, message):
    if not ok:
        raise SystemExit('Luxury Lifestyle form context: ' + message)


def check_identity(lifestyle, contact):
    require('<html lang="en"' in lifestyle and '<html lang="en"' in contact,
            'English pages only')
    require('<link rel="canonical" href="https://ibizavipmove.com/luxury-lifestyle-management-ibiza/"' in lifestyle,
            'Lifestyle canonical changed')
    require('<link rel="canonical" href="https://ibizavipmove.com/contact/"' in contact,
            'Contact canonical changed')
    require('name="robots" content="index,follow' in lifestyle and 'name="robots" content="index,follow' in contact,
            'robots/indexability changed')
    for marker in ('ivm-dmc-form-context', 'ivm-private-client-form-context',
                   'ivm-travel-concierge-form-context'):
        require(contact.count('id="'+marker+'"') == 1, 'existing service guard missing: '+marker)
    for contact_target in ('https://wa.me/34600703303', 'tel:+34600703303',
                           'partnership@ibizavipmove.com'):
        require(contact_target in lifestyle and contact_target in contact,
                'approved contact route missing')


def audit():
    lifestyle = LIFESTYLE.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    check_identity(lifestyle, contact)
    require(all(lifestyle.count(new) == 1 and old not in lifestyle
                for old, new in zip(OLD_LINKS, NEW_LINKS)),
            'three user-selected Lifestyle form links missing or repeated')
    require(contact.count(OPTION) == 1 and contact.count(EXISTING_OPTION) == 1,
            'named service not uniquely present')
    require(contact.count(SCRIPT) == 1 and contact.count('id="ivm-lifestyle-management-form-context"') == 1,
            'guard absent or repeated')
    require(lifestyle.count('<h1') == 1 and contact.count('<h1') == 1,
            'H1 heading count changed')
    print('PASS: Lifestyle context — three existing form links preserve a changeable service, without contact or SEO identity drift')


def enhance():
    require(LIFESTYLE.is_file() and CONTACT.is_file(), 'existing Lifestyle or Contact page missing')
    lifestyle = LIFESTYLE.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    check_identity(lifestyle, contact)
    installed = all(lifestyle.count(new) == 1 for new in NEW_LINKS) and OPTION in contact and SCRIPT in contact
    if installed:
        audit()
        return
    require(all(lifestyle.count(old) == 1 and new not in lifestyle
                for old, new in zip(OLD_LINKS, NEW_LINKS)),
            'unexpected original Lifestyle form CTA drift')
    require(contact.count(EXISTING_OPTION) == 1 and OPTION not in contact,
            'unexpected existing Contact service inventory')
    require('id="ivm-lifestyle-management-form-context"' not in contact
            and contact.count('</body>') == 1, 'unexpected Contact script/body structure')
    changed_lifestyle = lifestyle
    for old, new in zip(OLD_LINKS, NEW_LINKS):
        changed_lifestyle = changed_lifestyle.replace(old, new, 1)
    changed_contact = contact.replace(EXISTING_OPTION, EXISTING_OPTION + OPTION, 1).replace(
        '</body>', SCRIPT + '</body>', 1)
    require(changed_lifestyle.split('</head>', 1)[0] == lifestyle.split('</head>', 1)[0]
            and changed_contact.split('</head>', 1)[0] == contact.split('</head>', 1)[0],
            'head/SEO metadata drift')
    require(changed_lifestyle.count('<a ') == lifestyle.count('<a ')
            and changed_contact.count('<a ') == contact.count('<a '),
            'unintended link markup changes')
    LIFESTYLE.write_text(changed_lifestyle, encoding='utf-8')
    CONTACT.write_text(changed_contact, encoding='utf-8')
    audit()


if __name__ == '__main__':
    enhance()
