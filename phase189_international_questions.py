"""Localize the existing customer-question improvement for FR, DE and AR.

Reuse the visible/schema renderer and keep the other local service answers.
All routes already exist; Arabic retains the page's right-to-left direction.
"""
from pathlib import Path

from phase188_customer_questions import enhance as enhance_questions
from phase188_audit import audit


UPDATES = {
    '/fr/chauffeur-prive-ibiza/': {
        0: ('Comment réserver un chauffeur privé à Ibiza ?',
            'Contactez Ibiza VIP Move via le lien WhatsApp ou le formulaire du site. Indiquez la date, les lieux de prise en charge et de destination, le nombre de passagers, les bagages et si vous souhaitez un transfert ou plusieurs heures avec chauffeur. Pour une arrivée à l’aéroport, ajoutez les informations du vol. Nous confirmons par écrit le véhicule, les horaires, le prix et les conditions de réservation.'),
        1: ('Combien coûte un chauffeur privé à Ibiza ?',
            'Le devis dépend de la date, du trajet, du véhicule, du nombre de passagers et de la durée nécessaire. Précisez s’il s’agit d’un transfert aéroport, d’un aller-retour ou d’une mise à disposition à l’heure. Avant de réserver, vérifiez dans le devis écrit les heures prévues, l’attente, les arrêts supplémentaires, les prestations incluses et les conditions d’annulation.'),
        3: ('Puis-je réserver une Mercedes-Benz Classe V ou un Sprinter à Ibiza ?',
            'Vous pouvez demander une Mercedes-Benz Classe V ou un minibus Sprinter pour un service avec chauffeur privé. Précisez le nombre de passagers et les bagages afin de confirmer un véhicule adapté ou de coordonner plusieurs véhicules. Le modèle, la capacité et la disponibilité sont confirmés pour vos dates avant la réservation.'),
    },
    '/fr/villas-luxe-ibiza/': {
        0: ('Puis-je réserver une villa à Ibiza avec un chef privé et du personnel ?',
            'Oui. Ibiza VIP Move peut coordonner une demande de villa avec un chef privé et du personnel. Indiquez les dates, le nombre d’hôtes, le secteur souhaité, les repas et les horaires de service quotidiens. La propriété, la disponibilité du personnel, les missions, les achats alimentaires et les frais supplémentaires sont confirmés séparément par écrit ; ces prestations ne sont pas automatiquement incluses dans la réservation de la villa.'),
    },
    '/fr/location-yacht-ibiza/': {
        0: ('Comment organiser une journée en yacht privé d’Ibiza à Formentera ?',
            'Vous pouvez demander une journée en yacht privé au départ d’Ibiza avec Formentera comme destination souhaitée. Indiquez la date, le nombre de passagers, la marina de départ si vous la connaissez, l’itinéraire envisagé et vos projets de déjeuner. Le yacht, la capacité, le parcours, les horaires et les éventuels transferts vers la marina sont confirmés avant la réservation. L’itinéraire reste soumis à la météo et à la décision du capitaine.'),
        3: ('Que faut-il vérifier dans un devis de location de yacht à Ibiza ?',
            'Vérifiez le yacht, la capacité d’accueil, la durée de location, le lieu de départ et les conditions d’annulation. Demandez quels frais sont inclus ou facturés séparément, notamment le carburant, l’équipage, la restauration, les frais de port et les transferts. Ibiza VIP Move précise les conditions de l’opérateur pour le yacht choisi avant votre confirmation.'),
    },
    '/fr/restaurants-nightlife-ibiza/': {
        0: ('Pouvez-vous organiser des réservations de dernière minute dans les restaurants et clubs d’Ibiza ?',
            'Nous étudions les demandes de dernière minute pour les restaurants, beach clubs et établissements de nuit selon les disponibilités. Envoyez la date, l’heure, le nombre de personnes, le lieu souhaité et les alternatives possibles. Ibiza VIP Move vérifie les options et confirme les acomptes, le minimum de consommation et les conditions d’accès avant de considérer une réservation comme confirmée. Une demande ne garantit ni table ni entrée.'),
    },
    '/fr/securite-privee-ibiza/': {
        0: ('Comment demander un service de sécurité privée et de protection rapprochée à Ibiza ?',
            'Ibiza VIP Move coordonne les demandes de sécurité privée et de protection rapprochée pendant le séjour. Communiquez en privé les dates, les lieux, les déplacements prévus et vos besoins généraux. L’équipe adaptée, le périmètre, les disponibilités et les conditions du service sont définis pour chaque demande avant confirmation.'),
    },
    '/de/privater-chauffeur-ibiza/': {
        0: ('Wie buche ich einen privaten Chauffeur auf Ibiza?',
            'Kontaktieren Sie Ibiza VIP Move über den WhatsApp-Link oder das Anfrageformular auf der Website. Nennen Sie Datum, Abholort, Ziel, Fahrgastzahl, Gepäck und ob Sie einen Transfer oder mehrere Stunden mit Chauffeur benötigen. Bei Ankunft am Flughafen ergänzen Sie bitte die Flugdaten. Fahrzeug, Zeiten, Preis und Buchungsbedingungen bestätigen wir schriftlich.'),
        1: ('Was kostet ein privater Chauffeur auf Ibiza?',
            'Das Angebot richtet sich nach Datum, Strecke, Fahrzeug, Fahrgastzahl und benötigter Dauer. Geben Sie an, ob Sie einen Flughafentransfer, eine Hin- und Rückfahrt oder einen Chauffeur auf Stundenbasis wünschen. Prüfen Sie vor der Buchung die vereinbarten Stunden, Wartezeiten, zusätzlichen Stopps, enthaltenen Leistungen und Stornierungsbedingungen im schriftlichen Angebot.'),
        3: ('Kann ich eine Mercedes-Benz V-Klasse oder einen Sprinter auf Ibiza buchen?',
            'Für private Chauffeurdienste können Sie eine Mercedes-Benz V-Klasse oder einen Sprinter-Minibus anfragen. Nennen Sie Fahrgastzahl und Gepäck, damit ein geeignetes Fahrzeug bestätigt oder mehrere Fahrzeuge koordiniert werden können. Modell, Kapazität und Verfügbarkeit für Ihre Reisedaten werden vor der Buchung bestätigt.'),
    },
    '/de/luxusvillen-ibiza/': {
        0: ('Kann ich eine Villa auf Ibiza mit Privatkoch und Personal buchen?',
            'Ja. Ibiza VIP Move kann Villenanfragen mit Privatkoch und Personal koordinieren. Nennen Sie Reisedaten, Gästezahl, bevorzugte Lage, Mahlzeiten und tägliche Einsatzzeiten. Unterkunft, Personalverfügbarkeit, Aufgaben, Lebensmitteleinkäufe und Zusatzkosten werden gesondert schriftlich bestätigt; diese Leistungen sind nicht automatisch in der Villenbuchung enthalten.'),
    },
    '/de/yachtcharter-ibiza/': {
        0: ('Wie plane ich einen privaten Yachtausflug von Ibiza nach Formentera?',
            'Sie können einen privaten Yachttag ab Ibiza mit Formentera als gewünschtem Ziel anfragen. Nennen Sie Datum, Gästezahl, den Abfahrtshafen, falls bekannt, die gewünschte Route und Ihre Mittagspläne. Yacht, Kapazität, Route, Zeiten und mögliche Transfers zum Hafen werden vor der Buchung bestätigt. Die Route bleibt vom Wetter und der Entscheidung des Kapitäns abhängig.'),
        3: ('Was sollte ich bei einem Yachtcharter-Angebot auf Ibiza prüfen?',
            'Prüfen Sie Yacht, Gästekapazität, Charterdauer, Abfahrtsort und Stornierungsbedingungen. Fragen Sie, welche Kosten enthalten sind und welche separat berechnet werden, insbesondere Treibstoff, Crew, Verpflegung, Hafengebühren und Transfers. Ibiza VIP Move klärt die Bedingungen des Anbieters für die gewählte Yacht vor Ihrer Bestätigung.'),
    },
    '/de/restaurants-nightlife-ibiza/': {
        0: ('Können Sie kurzfristige Restaurant- und VIP-Reservierungen auf Ibiza organisieren?',
            'Wir prüfen kurzfristige Anfragen für Restaurants, Beachclubs und Nachtclubs nach Verfügbarkeit. Senden Sie Datum, Uhrzeit, Personenzahl, Wunschlokal und mögliche Alternativen. Ibiza VIP Move prüft die Optionen und bestätigt Anzahlungen, Mindestverzehr und Einlassbedingungen, bevor eine Reservierung als gebucht gilt. Eine Anfrage garantiert weder einen Tisch noch den Einlass.'),
    },
    '/de/private-sicherheit-ibiza/': {
        0: ('Wie frage ich private Sicherheit und Personenschutz auf Ibiza an?',
            'Ibiza VIP Move koordiniert Anfragen für private Sicherheit und Personenschutz während Ihres Aufenthalts. Teilen Sie Reisedaten, Orte, geplante Fahrten und allgemeine Anforderungen vertraulich mit. Das passende Team, der Leistungsumfang, die Verfügbarkeit und die Bedingungen werden für die konkrete Anfrage vor der Bestätigung festgelegt.'),
    },
    '/ar/private-chauffeur-ibiza/': {
        0: ('كيف أحجز سائقاً خاصاً في إيبيزا؟',
            'تواصل مع Ibiza VIP Move عبر رابط واتساب أو نموذج الاستفسار في الموقع. حدّد التاريخ ومكان الاستلام والوجهة وعدد الركاب والأمتعة، وما إذا كنت تحتاج إلى رحلة نقل واحدة أو سائق لعدة ساعات. عند الوصول إلى المطار، أضف بيانات الرحلة الجوية. نؤكد كتابياً السيارة والمواعيد والسعر وشروط الحجز.'),
        1: ('ما تكلفة السائق الخاص في إيبيزا؟',
            'يعتمد عرض السعر على التاريخ والمسار والسيارة وعدد الركاب والمدة المطلوبة. وضّح ما إذا كنت تحتاج إلى نقل من المطار أو إليه، أو رحلة ذهاب وعودة، أو سائق بالساعة. قبل الحجز، راجع الساعات المتفق عليها ووقت الانتظار والتوقفات الإضافية والخدمات المشمولة وشروط الإلغاء في العرض المكتوب.'),
        3: ('هل يمكنني حجز مرسيدس بنز الفئة V أو سبرينتر في إيبيزا؟',
            'يمكن طلب سيارات مرسيدس بنز الفئة V وحافلات سبرينتر الصغيرة لخدمات السائق الخاص. أرسل عدد الركاب وحجم الأمتعة لتأكيد سيارة مناسبة أو تنسيق عدة سيارات. يتم تأكيد الطراز والسعة والتوافر في تواريخك قبل الحجز.'),
    },
    '/ar/luxury-villas-ibiza/': {
        0: ('هل يمكنني حجز فيلا في إيبيزا مع طاهٍ خاص وطاقم خدمة؟',
            'نعم. يمكن لـ Ibiza VIP Move تنسيق طلب الفيلا مع طاهٍ خاص وطاقم خدمة. حدّد تواريخ الإقامة وعدد الضيوف والمنطقة المفضلة والوجبات وساعات العمل اليومية. يتم تأكيد العقار وتوافر الطاقم والمهام وشراء المواد الغذائية والتكاليف الإضافية بشكل منفصل وكتابياً؛ ولا تُدرج هذه الخدمات تلقائياً ضمن حجز الفيلا.'),
    },
    '/ar/yacht-charter-ibiza/': {
        0: ('كيف أنظّم رحلة بيخت خاص من إيبيزا إلى فورمينتيرا؟',
            'يمكنك طلب رحلة يومية بيخت خاص من إيبيزا مع فورمينتيرا كوجهة مقترحة. حدّد التاريخ وعدد الضيوف ومارينا الانطلاق إن كانت معروفة والمسار المفضل وخطط الغداء. يتم تأكيد اليخت والسعة والمسار والمواعيد وأي خدمات نقل إلى المارينا قبل الحجز. يبقى المسار خاضعاً للطقس وقرار القبطان.'),
        3: ('ما الذي يجب مراجعته في عرض استئجار يخت في إيبيزا؟',
            'راجع اليخت وسعة الضيوف وساعات الاستئجار ونقطة الانطلاق وشروط الإلغاء. اسأل عن التكاليف المشمولة والتي تُحسب بشكل منفصل، خصوصاً الوقود والطاقم والطعام ورسوم المارينا وخدمات النقل. يوضّح Ibiza VIP Move شروط المشغّل لليخت المختار قبل تأكيدك.'),
    },
    '/ar/restaurants-nightlife-ibiza/': {
        0: ('هل يمكنكم ترتيب حجوزات اللحظة الأخيرة للمطاعم وطاولات VIP في إيبيزا؟',
            'ندرس طلبات اللحظة الأخيرة للمطاعم والنوادي الشاطئية والنوادي الليلية حسب التوافر. أرسل التاريخ والوقت وعدد الأشخاص والمكان المفضل والبدائل الممكنة. يتحقق Ibiza VIP Move من الخيارات ويؤكد الدفعات المقدمة والحد الأدنى للإنفاق وشروط الدخول قبل اعتبار الحجز مؤكداً. إرسال الطلب لا يضمن طاولة أو دخولاً.'),
    },
    '/ar/private-security-ibiza/': {
        0: ('كيف أطلب خدمات الأمن الخاص والحماية الشخصية في إيبيزا؟',
            'ينسّق Ibiza VIP Move طلبات الأمن الخاص والحماية الشخصية خلال الإقامة. شارك بشكل خاص التواريخ والأماكن وخطط التنقل والاحتياجات العامة. يتم تحديد الفريق المناسب ونطاق الخدمة والتوافر والشروط وفق متطلبات كل طلب قبل التأكيد.'),
    },
}

