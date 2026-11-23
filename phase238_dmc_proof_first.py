"""Bring the existing DMC operational evidence closer to the first decision point.

Presentation-only: moves one pre-existing section. Does not change content,
links, metadata, canonicals, structured data, headings or site inventory.
"""
from pathlib import Path
import re

PAGE = Path("_site/destination-management-ibiza/index.html")
CANONICAL = "https://ibizavipmove.com/destination-management-ibiza/"
PROOF_START = '<section class="partners-strip ivm-phase105-proof" aria-label="Operational evidence">'
FOLLOWING_SECTION = '<section class="dark-panel">'
EDITORIAL_PATTERN = re.compile(r'<section class="editorial">.*?</section>', re.S)
PROOF_PATTERN = re.compile(
    r'<section class="partners-strip ivm-phase105-proof" aria-label="Operational evidence">.*?</section>',
    re.S,
)
REQUIRED_HREFS = (
    '/case-studies/multi-day-executive-chauffeur-program/',
    '/ibiza-luxury-operations-report-2026/',
    '/founder/',
)


def enhance() -> None:
    if not PAGE.is_file():
        raise SystemExit("Phase 238: existing DMC page missing")
    original = PAGE.read_text(encoding="utf-8")
    if original.count(f'<link rel="canonical" href="{CANONICAL}">') != 1:
        raise SystemExit("Phase 238: DMC canonical mismatch")
    if '<html lang="en"' not in original or original.count(PROOF_START) != 1:
        raise SystemExit("Phase 238: unexpected language or existing proof count")
    if original.count(FOLLOWING_SECTION) != 1:
        raise SystemExit("Phase 238: unexpected DMC section structure")

    proof_match = PROOF_PATTERN.search(original)
    editorial_match = EDITORIAL_PATTERN.search(original)
    if not proof_match or not editorial_match:
        raise SystemExit("Phase 238: DMC proof/editorial anchor unavailable")
    proof = proof_match.group(0)
    if any(proof.count(f'href="{href}"') != 1 for href in REQUIRED_HREFS):
        raise SystemExit("Phase 238: required real evidence links missing or duplicated")

    # Already positioned directly after the introductory editorial.
    if editorial_match.end() < proof_match.start() < original.index(FOLLOWING_SECTION):
        print("PASS: Phase 238 DMC proof already visible after the opening editorial")
        return

    # Move, never duplicate, the existing section; preserve every other byte.
    without_proof = original[:proof_match.start()] + original[proof_match.end():]
    editorial_match = EDITORIAL_PATTERN.search(without_proof)
    if not editorial_match or without_proof.count(PROOF_START) != 0:
        raise SystemExit("Phase 238: unsafe relocation")
    new_position = editorial_match.end()
    updated = without_proof[:new_position] + proof + without_proof[new_position:]

    if updated.replace(proof, "", 1) != original.replace(proof, "", 1):
        raise SystemExit("Phase 238: unexpected changes outside proof section")
    if updated.split("</head>", 1)[0] != original.split("</head>", 1)[0]:
        raise SystemExit("Phase 238: SEO head changed")
    if len(re.findall(r'<a\b', updated)) != len(re.findall(r'<a\b', original)):
        raise SystemExit("Phase 238: link count changed")
    if not (updated.index("</section>", updated.index('<section class="editorial">'))
            < updated.index(PROOF_START) < updated.index(FOLLOWING_SECTION)):
        raise SystemExit("Phase 238: proof not positioned before service benefits")
    if updated.count(PROOF_START) != 1:
        raise SystemExit("Phase 238: proof duplicated")

    PAGE.write_text(updated, encoding="utf-8")
    print("PASS: Phase 238 — existing Ibiza DMC operational proof moved after first editorial; metadata and links unchanged")


if __name__ == "__main__":
    enhance()
