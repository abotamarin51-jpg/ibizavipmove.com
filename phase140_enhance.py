"""Apply only the reviewed vocabulary file's eight additional professional-role terms.

The file explicitly treats these as profiles/functions, not new services or SEO pages.
This phase adds concise visible audience sections to existing Partners and Private Office
pages in the five current languages, without changing URLs, metadata, schema, links,
forms, tracking, sitemap or service inventory.
"""
from pathlib import Path
from html import escape

ROOT = Path('_site')
MARKER = 'ivm-phase140-audience-vocabulary'

DATA = {
    'en': {
        'private': {
            'path': '/private-office/',
            'eyebrow': 'Private household & residence teams',
            'title': 'Local Ibiza support for the people coordinating the household.',
            'lead': 'Family Assistants, Household Managers, Estate Managers and Directors of Residences may need a local operator to carry out the Ibiza part of a stay without taking over their own role.',
            'body': 'Ibiza VIP Move can coordinate transport and stay logistics around the agreed brief. We do not present this as household or estate management.',
            'cards': [
                ('Family Assistant', 'Local Ibiza support for family travel and day-to-day stay needs.'),
                ('Household Manager', 'Transport and stay coordination around the household’s Ibiza plans.'),
                ('Estate Manager', 'Local execution for guests and principals, not management of the property itself.'),
                ('Director of Residences', 'An Ibiza coordination point for providers and guest needs during the stay.'),
            ],
        },
        'partners': {
            'path': '/partners/',
            'eyebrow': 'Professional roles we can support in Ibiza',
            'title': 'A local operator for travel, hosting and touring teams.',
            'lead': 'Lifestyle Coordinators, VIP Hosts, Artist Liaisons and Tour Managers may need a reliable local handover when their client, guest or production is in Ibiza.',
            'body': 'Our role is local coordination around services that are actually requested and confirmed, including travel, transport, accommodation and stay logistics. These are partner and client profiles, not new Ibiza VIP Move service lines.',
            'cards': [
                ('Lifestyle Coordinator', 'Local travel and lifestyle support for clients arriving in Ibiza.'),
                ('VIP Host', 'On-island guest support when hosting forms part of the agreed brief.'),
                ('Artist Liaison', 'Local transport, accommodation and stay coordination for artists.'),
                ('Tour Manager', 'Ibiza support for music tours, artists and touring logistics.'),
            ],
        },
    },
    'fr': {
        'private': {
            'path': '/fr/private-office/',
            'eyebrow': 'Équipes de maison et de résidences privées',
            'title': 'Un relais local à Ibiza pour les équipes qui coordonnent le séjour.',
            'lead': 'Les Assistant personnel de famille, Intendant de maison, Intendant de propriétés privées et Directeur de résidences privées peuvent avoir besoin d’un opérateur local pour exécuter la partie Ibiza d’un séjour sans se substituer à leur fonction.',
            'body': 'Ibiza VIP Move peut coordonner le transport et la logistique du séjour selon le brief convenu. Nous ne présentons pas ce service comme de la gestion de maison ou de propriété.',
            'cards': [
                ('Assistant personnel de famille', 'Relais local à Ibiza pour les besoins de voyage et de séjour de la famille.'),
                ('Intendant de maison', 'Coordination du transport et du séjour autour des plans du foyer à Ibiza.'),
                ('Intendant de propriétés privées', 'Exécution locale pour les invités et principals, sans gérer la propriété elle-même.'),
                ('Directeur de résidences privées', 'Un point de coordination Ibiza pour les prestataires et les besoins des occupants pendant le séjour.'),
            ],
        },
        'partners': {
            'path': '/fr/partners/',
            'eyebrow': 'Profils professionnels accompagnés à Ibiza',
            'title': 'Un opérateur local pour les équipes voyage, accueil et tournée.',
            'lead': 'Les Coordinateur de voyages et de services lifestyle, Hôte VIP, Chargé de l’accueil des artistes et Responsable de tournée peuvent avoir besoin d’un relais local fiable lorsque leur client, invité ou production est à Ibiza.',
            'body': 'Notre rôle est la coordination locale des prestations réellement demandées et confirmées, notamment voyage, transport, hébergement et logistique du séjour. Il s’agit de profils partenaires ou clients, pas de nouveaux services Ibiza VIP Move.',
            'cards': [
                ('Coordinateur de voyages et de services lifestyle', 'Support local voyage et lifestyle pour les clients arrivant à Ibiza.'),
                ('Hôte VIP', 'Support invités sur l’île lorsque l’accueil fait partie du brief convenu.'),
                ('Chargé de l’accueil des artistes', 'Transport, hébergement et coordination locale du séjour des artistes.'),
                ('Responsable de tournée', 'Support Ibiza pour les tournées musicales, artistes et logistique de tournée.'),
            ],
        },
    },
    'de': {
        'private': {
            'path': '/de/private-office/',
            'eyebrow': 'Private Haushalts- & Residenzteams',
            'title': 'Lokale Ibiza-Unterstützung für Teams, die den Aufenthalt koordinieren.',
            'lead': 'Private Familienassistenz, Hausmanager für Privathaushalte, Verwalter privater Anwesen und Leiter privater Residenzen können einen lokalen Operator benötigen, der den Ibiza-Teil eines Aufenthalts ausführt, ohne ihre eigene Funktion zu übernehmen.',
            'body': 'Ibiza VIP Move kann Transport und Aufenthaltslogistik nach dem vereinbarten Briefing koordinieren. Wir stellen diese Leistung nicht als Haushalts- oder Anwesenverwaltung dar.',
            'cards': [
                ('Private Familienassistenz', 'Lokale Ibiza-Unterstützung für Familienreisen und Anforderungen während des Aufenthalts.'),
                ('Hausmanager für Privathaushalte', 'Transport- und Aufenthaltskoordination rund um die Ibiza-Pläne des Haushalts.'),
                ('Verwalter privater Anwesen', 'Lokale Ausführung für Gäste und Principals, ohne die Immobilie selbst zu verwalten.'),
                ('Leiter privater Residenzen', 'Ein Ibiza-Koordinationspunkt für Dienstleister und Gästebedürfnisse während des Aufenthalts.'),
            ],
        },
        'partners': {
            'path': '/de/partners/',
            'eyebrow': 'Professionelle Rollen, die wir auf Ibiza unterstützen',
            'title': 'Ein lokaler Operator für Reise-, Gäste- und Touring-Teams.',
            'lead': 'Koordinator für Reise- und Lifestyle-Services, VIP-Gästebetreuer, Künstlerbetreuer und Tourmanager für Musikproduktionen können eine verlässliche lokale Übergabe benötigen, wenn ihr Kunde, Gast oder ihre Produktion auf Ibiza ist.',
            'body': 'Unsere Rolle ist die lokale Koordination tatsächlich angefragter und bestätigter Leistungen, einschließlich Reise, Transport, Unterkunft und Aufenthaltslogistik. Diese Bezeichnungen sind Partner- und Kundenprofile, keine neuen Ibiza VIP Move Services.',
            'cards': [
                ('Koordinator für Reise- und Lifestyle-Services', 'Lokale Reise- und Lifestyle-Unterstützung für Kunden auf Ibiza.'),
                ('VIP-Gästebetreuer', 'Gästebetreuung auf der Insel, wenn Hosting Teil des vereinbarten Briefings ist.'),
                ('Künstlerbetreuer', 'Lokale Transport-, Unterkunfts- und Aufenthaltskoordination für Künstler.'),
                ('Tourmanager für Musikproduktionen', 'Ibiza-Unterstützung für Musiktourneen, Künstler und Touring-Logistik.'),
            ],
        },
    },
    'ar': {
        'private': {
            'path': '/ar/private-office/',
            'eyebrow': 'فرق المنازل والمساكن الخاصة',
            'title': 'دعم محلي في إيبيزا للفرق التي تنسق الإقامة.',
            'lead': 'قد يحتاج مساعد شخصي للعائلة أو مدير شؤون المنزل أو مدير الأملاك السكنية الخاصة أو مدير المساكن الخاصة إلى جهة تشغيل محلية تنفذ جزء إيبيزا من الإقامة من دون أن تحل محل دوره الأساسي.',
            'body': 'يمكن لـ Ibiza VIP Move تنسيق النقل ولوجستيات الإقامة وفق الـ brief المتفق عليه. ولا نقدم هذه الخدمة باعتبارها إدارة منزل أو إدارة عقار.',
            'cards': [
                ('مساعد شخصي للعائلة', 'دعم محلي في إيبيزا لاحتياجات سفر العائلة وإقامتها اليومية.'),
                ('مدير شؤون المنزل', 'تنسيق النقل والإقامة حول خطط الأسرة في إيبيزا.'),
                ('مدير الأملاك السكنية الخاصة', 'تنفيذ محلي للضيوف والـ principals من دون إدارة العقار نفسه.'),
                ('مدير المساكن الخاصة', 'نقطة تنسيق في إيبيزا لمقدمي الخدمات واحتياجات الضيوف خلال الإقامة.'),
            ],
        },
        'partners': {
            'path': '/ar/partners/',
            'eyebrow': 'أدوار مهنية ندعمها في إيبيزا',
            'title': 'جهة تشغيل محلية لفرق السفر والاستضافة والجولات.',
            'lead': 'قد يحتاج منسق خدمات السفر ونمط الحياة أو مضيف كبار الشخصيات أو منسق شؤون الفنانين أو مدير الجولات الفنية إلى تسليم محلي موثوق عندما يكون العميل أو الضيف أو الإنتاج في إيبيزا.',
            'body': 'دورنا هو التنسيق المحلي للخدمات المطلوبة والمؤكدة فعليًا، بما في ذلك السفر والنقل والإقامة ولوجستيات الإقامة. هذه ملفات تعريف لشركاء وعملاء محتملين وليست خطوط خدمات جديدة لـ Ibiza VIP Move.',
            'cards': [
                ('منسق خدمات السفر ونمط الحياة', 'دعم محلي للسفر وخدمات نمط الحياة للعملاء القادمين إلى إيبيزا.'),
                ('مضيف كبار الشخصيات', 'دعم الضيوف على الجزيرة عندما تكون الاستضافة جزءًا من الـ brief المتفق عليه.'),
                ('منسق شؤون الفنانين', 'تنسيق محلي للنقل والإقامة واحتياجات الفنانين أثناء وجودهم في إيبيزا.'),
                ('مدير الجولات الفنية', 'دعم في إيبيزا للجولات الموسيقية والفنانين ولوجستيات الجولات.'),
            ],
        },
    },
    'es': {
        'private': {
            'path': '/es/private-office/',
            'eyebrow': 'Equipos de hogares y residencias privadas',
            'title': 'Apoyo local en Ibiza para quienes coordinan la estancia.',
            'lead': 'Un Asistente personal de familias, Administrador del hogar, Gestor de propiedades residenciales privadas o Director de residencias privadas puede necesitar un operador local que ejecute la parte de Ibiza sin asumir su función principal.',
            'body': 'Ibiza VIP Move puede coordinar transporte y logística de la estancia según el brief acordado. No presentamos este servicio como gestión del hogar ni de la propiedad.',
            'cards': [
                ('Asistente personal de familias', 'Apoyo local en Ibiza para viajes y necesidades de estancia de la familia.'),
                ('Administrador del hogar', 'Coordinación de transporte y estancia alrededor de los planes del hogar en Ibiza.'),
                ('Gestor de propiedades residenciales privadas', 'Ejecución local para huéspedes y principals, sin gestionar la propiedad en sí.'),
                ('Director de residencias privadas', 'Un punto de coordinación en Ibiza para proveedores y necesidades de huéspedes durante la estancia.'),
            ],
        },
        'partners': {
            'path': '/es/partners/',
            'eyebrow': 'Perfiles profesionales a los que apoyamos en Ibiza',
            'title': 'Un operador local para equipos de viajes, hosting y giras.',
            'lead': 'Un Coordinador de viajes y servicios lifestyle, Anfitrión VIP, Coordinador de atención a artistas o Mánager de giras musicales puede necesitar un relevo local fiable cuando su cliente, huésped o producción está en Ibiza.',
            'body': 'Nuestro papel es la coordinación local de servicios realmente solicitados y confirmados, como viajes, transporte, alojamiento y logística de estancia. Son perfiles de clientes o partners, no nuevos servicios de Ibiza VIP Move.',
            'cards': [
                ('Coordinador de viajes y servicios lifestyle', 'Apoyo local de viaje y lifestyle para clientes que llegan a Ibiza.'),
                ('Anfitrión VIP', 'Atención en la isla cuando el hosting forma parte del brief acordado.'),
                ('Coordinador de atención a artistas', 'Coordinación local de transporte, alojamiento y estancia para artistas.'),
                ('Mánager de giras musicales', 'Apoyo en Ibiza para giras musicales, artistas y logística de touring.'),
            ],
        },
    },
}


