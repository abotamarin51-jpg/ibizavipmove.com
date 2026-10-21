"""Preserve the French Services pathway, then apply the English Private Office handoff."""
from pathlib import Path
from phase179_enhance import enhance as enhance_private_office_handoff

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


if __name__ == '__main__':
    enhance()
    enhance_private_office_handoff()
