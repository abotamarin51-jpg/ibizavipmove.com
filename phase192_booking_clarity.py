"""Replace generic process copy with practical booking guidance on 30 core pages.

The six service pillars share a layout, but each has its own scope, enquiry
checklist and quotation details. Existing approved FAQs and metadata stay intact.
"""
from html import escape
from pathlib import Path
import hashlib
import re

BASE = 'https://ibizavipmove.com'
LANGS = ('en', 'es', 'fr', 'de', 'ar')
ROUTES = {
    'chauffeur': ('private-chauffeur-ibiza', 'es/chauffeur-privado-ibiza', 'fr/chauffeur-prive-ibiza', 'de/privater-chauffeur-ibiza', 'ar/private-chauffeur-ibiza'),
    'villas': ('luxury-villas-ibiza', 'es/villas-lujo-ibiza', 'fr/villas-luxe-ibiza', 'de/luxusvillen-ibiza', 'ar/luxury-villas-ibiza'),
    'yacht': ('yacht-charter-ibiza', 'es/yate-privado-ibiza', 'fr/location-yacht-ibiza', 'de/yachtcharter-ibiza', 'ar/yacht-charter-ibiza'),
    'access': ('restaurants-nightlife-ibiza', 'es/restaurantes-nightlife-ibiza', 'fr/restaurants-nightlife-ibiza', 'de/restaurants-nightlife-ibiza', 'ar/restaurants-nightlife-ibiza'),
    'aviation': ('private-aviation-ibiza', 'es/aviacion-privada-ibiza', 'fr/aviation-privee-ibiza', 'de/private-aviation-ibiza', 'ar/private-aviation-ibiza'),
    'security': ('private-security-ibiza', 'es/seguridad-privada-ibiza', 'fr/securite-privee-ibiza', 'de/private-sicherheit-ibiza', 'ar/private-security-ibiza'),
}
CONTACT = {'en': '/contact/', 'es': '/es/contacto/', 'fr': '/fr/contact/', 'de': '/de/kontakt/', 'ar': '/ar/contact/'}
LABELS = {
    'en': ('Plan your service', 'What we can arrange', 'What to send', 'Before you confirm', 'Request a tailored quote', 'Ask on WhatsApp', 'Send your request by form or WhatsApp. We check availability, clarify the details and provide pricing and terms before your booking is confirmed.'),
    'es': ('Prepara tu reserva', 'Qué podemos organizar', 'Qué datos enviar', 'Antes de confirmar', 'Solicitar presupuesto', 'Consultar por WhatsApp', 'Envía tu solicitud por formulario o WhatsApp. Revisamos disponibilidad, concretamos los detalles y te facilitamos precio y condiciones antes de confirmar la reserva.'),
    'fr': ('Préparez votre réservation', 'Ce que nous organisons', 'Les informations à envoyer', 'Avant de confirmer', 'Demander un devis', 'Échanger sur WhatsApp', 'Envoyez votre demande par formulaire ou WhatsApp. Nous vérifions les disponibilités, précisons les détails et communiquons le prix et les conditions avant la confirmation de votre réservation.'),
    'de': ('Ihre Buchung vorbereiten', 'Was wir organisieren', 'Diese Angaben benötigen wir', 'Vor der Bestätigung', 'Angebot anfordern', 'Über WhatsApp anfragen', 'Senden Sie Ihre Anfrage per Formular oder WhatsApp. Wir prüfen die Verfügbarkeit, klären die Details und teilen Ihnen Preis und Bedingungen vor der Buchungsbestätigung mit.'),
    'ar': ('خطّط لحجزك', 'ما يمكننا تنسيقه', 'المعلومات المطلوبة', 'قبل تأكيد الحجز', 'اطلب عرض سعر', 'تواصل عبر واتساب', 'أرسل طلبك عبر النموذج أو واتساب. نتحقق من التوافر ونوضّح التفاصيل والسعر والشروط قبل تأكيد الحجز.'),
}

