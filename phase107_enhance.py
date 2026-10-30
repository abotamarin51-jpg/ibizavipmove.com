from pathlib import Path
from html import escape
import re

ROOT=Path('_site')
SCRIPT='/assets/phase107.js?v=107'
SRC=Path('phase107.js')
DEST=ROOT/'assets'/'phase107.js'
DEST.write_text(SRC.read_text(encoding='utf-8'),encoding='utf-8')

CONTACTS={
'en':('/contact/','I am','Stay / area',[
('private_client','Private client'),('assistant','Personal / Executive Assistant'),('family_office','Family Office'),('travel_advisor','Luxury Travel Advisor / Concierge Partner'),('hospitality_partner','Hotel / Villa / Hospitality Partner'),('other','Other')],[
('','Not decided / Other'),('ibiza_town','Ibiza Town / Marina Botafoch / Talamanca'),('south','Cala Jondal / Es Cubells / South Ibiza'),('east','Santa Eulària / Roca Llisa / East Ibiza'),('central','Santa Gertrudis / Central Ibiza'),('playa_den_bossa','Playa d’en Bossa / Sant Josep'),('west','San Antonio / West Ibiza')]),
'es':('/es/contacto/','Perfil','Estancia / zona',[
('private_client','Cliente privado'),('assistant','Asistente personal / ejecutivo'),('family_office','Family Office'),('travel_advisor','Travel advisor / Concierge partner'),('hospitality_partner','Hotel / Villa / Hospitality partner'),('other','Otro')],[
('','Por decidir / Otra zona'),('ibiza_town','Ibiza Town / Marina Botafoch / Talamanca'),('south','Cala Jondal / Es Cubells / Sur de Ibiza'),('east','Santa Eulària / Roca Llisa / Este de Ibiza'),('central','Santa Gertrudis / Centro de Ibiza'),('playa_den_bossa','Playa d’en Bossa / Sant Josep'),('west','San Antonio / Oeste de Ibiza')]),
'fr':('/fr/contact/','Profil','Séjour / zone',[
('private_client','Client privé'),('assistant','Assistant personnel / exécutif'),('family_office','Family Office'),('travel_advisor','Travel advisor / Concierge partner'),('hospitality_partner','Hôtel / Villa / Hospitality partner'),('other','Autre')],[
('','À définir / Autre'),('ibiza_town','Ibiza Town / Marina Botafoch / Talamanca'),('south','Cala Jondal / Es Cubells / Sud Ibiza'),('east','Santa Eulària / Roca Llisa / Est Ibiza'),('central','Santa Gertrudis / Centre Ibiza'),('playa_den_bossa','Playa d’en Bossa / Sant Josep'),('west','San Antonio / Ouest Ibiza')]),
'de':('/de/kontakt/','Profil','Aufenthalt / Region',[
('private_client','Privatkunde'),('assistant','Personal / Executive Assistant'),('family_office','Family Office'),('travel_advisor','Luxury Travel Advisor / Concierge Partner'),('hospitality_partner','Hotel / Villa / Hospitality Partner'),('other','Andere')],[
('','Noch offen / Andere'),('ibiza_town','Ibiza Town / Marina Botafoch / Talamanca'),('south','Cala Jondal / Es Cubells / Süd-Ibiza'),('east','Santa Eulària / Roca Llisa / Ost-Ibiza'),('central','Santa Gertrudis / Zentral-Ibiza'),('playa_den_bossa','Playa d’en Bossa / Sant Josep'),('west','San Antonio / West-Ibiza')]),
'ar':('/ar/contact/','الصفة','الإقامة / المنطقة',[
('private_client','عميل خاص'),('assistant','مساعد شخصي / تنفيذي'),('family_office','Family Office'),('travel_advisor','مستشار سفر فاخر / شريك كونسيرج'),('hospitality_partner','فندق / فيلا / شريك ضيافة'),('other','أخرى')],[
('','غير محدد / أخرى'),('ibiza_town','Ibiza Town / Marina Botafoch / Talamanca'),('south','Cala Jondal / Es Cubells / جنوب إيبيزا'),('east','Santa Eulària / Roca Llisa / شرق إيبيزا'),('central','Santa Gertrudis / وسط إيبيزا'),('playa_den_bossa','Playa d’en Bossa / Sant Josep'),('west','San Antonio / غرب إيبيزا')])
}

def page(path): return ROOT/path.strip('/')/'index.html'

def opts(items):
    return ''.join(f'<option value="{escape(value,quote=True)}">{escape(label)}</option>' for value,label in items)

