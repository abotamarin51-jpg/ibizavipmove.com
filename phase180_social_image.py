"""Generate a real 1200x630 JPEG from the existing Pexels editorial image.

Run only through the repository's pinned image-tool virtualenv, before the
standard Python site generator. No external requests or identifying imagery.
"""
from PIL import Image, ImageOps
from phase180_enhance import SOCIAL_SOURCE, SOCIAL_TARGET


def build() -> None:
    if not SOCIAL_SOURCE.is_file():
        raise SystemExit('Phase 180 image: licensed source asset missing')
    with Image.open(SOCIAL_SOURCE) as source:
        if source.width < 1200 or source.height < 630:
            raise SystemExit('Phase 180 image: source resolution too small')
        result = ImageOps.fit(source.convert('RGB'), (1200, 630), method=Image.Resampling.LANCZOS)
        SOCIAL_TARGET.parent.mkdir(parents=True, exist_ok=True)
        result.save(SOCIAL_TARGET, format='JPEG', quality=85, optimize=True)
    with Image.open(SOCIAL_TARGET) as output:
        if output.size != (1200, 630) or output.format != 'JPEG':
            raise SystemExit('Phase 180 image: output shape/format wrong')
    if SOCIAL_TARGET.stat().st_size < 20_000:
        raise SystemExit('Phase 180 image: JPEG unexpectedly small')
    print('PASS: Phase 180 licensed editorial preview — 1200x630 JPEG')


if __name__ == '__main__':
    build()
