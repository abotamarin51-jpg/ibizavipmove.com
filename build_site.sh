#!/usr/bin/env bash
set -euo pipefail

rm -rf _site
python3 premium_site.py
mkdir -p _site/assets/images
cp premium.css _site/assets/premium.css
cp premium.js _site/assets/premium.js
cp luxury-overrides.css _site/assets/luxury-overrides.css
cp brand-logo.jpg _site/assets/brand-logo.jpg
cp brand-logo.svg _site/assets/brand-logo.svg
cp brand-mark.svg _site/assets/brand-mark.svg

# Curated, high-resolution editorial imagery. The source set is fetched on
# every build so an older live asset cannot silently override a new release.
fetch_image() {
  name="$1"
  source="$2"
  target="_site/assets/images/${name}.jpg"
  curl -LfsS --retry 3 --connect-timeout 15 "$source" -o "$target"
  test -s "$target"
}

fetch_image hero 'https://images.unsplash.com/photo-1782113326494-87602b41cbdf?auto=format&fit=crop&w=2400&q=90&fm=jpg'
fetch_image villa 'https://images.unsplash.com/photo-1778694276931-056406c4f4d9?auto=format&fit=crop&w=2400&q=90&fm=jpg'
fetch_image yacht 'https://images.unsplash.com/photo-1779987680720-ca6e1b6fb4b0?auto=format&fit=crop&w=2400&q=90&fm=jpg'
fetch_image aviation 'https://images.unsplash.com/photo-1773554644657-2c9a9ecc95f9?auto=format&fit=crop&w=2400&q=90&fm=jpg'
fetch_image chauffeur 'https://images.unsplash.com/photo-1780296269553-84ec2dd53065?auto=format&fit=crop&w=2400&q=90&fm=jpg'
fetch_image nightlife 'https://images.unsplash.com/photo-1778694276945-a3ee92331709?auto=format&fit=crop&w=2200&q=90&fm=jpg'
fetch_image security 'https://images.unsplash.com/photo-1773580995586-b0195c43386c?auto=format&fit=crop&w=2200&q=88&fm=jpg'
fetch_image chef 'https://images.unsplash.com/photo-1653233797467-1a528819fd4f?auto=format&fit=crop&w=2200&q=88&fm=jpg'
fetch_image events 'https://images.unsplash.com/photo-1770140304098-46700a5c45c8?auto=format&fit=crop&w=2200&q=90&fm=jpg'
fetch_image wellness 'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=2200&q=88&fm=jpg'
fetch_image bespoke 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2200&q=88&fm=jpg'

python3 - <<'PY'
from pathlib import Path
replacements = {
    'https://images.unsplash.com/photo-1757439402359-aed14d39fc1b?auto=format&fit=crop&w=2400&q=88': '/assets/images/hero.jpg',
    'https://images.unsplash.com/photo-1757439402359-aed14d39fc1b?auto=format&fit=crop&w=2200&q=88': '/assets/images/villa.jpg',
    'https://www.charteranddreams.com/wp-content/uploads/2024/01/a-gran-abe.jpg': '/assets/images/yacht.jpg',
    'https://tempusmagazine.co.uk/app/uploads/news_images/9440624415.jpg': '/assets/images/aviation.jpg',
    'https://admin.londonvipchauffeur.co.uk/uploads/mercedes_benz_v_class_chauffeur_driver_5a5bdd584e.jpg': '/assets/images/chauffeur.jpg',
    'https://www.lucasfox.es/blog-images/containers/assets/blog/ibiza-beach-club-%282%29.png/945bd1461891e4848aeda100d02ad638/ibiza-beach-club-%282%29.png': '/assets/images/nightlife.jpg',
    'https://www.kleininvestigations.com/wp-content/uploads/2019/07/personal-protection-800x1035.jpg': '/assets/images/security.jpg',
    'https://www.tombenzon.com/media/pages/blog/the-art-of-in-villa-dining-securin/e42c0fe7b0-1775741021/hero-the-art-of-in-villa-dining-securin-1000x562-crop-50-50.jpg': '/assets/images/chef.jpg',
    'https://www.almabeachibiza.es/img/article-eventos.jpg': '/assets/images/events.jpg',
    'https://cdn.prod.website-files.com/675442d885557b7a328aa0aa/69813fcc610f09fb2962f68b_Luxury%20Shopping%20Trip%20Chauffeur%20in%20Mercedes%20V%20Class-m%402x.jpg': '/assets/images/chauffeur.jpg',
    'https://images.unsplash.com/photo-1540555700478-4be289fbecef?auto=format&fit=crop&w=2200&q=88': '/assets/images/wellness.jpg',
    'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=2200&q=88': '/assets/images/bespoke.jpg',
}
for path in Path('_site').rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    for old, new in replacements.items():
        text = text.replace(old, new)
    path.write_text(text, encoding='utf-8')
PY

