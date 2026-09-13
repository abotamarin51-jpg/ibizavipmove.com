"""Add a concise Services-hub vocabulary bridge from the user-supplied reference PDF.

Phase 141 creates no URL and no new service. It helps visitors who may search for
travel-planning/support language rather than the word concierge, using only a small
subset of B01-B24 that naturally belongs on the existing Services hubs.
"""
from pathlib import Path

ROOT = Path('_site')
MARKER = 'ivm-phase141-vocabulary'
TARGET = '<section class="ivm-services-concierge">'

COPY = {
    'services': '''<section class="ivm-services-concierge ivm-phase141-vocabulary" aria-labelledby="ivm141-en"><div class="ivm-services-concierge-inner"><div><div class="eyebrow">Search language</div><h2 id="ivm141-en">You do not need to know the word concierge.</h2></div><div><p>If your brief sounds more like Luxury travel planning, Bespoke travel or Custom travel, Itinerary planning, Destination services, On-the-ground support, Travel coordination or Luxury travel services, start here. These are different ways clients describe support around an Ibiza stay, not separate Ibiza VIP Move products.</p></div></div></section>''',
    'fr/services': '''<section class="ivm-services-concierge ivm-phase141-vocabulary" aria-labelledby="ivm141-fr"><div class="ivm-services-concierge-inner"><div><div class="eyebrow">Vocabulaire de recherche</div><h2 id="ivm141-fr">Vous n’avez pas besoin d’utiliser le mot « concierge ».</h2></div><div><p>Si votre besoin ressemble davantage à une Organisation de voyages de luxe, des Voyages sur mesure, une Création d’itinéraires, des Services à destination, une Assistance sur place, une Coordination de voyages ou des Services de voyage haut de gamme, commencez ici. Ces expressions décrivent différentes façons de demander un accompagnement pour un séjour à Ibiza, et non des services Ibiza VIP Move distincts.</p></div></div></section>''',
    'de/services': '''<section class="ivm-services-concierge ivm-phase141-vocabulary" aria-labelledby="ivm141-de"><div class="ivm-services-concierge-inner"><div><div class="eyebrow">Suchbegriffe</div><h2 id="ivm141-de">Sie müssen nicht nach „Concierge“ suchen.</h2></div><div><p>Wenn Ihr Anliegen eher als Luxusreiseplanung, Maßgeschneiderte Reisen (Schweiz: Massgeschneiderte Reisen), Individuelle Reiseplanung, Services am Urlaubsort, Betreuung vor Ort, Reisekoordination oder Luxusreiseservice beschrieben wird, können Sie hier beginnen. Diese Begriffe beschreiben unterschiedliche Arten, Unterstützung für einen Ibiza-Aufenthalt zu suchen, und keine separaten Ibiza VIP Move Services.</p></div></div></section>''',
    'ar/services': '''<section class="ivm-services-concierge ivm-phase141-vocabulary" aria-labelledby="ivm141-ar"><div class="ivm-services-concierge-inner"><div><div class="eyebrow">مصطلحات البحث</div><h2 id="ivm141-ar">لست بحاجة إلى استخدام كلمة «كونسيرج».</h2></div><div><p>إذا كان طلبك أقرب إلى تخطيط السفر الفاخر، أو رحلات مصممة حسب الطلب، أو تخطيط برامج الرحلات، أو خدمات الوجهة السياحية، أو مساعدة أثناء الإقامة، أو تنسيق السفر، أو خدمات السفر الفاخر، فيمكنك البدء من هنا. هذه تعبيرات مختلفة لوصف الدعم المطلوب لإقامة في إيبيزا، وليست خدمات منفصلة جديدة لدى Ibiza VIP Move.</p></div></div></section>''',
    'es/servicios': '''<section class="ivm-services-concierge ivm-phase141-vocabulary" aria-labelledby="ivm141-es"><div class="ivm-services-concierge-inner"><div><div class="eyebrow">Cómo se busca este apoyo</div><h2 id="ivm141-es">No necesitas conocer la palabra «concierge».</h2></div><div><p>Si lo que necesitas se parece más a Planificación de viajes de lujo, Viajes a medida, Planificación de itinerarios, Servicios en destino, Asistencia durante la estancia, Coordinación de viajes o Servicios de viajes de lujo, puedes empezar aquí. Son distintas formas de describir apoyo alrededor de una estancia en Ibiza, no servicios separados nuevos de Ibiza VIP Move.</p></div></div></section>''',
}


def enhance():
    sitemap = (ROOT / 'sitemap.xml').read_bytes()
    changed = 0
    for slug, block in COPY.items():
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        if MARKER in html:
            if html.count(MARKER) != 1 or block not in html:
                raise SystemExit(f'Phase 141: malformed existing vocabulary bridge in {slug}')
            continue
        if html.count(TARGET) != 1:
            raise SystemExit(f'Phase 141: expected one existing concierge section in {slug}')
        html = html.replace(TARGET, block + TARGET, 1)
        path.write_text(html, encoding='utf-8')
        changed += 1
    if (ROOT / 'sitemap.xml').read_bytes() != sitemap:
        raise SystemExit('Phase 141: sitemap changed unexpectedly')
    print(f'PASS: Phase 141 — non-concierge vocabulary bridge added to {changed} existing Services hubs; no URL created')


if __name__ == '__main__':
    enhance()
