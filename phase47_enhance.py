from pathlib import Path
import json
import re

ROOT=Path('_site')
STYLE='/assets/phase45.css?v=45'

PAGES={
'/es/chauffeur-privado-ibiza/':[
('¿Qué información es útil para solicitar un chófer privado en Ibiza?','Comparte las fechas, número de pasajeros, puntos de recogida, horario previsto y cualquier necesidad de equipaje o varios vehículos. Si el itinerario aún cambia, los horarios ya confirmados son suficientes para empezar.'),
('¿Se puede coordinar el chófer para varias paradas en un mismo día?','Sí. El servicio puede organizarse alrededor de varios movimientos confirmados, como villa, marina, restaurante y nightlife, manteniendo el planning bajo una sola línea de comunicación.'),
('¿Qué ocurre si cambia el horario?','Se revisan los movimientos afectados alrededor del nuevo horario. Es útil distinguir desde el principio qué elementos son fijos y cuáles pueden adaptarse.'),
('¿Se pueden coordinar varios vehículos?','Sí. Cuando el número de invitados, el equipaje o la agenda lo requieren, varios vehículos pueden coordinarse alrededor del mismo itinerario.')],
'/es/villas-lujo-ibiza/':[
('¿Qué debería incluir un brief para una villa privada?','Fechas, número de huéspedes, zona preferida, prioridades de privacidad y necesidades conocidas como personal, transporte, seguridad o acceso ayudan a definir el brief.'),
('¿La villa puede coordinarse con el resto de la estancia?','Sí. La llegada, los movimientos con chófer, los días de yate, las reservas y otros servicios confirmados pueden alinearse alrededor del mismo itinerario.'),
('¿Cómo conviene organizar el acceso a la llegada?','Es útil confirmar quién controla el acceso, la ventana estimada de llegada y quién puede resolver un cambio. Esa información debería estar conectada con el plan de transporte.'),
('¿Podemos empezar aunque el itinerario final no esté cerrado?','Sí. Se puede comenzar con los elementos esenciales ya confirmados y añadir otros servicios a medida que el planning se vaya definiendo.')],
'/es/yate-privado-ibiza/':[
('¿Qué información ayuda a planificar un día de yate en Ibiza?','Fecha, número de invitados, estilo de día deseado y prioridades conocidas de marina, restauración o Formentera son un buen punto de partida. También conviene considerar el transporte de ida y vuelta.'),
('¿El día de yate puede conectarse con la villa y los planes de la noche?','Sí. Horarios de marina, chófer, comida y el plan posterior pueden coordinarse como un único itinerario.'),
('¿Cómo se gestionan los cambios de horario?','El tiempo, la operativa de marina o las preferencias del grupo pueden modificar el planning. Si un cambio afecta a otros servicios, se revisan los elementos conectados.'),
('¿Hay que tener todo el día decidido antes de consultar?','No. Para empezar son suficientes la fecha, los invitados y las prioridades principales; el resto puede definirse según disponibilidad y planificación.')],
'/es/aviacion-privada-ibiza/':[
('¿Qué información es útil para coordinar una llegada en aviación privada?','Horario de vuelo, pasajeros, volumen de equipaje, destino posterior y el contacto autorizado para comunicar cambios son los datos esenciales.'),
('¿Se puede coordinar la llegada del avión con chófer y acceso a la villa?','Sí. Vuelo, equipaje, capacidad de vehículos y preparación del destino pueden tratarse como una misma llegada.'),
('¿Qué sucede si cambia la hora estimada de llegada?','Los servicios afectados por el nuevo horario se revisan alrededor de la ETA actualizada para evitar que los distintos equipos trabajen con horarios diferentes.'),
('¿Cómo se decide cuántos vehículos hacen falta?','No depende solo del número de pasajeros. Equipaje, material, necesidades de seguridad y movimientos separados también pueden cambiar la capacidad necesaria.')],
'/es/seguridad-privada-ibiza/':[
('¿Qué debería incluir un brief de seguridad privada?','Fechas, perfil del principal o invitados, ubicaciones relevantes, movimientos previstos y necesidades conocidas de privacidad o close protection son un buen punto de partida.'),
('¿La seguridad puede coordinarse con chófer y movimientos entre venues?','Sí. Seguridad, transporte, acceso a propiedades y horarios de venues pueden alinearse alrededor del mismo itinerario.'),
('¿Todas las estancias requieren la misma estructura de seguridad?','No. La estructura adecuada depende del principal, las ubicaciones, la agenda y los requisitos concretos.'),
('¿Se puede adaptar la seguridad si cambia el planning?','Sí. Si cambia el itinerario, también pueden revisarse los elementos de seguridad vinculados a esos movimientos.')],

'/fr/chauffeur-prive-ibiza/':[
('Quelles informations sont utiles pour demander un chauffeur privé à Ibiza ?','Partagez les dates, le nombre de passagers, les points de prise en charge, l’horaire prévu ainsi que les besoins en bagages ou en plusieurs véhicules. Si l’itinéraire évolue encore, les horaires déjà confirmés suffisent pour commencer.'),
('Le chauffeur peut-il être coordonné autour de plusieurs arrêts dans la journée ?','Oui. Villa, marina, restaurant, nightlife et autres mouvements confirmés peuvent être organisés autour d’un même planning et d’une seule ligne de communication.'),
('Que se passe-t-il si l’horaire change ?','Les mouvements concernés sont réévalués autour du nouvel horaire. Il est utile d’identifier dès le départ ce qui est fixe et ce qui peut s’adapter.'),
('Plusieurs véhicules peuvent-ils être coordonnés ensemble ?','Oui. Lorsque le nombre d’invités, les bagages ou le programme le nécessitent, plusieurs véhicules peuvent être alignés autour du même itinéraire.')],
'/fr/villas-luxe-ibiza/':[
('Que doit contenir un brief pour une villa privée ?','Les dates, le nombre d’invités, la zone souhaitée, les priorités de confidentialité et les besoins connus en personnel, transport, sécurité ou accès permettent de cadrer le brief.'),
('La villa peut-elle être coordonnée avec le reste du séjour ?','Oui. L’arrivée, les chauffeurs, les journées en yacht, les réservations et les autres services confirmés peuvent être alignés autour du même itinéraire.'),
('Comment préparer l’accès à la villa à l’arrivée ?','Il est utile de confirmer qui gère l’accès, la fenêtre d’arrivée prévue et qui peut résoudre un changement. Ces informations doivent être reliées au plan de transport.'),
('Peut-on commencer sans itinéraire finalisé ?','Oui. Les éléments essentiels déjà confirmés suffisent pour démarrer, puis les autres services peuvent être ajoutés à mesure que le planning se précise.')],
'/fr/location-yacht-ibiza/':[
('Quelles informations sont utiles pour préparer une journée en yacht à Ibiza ?','La date, le nombre d’invités, le style de journée recherché et les priorités connues concernant la marina, le déjeuner ou Formentera constituent un bon départ.'),
('La journée en yacht peut-elle être reliée à la villa et aux plans du soir ?','Oui. Les horaires de marina, le chauffeur, le déjeuner et la suite de la journée peuvent être coordonnés comme un seul itinéraire.'),
('Comment gérer un changement d’horaire ?','La météo, les opérations de marina ou les préférences des invités peuvent modifier le programme. Les services connectés sont alors réévalués autour du nouvel horaire.'),
('Faut-il avoir toute la journée définie avant de demander ?','Non. La date, les invités et les priorités principales suffisent pour commencer ; le reste peut être précisé selon les disponibilités.')],
'/fr/aviation-privee-ibiza/':[
('Quelles informations sont utiles pour coordonner une arrivée en aviation privée ?','L’horaire du vol, le nombre de passagers, le volume de bagages, la destination suivante et le contact autorisé à communiquer les changements sont les éléments essentiels.'),
('L’arrivée peut-elle être coordonnée avec le chauffeur et l’accès à la villa ?','Oui. Le vol, les bagages, la capacité des véhicules et la préparation de la destination peuvent être gérés comme un seul passage au sol.'),
('Que se passe-t-il si l’ETA change ?','Les services impactés sont réévalués autour de la nouvelle ETA afin que les équipes concernées travaillent avec le même horaire.'),
('Comment déterminer le nombre de véhicules nécessaires ?','Le nombre de passagers ne suffit pas. Les bagages, les équipements, la sécurité et les mouvements séparés peuvent modifier la capacité requise.')],
'/fr/securite-privee-ibiza/':[
('Que doit contenir un brief de sécurité privée ?','Les dates, le profil du principal ou des invités, les lieux concernés, les mouvements prévus et les besoins connus de confidentialité ou de protection rapprochée constituent une bonne base.'),
('La sécurité peut-elle être coordonnée avec chauffeur et déplacements entre lieux ?','Oui. Sécurité, transport, accès aux propriétés et horaires des lieux peuvent être alignés autour du même itinéraire.'),
('Tous les séjours nécessitent-ils la même structure de sécurité ?','Non. La structure appropriée dépend du principal, des lieux, du planning et des besoins spécifiques.'),
('La sécurité peut-elle évoluer si le programme change ?','Oui. Si l’itinéraire évolue, les éléments de sécurité liés aux mouvements concernés peuvent également être réévalués.')],

'/de/privater-chauffeur-ibiza/':[
('Welche Informationen sind für eine Anfrage nach einem privaten Chauffeur auf Ibiza hilfreich?','Teilen Sie Reisedaten, Anzahl der Gäste, Abholorte, den erwarteten Zeitplan sowie Gepäck- oder Mehrfahrzeugbedarf mit. Wenn die Route noch nicht final ist, reichen bestätigte Eckpunkte für den Start.'),
('Kann ein Chauffeur für mehrere Stopps an einem Tag koordiniert werden?','Ja. Villa, Marina, Restaurant, Nightlife und weitere bestätigte Fahrten können rund um einen Zeitplan und eine zentrale Kommunikationslinie organisiert werden.'),
('Was passiert, wenn sich eine Uhrzeit ändert?','Die betroffenen Fahrten werden rund um die neue Zeit neu abgestimmt. Hilfreich ist eine klare Trennung zwischen festen und flexiblen Bestandteilen.'),
('Können mehrere Fahrzeuge gemeinsam koordiniert werden?','Ja. Wenn Gästezahl, Gepäck oder Zeitplan es erfordern, können mehrere Fahrzeuge um dieselbe Route herum koordiniert werden.')],
'/de/luxusvillen-ibiza/':[
('Welche Angaben sollte ein Briefing für eine private Villa enthalten?','Reisedaten, Gästezahl, bevorzugte Lage, Privatsphäre-Prioritäten und bekannte Anforderungen an Personal, Transport, Security oder Zugang helfen bei der Planung.'),
('Kann die Villa mit dem restlichen Aufenthalt koordiniert werden?','Ja. Anreise, Chauffeur-Fahrten, Yachttage, Reservierungen und andere bestätigte Services können um dieselbe Reiseroute abgestimmt werden.'),
('Wie sollte der Zugang bei Ankunft vorbereitet werden?','Es sollte klar sein, wer den Zugang kontrolliert, welches Ankunftsfenster erwartet wird und wer bei Änderungen reagieren kann. Diese Informationen sollten mit dem Transportplan verbunden sein.'),
('Kann die Planung beginnen, wenn die finale Reiseroute noch nicht steht?','Ja. Bestätigte Kernelemente reichen für den Start; weitere Services können ergänzt werden, sobald sich der Zeitplan entwickelt.')],
'/de/yachtcharter-ibiza/':[
('Welche Informationen helfen bei der Planung eines Yachttages auf Ibiza?','Datum, Gästezahl, gewünschter Tagesstil und bekannte Prioritäten für Marina, Dining oder Formentera sind ein guter Ausgangspunkt. Auch Hin- und Rücktransport sollten mitgedacht werden.'),
('Kann der Yachttag mit Villa und Abendplanung verbunden werden?','Ja. Marina-Zeiten, Chauffeur, Lunch und die anschließende Abendplanung können als ein zusammenhängender Ablauf koordiniert werden.'),
('Wie werden Zeitänderungen behandelt?','Wetter, Marina-Abläufe oder Gästewünsche können den Plan verändern. Betroffene Services werden dann rund um die neue Zeit neu abgestimmt.'),
('Muss der gesamte Tag vor der Anfrage feststehen?','Nein. Datum, Gäste und Hauptprioritäten reichen für den Start; weitere Details können nach Verfügbarkeit konkretisiert werden.')],
'/de/private-aviation-ibiza/':[
('Welche Informationen sind für die Bodenkoordination bei Private Aviation hilfreich?','Flugzeit, Passagierzahl, Gepäckprofil, Weiterreiseziel und der für Zeitänderungen autorisierte Kontakt sind die wichtigsten Angaben.'),
('Kann die Flugankunft mit Chauffeur und Villenzugang koordiniert werden?','Ja. Flug, Gepäck, Fahrzeugkapazität und Bereitschaft des Zielorts können als ein zusammenhängender Ground-Movement-Prozess behandelt werden.'),
('Was passiert, wenn sich die ETA ändert?','Die von der neuen Ankunftszeit betroffenen Services werden neu abgestimmt, damit alle beteiligten Teams mit derselben Zeit arbeiten.'),
('Wie wird die erforderliche Fahrzeugkapazität bestimmt?','Nicht nur die Passagierzahl zählt. Gepäck, Equipment, Security-Anforderungen und getrennte Gästebewegungen können den Bedarf verändern.')],
'/de/private-sicherheit-ibiza/':[
('Welche Angaben sollte ein Private-Security-Briefing enthalten?','Reisedaten, Profil des Principals oder der Gäste, relevante Orte, geplante Bewegungen sowie bekannte Anforderungen an Privatsphäre oder Close Protection sind eine gute Grundlage.'),
('Kann Security mit Chauffeur und Venue-Bewegungen koordiniert werden?','Ja. Security, Transport, Zugang zu Immobilien und Venue-Zeiten können rund um denselben Zeitplan abgestimmt werden.'),
('Benötigt jeder Aufenthalt dieselbe Security-Struktur?','Nein. Die passende Struktur hängt vom Principal, den Orten, dem Zeitplan und den konkreten Anforderungen ab.'),
('Kann Security angepasst werden, wenn sich der Plan ändert?','Ja. Wenn sich die Route verändert, können auch die daran geknüpften Security-Elemente neu bewertet werden.')],

'/ar/private-chauffeur-ibiza/':[
('ما المعلومات المفيدة عند طلب سائق خاص في إيبيزا؟','شارك التواريخ وعدد الضيوف ونقاط الاستلام والجدول المتوقع وأي احتياجات تتعلق بالأمتعة أو بعدة سيارات. إذا كان البرنامج ما زال يتغير، تكفي المواعيد المؤكدة للبدء.'),
('هل يمكن تنسيق السائق لعدة توقفات في اليوم نفسه؟','نعم. يمكن تنظيم الفيلا والمارينا والمطاعم والحياة الليلية وغيرها من التحركات المؤكدة ضمن جدول واحد وخط تواصل واحد.'),
('ماذا يحدث إذا تغير الوقت؟','تتم مراجعة التحركات المتأثرة وفق التوقيت الجديد. من المفيد تحديد العناصر الثابتة والعناصر القابلة للتعديل منذ البداية.'),
('هل يمكن تنسيق عدة سيارات معاً؟','نعم. عندما يتطلب عدد الضيوف أو الأمتعة أو الجدول ذلك، يمكن تنسيق عدة سيارات حول البرنامج نفسه.')],
'/ar/luxury-villas-ibiza/':[
('ما الذي يجب أن يتضمنه طلب الفيلا الخاصة؟','التواريخ وعدد الضيوف والمنطقة المفضلة وأولويات الخصوصية وأي احتياجات معروفة مثل الطاقم أو النقل أو الأمن أو الدخول تساعد على تحديد الطلب.'),
('هل يمكن تنسيق الفيلا مع بقية الإقامة؟','نعم. يمكن ربط الوصول والسائق وأيام اليخت والحجوزات والخدمات المؤكدة الأخرى ضمن برنامج واحد.'),
('كيف يفضل تنظيم الدخول إلى الفيلا عند الوصول؟','من المفيد تأكيد من يدير الدخول ووقت الوصول المتوقع ومن يستطيع التعامل مع أي تغيير، وربط هذه المعلومات بخطة النقل.'),
('هل يمكن البدء قبل اكتمال البرنامج النهائي؟','نعم. تكفي العناصر الأساسية المؤكدة للبدء، ويمكن إضافة الخدمات الأخرى مع تطور البرنامج.')],
'/ar/yacht-charter-ibiza/':[
('ما المعلومات المفيدة لتخطيط يوم يخت في إيبيزا؟','التاريخ وعدد الضيوف ونمط اليوم المطلوب وأي أولويات معروفة للمارينا أو الطعام أو فورمينتيرا تشكل بداية جيدة. ومن الأفضل أيضاً التفكير في النقل من وإلى المارينا.'),
('هل يمكن ربط يوم اليخت بالفيلا وخطط المساء؟','نعم. يمكن تنسيق توقيت المارينا والسائق والغداء وما بعده كبرنامج واحد مترابط.'),
('كيف تتم إدارة تغييرات التوقيت؟','قد يؤثر الطقس أو تشغيل المارينا أو رغبات الضيوف على الجدول. عندها تتم مراجعة الخدمات المرتبطة وفق الوقت الجديد.'),
('هل يجب تحديد اليوم كاملاً قبل الاستفسار؟','لا. يكفي التاريخ والضيوف والأولويات الرئيسية للبدء، ثم يتم استكمال التفاصيل حسب التوفر.')],
'/ar/private-aviation-ibiza/':[
('ما المعلومات المفيدة لتنسيق الوصول بالطيران الخاص؟','توقيت الرحلة وعدد الركاب وحجم الأمتعة والوجهة التالية والشخص المخول بإبلاغ تغييرات الجدول هي المعلومات الأساسية.'),
('هل يمكن تنسيق وصول الطائرة مع السائق والدخول إلى الفيلا؟','نعم. يمكن التعامل مع الرحلة والأمتعة وسعة السيارات واستعداد الوجهة كعملية وصول واحدة مترابطة.'),
('ماذا يحدث إذا تغير وقت الوصول المتوقع؟','تتم مراجعة الخدمات المتأثرة وفق الوقت الجديد حتى تعمل جميع الفرق المعنية على نفس الجدول.'),
('كيف يتم تحديد عدد السيارات المطلوبة؟','الأمر لا يعتمد على عدد الركاب فقط؛ فالأمتعة والمعدات ومتطلبات الأمن والتحركات المنفصلة قد تغير السعة المطلوبة.')],
'/ar/private-security-ibiza/':[
('ما الذي يجب أن يتضمنه طلب الأمن الخاص؟','التواريخ وملف الضيف الرئيسي أو المجموعة والمواقع المهمة والتحركات المتوقعة وأي احتياجات معروفة للخصوصية أو الحماية القريبة تشكل أساساً جيداً.'),
('هل يمكن تنسيق الأمن مع السائق والتنقل بين المواقع؟','نعم. يمكن تنسيق الأمن والنقل والدخول إلى العقارات وتوقيت المواقع ضمن البرنامج نفسه.'),
('هل تحتاج كل إقامة إلى نفس هيكل الأمن؟','لا. يعتمد الهيكل المناسب على الضيف الرئيسي والمواقع والجدول والمتطلبات المحددة.'),
('هل يمكن تعديل الأمن إذا تغير البرنامج؟','نعم. إذا تغيرت التحركات، يمكن أيضاً مراجعة عناصر الأمن المرتبطة بها.')]
}

