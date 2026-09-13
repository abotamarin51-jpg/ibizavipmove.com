"""Phase 145: tighten search/social metadata on four existing local concierge pages.

This is deliberately head-only. It does not change visible body copy, URLs, canonicals,
hreflang, contact routes, service scope, sitemap inventory, or freshness dates.
"""
from html import escape
from pathlib import Path

ROOT = Path('_site')

PAGES = {
    'private-concierge-marina-botafoch-ibiza': {
        'old_title': 'Private Concierge Marina Botafoch Ibiza | Ibiza VIP Move',
        'new_title': 'Private Concierge Marina Botafoch Ibiza | Ibiza VIP Move',
        'old_desc': 'Private concierge for Marina Botafoch, Ibiza Town and Talamanca, coordinating chauffeur transport, yachts, dining, nightlife, villas and private client logistics.',
        'new_desc': 'Private concierge for Marina Botafoch, Ibiza Town and Talamanca, coordinating chauffeurs, yachts, dining, nightlife, villas and private logistics.',
    },
    'private-concierge-cala-jondal-es-cubells-ibiza': {
        'old_title': 'Private Concierge Cala Jondal & Es Cubells Ibiza | Ibiza VIP Move',
        'new_title': 'Private Concierge Cala Jondal & Es Cubells | Ibiza VIP Move',
        'old_desc': 'Private concierge for Cala Jondal, Es Cubells and the south of Ibiza, connecting villas, chauffeur transport, beach clubs, yachts, dining, staffing and security.',
        'new_desc': 'Private concierge for Cala Jondal, Es Cubells and south Ibiza, coordinating villas, chauffeurs, beach clubs, yachts, dining, staffing and security.',
    },
    'private-concierge-santa-eulalia-roca-llisa-ibiza': {
        'old_title': 'Private Concierge Santa Eulalia & Roca Llisa Ibiza | Ibiza VIP Move',
        'new_title': 'Concierge Santa Eulalia & Roca Llisa | Ibiza VIP Move',
        'old_desc': 'Private concierge for Santa Eulalia, Roca Llisa and east Ibiza, coordinating villas, family stays, chauffeur transport, dining, yachts, wellness and private support.',
        'new_desc': 'Private concierge for Santa Eulalia, Roca Llisa and east Ibiza, coordinating villas, family stays, chauffeurs, dining, yachts, wellness and private support.',
    },
    'private-concierge-santa-gertrudis-ibiza': {
        'old_title': 'Private Concierge Santa Gertrudis Ibiza | Central Ibiza Villas',
        'new_title': 'Private Concierge Santa Gertrudis | Ibiza VIP Move',
        'old_desc': 'Private concierge for Santa Gertrudis and central Ibiza villas, coordinating chauffeur transport, private chefs, family logistics, wellness, dining, yachts and bespoke support.',
        'new_desc': 'Private concierge for Santa Gertrudis and central Ibiza villas, coordinating chauffeurs, private chefs, family logistics, wellness, dining and yacht days.',
    },
}


def _replace_exact(head, old, new, expected, label):
    count = head.count(old)
    if count != expected:
        raise SystemExit(f'Phase 145: {label} expected {expected} occurrences, found {count}')
    return head.replace(old, new)


def enhance():
    sitemap_path = ROOT / 'sitemap.xml'
    sitemap_before = sitemap_path.read_bytes()
    changed = 0

    for slug, data in PAGES.items():
        path = ROOT / slug / 'index.html'
        html = path.read_text(encoding='utf-8')
        if '</head>' not in html:
            raise SystemExit(f'Phase 145: missing head boundary on {slug}')
        head, body = html.split('</head>', 1)

        # Idempotent completed-state check.
        new_html_title = escape(data['new_title'], quote=True)
        if data['new_desc'] in head and new_html_title in head and data['old_desc'] not in head:
            if body.count(data['old_desc']) != 1:
                raise SystemExit(f'Phase 145: visible body baseline changed on {slug}')
            continue

        # Keep the visible body byte-for-byte unchanged. Only metadata/schema in <head> moves.
        old_html_title = escape(data['old_title'], quote=True)
        new_html_title = escape(data['new_title'], quote=True)
        if old_html_title == data['old_title']:
            head = _replace_exact(head, data['old_title'], data['new_title'], 4, f'{slug} head title')
        else:
            head = _replace_exact(head, old_html_title, new_html_title, 3, f'{slug} HTML title')
            head = _replace_exact(head, data['old_title'], data['new_title'], 1, f'{slug} JSON-LD title')

        head = _replace_exact(head, data['old_desc'], data['new_desc'], 5, f'{slug} head description')
        if body.count(data['old_desc']) != 1 or data['new_desc'] in body:
            raise SystemExit(f'Phase 145: visible body must remain unchanged on {slug}')

        path.write_text(head + '</head>' + body, encoding='utf-8')
        changed += 1

    if sitemap_path.read_bytes() != sitemap_before:
        raise SystemExit('Phase 145: sitemap changed unexpectedly')
    print(f'PASS: Phase 145 — head-only local concierge metadata tightened on {changed} pages; visible body and sitemap unchanged')


if __name__ == '__main__':
    enhance()