def target(path: str) -> Path:
    return ROOT / path.strip('/') / 'index.html'


def render(kind: str, data: dict) -> str:
    cards = ''.join(
        '<div><strong>' + escape(role) + '</strong><span>' + escape(copy) + '</span></div>'
        for role, copy in data['cards']
    )
    return (
        f'<section class="ivm-b2b-overview {MARKER} ivm-phase140-{kind}-roles" '
        'aria-label="Professional roles supported in Ibiza">'
        '<div class="ivm-b2b-overview-inner"><div><div class="eyebrow">' + escape(data['eyebrow']) + '</div>'
        '<h2>' + escape(data['title']) + '</h2></div><div><p class="lead">' + escape(data['lead']) + '</p>'
        '<p>' + escape(data['body']) + '</p><div class="ivm-b2b-audiences">' + cards + '</div></div></div></section>'
    )


def enhance():
    sitemap = ROOT / 'sitemap.xml'
    sitemap_before = sitemap.read_bytes()
    changed = 0
    for lang, groups in DATA.items():
        for kind, data in groups.items():
            page = target(data['path'])
            if not page.is_file():
                raise SystemExit(f'Phase 140 missing target: {data["path"]}')
            html = page.read_text(encoding='utf-8')
            section = render(kind, data)
            role_marker = f'ivm-phase140-{kind}-roles'
            if role_marker in html:
                if html.count(role_marker) != 1 or section not in html:
                    raise SystemExit(f'Phase 140 malformed existing section: {data["path"]}')
                continue
            marker = '<section class="ivm-b2b-operating">'
            if html.count(marker) != 1:
                raise SystemExit(f'Phase 140 operating marker mismatch: {data["path"]}')
            html = html.replace(marker, section + marker, 1)
            page.write_text(html, encoding='utf-8')
            changed += 1
    if changed not in (0, 10):
        raise SystemExit(f'Phase 140 expected 10 changed pages or idempotent 0, got {changed}')
    if sitemap.read_bytes() != sitemap_before:
        raise SystemExit('Phase 140 must not change sitemap')
    print(f'PASS: Phase 140 vocabulary application — {changed} pages changed; A1-A8 applied across five languages as professional profiles, not new services or URLs')


if __name__ == '__main__':
    enhance()
