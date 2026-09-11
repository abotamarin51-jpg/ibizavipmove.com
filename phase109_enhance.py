from pathlib import Path
from html import escape

ROOT=Path('_site')

PAGES={
'fr/conciergerie-privee-ibiza':{
 'kicker':'Conciergerie privée · Ibiza',
 'h2':'Une conciergerie privée pensée pour les séjours qui demandent plus qu’une réservation.',
 'intro':'Ibiza VIP Move accompagne les clients privés, couples, familles et assistants qui souhaitent centraliser plusieurs éléments de leur séjour à Ibiza auprès d’un seul contact local. Le rôle du concierge est de relier les horaires, les personnes, les lieux et les prestataires afin que l’ensemble reste cohérent lorsque le programme évolue.',
 'how':'Comment nous travaillons.',
 'steps':[
   ('01 · Brief privé','Nous commençons par les dates, le nombre de voyageurs, le lieu de séjour et les priorités. Un itinéraire complet n’est pas nécessaire pour démarrer.'),
   ('02 · Coordination locale','Les demandes sont organisées autour du séjour: chauffeur, villa, yacht, aviation privée, restaurants, nightlife, sécurité, chef, staffing ou demandes sur mesure.'),
   ('03 · Confirmations claires','Chaque service reste soumis à disponibilité, prix, conditions et confirmation. Nous évitons de présenter une demande comme garantie avant validation réelle.'),
   ('04 · Ajustements pendant le séjour','Lorsque les horaires changent, nous réalignons les éléments concernés et gardons la communication concentrée autour d’un point de contact.'),
 ],
 'areas':'Où nous opérons le plus souvent.',
 'areap':'Nous coordonnons des séjours dans toute Ibiza, avec une présence fréquente autour d’Ibiza Town, Marina Botafoch, Talamanca, Cap Martinet, Cala Jondal, Es Cubells, Santa Eulària, Roca Llisa, Santa Gertrudis, Sant Josep et les principales zones de villas, marinas, hôtels et beach clubs.',
 'fit':'Quand choisir la conciergerie privée?',
 'fitp':'Cette formule convient particulièrement lorsqu’un client combine plusieurs services ou lorsque les horaires se chevauchent. Pour une demande isolée, un service individuel peut suffire; pour un séjour complexe, la valeur vient surtout de la coordination entre les services.',
 'links':[
   ('/fr/chauffeur-prive-ibiza/','Chauffeur privé'),('/fr/villas-luxe-ibiza/','Villas de luxe'),('/fr/location-yacht-ibiza/','Yachts & charters'),('/fr/aviation-privee-ibiza/','Aviation privée'),('/fr/restaurants-nightlife-ibiza/','Restaurants & nightlife'),('/fr/securite-privee-ibiza/','Sécurité privée'),('/fr/contact/','Demander un brief privé')
 ]
},
'de/privater-concierge-ibiza':{
 'kicker':'Privater Concierge · Ibiza',
 'h2':'Private Concierge-Unterstützung für Aufenthalte, bei denen mehr als eine Buchung zusammenspielen muss.',
 'intro':'Ibiza VIP Move unterstützt Privatkunden, Paare, Familien und Assistenten, die mehrere Elemente ihres Ibiza-Aufenthalts über einen lokalen Ansprechpartner koordinieren möchten. Der Concierge verbindet Zeiten, Personen, Orte und Dienstleister, damit der Ablauf auch dann zusammenpasst, wenn sich Pläne ändern.',
 'how':'So arbeiten wir.',
 'steps':[
   ('01 · Privates Briefing','Wir starten mit Reisedaten, Gästezahl, Unterkunft und Prioritäten. Ein vollständig ausgearbeiteter Reiseplan ist für den ersten Schritt nicht erforderlich.'),
   ('02 · Lokale Koordination','Anfragen werden rund um den Aufenthalt organisiert: Chauffeur, Villa, Yacht, Private Aviation, Restaurants, Nightlife, Security, Private Chef, Villa Staff oder individuelle Wünsche.'),
   ('03 · Klare Bestätigung','Jeder Service bleibt abhängig von Verfügbarkeit, Preis, Bedingungen und finaler Bestätigung. Eine Anfrage wird nicht als garantiert dargestellt, bevor sie tatsächlich bestätigt ist.'),
   ('04 · Anpassung vor Ort','Wenn Zeiten oder Anforderungen wechseln, werden die betroffenen Elemente neu abgestimmt und die Kommunikation bleibt über einen zentralen Kontakt gebündelt.'),
 ],
 'areas':'Wo wir besonders häufig koordinieren.',
 'areap':'Wir betreuen Aufenthalte auf ganz Ibiza, häufig rund um Ibiza Town, Marina Botafoch, Talamanca, Cap Martinet, Cala Jondal, Es Cubells, Santa Eulària, Roca Llisa, Santa Gertrudis, Sant Josep sowie die wichtigsten Villen-, Marina-, Hotel- und Beach-Club-Zonen.',
 'fit':'Wann ist Private Concierge die richtige Wahl?',
 'fitp':'Dieses Modell eignet sich besonders, wenn mehrere Services verbunden werden müssen oder sich Zeitpläne gegenseitig beeinflussen. Für eine einzelne Leistung kann eine direkte Servicebuchung genügen; bei einem komplexeren Aufenthalt entsteht der eigentliche Mehrwert durch die Koordination zwischen den Leistungen.',
 'links':[
   ('/de/privater-chauffeur-ibiza/','Privater Chauffeur'),('/de/luxusvillen-ibiza/','Luxusvillen'),('/de/yachtcharter-ibiza/','Yachten & Charter'),('/de/private-aviation-ibiza/','Private Aviation'),('/de/restaurants-nightlife-ibiza/','Restaurants & Nightlife'),('/de/private-sicherheit-ibiza/','Private Sicherheit'),('/de/kontakt/','Privates Briefing senden')
 ]
},
'ar/private-concierge-ibiza':{
 'kicker':'كونسيرج خاص · إيبيزا',
 'h2':'خدمة كونسيرج خاصة للإقامات التي تحتاج إلى تنسيق أكثر من مجرد حجز واحد.',
 'intro':'تدعم Ibiza VIP Move العملاء الخاصين والأزواج والعائلات والمساعدين الذين يرغبون في إدارة عدة عناصر من إقامتهم في إيبيزا عبر جهة اتصال محلية واحدة. دور الكونسيرج هو ربط التوقيت والأشخاص والمواقع ومقدمي الخدمات بحيث تبقى الخطة مترابطة حتى عند تغير البرنامج.',
 'how':'كيف نعمل.',
 'steps':[
   ('01 · موجز خاص','نبدأ بالتواريخ وعدد الضيوف ومكان الإقامة والأولويات. لا يشترط وجود برنامج كامل قبل بدء التنسيق.'),
   ('02 · تنسيق محلي','يتم تنظيم الطلبات حول الإقامة: السائق الخاص، الفيلا، اليخت، الطيران الخاص، المطاعم والحياة الليلية، الأمن، الشيف، طاقم الفيلا أو الطلبات المخصصة.'),
   ('03 · تأكيد واضح','تظل كل خدمة خاضعة للتوفر والسعر والشروط والتأكيد النهائي. لا نعرض أي طلب على أنه مضمون قبل الحصول على التأكيد الفعلي.'),
   ('04 · تعديلات أثناء الإقامة','عند تغير التوقيت أو المتطلبات، نعيد تنسيق العناصر المتأثرة ونحافظ على التواصل من خلال نقطة اتصال واحدة.'),
 ],
 'areas':'المناطق التي ننسق فيها بشكل متكرر.',
 'areap':'ننسق الإقامات في مختلف أنحاء إيبيزا، بما في ذلك Ibiza Town وMarina Botafoch وTalamanca وCap Martinet وCala Jondal وEs Cubells وSanta Eulària وRoca Llisa وSanta Gertrudis وSant Josep، إضافة إلى مناطق الفلل والمراسي والفنادق والـ beach clubs الرئيسية.',
 'fit':'متى تكون خدمة الكونسيرج الخاص هي الأنسب؟',
 'fitp':'تكون هذه الخدمة مناسبة خصوصاً عندما يحتاج العميل إلى أكثر من خدمة في الوقت نفسه أو عندما تكون المواعيد مترابطة. يمكن أن تكفي خدمة منفردة لطلب بسيط، أما في الإقامة المعقدة فتأتي القيمة الأساسية من تنسيق جميع العناصر معاً.',
 'links':[
   ('/ar/private-chauffeur-ibiza/','السائق الخاص'),('/ar/luxury-villas-ibiza/','الفلل الفاخرة'),('/ar/yacht-charter-ibiza/','اليخوت والرحلات البحرية'),('/ar/private-aviation-ibiza/','الطيران الخاص'),('/ar/restaurants-nightlife-ibiza/','المطاعم والحياة الليلية'),('/ar/private-security-ibiza/','الأمن الخاص'),('/ar/contact/','إرسال طلب خاص')
 ]
},
}


