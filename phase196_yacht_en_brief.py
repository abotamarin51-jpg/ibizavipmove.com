"""Preserve yacht-specific enquiry context in three existing English service links.

Only the three service-specific WhatsApp hrefs change. Global, footer and
floating contact remain as approved. Opening a draft never sends a message.
"""
from pathlib import Path
import re
from urllib.parse import quote

ROUTE = 'yacht-charter-ibiza/index.html'
CANONICAL = 'https://ibizavipmove.com/yacht-charter-ibiza/'
WHATSAPP = 'https://wa.me/34600703303'
OLD_MESSAGE = (
    "Hello Ibiza VIP Move, I'm interested in yacht charter. Could you please "
    'help me with availability and the next steps? Thank you.'
)
MESSAGE = (
    'Hello Ibiza VIP Move,\n\n'
    'I would like a private yacht charter proposal for Ibiza.\n\n'
    'Preferred date:\n'
    'Number of guests:\n'
    'Duration and preferred route:\n'
    'Indicative budget:\n'
    'Marina transfer (if needed):\n\n'
    'Thank you.'
)
OLD_DRAFT_URL = WHATSAPP + '?text=' + quote(OLD_MESSAGE, safe='')
DRAFT_URL = WHATSAPP + '?text=' + quote(MESSAGE, safe='')
ANCHORS = (
    '<a class="btn gold" href="' + OLD_DRAFT_URL + '">Request this service</a>',
    '<a class="text-link" href="' + WHATSAPP + '">Ask on WhatsApp</a>',
    '<a class="btn dark" href="' + OLD_DRAFT_URL + '">WhatsApp Concierge</a>',
)
UPDATED = (
    ANCHORS[0].replace(OLD_DRAFT_URL, DRAFT_URL),
    ANCHORS[1].replace(WHATSAPP, DRAFT_URL),
    ANCHORS[2].replace(OLD_DRAFT_URL, DRAFT_URL),
)


def transform(html):
    if html.count('<link rel="canonical" href="' + CANONICAL + '">') != 1:
        raise ValueError('English yacht brief: unexpected canonical')
    if '<html lang="en"' not in html:
        raise ValueError('English yacht brief: unexpected language')
    region = re.search(r'<main\b[^>]*>(.*?)</main>', html, re.S)
    if not region or len(re.findall(r'<main\b', html)) != 1:
        raise ValueError('English yacht brief: main region missing or duplicated')
    main = region.group(1)
    for old, new in zip(ANCHORS, UPDATED):
        if (html.count(old), html.count(new)) not in ((1, 0), (0, 1)):
            raise ValueError('English yacht brief: missing, duplicate or changed CTA')
        if main.count(old) + main.count(new) != 1:
            raise ValueError('English yacht brief: CTA outside main content')
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
        raise ValueError('English yacht brief: unrelated HTML changed')
    if updated.split('</head>', 1)[0] != html.split('</head>', 1)[0]:
        raise ValueError('English yacht brief: SEO metadata changed')
    if updated.count('href="' + WHATSAPP + '"') != baseline.count('href="' + WHATSAPP + '"') - 1:
        raise ValueError('English yacht brief: generic contact changed')
    for token in ('tel:+34600703303', 'partnership@ibizavipmove.com',
                  '/contact/?service=yacht'):
        if token not in html or updated.count(token) != html.count(token):
            raise ValueError('English yacht brief: approved contact missing or changed')
    return updated


def enhance(root=Path('_site')):
    path = root / ROUTE
    before = path.read_text(encoding='utf-8')
    after = transform(before)
    if after != before:
        path.write_text(after, encoding='utf-8')
    print('PASS: English yacht WhatsApp brief — three service CTAs; generic contacts preserved')


if __name__ == '__main__':
    enhance()