for lang,(path,role_label,area_label,roles,areas) in CONTACTS.items():
    target=page(path)
    if not target.exists(): raise SystemExit(f'Phase 107 contact missing: {path}')
    html=target.read_text(encoding='utf-8')
    if 'id="fClientType"' not in html:
        role=f'<label>{escape(role_label)}<select id="fClientType" required>{opts(roles)}</select></label>'
        area=f'<label>{escape(area_label)}<select id="fArea">{opts(areas)}</select></label>'
        html,n=re.subn(r'(<label[^>]*>.*?<input\s+id="fPhone"[^>]*>.*?</label>)',r'\1'+role+area,html,count=1,flags=re.I|re.S)
        if n!=1: raise SystemExit(f'Phase 107 could not insert qualification fields: {path}')
    tag=f'<script src="{SCRIPT}" defer></script>'
    if tag not in html: html=html.replace('</body>',tag+'</body>',1)
    if 'data-ivm-qualified-brief="true"' not in html:
        html,n=re.subn(
            r'<form\b([^>]*\bid=["\'](?:conciergeForm|localizedConciergeForm)["\'][^>]*)>',
            r'<form\1 data-ivm-qualified-brief="true">',
            html,count=1,flags=re.I
        )
        if n!=1: raise SystemExit(f'Phase 107 could not mark qualified form: {path}')
    # Opening WhatsApp prepares a message; it does not send the enquiry.
    # Keep the existing confirmation terms, fields and routing unchanged.
    handoff_copy_by_language = {
        'en': (
            ('>Send Private Brief</button>', '>Continue to WhatsApp</button>'),
            ('Submitting opens a private WhatsApp conversation with the details above.',
             'Opens WhatsApp with your details. Review the message and press Send there.'),
        ),
        'fr': (
            ('>Envoyer le brief privé</button>', '>Continuer sur WhatsApp</button>'),
            ('L’envoi ouvre une conversation WhatsApp privée avec ces informations.',
             'WhatsApp s’ouvre avec vos informations. Vérifiez le message, puis appuyez sur Envoyer dans WhatsApp.'),
        ),
        'de': (
            ('>Privates Briefing senden</button>', '>Weiter zu WhatsApp</button>'),
            ('Beim Senden öffnet sich eine private WhatsApp-Unterhaltung mit diesen Angaben.',
             'WhatsApp öffnet sich mit Ihren Angaben. Prüfen Sie die Nachricht und senden Sie sie dort ab.'),
        ),
        'ar': (
            ('>إرسال الطلب الخاص</button>', '>المتابعة عبر واتساب</button>'),
            ('عند الإرسال سيتم فتح محادثة واتساب خاصة بهذه المعلومات.',
             'سيُفتح واتساب مع معلوماتك. راجع الرسالة ثم اضغط على إرسال داخل واتساب.'),
        ),
    }
    if lang in handoff_copy_by_language:
        for old_copy, new_copy in handoff_copy_by_language[lang]:
            if html.count(old_copy) == 1:
                html = html.replace(old_copy, new_copy, 1)
            elif html.count(new_copy) != 1:
                raise SystemExit('Contact WhatsApp handoff copy marker missing or duplicated')
    target.write_text(html,encoding='utf-8')

print('PASS: Phase 107 qualification fields added to five Private Members Desk forms with privacy-safe deferred routing script')

# Preserve the existing English DMC request context without adding a form,
# tracking event, client-profile assumption or language. Run after Phase 102.
def preserve_dmc_form_context(root):
    contact_path = root / 'contact' / 'index.html'
    dmc_path = root / 'destination-management-ibiza' / 'index.html'
    contact = contact_path.read_text(encoding='utf-8')
    dmc = dmc_path.read_text(encoding='utf-8')
    option = '<option value="Destination Management">Destination Management</option>'
    anchor = '<option value="Full Concierge">Full Concierge</option>'
    if option not in contact:
        assert contact.count(anchor) == 1, 'English Full Concierge option missing or duplicated'
        contact = contact.replace(anchor, anchor + option, 1)
    assert contact.count(option) == 1, 'Duplicate DMC option'

    # Only an explicit allowlisted service is preselected. Do not replace a
    # visitor/browser-restored selection, infer their role, or dispatch events.
    script = '''<script id="ivm-dmc-form-context">(()=>{
  const apply=()=>{
    if(document.documentElement.lang!=='en'||window.location.pathname!=='/contact/')return;
    const params=new URLSearchParams(window.location.search);
    if(params.getAll('service').length!==1||params.get('service')!=='dmc')return;
    const select=document.getElementById('fService');
    if(select&&!select.value&&[...select.options].some(o=>o.value==='Destination Management')){
      select.value='Destination Management';
    }
  };
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',apply,{once:true});
  else apply();
})();</script>'''
    if 'id="ivm-dmc-form-context"' not in contact:
        assert contact.count('</body>') == 1, 'English Contact body missing or duplicated'
        contact = contact.replace('</body>', script + '</body>', 1)
    assert contact.count(script) == 1, 'DMC context script drift or duplication'

    for old in (
        '<a class="text-link" href="/contact/">Request private support →</a>',
        '<a class="btn dark" href="/contact/">Start your brief</a>',
    ):
        new = old.replace('href="/contact/"', 'href="/contact/?service=dmc"')
        if old in dmc:
            assert dmc.count(old) == 1, 'Ambiguous DMC contextual contact link'
            dmc = dmc.replace(old, new, 1)
        assert dmc.count(new) == 1, 'Expected DMC contextual contact link missing'
    assert '<link rel="canonical" href="https://ibizavipmove.com/contact/"' in contact
    assert '<link rel="canonical" href="https://ibizavipmove.com/destination-management-ibiza/"' in dmc
    contact_path.write_text(contact, encoding='utf-8')
    dmc_path.write_text(dmc, encoding='utf-8')


preserve_dmc_form_context(ROOT)
print('PASS: English DMC context retained through the two existing Contact links; profile remains visitor-selected')