# Each entry is: heading, scope, enquiry checklist, quotation checklist.
COPY = {
 'en': {
  'chauffeur': ('Book your private chauffeur in Ibiza.', 'Airport transfers, hourly or multi-day driving, with stops at villas, hotels, marinas and venues. Vehicle and itinerary are agreed for your booking.', 'Travel date and times; pickup and destination; passengers and luggage. Add your flight number for airport arrivals and planned stops for hourly service.', 'Check the vehicle, booked hours, total price, taxes, waiting allowance, extra stops or hours, and cancellation terms in your written proposal.'),
  'villas': ('Plan your Ibiza villa stay.', 'Villa sourcing and pre-arrival coordination. Chefs, housekeeping, transport and other villa services can be requested alongside the property.', 'Check-in and check-out dates; guests and bedrooms; preferred area and budget. Include accessibility needs and any staff or arrival arrangements.', 'Check the property, included services, total price, deposit, check-in arrangements and cancellation terms. Requested staff and extras are quoted separately unless expressly included.'),
  'yacht': ('Plan your yacht charter in Ibiza.', 'Private yacht and day-charter requests, including proposed Formentera routes. Marina transfers and onboard catering can be coordinated on request.', 'Date, guests, preferred duration and budget; desired route and departure area. Mention catering, lunch plans and transport to the marina.', 'Check the vessel, capacity, hours and boarding point. Your proposal should identify crew, fuel, catering, taxes and any extra charges, plus weather and cancellation terms.'),
  'access': ('Arrange your Ibiza reservations.', 'Restaurant tables, beach-club daybeds or cabanas, and nightclub VIP table requests. Chauffeur transport can be added to the confirmed plan.', 'Date, venue or event, time, guest count and budget. Specify a restaurant table, daybed, cabana or VIP table, and any flexible alternatives.', 'Review the venue-confirmed option, table location where applicable, minimum spend, deposit, entry requirements and cancellation terms before accepting.'),
  'aviation': ('Arrange your private-flight arrival in Ibiza.', 'Ground transport and luggage coordination around your private flight, linked to your villa, hotel or marina. Aviation operations remain with the relevant providers.', 'Flight date and schedule; passengers and luggage; ground destination and an authorised contact for changes. Include terminal or handling details if available.', 'Confirm the vehicle, meeting arrangements, waiting time, total price and change terms. Airport access and handling arrangements depend on the relevant providers.'),
  'security': ('Request private security in Ibiza.', 'Private security and close-protection requests for stays, movements and events, coordinated with transport and the wider itinerary.', 'Share dates, locations, service hours and general requirements privately. Identify the person who will coordinate the request and approve the scope.', 'Review the proposed team, duties, coverage hours, access arrangements, price and cancellation terms. The service is defined for your specific requirements.'),
 },
 'es': {
  'chauffeur': ('Reserva tu chófer privado en Ibiza.', 'Traslados de aeropuerto y chófer por horas o varios días, con paradas en villas, hoteles, marinas y locales. Vehículo y recorrido se acuerdan para tu reserva.', 'Fecha y horarios; recogida y destino; pasajeros y equipaje. Añade número de vuelo para llegadas al aeropuerto y paradas previstas para el servicio por horas.', 'Revisa vehículo, horas contratadas, precio total, impuestos, espera incluida, paradas u horas extra y condiciones de cancelación en la propuesta escrita.'),
  'villas': ('Organiza tu estancia en una villa de Ibiza.', 'Búsqueda de villa y preparación de la llegada. Puedes solicitar chef, limpieza, transporte y otros servicios junto con el alojamiento.', 'Fechas de entrada y salida; huéspedes y dormitorios; zona preferida y presupuesto. Añade necesidades de accesibilidad, personal o preparación de la llegada.', 'Revisa propiedad, servicios incluidos, precio total, depósito, entrega y cancelación. El personal y los extras se presupuestan aparte salvo que se incluyan expresamente.'),
  'yacht': ('Organiza tu alquiler de yate en Ibiza.', 'Solicitudes de yates privados y salidas de día, con posibles rutas a Formentera. Podemos coordinar traslados a la marina y catering a bordo bajo petición.', 'Fecha, invitados, duración y presupuesto; ruta deseada y zona de salida. Indica catering, planes de comida y transporte a la marina.', 'Revisa embarcación, capacidad, horarios y embarque. La propuesta debe detallar tripulación, combustible, catering, impuestos y extras, además de condiciones por meteorología y cancelación.'),
  'access': ('Organiza tus reservas en Ibiza.', 'Mesas de restaurante, camas o cabañas en beach clubs y solicitudes de mesas VIP en discotecas. Puedes añadir chófer al plan confirmado.', 'Fecha, local o evento, hora, personas y presupuesto. Especifica mesa de restaurante, cama, cabaña o mesa VIP y posibles alternativas.', 'Revisa la opción confirmada por el local, ubicación de la mesa cuando corresponda, consumo mínimo, depósito, requisitos de entrada y condiciones de cancelación antes de aceptar.'),
  'aviation': ('Organiza tu llegada en vuelo privado a Ibiza.', 'Transporte terrestre y equipaje alrededor de tu vuelo privado, conectados con tu villa, hotel o marina. La operación aérea corresponde a los proveedores pertinentes.', 'Fecha y horario del vuelo; pasajeros y equipaje; destino terrestre y contacto autorizado para cambios. Añade terminal o datos de handling si los tienes.', 'Confirma vehículo, punto de encuentro, espera, precio total y condiciones de cambios. El acceso al aeropuerto y el handling dependen de los proveedores correspondientes.'),
  'security': ('Solicita seguridad privada en Ibiza.', 'Solicitudes de seguridad privada y protección personal para estancias, desplazamientos y eventos, coordinadas con el transporte y el itinerario.', 'Comparte de forma privada fechas, lugares, horas de servicio y necesidades generales. Indica quién coordinará la solicitud y aprobará su alcance.', 'Revisa equipo propuesto, funciones, horas de cobertura, acceso, precio y cancelación. El servicio se define según tus necesidades concretas.'),
 },
 'fr': {
  'chauffeur': ('Réservez votre chauffeur privé à Ibiza.', 'Transferts aéroport et chauffeur à l’heure ou sur plusieurs jours, avec arrêts aux villas, hôtels, marinas et établissements. Le véhicule et le parcours sont convenus pour votre réservation.', 'Date et horaires ; prise en charge et destination ; passagers et bagages. Ajoutez le numéro de vol pour une arrivée aéroport et les arrêts prévus pour une mise à disposition.', 'Vérifiez véhicule, heures réservées, prix total, taxes, attente incluse, arrêts ou heures supplémentaires et conditions d’annulation dans le devis écrit.'),
  'villas': ('Organisez votre séjour en villa à Ibiza.', 'Recherche de villa et préparation de l’arrivée. Chef, ménage, transport et autres services peuvent être demandés avec l’hébergement.', 'Dates d’arrivée et de départ ; voyageurs et chambres ; secteur souhaité et budget. Précisez les besoins d’accessibilité, de personnel ou de préparation de l’arrivée.', 'Vérifiez la propriété, les services inclus, le prix total, le dépôt, l’arrivée et les conditions d’annulation. Personnel et extras sont chiffrés séparément sauf inclusion explicite.'),
  'yacht': ('Organisez votre location de yacht à Ibiza.', 'Demandes de yachts privés et de sorties à la journée, avec itinéraire possible vers Formentera. Transferts à la marina et restauration à bord sur demande.', 'Date, passagers, durée et budget ; itinéraire et zone de départ souhaités. Précisez la restauration, les projets de déjeuner et le transport vers la marina.', 'Vérifiez yacht, capacité, horaires et embarquement. Le devis doit préciser équipage, carburant, restauration, taxes et suppléments, ainsi que les conditions météo et d’annulation.'),
  'access': ('Organisez vos réservations à Ibiza.', 'Tables de restaurant, lits de plage ou cabanas et demandes de tables VIP en club. Un chauffeur peut compléter le programme confirmé.', 'Date, établissement ou événement, horaire, nombre de personnes et budget. Précisez table de restaurant, lit de plage, cabana ou table VIP et les alternatives possibles.', 'Vérifiez l’option confirmée par l’établissement, l’emplacement de la table si applicable, le minimum de consommation, l’acompte, les conditions d’entrée et d’annulation avant d’accepter.'),
  'aviation': ('Organisez votre arrivée en vol privé à Ibiza.', 'Transport terrestre et coordination des bagages autour du vol privé, vers votre villa, hôtel ou marina. Les opérations aériennes relèvent des prestataires concernés.', 'Date et horaires du vol ; passagers et bagages ; destination au sol et contact autorisé pour les changements. Ajoutez les détails du terminal ou du handling si disponibles.', 'Confirmez véhicule, point de rencontre, attente, prix total et conditions de modification. L’accès à l’aéroport et le handling dépendent des prestataires concernés.'),
  'security': ('Demandez une sécurité privée à Ibiza.', 'Demandes de sécurité privée et de protection rapprochée pour séjours, déplacements et événements, coordonnées avec le transport et l’itinéraire.', 'Communiquez en privé dates, lieux, horaires de service et besoins généraux. Désignez la personne chargée de coordonner la demande et d’approuver le périmètre.', 'Vérifiez l’équipe proposée, les missions, les horaires de couverture, les accès, le prix et les conditions d’annulation. La prestation est définie selon vos besoins précis.'),
 },
 'de': {
  'chauffeur': ('Buchen Sie Ihren privaten Chauffeur auf Ibiza.', 'Flughafentransfers und Chauffeurdienste stundenweise oder für mehrere Tage, mit Stopps an Villen, Hotels, Häfen und Veranstaltungsorten. Fahrzeug und Route werden für Ihre Buchung vereinbart.', 'Datum und Uhrzeiten; Abholort und Ziel; Fahrgäste und Gepäck. Ergänzen Sie bei Flughafenankünften die Flugnummer und bei Stundenbuchungen die geplanten Stopps.', 'Prüfen Sie Fahrzeug, gebuchte Stunden, Gesamtpreis, Steuern, enthaltene Wartezeit, zusätzliche Stopps oder Stunden und Stornierungsbedingungen im schriftlichen Angebot.'),
  'villas': ('Planen Sie Ihren Villenaufenthalt auf Ibiza.', 'Villensuche und Vorbereitung der Ankunft. Privatkoch, Reinigung, Transport und weitere Leistungen können zusammen mit der Unterkunft angefragt werden.', 'Anreise und Abreise; Gäste und Schlafzimmer; gewünschte Lage und Budget. Nennen Sie Anforderungen an Barrierefreiheit, Personal oder Ankunftsvorbereitung.', 'Prüfen Sie Unterkunft, enthaltene Leistungen, Gesamtpreis, Kaution, Anreise und Stornierung. Personal und Extras werden separat angeboten, sofern sie nicht ausdrücklich enthalten sind.'),
  'yacht': ('Planen Sie Ihren Yachtcharter auf Ibiza.', 'Private Yachten und Tagescharter, auch mit gewünschter Route nach Formentera. Transfers zum Hafen und Verpflegung an Bord können auf Anfrage koordiniert werden.', 'Datum, Gäste, Dauer und Budget; gewünschte Route und Abfahrtsregion. Nennen Sie Verpflegung, Mittagspläne und benötigte Hafentransfers.', 'Prüfen Sie Yacht, Kapazität, Zeiten und Einstiegspunkt. Das Angebot sollte Crew, Treibstoff, Verpflegung, Steuern und Zusatzkosten sowie Wetter- und Stornierungsbedingungen ausweisen.'),
  'access': ('Planen Sie Ihre Reservierungen auf Ibiza.', 'Restauranttische, Liegen oder Cabanas in Beachclubs und VIP-Tischanfragen in Nachtclubs. Ein Chauffeur kann den bestätigten Ablauf ergänzen.', 'Datum, Lokal oder Event, Uhrzeit, Personenzahl und Budget. Geben Sie Restauranttisch, Liege, Cabana oder VIP-Tisch sowie mögliche Alternativen an.', 'Prüfen Sie das vom Lokal bestätigte Angebot, gegebenenfalls die Tischlage, Mindestverzehr, Anzahlung, Einlassregeln und Stornierungsbedingungen vor der Zusage.'),
  'aviation': ('Planen Sie Ihre Privatflugankunft auf Ibiza.', 'Bodentransport und Gepäckkoordination rund um Ihren Privatflug, abgestimmt auf Villa, Hotel oder Hafen. Der Flugbetrieb liegt bei den zuständigen Anbietern.', 'Flugdatum und Zeiten; Passagiere und Gepäck; Ziel am Boden und autorisierte Kontaktperson für Änderungen. Ergänzen Sie bekannte Terminal- oder Handlingdetails.', 'Bestätigen Sie Fahrzeug, Treffpunkt, Wartezeit, Gesamtpreis und Änderungsbedingungen. Flughafenzugang und Handling richten sich nach den zuständigen Anbietern.'),
  'security': ('Fragen Sie private Sicherheit auf Ibiza an.', 'Anfragen für private Sicherheit und Personenschutz bei Aufenthalten, Fahrten und Veranstaltungen, abgestimmt auf Transport und Reiseablauf.', 'Teilen Sie Daten, Orte, Einsatzzeiten und allgemeine Anforderungen vertraulich mit. Benennen Sie die Person, die die Anfrage koordiniert und den Umfang freigibt.', 'Prüfen Sie vorgeschlagenes Team, Aufgaben, Einsatzzeiten, Zugangsregelungen, Preis und Stornierungsbedingungen. Die Leistung wird nach Ihren konkreten Anforderungen festgelegt.'),
 },
 'ar': {
  'chauffeur': ('احجز سائقك الخاص في إيبيزا.', 'نقل من المطار وإليه وسائق بالساعة أو لعدة أيام، مع توقفات في الفلل والفنادق والمراسي والوجهات المطلوبة. تُحدّد السيارة والمسار لكل حجز.', 'التاريخ والمواعيد؛ مكان الاستلام والوجهة؛ عدد الركاب والأمتعة. أضف رقم الرحلة للوصول إلى المطار والتوقفات المتوقعة للخدمة بالساعة.', 'راجع السيارة والساعات المحجوزة والسعر الإجمالي والضرائب ووقت الانتظار المشمول والتوقفات أو الساعات الإضافية وشروط الإلغاء في العرض المكتوب.'),
  'villas': ('خطّط لإقامتك في فيلا بإيبيزا.', 'البحث عن فيلا وتنسيق الاستعداد للوصول. يمكن طلب طاهٍ خاص وتنظيف ونقل وخدمات أخرى مع الإقامة.', 'تواريخ الوصول والمغادرة؛ عدد الضيوف وغرف النوم؛ المنطقة المفضلة والميزانية. وضّح احتياجات سهولة الوصول أو الطاقم أو تجهيزات الوصول.', 'راجع العقار والخدمات المشمولة والسعر الإجمالي ومبلغ التأمين وترتيبات الوصول والإلغاء. تُسعّر خدمات الطاقم والإضافات بشكل منفصل ما لم تُدرج صراحةً.'),
  'yacht': ('خطّط لاستئجار يخت في إيبيزا.', 'طلبات اليخوت الخاصة والرحلات اليومية، مع إمكانية اقتراح مسار نحو فورمينتيرا. يمكن تنسيق النقل إلى المارينا والطعام على متن اليخت عند الطلب.', 'التاريخ وعدد الضيوف والمدة والميزانية؛ المسار ومنطقة الانطلاق المفضّلان. اذكر طلبات الطعام وخطط الغداء والنقل إلى المارينا.', 'راجع اليخت والسعة والمواعيد ونقطة الصعود. ينبغي أن يوضّح العرض الطاقم والوقود والطعام والضرائب والإضافات، إلى جانب شروط الطقس والإلغاء.'),
  'access': ('نظّم حجوزاتك في إيبيزا.', 'طاولات المطاعم وأسرّة الاسترخاء والكابانات في النوادي الشاطئية وطلبات طاولات VIP في النوادي الليلية. يمكن إضافة سائق إلى البرنامج المؤكّد.', 'التاريخ والمكان أو الفعالية والوقت وعدد الأشخاص والميزانية. حدّد نوع الحجز: طاولة مطعم أو سرير استرخاء أو كابانا أو طاولة VIP، مع البدائل الممكنة.', 'راجع الخيار الذي أكّده المكان وموقع الطاولة عند انطباقه والحد الأدنى للإنفاق والدفعة المقدّمة وشروط الدخول والإلغاء قبل الموافقة.'),
  'aviation': ('نظّم وصول رحلتك الخاصة إلى إيبيزا.', 'النقل البري وتنسيق الأمتعة حول رحلتك الخاصة، وربطها بالفيلا أو الفندق أو المارينا. تبقى عمليات الطيران لدى الجهات المعنية.', 'تاريخ الرحلة ومواعيدها؛ الركاب والأمتعة؛ الوجهة البرية وجهة اتصال مخوّلة بالتغييرات. أضف معلومات مبنى المطار أو المناولة إن توفرت.', 'أكّد السيارة ونقطة اللقاء والانتظار والسعر الإجمالي وشروط التعديل. يخضع دخول المطار وترتيبات المناولة للجهات المعنية.'),
  'security': ('اطلب خدمات الأمن الخاص في إيبيزا.', 'طلبات الأمن الخاص والحماية الشخصية للإقامات والتنقلات والفعاليات، بالتنسيق مع النقل وبرنامج الإقامة.', 'شارك بشكل خاص التواريخ والأماكن وساعات الخدمة والاحتياجات العامة. حدّد الشخص الذي سينسّق الطلب ويوافق على نطاق الخدمة.', 'راجع الفريق المقترح والمهام وساعات التغطية وترتيبات الدخول والسعر وشروط الإلغاء. تُحدّد الخدمة وفق احتياجاتك الخاصة.'),
 },
}