HEADINGS={
'es':('Antes del brief privado','Lo que normalmente conviene saber.','Respuestas operativas breves a las preguntas que suelen definir la primera conversación.'),
'fr':('Avant le brief privé','Ce qu’il est utile de savoir.','Des réponses opérationnelles courtes aux questions qui structurent le plus souvent la première conversation.'),
'de':('Vor dem privaten Briefing','Was vor der Anfrage hilfreich ist.','Kurze operative Antworten auf die Fragen, die das erste Gespräch am häufigsten prägen.'),
'ar':('قبل الطلب الخاص','ما الذي من المفيد معرفته أولاً.','إجابات تشغيلية مختصرة على الأسئلة التي تحدد عادة بداية المحادثة.')}


def lang_for(path):
    return path.split('/')[1]

def faq_schema(items):
    return {'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in items]}

for path,items in PAGES.items():
    file=ROOT/path.strip('/')/'index.html'
    if not file.exists():raise SystemExit(f'Phase 47 page missing: {path}')
    html=file.read_text(encoding='utf-8')
    if STYLE not in html:html=html.replace('</head>',f'<link rel="stylesheet" href="{STYLE}"></head>',1)
    if 'ivm-service-faq' not in html:
        lang=lang_for(path);eyebrow,h2,intro=HEADINGS[lang]
        details=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in items)
        section=f'<section class="ivm-service-faq" aria-label="Service planning questions"><div class="ivm-service-faq-inner"><div class="ivm-service-faq-head"><div class="eyebrow">{eyebrow}</div><h2>{h2}</h2><p>{intro}</p></div><div class="ivm-faq-list">{details}</div></div></section>'
        html=html.replace('</main>',section+'</main>',1)
    pattern=re.compile(r'<script\s+type="application/ld\+json">(.*?)</script>',re.I|re.S)
    out=[];cursor=0
    for m in pattern.finditer(html):
        out.append(html[cursor:m.start()])
        try:obj=json.loads(m.group(1))
        except Exception:obj=None
        if not (isinstance(obj,dict) and obj.get('@type')=='FAQPage'):out.append(m.group(0))
        cursor=m.end()
    out.append(html[cursor:]);html=''.join(out)
    html=html.replace('</head>',f'<script type="application/ld+json">{json.dumps(faq_schema(items),ensure_ascii=False)}</script></head>',1)
    file.write_text(html,encoding='utf-8')

for path,items in PAGES.items():
    html=(ROOT/path.strip('/')/'index.html').read_text(encoding='utf-8')
    faq=re.search(r'<section class="ivm-service-faq".*?</section>',html,re.I|re.S)
    assert faq and faq.group(0).count('<details>')==4,path
    faq_schemas=[]
    for m in re.finditer(r'<script\s+type="application/ld\+json">(.*?)</script>',html,re.I|re.S):
        try:obj=json.loads(m.group(1))
        except Exception:continue
        if isinstance(obj,dict) and obj.get('@type')=='FAQPage':faq_schemas.append(obj)
    assert len(faq_schemas)==1 and len(faq_schemas[0]['mainEntity'])==4,path
    assert STYLE in html and html.count('<h1')==1,path
print(f'PASS: Phase 47 localized FAQ decision layer added to {len(PAGES)} core service pages')
