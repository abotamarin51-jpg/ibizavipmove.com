"""Add one contextual French Services -> Private Concierge pathway.

Preserve the existing French pathway. The German event extension changes only
the draft text on two existing WhatsApp links, never their approved recipient.
No visible copy, metadata, layout, consent, tracking or sitemap change.
"""
from pathlib import Path
from urllib.parse import quote

PATH = Path('_site/fr/services/index.html')
OLD = 'Passez par le concierge plutôt que de gérer chaque catégorie séparément. Partagez dates, invités et priorités ; nous clarifions le brief et poursuivons en privé.'
NEW = 'Passez par la <a class="text-link" href="/fr/conciergerie-privee-ibiza/">conciergerie privée</a> plutôt que de gérer chaque catégorie séparément. Partagez dates, invités et priorités ; nous clarifions le brief et poursuivons en privé.'


def enhance():
    html = PATH.read_text(encoding='utf-8')
    if NEW in html:
        if html.count(NEW) != 1:
            raise SystemExit('Phase 178: duplicate French Services-to-Concierge pathway')
        print('PASS: Phase 178 — French Services-to-Concierge pathway already present')
        return

    if html.count(OLD) != 1:
        raise SystemExit('Phase 178: expected one French concierge coordination sentence')

    PATH.write_text(html.replace(OLD, NEW, 1), encoding='utf-8')
    print('PASS: Phase 178 — one French Services-to-Concierge pathway added')

DE_EVENT_PATH = Path('_site/de/private-events-ibiza/index.html')
DE_EVENT_WA = 'https://wa.me/34600703303'
DE_EVENT_DRAFT = (
    'Hallo Ibiza VIP Move, ich möchte die Koordination eines Events auf Ibiza anfragen.\n'
    'Datum oder Zeitraum: [noch offen]\n'
    'Gästezahl: [noch offen]\n'
    'Anlass und gewünschte Unterstützung: [bitte ergänzen]'
)
DE_EVENT_HREF = DE_EVENT_WA + '?text=' + quote(DE_EVENT_DRAFT, safe='')


def event_whatsapp_html(html: str) -> str:
    """Change exactly two reviewed service links; refuse ambiguous markup."""
    if ('<html lang="de"' not in html or
            '<link rel="canonical" href="https://ibizavipmove.com/de/private-events-ibiza/"' not in html):
        raise ValueError('German event page identity mismatch')
    original = html
    for style in ('gold', 'dark'):
        old = f'<a class="btn {style}" href="{DE_EVENT_WA}">Private Event anfragen</a>'
        new = old.replace(DE_EVENT_WA, DE_EVENT_HREF)
        if html.count(old) == 1 and new not in html:
            html = html.replace(old, new, 1)
        elif html.count(new) != 1 or old in html:
            raise ValueError('German event WhatsApp CTA missing, duplicated or changed')
    # Replacing the two hrefs back must recover every original byte on first run.
    if DE_EVENT_HREF not in original and html.replace(DE_EVENT_HREF, DE_EVENT_WA) != original:
        raise ValueError('Unexpected German event output drift')
    return html


def enhance_event_whatsapp():
    before = DE_EVENT_PATH.read_text(encoding='utf-8')
    after = event_whatsapp_html(before)
    if after != before:
        DE_EVENT_PATH.write_text(after, encoding='utf-8')
    print('PASS: two existing German event WhatsApp links retain the approved recipient and an editable draft')


if __name__ == '__main__':
    enhance()
    enhance_event_whatsapp()