PROCESS = re.compile(r'<section class="process">.*?</section>', re.S)
EXISTING = re.compile(r'<section class="ivm-booking-guide"[^>]*>.*?</section>', re.S)
STYLE = re.compile(r'<link rel="stylesheet" href="(/assets/bundles/[^"/]+\.css)">')
CSS_MARKER = '\n/* Service booking clarity */\n'


def render(lang, service):
    kicker, scope_label, request_label, confirm_label, form_label, wa_label, intro = LABELS[lang]
    heading, *paragraphs = COPY[lang][service]
    cards = ''.join(
        f'<article><span class="ivm-booking-step" aria-hidden="true">0{i}</span>'
        f'<h3>{escape(label)}</h3><p>{escape(paragraph)}</p></article>'
        for i, (label, paragraph) in enumerate(zip((scope_label, request_label, confirm_label), paragraphs), 1)
    )
    return (
        '<section class="ivm-booking-guide" id="service-booking" aria-labelledby="service-booking-title">'
        f'<div class="section-head"><div class="kicker dark">{escape(kicker)}</div>'
        f'<h2 id="service-booking-title">{escape(heading)}</h2><p>{escape(intro)}</p></div>'
        f'<div class="ivm-booking-grid">{cards}</div><div class="ivm-booking-actions">'
        f'<a class="btn dark" href="{CONTACT[lang]}?service={service}">{escape(form_label)}</a>'
        f'<a class="text-link" href="https://wa.me/34600703303">{escape(wa_label)}</a></div></section>'
    )


