"""Keep an explicit Private Client Services form brief intact between two existing EN pages."""
from pathlib import Path

PRIVATE = Path('_site/private-client-services-ibiza/index.html')
CONTACT = Path('_site/contact/index.html')
PARAM = '/contact/?service=private-client'
SERVICE = 'Private Client Services'
OLD_LINKS = (
    '<a class="text-link" href="/contact/">Request private support →</a>',
    '<a class="btn dark" href="/contact/">Start your brief</a>',
    '<a class="btn dark" href="/contact/">Private brief</a>',
)
NEW_LINKS = tuple(s.replace('href="/contact/"', f'href="{PARAM}"') for s in OLD_LINKS)
DESTINATION_OPTION = '<option value="Destination Management">Destination Management</option>'
PRIVATE_OPTION = '<option value="Private Client Services">Private Client Services</option>'
SCRIPT = '''<script id="ivm-private-client-form-context">(()=>{
  const apply=()=>{
    if(document.documentElement.lang!=='en'||window.location.pathname!=='/contact/')return;
    const values=new URLSearchParams(window.location.search).getAll('service');
    if(values.length!==1||values[0]!=='private-client')return;
    const select=document.getElementById('fService');
    if(select&&!select.value&&[...select.options].some(o=>o.value==='Private Client Services')){
      select.value='Private Client Services';
    }
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});
  else apply();
})();</script>'''


def require(value, message):
    if not value:
        raise SystemExit('Private Client form context: ' + message)


def identity(private, contact):
    require('<html lang="en"' in private and '<html lang="en"' in contact, 'English pages required')
    require('<link rel="canonical" href="https://ibizavipmove.com/private-client-services-ibiza/"' in private,
            'private client canonical mismatch')
    require('<link rel="canonical" href="https://ibizavipmove.com/contact/"' in contact,
            'contact canonical mismatch')
    require('name="robots" content="index,follow' in private and 'name="robots" content="index,follow' in contact,
            'unexpected robots instruction')
    require('id="ivm-dmc-form-context"' in contact, 'existing DMC preselection missing')
    for text in ('https://wa.me/34600703303', 'tel:+34600703303', 'partnership@ibizavipmove.com'):
        require(text in private and text in contact, 'approved contact route missing: ' + text)


def audit():
    private = PRIVATE.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    identity(private, contact)
    require(all(private.count(new) == 1 and old not in private for old, new in zip(OLD_LINKS, NEW_LINKS)),
            'three contextual Private Client links missing, old or repeated')
    require(contact.count(PRIVATE_OPTION) == 1 and contact.count(DESTINATION_OPTION) == 1,
            'required contact form options missing or repeated')
    require(contact.count(SCRIPT) == 1, 'new context guard missing or repeated')
    require(private.count('<h1') == 1 and contact.count('<h1') == 1, 'unexpected heading structure')
    print('PASS: Private Client context — three form paths, editable named service, unchanged canonicals and contacts')


def enhance():
    require(PRIVATE.is_file() and CONTACT.is_file(), 'one of the two existing pages is missing')
    private = PRIVATE.read_text(encoding='utf-8')
    contact = CONTACT.read_text(encoding='utf-8')
    identity(private, contact)
    applied = all(private.count(new) == 1 for new in NEW_LINKS) and PRIVATE_OPTION in contact and SCRIPT in contact
    if applied:
        audit()
        print('PASS: Private Client context already installed, no duplication')
        return
    require(all(private.count(old) == 1 and new not in private for old, new in zip(OLD_LINKS, NEW_LINKS)),
            'unexpected private client CTA drift')
    require(contact.count(DESTINATION_OPTION) == 1 and PRIVATE_OPTION not in contact,
            'unexpected form option drift')
    require('id="ivm-private-client-form-context"' not in contact and contact.count('</body>') == 1,
            'unexpected script/body drift')
    updated_private = private
    for old, new in zip(OLD_LINKS, NEW_LINKS):
        updated_private = updated_private.replace(old, new, 1)
    updated_contact = contact.replace(DESTINATION_OPTION, PRIVATE_OPTION + DESTINATION_OPTION, 1).replace(
        '</body>', SCRIPT + '</body>', 1)
    require(updated_private.split('</head>', 1)[0] == private.split('</head>', 1)[0]
            and updated_contact.split('</head>', 1)[0] == contact.split('</head>', 1)[0],
            'SEO metadata/head drift')
    require(updated_private.count('<a ') == private.count('<a ')
            and updated_contact.count('<a ') == contact.count('<a '), 'unexpected link structure drift')
    PRIVATE.write_text(updated_private, encoding='utf-8')
    CONTACT.write_text(updated_contact, encoding='utf-8')
    audit()


if __name__ == '__main__':
    enhance()
