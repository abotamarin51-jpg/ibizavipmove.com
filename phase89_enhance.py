from pathlib import Path
import re

ROOT=Path('_site')

DATA={
'en':{
 'path':'/ibiza-intelligence/','link':'/private-concierge-ibiza/','kicker':'Choosing a private concierge in Ibiza','title':'What should be clear before you hand over the stay.','lead':'A useful concierge relationship is not defined by the length of a service list. It is defined by how clearly one team can connect the confirmed parts of the stay, communicate changes and separate what is requested from what is actually secured.','body':'For private clients, personal assistants and family offices, the first conversation should establish the dates, guests, accommodation, arrivals, priority reservations, transport requirements and who is authorised to approve changes. The more complex the stay, the more valuable a single accountable line of communication becomes.','cards':[
  ('01 · One accountable contact','Know who owns the brief and who should be contacted when timing, guests or priorities change.'),
  ('02 · Written confirmations','Reservations, access, vehicles and supplier services should be treated as confirmed only when the relevant terms and timing are clear.'),
  ('03 · Realistic access','A serious concierge distinguishes between a request, an option and a confirmed booking instead of promising unlimited access.'),
  ('04 · Change control','When one part of the itinerary moves, the affected transport, villa, dining, yacht or security plan should be reviewed together.')],
 'cta':'Explore Private Concierge Ibiza →'
},
'es':{
 'path':'/es/ibiza-intelligence/','link':'/es/concierge-privado-ibiza/','kicker':'Cómo elegir un concierge privado en Ibiza','title':'Qué debería estar claro antes de delegar la estancia.','lead':'Una buena relación de concierge no se define por una lista interminable de servicios. Se define por la capacidad de un equipo para conectar lo confirmado, comunicar cambios y distinguir con claridad entre una solicitud y una reserva realmente asegurada.','body':'Para clientes privados, asistentes personales y family offices, la primera conversación debería fijar fechas, huéspedes, alojamiento, llegadas, reservas prioritarias, transporte y quién puede aprobar cambios. Cuanto más compleja sea la estancia, más valor aporta una sola línea de comunicación responsable.','cards':[
  ('01 · Un contacto responsable','Debe estar claro quién gestiona el brief y a quién se informa cuando cambian horarios, huéspedes o prioridades.'),
  ('02 · Confirmaciones por escrito','Reservas, accesos, vehículos y servicios de proveedores solo deben considerarse confirmados cuando términos y horarios estén claros.'),
  ('03 · Acceso realista','Un concierge serio diferencia entre solicitud, opción y reserva confirmada, sin prometer acceso ilimitado.'),
  ('04 · Control de cambios','Si cambia una parte del itinerario, transporte, villa, dining, yate o seguridad afectados deben revisarse en conjunto.')],
 'cta':'Explorar Concierge Privado Ibiza →'
},
'fr':{
 'path':'/fr/ibiza-intelligence/','link':'/fr/conciergerie-privee-ibiza/','kicker':'Choisir une conciergerie privée à Ibiza','title':'Ce qui doit être clair avant de déléguer le séjour.','lead':'Une bonne relation de conciergerie ne se résume pas à une longue liste de services. Elle repose sur la capacité d’une équipe à relier les éléments confirmés, communiquer les changements et distinguer clairement une demande d’une réservation réellement sécurisée.','body':'Pour les clients privés, assistants personnels et family offices, le premier échange doit préciser les dates, invités, hébergement, arrivées, réservations prioritaires, transport et la personne autorisée à valider les changements. Plus le séjour est complexe, plus un point de contact unique et responsable devient précieux.','cards':[
  ('01 · Un contact responsable','Savoir qui porte le brief et qui contacter lorsque les horaires, invités ou priorités changent.'),
  ('02 · Confirmations écrites','Réservations, accès, véhicules et prestations fournisseurs ne doivent être considérés confirmés que lorsque conditions et horaires sont clairs.'),
  ('03 · Accès réaliste','Une conciergerie sérieuse distingue demande, option et réservation confirmée sans promettre un accès illimité.'),
  ('04 · Gestion des changements','Lorsqu’un élément bouge, les transports, villa, dining, yacht ou sécurité concernés doivent être revus ensemble.')],
 'cta':'Découvrir la Conciergerie Privée Ibiza →'
},
'de':{
 'path':'/de/ibiza-intelligence/','link':'/de/privater-concierge-ibiza/','kicker':'Einen privaten Concierge auf Ibiza auswählen','title':'Was klar sein sollte, bevor Sie den Aufenthalt übergeben.','lead':'Eine gute Concierge-Beziehung wird nicht durch eine endlose Serviceliste definiert. Entscheidend ist, wie klar ein Team bestätigte Teile des Aufenthalts verbindet, Änderungen kommuniziert und zwischen Anfrage und tatsächlich bestätigter Leistung unterscheidet.','body':'Für Privatkunden, Personal Assistants und Family Offices sollte das erste Briefing Daten, Gäste, Unterkunft, Ankünfte, priorisierte Reservierungen, Transport und die Person klären, die Änderungen freigeben darf. Je komplexer der Aufenthalt, desto wertvoller ist eine einzige verantwortliche Kommunikationslinie.','cards':[
  ('01 · Ein verantwortlicher Kontakt','Es sollte klar sein, wer das Briefing führt und bei Änderungen von Zeiten, Gästen oder Prioritäten informiert wird.'),
  ('02 · Schriftliche Bestätigungen','Reservierungen, Zugang, Fahrzeuge und Anbieterleistungen gelten erst dann als bestätigt, wenn Bedingungen und Timing klar sind.'),
  ('03 · Realistischer Zugang','Ein seriöser Concierge unterscheidet zwischen Anfrage, Option und bestätigter Buchung, statt unbegrenzten Zugang zu versprechen.'),
  ('04 · Änderungssteuerung','Wenn sich ein Teil der Route ändert, sollten betroffene Transport-, Villa-, Dining-, Yacht- oder Sicherheitspläne gemeinsam geprüft werden.')],
 'cta':'Privaten Concierge Ibiza ansehen →'
},
'ar':{
 'path':'/ar/ibiza-intelligence/','link':'/ar/private-concierge-ibiza/','kicker':'اختيار كونسيرج خاص في إيبيزا','title':'ما الذي يجب أن يكون واضحاً قبل تسليم تفاصيل الإقامة.','lead':'لا تُقاس علاقة الكونسيرج الجيدة بطول قائمة الخدمات، بل بقدرة فريق واحد على ربط العناصر المؤكدة في الإقامة، وإدارة التغييرات، والتمييز بوضوح بين الطلب والخيار والحجز المؤكد فعلياً.','body':'بالنسبة للعملاء الخاصين والمساعدين الشخصيين والمكاتب العائلية، يجب أن يحدد الطلب الأول التواريخ والضيوف والسكن والوصول والحجوزات ذات الأولوية والنقل والشخص المخول بالموافقة على التغييرات. وكلما زادت تعقيدات الإقامة، زادت قيمة وجود جهة اتصال واحدة مسؤولة.','cards':[
  ('01 · جهة اتصال مسؤولة','يجب معرفة من يدير الطلب ومن يتم التواصل معه عند تغير المواعيد أو الضيوف أو الأولويات.'),
  ('02 · تأكيدات مكتوبة','لا تعتبر الحجوزات أو الدخول أو السيارات أو خدمات الموردين مؤكدة إلا بعد وضوح الشروط والتوقيت.'),
  ('03 · وصول واقعي','الكونسيرج الجاد يفرق بين الطلب والخيار والحجز المؤكد ولا يعد بوصول غير محدود.'),
  ('04 · إدارة التغييرات','عند تغير جزء من البرنامج يجب مراجعة النقل أو الفيلا أو المطاعم أو اليخت أو الأمن المتأثر ضمن خطة واحدة.')],
 'cta':'استكشف الكونسيرج الخاص في إيبيزا ←'
}}

