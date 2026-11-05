"""Keep the French yacht enquiry context on its three service-specific CTAs.

No generic/header/footer/mobile contact, number, visible copy, metadata,
script, style, sitemap or other page changes. The message is an editable
draft; opening a link does not send an enquiry or confirm a reservation.
"""
from pathlib import Path
import re
from urllib.parse import quote

ROUTE = 'fr/location-yacht-ibiza/index.html'
CANONICAL = 'https://ibizavipmove.com/fr/location-yacht-ibiza/'
WHATSAPP = 'https://wa.me/34600703303'
MESSAGE = (
    'Bonjour Ibiza VIP Move,\n\n'
    'Je souhaite recevoir une proposition pour un yacht privé à Ibiza.\n\n'
    'Date souhaitée :\n'
    'Nombre de passagers :\n'
    'Durée et itinéraire souhaités :\n'
    'Budget indicatif :\n'
    'Transfert vers la marina (si nécessaire) :\n\n'
    'Merci.'
)
DRAFT_URL = WHATSAPP + '?text=' + quote(MESSAGE, safe='')
ANCHORS = (
    '<a class="btn gold" href="' + WHATSAPP + '">Demander un yacht privé</a>',
    '<a class="text-link" href="' + WHATSAPP + '">Échanger sur WhatsApp</a>',
    '<a class="btn dark" href="' + WHATSAPP + '">Demander un yacht privé</a>',
)
UPDATED = tuple(a.replace(WHATSAPP, DRAFT_URL) for a in ANCHORS)


def transform(html):
    """Fail closed on unexpected markup and preserve all unrelated bytes."""
    if html.count('<link rel="canonical" href="' + CANONICAL + '">') != 1:
        raise ValueError('French yacht brief: unexpected canonical')
    if '<html lang="fr"' not in html:
        raise ValueError('French yacht brief: unexpected language')
    region = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S)
    if not region or len(re.findall(r'<main\b', html)) != 1:
        raise ValueError('French yacht brief: main region missing or duplicated')
    main = region.group(1)
    for old, new in zip(ANCHORS, UPDATED):
        if (html.count(old), html.count(new)) not in ((1, 0), (0, 1)):
            raise ValueError('French yacht brief: missing, duplicate or changed CTA')
        if main.count(old) + main.count(new) != 1:
            raise ValueError('French yacht brief: CTA outside the service content')
    baseline = html
    for old, new in zip(ANCHORS, UPDATED):
        baseline = baseline.replace(new, old)
    updated = baseline
    for old, new in zip(ANCHORS, UPDATED):
        updated = updated.replace(old, new, 1)
    restored = updated
    for old, new in zip(ANCHORS, UPDATED):
        restored = restored.replace(new, old)
    if restored != baseline or updated.count(DRAFT_URL) != 3:
        raise ValueError('French yacht brief: change exceeds the three reviewed links')
    if updated.split('</head>', 1)[0] != html.split('</head>', 1)[0]:
        raise ValueError('French yacht brief: head changed')
    if updated.count('href="' + WHATSAPP + '"') != baseline.count('href="' + WHATSAPP + '"') - 3:
        raise ValueError('French yacht brief: generic contact link count changed')
    for token in ('tel:+34600703303', 'partnership@ibizavipmove.com',
                  '/fr/contact/?service=yacht'):
        if updated.count(token) != baseline.count(token) or token not in baseline:
            raise ValueError('French yacht brief: approved contact route changed')
    return updated


def enhance(root=Path('_site')):
    path = root / ROUTE
    before = path.read_text(encoding='utf-8')
    after = transform(before)
    if after != before:
        path.write_text(after, encoding='utf-8')
    print('PASS: French yacht brief — three service CTAs, approved number and generic access preserved')


if __name__ == '__main__':
    enhance()