python3 trust_enhance.py
python3 international_pages.py
python3 postprocess_site.py
python3 legal_pages.py
python3 authority_enhance.py
python3 image_markup_enhance.py
python3 validate_site.py

test -f _site/index.html
test -f _site/services/index.html
test -f _site/services/chauffeur/index.html
test -f _site/services/transfers/index.html
test -f _site/contact/index.html
test -f _site/international-clients/index.html
test -f _site/fr/index.html
test -f _site/de/index.html
test -f _site/ar/index.html
test -f _site/privacy/index.html
test -f _site/terms/index.html
test -f _site/cookies/index.html
test -f _site/404.html
test -f _site/sitemap.xml
test -f _site/robots.txt
test -f _site/llms.txt
test -f _site/assets/legal.css
test -f _site/assets/brand-logo.svg
test -f _site/assets/brand-mark.svg
test -f _site/assets/luxury-overrides.css

grep -q 'url=https://ibizavipmove.com/private-chauffeur-ibiza/' _site/services/chauffeur/index.html
grep -q 'url=https://ibizavipmove.com/private-chauffeur-ibiza/' _site/services/transfers/index.html

for img in hero villa yacht aviation chauffeur nightlife security chef events wellness bespoke; do
  test -s "_site/assets/images/${img}.jpg"
done

python3 - <<'PY'
from pathlib import Path

html_files = list(Path('_site').rglob('*.html'))
combined = '\n'.join(p.read_text(encoding='utf-8') for p in html_files)
contact = Path('_site/contact/index.html').read_text(encoding='utf-8')
partners = Path('_site/partners/index.html').read_text(encoding='utf-8')
home = Path('_site/index.html').read_text(encoding='utf-8')
intl = Path('_site/international-clients/index.html').read_text(encoding='utf-8')
fr = Path('_site/fr/index.html').read_text(encoding='utf-8')
de = Path('_site/de/index.html').read_text(encoding='utf-8')
ar = Path('_site/ar/index.html').read_text(encoding='utf-8')
privacy = Path('_site/privacy/index.html').read_text(encoding='utf-8')
sitemap = Path('_site/sitemap.xml').read_text(encoding='utf-8')
llms = Path('_site/llms.txt').read_text(encoding='utf-8')

checks = {
    'old display number removed': '+34 613 75 62 11' not in combined,
    'old WhatsApp number removed': '34613756211' not in combined,
    'new phone number present': '+34 600 703 303' in contact,
    'new WhatsApp number present': '34600703303' in contact,
    'logo referenced on homepage': '/assets/brand-logo.svg' in home,
    'logo asset exists': Path('_site/assets/brand-logo.svg').is_file() and Path('_site/assets/brand-logo.svg').stat().st_size > 0,
    'absolute social image present': 'https://ibizavipmove.com/assets/images/' in home,
    'unified organization id present': 'https://ibizavipmove.com/#organization' in combined,
    'llms.txt identifies official site': 'Official website: https://ibizavipmove.com/' in llms,
    'legal footer links present': '/privacy/' in home and '/terms/' in home and '/cookies/' in home,
    'privacy page has current contact': '+34 600 703 303' in privacy,
    'legal pages included in sitemap': all(f'https://ibizavipmove.com/{slug}/' in sitemap for slug in ('privacy','terms','cookies')),
    'partner workflow visible': 'Built for professional partners' in partners and 'Partner workflow' in partners,
    'contact next steps visible': 'What happens next' in contact and 'From first message to coordinated stay.' in contact,
    'home partner trust reinforced': 'Client-facing or discreet behind-the-scenes coordination' in home,
    'international hub visible': 'International Private Clients & Partners' in intl and 'One Ibiza-based point of contact' in intl,
    'French landing page valid': '<html lang="fr"' in fr and 'Conciergerie de luxe' in fr,
    'German landing page valid': '<html lang="de"' in de and 'Luxus Concierge' in de,
    'Arabic landing page valid': '<html lang="ar" dir="rtl"' in ar and 'كونسيرج' in ar,
    'hreflang set on home': all(f'hreflang="{lang}"' in home for lang in ('en','fr','de','ar','x-default')),
    'international pages in sitemap': all(f'https://ibizavipmove.com/{slug}/' in sitemap for slug in ('fr','de','ar','international-clients')),
    'semantic hero image present': 'class="hero-media"' in home and '/assets/images/hero.jpg' in home,
    'image override stylesheet present': '/assets/luxury-overrides.css' in home,
    'service cards use semantic images': home.count('class="service-card-img"><img') >= 6,
}

for name, ok in checks.items():
    print(f"{'PASS' if ok else 'FAIL'}: {name}")
failed = [name for name, ok in checks.items() if not ok]
if failed:
    raise SystemExit('Validation failed: ' + ', '.join(failed))
PY

printf 'ibizavipmove.com\n' > _site/CNAME
touch _site/.nojekyll
