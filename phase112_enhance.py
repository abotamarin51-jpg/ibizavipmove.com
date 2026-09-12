from pathlib import Path
from html import escape

ROOT = Path('_site')

PAGES = {
    '/fr/partners/': {
        'eyebrow': 'DMC · Destination Management · Partenaires internationaux',
        'title': 'Un relais Ibiza clair pour les briefs internationaux.',
        'lead': "Pour une société de conciergerie, un travel advisor ou un private office, le besoin n’est pas une longue liste de fournisseurs : c’est un opérateur local capable de reprendre un brief international et de coordonner l’exécution à Ibiza.",
        'body': "Ibiza VIP Move peut intervenir comme partenaire DMC / destination management, relais de private travel management ou couche opérationnelle locale, selon le workflow convenu avec le partenaire. La relation client reste protégée et aucun service n’est considéré comme confirmé avant validation réelle de la disponibilité, du périmètre et des conditions applicables.",
        'cards': [
            ('DMC / destination management', "Coordination locale du transport, des villas, yachts, de l’aviation privée, de l’hospitality et de la logistique invités autour d’un même itinéraire.", '/fr/services/', 'Voir les services Ibiza →'),
            ('Private travel management', "Passage du travel planning international à l’exécution sur l’île, avec un seul point de contact pour les dépendances et les changements du séjour.", '/fr/conciergerie-privee-ibiza/', 'Conciergerie privée Ibiza →'),
            ('PAs & family offices', "Support discret pour principals et représentants autorisés, avec communication need-to-know et coordination multi-services.", '/fr/private-office/', 'Private Office Ibiza →'),
        ],
    },
    '/de/partners/': {
        'eyebrow': 'DMC · Destination Management · Internationale Partner',
        'title': 'Eine klare Ibiza-Schnittstelle für internationale Briefings.',
        'lead': 'Für Concierge-Unternehmen, Luxury Travel Advisors oder Private Offices zählt nicht eine lange Lieferantenliste, sondern ein lokaler Operator, der ein internationales Briefing übernimmt und die Ausführung auf Ibiza verbindet.',
        'body': 'Ibiza VIP Move kann je nach vereinbartem Workflow als lokaler DMC-/Destination-Management-Partner, als operative Ebene für Private Travel Management oder als Ibiza-Schnittstelle im Hintergrund arbeiten. Die Kundenbeziehung bleibt beim Partner; Leistungen gelten erst nach tatsächlicher Prüfung von Verfügbarkeit, Umfang und Bedingungen als bestätigt.',
        'cards': [
            ('DMC / Destination Management', 'Lokale Koordination von Transport, Villen, Yachten, Private Aviation, Hospitality und Gästelogistik rund um eine gemeinsame Reiseroute.', '/de/services/', 'Ibiza Services ansehen →'),
            ('Private Travel Management', 'Übergabe vom internationalen Travel Planning an die Ausführung auf der Insel – mit einem Ibiza-Kontakt für Abhängigkeiten und Planänderungen.', '/de/privater-concierge-ibiza/', 'Privater Concierge Ibiza →'),
            ('PAs & Family Offices', 'Diskreter Support für Principals und autorisierte Vertreter mit Need-to-know-Kommunikation und Multi-Service-Koordination.', '/de/private-office/', 'Private Office Ibiza →'),
        ],
    },
    '/ar/partners/': {
        'eyebrow': 'DMC · إدارة الوجهة · الشركاء الدوليون',
        'title': 'واجهة تشغيل واضحة في إيبيزا للطلبات الدولية.',
        'lead': 'بالنسبة لشركات الكونسيرج ومستشاري السفر الفاخر والمكاتب الخاصة، القيمة ليست في قائمة موردين طويلة، بل في جهة تشغيل محلية تستطيع استلام الـ brief الدولي وربط التنفيذ على الجزيرة.',
        'body': 'يمكن لـ Ibiza VIP Move العمل كشريك DMC محلي لإدارة الوجهة، أو كطبقة تشغيل لإدارة السفر الخاص، أو كجهة اتصال في إيبيزا خلف الكواليس وفق أسلوب العمل المتفق عليه مع الشريك. تبقى علاقة العميل محفوظة لدى الشريك، ولا تُعد أي خدمة مؤكدة قبل التحقق الفعلي من التوفر والنطاق والشروط.',
        'cards': [
            ('DMC / إدارة الوجهة', 'تنسيق محلي للنقل والفلل واليخوت والطيران الخاص والضيافة ولوجستيات الضيوف حول برنامج واحد مترابط.', '/ar/services/', 'عرض خدمات إيبيزا →'),
            ('إدارة السفر الخاص', 'ربط تخطيط السفر الدولي بالتنفيذ على الجزيرة عبر جهة اتصال واحدة لمتابعة الاعتماديات وتغييرات البرنامج.', '/ar/private-concierge-ibiza/', 'كونسيرج خاص في إيبيزا →'),
            ('المساعدون والمكاتب العائلية', 'دعم متحفظ للـ principals والممثلين المصرح لهم مع مشاركة المعلومات حسب الحاجة وتنسيق متعدد الخدمات.', '/ar/private-office/', 'Private Office Ibiza →'),
        ],
    },
}


def file_for(path):
    return ROOT / path.strip('/') / 'index.html'


def section(data):
    cards = ''.join(
        '<div><strong>' + escape(title) + '</strong><span>' + escape(copy) + '</span>'
        '<a class="text-link" href="' + escape(href, quote=True) + '">' + escape(label) + '</a></div>'
        for title, copy, href, label in data['cards']
    )
    return (
        '<section class="ivm-b2b-overview ivm-phase112-b2b-intent" aria-label="International partner operating scope">'
        '<div class="ivm-b2b-overview-inner"><div><div class="eyebrow">' + escape(data['eyebrow']) + '</div>'
        '<h2>' + escape(data['title']) + '</h2></div><div>'
        '<p class="lead">' + escape(data['lead']) + '</p><p>' + escape(data['body']) + '</p>'
        '<div class="ivm-b2b-audiences">' + cards + '</div></div></div></section>'
    )

sitemap = ROOT / 'sitemap.xml'
if not sitemap.exists():
    raise SystemExit('Phase 112 sitemap missing')
sitemap_before = sitemap.read_text(encoding='utf-8')

for path, data in PAGES.items():
    target = file_for(path)
    if not target.exists():
        raise SystemExit(f'Phase 112 target missing: {path}')
    html = target.read_text(encoding='utf-8')
    if 'ivm-phase112-b2b-intent' in html:
        raise SystemExit(f'Phase 112 duplicate section: {path}')
    marker = '<section class="ivm-b2b-operating">'
    if html.count(marker) != 1:
        raise SystemExit(f'Phase 112 operating marker mismatch: {path}')
    html = html.replace(marker, section(data) + marker, 1)
    target.write_text(html, encoding='utf-8')

if sitemap.read_text(encoding='utf-8') != sitemap_before:
    raise SystemExit('Phase 112 must not change sitemap inventory')

print('PASS: Phase 112 multilingual B2B intent — FR/DE/AR Partner pages now explain DMC, destination management and private travel management as Ibiza-local partner workflows without adding URLs or CSS')
