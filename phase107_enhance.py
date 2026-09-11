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
    tag=f'<script src="{SCRIPT}"></script>'
    if tag not in html: html=html.replace('</body>',tag+'</body>',1)
    if 'data-ivm-qualified-brief="true"' not in html:
        html,n=re.subn(r'<form\b([^>]*\bid="conciergeForm"[^>]*)>',r'<form\1 data-ivm-qualified-brief="true">',html,count=1,flags=re.I)
        if n!=1: raise SystemExit(f'Phase 107 could not mark qualified form: {path}')
    target.write_text(html,encoding='utf-8')

print('PASS: Phase 107 qualification fields added to five Private Members Desk forms with privacy-safe routing script')
