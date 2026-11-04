# Frozen editorial assets

These source files are copied into the generated site so an unrelated release cannot silently change approved photography.

## `villa.jpg`

- Approved bytes: GitHub Pages artifact from deployment run 34961645197 (15 September 2026).
- SHA-256: `920a2d479f869c385e47bbaf7cec73235da990c450283a75c0fb8d687de945dd`
- Dimensions: 2000 × 1334 pixels.
- Editorial source: `https://images.unsplash.com/photo-1778694276931-056406c4f4d9`

The build verifies the checksum before copying this file. Replace it only through an explicit visual review, update the checksum in `build_site.sh`, and confirm the derived AVIF/WebP files and all existing image budgets.

## `performance/`

The eight JPEGs in this directory match the production bytes verified on 4 November 2026, before the reliability change (main `57564db5ed739a28ac302151f31f0dc1bc8e84d8`):

- `hero.jpg`, `hero-desktop.jpg` and `hero-mobile.jpg`
- `yacht.jpg`, `nightlife.jpg`, `events.jpg`, `chef.jpg` and `aviation.jpg`

`phase101_enhance.py` verifies each file's approved size and SHA-256 before copying it to its existing public URL. It no longer downloads these final images from the live website, which returned HTTP 503 during an otherwise unrelated release. No images are re-encoded and there is no network fallback. The existing crop, dimensions and performance checks remain in force.

`tests/pinned_performance_images_check.py` exercises the stage with network access blocked and verifies that missing or same-size corrupted files are rejected. The pull-request workflow runs this check before building the site.

## `legacy/`

The five earlier image-input stages are also frozen. `manifest.json` records 27 stage inputs with their original source URL, capture URL, exact byte size and SHA-256. The initial, secondary, optimized and two responsive-hero stages keep their existing sequence, thresholds and output names. Their source JPEGs are stored separately so later performance comparisons remain meaningful.

The four final JPEGs not already frozen by the performance stage (security, wellness, bespoke and Private Office) were captured directly from production on 4 November 2026, before the change (main `4ed8f4287934309d341f3e04fb1db8b18efa9634`). Their currently published bytes take priority over mutable provider transforms. Intermediate inputs were captured from their recorded original URLs.

`frozen_image_inputs.py` checks the requested source, file size and checksum without fetching a replacement. A whole-stage copy validates all files before writing output. Update the input, provenance and checksum together only after reviewing the resulting image and existing image budgets.

`tests/frozen_image_inputs_check.py` runs the actual initial build and all image stages with Python network connections blocked and curl/wget unavailable. It checks all 14 final JPEGs, missing files, same-size corruption and an unreviewed source change. Dependency installation and the separate live-site browser reviews still require network access; image generation does not contact image providers or the live site.
