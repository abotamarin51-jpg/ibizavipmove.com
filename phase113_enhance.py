"""Improve existing FR/DE/AR enquiry journeys without adding URLs or assets."""
from html import escape
from pathlib import Path
from urllib.parse import quote
import re

ROOT = Path('_site')
WA = 'https://wa.me/34600703303'
DATA = {
    'fr': {
        'international': 'clients-internationaux',
        'contact': '/fr/contact/',
        'contact_label': 'Préparer la demande avec le formulaire',
        'audiences': [
            ('Clients privés et familles', '/fr/conciergerie-privee-ibiza/'),
            ('Assistants personnels', '/fr/private-office/'),
            ('Family offices', '/fr/private-office/'),
            ('Luxury travel advisors', '/fr/partners/'),
            ('Sociétés de conciergerie', '/fr/partners/'),
            ('Partenaires de l’aviation privée', '/fr/aviation-privee-ibiza/'),
        ],
        'old_intro': 'Le brief peut venir de Londres, New York, Dubaï, Riyad, Genève, Paris, Francfort, Doha ou d’ailleurs. Le besoin reste le même : communication claire et exécution fiable sur l’île.',
        'intro': 'Vous préparez un séjour à Ibiza depuis l’étranger ? Centralisez les horaires d’arrivée, les services souhaités et les changements de programme avec un interlocuteur sur l’île.',
        'brief': 'Pour un premier échange, indiquez les dates, le nombre d’invités, les services souhaités et votre rôle. Précisez votre fuseau horaire, la personne autorisée à valider les demandes et si nous devons communiquer uniquement avec vous. Inutile d’envoyer des documents d’identité ou des coordonnées bancaires dans ce premier message.',
        'message': 'Bonjour Ibiza VIP Move, je vous contacte en tant que représentant pour organiser un séjour privé à Ibiza. Je souhaite préciser les services nécessaires, les validations et le mode de communication avant de transmettre le brief.',
    },
    'de': {
        'international': 'internationale-kunden',
        'contact': '/de/kontakt/',
        'contact_label': 'Anfrage im Formular vorbereiten',
        'audiences': [
            ('Privatkunden & Familien', '/de/privater-concierge-ibiza/'),
            ('Persönliche Assistenten', '/de/private-office/'),
            ('Family Offices', '/de/private-office/'),
            ('Luxury Travel Advisors', '/de/partners/'),
            ('Concierge-Unternehmen', '/de/partners/'),
            ('Private-Aviation-Partner', '/de/private-aviation-ibiza/'),
        ],
        'old_intro': 'Ob der Brief aus London, New York, Dubai, Riad, Genf, Paris, Frankfurt, Doha oder anderswo kommt: klare Kommunikation und zuverlässige Ausführung auf der Insel bleiben entscheidend.',
        'intro': 'Sie planen einen Aufenthalt auf Ibiza aus dem Ausland? Stimmen Sie Ankunftszeiten, gewünschte Leistungen und Änderungen im Reiseplan mit einem Ansprechpartner auf der Insel ab.',
        'brief': 'Nennen Sie für das erste Gespräch Reisedaten, Gästezahl, gewünschte Leistungen und Ihre Rolle. Geben Sie Ihre Zeitzone an, wer Anfragen freigeben darf und ob die Kommunikation ausschließlich über Sie laufen soll. Ausweisdokumente oder Bankdaten sind für diese erste Nachricht nicht nötig.',
        'message': 'Hallo Ibiza VIP Move, ich organisiere als Vertreter einen privaten Aufenthalt auf Ibiza. Vor der Übergabe des Briefings möchte ich die benötigten Leistungen, Freigaben und Kommunikationswege abstimmen.',
    },
    'ar': {
        'international': 'international-clients',
        'contact': '/ar/contact/',
        'contact_label': 'إعداد الطلب عبر النموذج',
        'audiences': [
            ('العملاء الخاصون والعائلات', '/ar/private-concierge-ibiza/'),
            ('المساعدون الشخصيون', '/ar/private-office/'),
            ('المكاتب العائلية', '/ar/private-office/'),
            ('مستشارو السفر الفاخر', '/ar/partners/'),
            ('شركات الكونسيرج', '/ar/partners/'),
            ('شركاء الطيران الخاص', '/ar/private-aviation-ibiza/'),
        ],
        'old_intro': 'سواء جاء الطلب من لندن أو نيويورك أو دبي أو الرياض أو جنيف أو باريس أو فرانكفورت أو الدوحة أو أي مكان آخر، تبقى الحاجة واحدة: تواصل واضح وتنفيذ موثوق على الجزيرة.',
        'intro': 'هل تخطط لإقامة في إيبيزا من الخارج؟ نسّق مواعيد الوصول والخدمات المطلوبة والتغييرات في البرنامج مع جهة اتصال واحدة على الجزيرة.',
        'brief': 'للتواصل الأول، اذكر التواريخ وعدد الضيوف والخدمات المطلوبة وصفتك. وضّح منطقتك الزمنية ومن يملك صلاحية الموافقة على الطلبات، وما إذا كان التواصل ينبغي أن يتم من خلالك فقط. لا حاجة لإرسال وثائق الهوية أو البيانات المصرفية في هذه الرسالة الأولى.',
        'message': 'مرحباً Ibiza VIP Move، أتواصل بصفتي ممثلاً لترتيب إقامة خاصة في إيبيزا. أود توضيح الخدمات المطلوبة وصلاحيات الموافقة وطريقة التواصل قبل إرسال تفاصيل الطلب.',
    },
}