def block(d):
    parts=[]
    for label,p in d['steps']:
        number,title=(label.split(' · ',1)+[''])[:2] if ' · ' in label else ('',label)
        parts.append(f'<article><span>{escape(number)}</span><h3>{escape(title)}</h3><p>{escape(p)}</p></article>')
    steps=''.join(parts)
    links=''.join(f'<a class="text-link" href="{escape(href,quote=True)}">{escape(label)} →</a>' for href,label in d['links'])
    return f'''<section class="editorial ivm-phase109-depth"><div><div class="kicker dark">{escape(d['kicker'])}</div><h2>{escape(d['h2'])}</h2></div><div><p class="large">{escape(d['intro'])}</p><h3>{escape(d['fit'])}</h3><p>{escape(d['fitp'])}</p><h3>{escape(d['areas'])}</h3><p>{escape(d['areap'])}</p></div></section><section class="process ivm-phase109-process"><div class="section-head"><div class="kicker dark">Private coordination</div><h2>{escape(d['how'])}</h2></div><div class="process-grid">{steps}</div><div class="ivm-phase109-links">{links}</div></section>'''

for slug,d in PAGES.items():
    target=ROOT/slug/'index.html'
    if not target.exists(): raise SystemExit(f'Phase 109 page missing: /{slug}/')
    html=target.read_text(encoding='utf-8')
    if 'ivm-phase109-depth' in html: raise SystemExit(f'Phase 109 duplicate depth block: /{slug}/')
    marker='<section class="closing-simple">'
    if marker not in html: raise SystemExit(f'Phase 109 closing marker missing: /{slug}/')
    html=html.replace(marker,block(d)+marker,1)
    target.write_text(html,encoding='utf-8')

print('PASS: Phase 109 multilingual concierge authority — FR/DE/AR cornerstone pages deepened with operating model, local Ibiza coverage and same-language service pathways')