ADDITIONS = {
    '/fr/conciergerie-privee-ibiza/': {
        'kicker': 'Questions fréquentes',
        'heading': 'Organiser votre séjour à Ibiza.',
        'service_name': 'Conciergerie privée à Ibiza',
        'items': [
            ('Que comprend un service de conciergerie de luxe à Ibiza ?',
             'Ibiza VIP Move coordonne chauffeurs privés, villas, yachts, réservations de restaurants et expériences VIP, assistance en aviation privée, sécurité, chefs et personnel via un interlocuteur local. Vous pouvez demander une prestation ou un itinéraire complet. Chaque service, sa disponibilité, son prix et les conditions du prestataire sont convenus séparément avant confirmation.'),
            ('Puis-je faire appel au concierge pour une seule réservation à Ibiza ?',
             'Oui. Vous pouvez demander une réservation précise ou coordonner plusieurs services pour votre séjour. Indiquez les dates, le nombre de personnes et vos besoins ; nous confirmons le périmètre et les conditions applicables avant de réserver.'),
            ('Accompagnez-vous les assistants personnels et les family offices à Ibiza ?',
             'Oui. Notre Private Office offre un interlocuteur local aux assistants personnels, family offices et conseillers en voyages qui organisent un séjour à Ibiza. Indiquez les dates, les voyageurs, le secteur de l’hébergement, les services souhaités, le fuseau horaire pour les réponses et la personne habilitée à autoriser les changements. Nous coordonnons les réservations confirmées et les mises à jour via le canal convenu.'),
            ('Les réservations et l’accès VIP à Ibiza sont-ils garantis ?',
             'La disponibilité, les acomptes, le minimum de consommation, les conditions d’accès et les modalités de chaque prestataire sont vérifiés avant confirmation. Une demande de réservation ne constitue pas une réservation confirmée.'),
        ],
    },
    '/de/privater-concierge-ibiza/': {
        'kicker': 'Häufige Fragen',
        'heading': 'Ihren Aufenthalt auf Ibiza planen.',
        'service_name': 'Privater Concierge auf Ibiza',
        'items': [
            ('Was umfasst ein Luxus-Concierge-Service auf Ibiza?',
             'Ibiza VIP Move koordiniert private Chauffeure, Villen, Yachten, Restaurant- und VIP-Reservierungen, Unterstützung bei Privatflügen, Sicherheit, Privatköche und Personal über einen lokalen Ansprechpartner. Sie können eine einzelne Leistung oder ein komplettes Reiseprogramm anfragen. Jede Leistung, ihre Verfügbarkeit, ihr Preis und die Bedingungen des Anbieters werden vor der Bestätigung gesondert vereinbart.'),
            ('Kann ich den Concierge auf Ibiza für eine einzelne Reservierung beauftragen?',
             'Ja. Sie können eine einzelne Reservierung anfragen oder mehrere Leistungen für Ihren Aufenthalt koordinieren lassen. Nennen Sie Reisedaten, Personenzahl und Ihre Wünsche; wir bestätigen den Umfang und die geltenden Bedingungen vor der Buchung.'),
            ('Unterstützen Sie persönliche Assistenten und Family Offices auf Ibiza?',
             'Ja. Unser Private Office bietet persönlichen Assistenten, Family Offices und Reiseberatern einen lokalen Ansprechpartner für die Planung eines Ibiza-Aufenthalts. Nennen Sie Reisedaten, Gäste, die Lage der Unterkunft, benötigte Leistungen, die Zeitzone für Rückmeldungen und die Person, die Änderungen freigeben darf. Wir koordinieren bestätigte Buchungen und Aktualisierungen über den vereinbarten Kommunikationskanal.'),
            ('Sind Reservierungen und VIP-Zugang auf Ibiza garantiert?',
             'Verfügbarkeit, Anzahlungen, Mindestverzehr, Einlassbedingungen und die Bedingungen des jeweiligen Anbieters werden vor der Bestätigung geprüft. Eine Buchungsanfrage ist noch keine bestätigte Buchung.'),
        ],
    },
    '/ar/private-concierge-ibiza/': {
        'kicker': 'الأسئلة الشائعة',
        'heading': 'تنظيم إقامتك في إيبيزا.',
        'service_name': 'كونسيرج خاص في إيبيزا',
        'items': [
            ('ماذا تشمل خدمة الكونسيرج الفاخرة في إيبيزا؟',
             'ينسّق Ibiza VIP Move خدمات السائق الخاص والفلل واليخوت وحجوزات المطاعم وتجارب VIP ودعم الطيران الخاص والأمن والطهاة وطاقم الخدمة عبر جهة اتصال محلية واحدة. يمكنك طلب خدمة واحدة أو برنامج إقامة متكامل. يتم الاتفاق بشكل منفصل على كل خدمة وتوافرها وسعرها وشروط المورّد قبل التأكيد.'),
            ('هل يمكنني الاستعانة بالكونسيرج لحجز واحد فقط في إيبيزا؟',
             'نعم. يمكنك طلب حجز محدد أو تنسيق عدة خدمات خلال إقامتك. شارك التواريخ وعدد الأشخاص واحتياجاتك؛ ونؤكد نطاق الخدمة والشروط المطبقة قبل الحجز.'),
            ('هل تتعاونون مع المساعدين الشخصيين والمكاتب العائلية في إيبيزا؟',
             'نعم. يوفّر مكتبنا الخاص جهة اتصال محلية واحدة للمساعدين الشخصيين والمكاتب العائلية ومستشاري السفر الذين ينظّمون إقامة في إيبيزا. حدّد التواريخ والضيوف ومنطقة السكن والخدمات المطلوبة والمنطقة الزمنية للردود والشخص المخوّل بالموافقة على التغييرات. ننسّق الحجوزات المؤكدة والتحديثات عبر قناة التواصل المتفق عليها.'),
            ('هل الحجوزات ودخول أماكن VIP في إيبيزا مضمونان؟',
             'يتم التحقق من التوافر والدفعات المقدمة والحد الأدنى للإنفاق وشروط الدخول وشروط كل مورّد قبل التأكيد. طلب الحجز لا يعني أن الحجز قد تأكد.'),
        ],
    },
}
ROUTES = tuple(UPDATES) + tuple(ADDITIONS)


def enhance(root=Path('_site')):
    enhance_questions(root, updates=UPDATES, additions=ADDITIONS)
    audit(root, routes=ROUTES)


if __name__ == '__main__':
    enhance()
