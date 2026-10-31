"""Add owner-provided Ibiza VIP Move Google Maps profile links to existing pages.

Google Business Profile is not modified. The external shortlink must be
confirmed as the exact business listing before this change is published.
"""
from pathlib import Path

MAPS_PROFILE_URL = 'https://maps.app.goo.gl/z1z9RaegNvDc8YFb9?g_st=ic'
MAPS_LINK_HOME = (
    f'<a data-ivm-google-maps-profile="home" href="{MAPS_PROFILE_URL}" '
    'target="_blank" rel="noopener noreferrer external" '
    'aria-label="Ibiza VIP Move on Google Maps">Google Maps</a>'
)
MAPS_LINK_CONTACT = (
    f'<a class="text-link" data-ivm-google-maps-profile="contact" href="{MAPS_PROFILE_URL}" '
    'target="_blank" rel="noopener noreferrer external" '
    'aria-label="View Ibiza VIP Move on Google Maps">View Ibiza VIP Move on Google Maps</a>'
)
MAPS_ANCHOR_HOME = '<a href="/about/">Official brand information</a>'
MAPS_ANCHOR_CONTACT = '<div><span>Coverage</span><strong>Ibiza · Private client support</strong></div>'


def add_google_maps_profile_links(root=Path('_site')):
    """Add exactly one visible Google Maps profile link on Home and Contact."""
    changes = []
    for relative, old_marker, new_marker, link, canonical, landmark in (
        ('index.html', MAPS_ANCHOR_HOME, MAPS_ANCHOR_HOME + MAPS_LINK_HOME,
         MAPS_LINK_HOME, 'https://ibizavipmove.com/', 'footer'),
        ('contact/index.html', MAPS_ANCHOR_CONTACT,
         MAPS_ANCHOR_CONTACT.replace('</strong></div>', '</strong>' + MAPS_LINK_CONTACT + '</div>'),
         MAPS_LINK_CONTACT, 'https://ibizavipmove.com/contact/', 'main'),
    ):
        path = root / relative
        if not path.is_file():
            raise SystemExit(f'Google Maps link: expected page missing: {relative}')
        original = path.read_text(encoding='utf-8')
        if original.count(f'<link rel="canonical" href="{canonical}">') != 1:
            raise SystemExit(f'Google Maps link: unexpected canonical: {relative}')
        if original.count(f'<{landmark}') != 1 or original.count(f'</{landmark}>') != 1:
            raise SystemExit(f'Google Maps link: expected landmark missing: {relative}')
        if original.count(MAPS_PROFILE_URL) not in (0, 1):
            raise SystemExit(f'Google Maps link: duplicate or conflicting destination: {relative}')
        if original.count(link) == 1:
            updated = original
        else:
            if original.count(old_marker) != 1 or original.count(MAPS_PROFILE_URL):
                raise SystemExit(f'Google Maps link: ambiguous source marker/URL: {relative}')
            position = original.index(old_marker)
            if not original.index(f'<{landmark}') < position < original.index(f'</{landmark}>'):
                raise SystemExit(f'Google Maps link: unexpected insertion scope: {relative}')
            updated = original.replace(old_marker, new_marker, 1)
            if (updated.split('</head>', 1)[0] != original.split('</head>', 1)[0]
                    or updated.count('<a ') != original.count('<a ') + 1
                    or any(updated.count(s) != original.count(s) for s in (
                        '<h1', '<script', '<img', 'tel:+34600703303',
                        'wa.me/34600703303', 'partnership@ibizavipmove.com'))):
                raise SystemExit(f'Google Maps link: unrelated HTML drift: {relative}')
        if updated.count(MAPS_PROFILE_URL) != 1 or updated.count(link) != 1:
            raise SystemExit(f'Google Maps link: output cardinality mismatch: {relative}')
        changes.append((path, original, updated))
    # Validate both pages before writing either one.
    for path, before, after in changes:
        if before != after:
            path.write_text(after, encoding='utf-8')
    print('PASS: owner-provided Maps profile link in Home footer and Contact; contacts and metadata preserved')


if __name__ == '__main__':
    add_google_maps_profile_links()
