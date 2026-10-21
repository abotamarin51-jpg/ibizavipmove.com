"""Keep Luxury Travel Concierge as the explicit service when a visitor opens the EN private form."""
from pathlib import Path

TRAVEL = Path('_site/luxury-travel-concierge-ibiza/index.html')
CONTACT = Path('_site/contact/index.html')
PARAM = '/contact/?service=travel-concierge'
SERVICE = 'Luxury Travel Concierge'
OLD_LINKS = (
    '<a class="text-link" href="/contact/">Request private support →</a>',
    '<a class="btn dark" href="/contact/">Start your brief</a>',
)
NEW_LINKS = tuple(link.replace('href="/contact/"', f'href="{PARAM}"') for link in OLD_LINKS)
EXISTING_OPTION = '<option value="Private Client Services">Private Client Services</option>'
OPTION = '<option value="Luxury Travel Concierge">Luxury Travel Concierge</option>'
SCRIPT = '''<script id="ivm-travel-concierge-form-context">(()=>{
  const apply=()=>{
    if(document.documentElement.lang!=='en'||location.pathname!=='/contact/')return;
    const values=new URLSearchParams(location.search).getAll('service');
    if(values.length!==1||values[0]!=='travel-concierge')return;
    const select=document.getElementById('fService');
    if(select&&!select.value&&[...select.options].some(o=>o.value==='Luxury Travel Concierge')){
      select.value='Luxury Travel Concierge';
    }
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});
  else apply();
})();</script>'''


def require(ok, message):
    if not ok:
        raise SystemExit('Luxury Travel contact context: ' + message)


def identity(travel, contact):
    require('<html lang="en"' in travel and '<html lang="en"' in contact, 'English identity required')
    require('<link rel="canonical" href="https://ibizavipmove.com/luxury-travel-concierge-ibiza/"' in travel,
            'Travel canonical drift')
    require('<link rel="canonical" href="https://ibizavipmove.com/contact/"' in contact,
            'Contact canonical drift')
    require('name="robots" content="index,follow' in travel and 'name="robots" content="index,follow' in contact,
            'unexpected robots instructions')
    require('id="ivm-dmc-form-context"' in contact and 'id="ivm-private-client-form-context"' in contact,
            'existing DMC/Private Client selectors missing')
    for target in ('https://wa.me/34600703303', 'tel:+34600703303', 'partnership@ibizavipmove.com'):
        require(target in travel and target in contact, 'approved contact route missing: ' + target)


def audit():
    travel = TRAVEL.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    identity(travel, contact)
    require(all(travel.count(new)==1 and old not in travel for old,new in zip(OLD_LINKS,NEW_LINKS)),
            'two travel form links must retain unique service context')
    require(contact.count(OPTION)==1 and contact.count(EXISTING_OPTION)==1,
            'form options missing or duplicated')
    require(contact.count(SCRIPT)==1 and contact.count('id="ivm-travel-concierge-form-context"')==1,
            'guard script absent or repeated')
    require(travel.count('<h1')==1 and contact.count('<h1')==1,
            'unexpected H1 structure')
    print('PASS: Luxury Travel concierge form carries selected service without touching identity or contacts')


def enhance():
    require(TRAVEL.is_file() and CONTACT.is_file(), 'expected existing pages missing')
    travel = TRAVEL.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    identity(travel, contact)
    installed = all(travel.count(new)==1 for new in NEW_LINKS) and OPTION in contact and SCRIPT in contact
    if installed:
        audit()
        return
    require(all(travel.count(old)==1 and new not in travel for old,new in zip(OLD_LINKS,NEW_LINKS)),
            'unexpected Travel CTA drift')
    require(contact.count(EXISTING_OPTION)==1 and OPTION not in contact,
            'unexpected form options')
    require('id="ivm-travel-concierge-form-context"' not in contact and contact.count('</body>')==1,
            'unexpected script/body structure')
    revised_travel = travel
    for old,new in zip(OLD_LINKS,NEW_LINKS):
        revised_travel = revised_travel.replace(old,new,1)
    revised_contact = contact.replace(EXISTING_OPTION,EXISTING_OPTION+OPTION,1).replace(
        '</body>',SCRIPT+'</body>',1)
    require(revised_travel.split('</head>',1)[0]==travel.split('</head>',1)[0]
            and revised_contact.split('</head>',1)[0]==contact.split('</head>',1)[0], 'head metadata drift')
    require(revised_travel.count('<a ')==travel.count('<a ')
            and revised_contact.count('<a ')==contact.count('<a '), 'unintended link markup change')
    TRAVEL.write_text(revised_travel,encoding='utf-8')
    CONTACT.write_text(revised_contact,encoding='utf-8')
    audit()


if __name__ == '__main__':
    enhance()