def file_for(path):
    return ROOT/path.strip('/')/'index.html'

def block(d):
    cards=''.join(f'<div class="intel-card"><span>{num}</span><h3>{title}</h3><p>{copy}</p></div>' for raw,copy in d['cards'] for num,title in [raw.split(' · ',1)])
    return (f'<section class="editorial ivm-concierge-selection"><div><div class="kicker dark">{d["kicker"]}</div><h2>{d["title"]}</h2></div>'
            f'<div><p class="large">{d["lead"]}</p><p>{d["body"]}</p><p><a href="{d["link"]}">{d["cta"]}</a></p></div></section>'
            f'<section class="intelligence-home hub ivm-concierge-criteria"><div class="intelligence-grid">{cards}</div></section>')

for lang,d in DATA.items():
    f=file_for(d['path'])
    if not f.exists(): raise SystemExit(f'Phase 89 hub missing: {d["path"]}')
    html=f.read_text(encoding='utf-8')
    if 'ivm-concierge-selection' in html: raise SystemExit(f'Phase 89 duplicate selection guide: {d["path"]}')
    marker='<section class="closing-simple">' if lang=='en' else '<section class="closing">'
    if marker not in html: raise SystemExit(f'Phase 89 closing marker missing: {d["path"]}')
    html=html.replace(marker,block(d)+marker,1)
    f.write_text(html,encoding='utf-8')

print('PASS: Phase 89 concierge selection guidance — five Black Book hubs strengthened with localized decision criteria and same-language concierge pathways')