def replace_once(text, old, new, context):
    if text.count(old) != 1:
        raise SystemExit(f'Phase 113 expected one {context}, found {text.count(old)}')
    return text.replace(old, new, 1)


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    pending = {}
    for lang, data in DATA.items():
        contact = '<p><a class="text-link" data-ivm113="contact" href="' + data['contact'] + '">' + escape(data['contact_label']) + '</a></p>'
        for slug in (data['international'], 'private-office'):
            path = ROOT / lang / slug / 'index.html'
            original = path.read_text(encoding='utf-8')
            if 'data-ivm113=' in original:
                raise SystemExit(f'Phase 113 duplicate application: {path}')
            match = re.search(r'<main\b[^>]*>(.*?)</main>', original, re.S)
            if not match:
                raise SystemExit(f'Phase 113 main landmark missing: {path}')
            main = match.group(1)
            if slug == data['international']:
                main = replace_once(main, escape(data['old_intro']), escape(data['intro']), str(path) + ' international intro')
                for label, href in data['audiences']:
                    if not (ROOT / href.strip('/') / 'index.html').is_file():
                        raise SystemExit(f'Phase 113 destination missing: {href}')
                    old = '<b>' + escape(label) + '</b>'
                    new = '<b><a class="text-link" data-ivm113="audience" href="' + href + '">' + escape(label) + '</a></b>'
                    main = replace_once(main, old, new, str(path) + ' audience ' + label)
                marker = '<div class="hero-actions" style="justify-content:center">'
                main = replace_once(main, marker, contact + marker, str(path) + ' contact actions')
            else:
                cta = re.search(r'(<section class="ivm-b2b-cta">.*?<h2>.*?</h2>)<p>.*?</p>', main, re.S)
                if not cta:
                    raise SystemExit(f'Phase 113 private office CTA missing: {path}')
                replacement = cta.group(1) + '<p data-ivm113="brief">' + escape(data['brief']) + '</p>' + contact
                main = replace_once(main, cta.group(0), replacement, str(path) + ' brief')
                old = 'href="' + WA + '"'
                if main.count(old) != 2:
                    raise SystemExit(f'Phase 113 expected two office WhatsApp CTAs: {path}')
                main = main.replace(old, 'data-ivm113="office" href="' + WA + '?text=' + quote(data['message'], safe='') + '"')
            if not (ROOT / data['contact'].strip('/') / 'index.html').is_file():
                raise SystemExit(f'Phase 113 contact destination missing: {data["contact"]}')
            # Preserve the full head, navigation, schema outside main and footer byte-for-byte.
            pending[path] = original[:match.start(1)] + main + original[match.end(1):]
    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 113 sitemap changed unexpectedly')
    # Do not partially patch the site when an expected source marker has drifted.
    for path, html in pending.items():
        path.write_text(html, encoding='utf-8')
    print('PASS: Phase 113 — six existing FR/DE/AR journeys; 18 contextual audience links; six contact-form routes; representative brief and localized office WhatsApp context; no new URLs/assets')


if __name__ == '__main__':
    enhance()