def transform(html, route, lang, service):
    canonical = BASE + '/' + route + '/'
    assert html.count(f'<link rel="canonical" href="{canonical}">') == 1, route
    assert f'<html lang="{lang}"' in html, route
    assert lang != 'ar' or 'dir="rtl"' in html, route
    section = render(lang, service)
    matches = list(EXISTING.finditer(html)) or list(PROCESS.finditer(html))
    assert len(matches) == 1, f'Expected one booking/process section: {route}'
    old = matches[0]
    # Do not discard links or other independent content from the old process.
    if not EXISTING.fullmatch(old.group()):
        assert not re.search(r'<(?:a|img|script)\b', old.group(), re.I), route
    updated = html[:old.start()] + section + html[old.end():]
    return updated


def enhance(root=Path('_site')):
    pending = {}
    bundles = {}
    scoped_css = Path(__file__).with_suffix('.css').read_text(encoding='utf-8')
    sitemap_path = root / 'sitemap.xml'
    sitemap = sitemap_path.read_text(encoding='utf-8')
    for service, routes in ROUTES.items():
        for lang, route in zip(LANGS, routes):
            path = root / route / 'index.html'
            before = path.read_text(encoding='utf-8')
            after = transform(before, route, lang, service)
            # The approved FAQ answers, structured data and page identity must survive.
            assert re.findall(r'<details\b.*?</details>', before, re.S) == re.findall(r'<details\b.*?</details>', after, re.S), route
            assert re.findall(r'<script\b.*?</script>', before, re.S) == re.findall(r'<script\b.*?</script>', after, re.S), route
            assert before.split('</head>', 1)[0] == after.split('</head>', 1)[0], route
            assert transform(after, route, lang, service) == after, f'Non-idempotent: {route}'
            assert (root / CONTACT[lang].strip('/') / 'index.html').is_file(), route
            styles = list(STYLE.finditer(after))
            assert len(styles) == 1, f'Expected existing CSS bundle: {route}'
            original_css = (root / styles[0].group(1).lstrip('/')).read_text(encoding='utf-8')
            combined_css = original_css.split(CSS_MARKER, 1)[0] + CSS_MARKER + scoped_css
            digest = hashlib.sha256(combined_css.encode('utf-8')).hexdigest()[:16]
            href = f'/assets/bundles/{digest}.css'
            bundles[root / href.lstrip('/')] = combined_css
            after = after.replace(styles[0].group(), f'<link rel="stylesheet" href="{href}">', 1)
            pending[path] = after
            pattern = rf'(<url><loc>{re.escape(BASE + "/" + route + "/")}</loc><lastmod>)[^<]+(</lastmod>)'
            sitemap, count = re.subn(pattern, r'\g<1>2026-10-31\g<2>', sitemap)
            assert count == 1, f'Sitemap entry: {route}'
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    for path, css in bundles.items():
        path.write_text(css, encoding='utf-8')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    print(f'PASS: Booking clarity on {len(pending)} service pages; approved FAQs, schema and page identity preserved')


if __name__ == '__main__':
    enhance()
