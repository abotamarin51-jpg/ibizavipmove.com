"""Check localized city selection, handoffs and market guides without sending enquiries."""
from urllib.parse import parse_qs, urlsplit
from playwright.sync_api import expect


def message(link):
    parsed = urlsplit(link.get_attribute('href'))
    assert parsed.hostname == 'wa.me' and parsed.path == '/34600703303'
    return parse_qs(parsed.query)['text'][0]


def review_origins(page, origin, mode, output):
    cases = (
        ('international-clients', 'en', 'ch-geneva', 'Geneva', 'Switzerland'),
        ('es/clientes-internacionales', 'es', 'us-miami', 'Miami', 'Estados Unidos'),
        ('fr/clients-internationaux', 'fr', 'gb-london', 'Londres', 'Royaume-Uni'),
        ('de/internationale-kunden', 'de', 'jp-tokyo', 'Tokio', 'Japan'),
        ('ar/international-clients', 'ar', 'ae-dubai', 'دبي', 'الإمارات العربية المتحدة'),
    )
    for path, lang, key, city, region in cases:
        response = page.goto(f'{origin}/{path}/#from-{key}')
        assert response.status == 200 and page.locator('html').get_attribute('lang') == lang
        country_code, city_code = key.split('-', 1)
        expect(page.locator('#origin-country')).to_have_value(country_code.upper())
        expect(page.locator('#origin-city')).to_have_value(city_code)
        expect(page.locator('#origin-local-clock')).to_be_visible()
        assert page.locator('#origin-local-clock strong').inner_text().strip()
        assert page.locator('#origin-ibiza-time').inner_text().strip()
        assert city in message(page.locator('#origin-whatsapp'))
        assert region in message(page.locator('#origin-whatsapp'))
        assert page.locator('link[rel="canonical"]').get_attribute('href') == f'https://ibizavipmove.com/{path}/'
        assert page.locator('#origin-planner .origin-guides a').count() == 3
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (mode, path)
    assert page.locator('html').get_attribute('dir') == 'rtl'
    page.goto(origin + '/international-clients/#from-us')
    expect(page.locator('#origin-city')).to_have_value('')
    expect(page.locator('#origin-local-clock')).to_be_hidden()
    assert 'United States' in message(page.locator('#origin-whatsapp'))
    page.locator('#origin-country').select_option('other')
    page.locator('#origin-custom').fill('Nassau, Bahamas')
    page.locator('#origin-service').select_option(label='Villa and chauffeur')
    brief = message(page.locator('#origin-whatsapp'))
    assert 'Nassau, Bahamas' in brief and 'Villa and chauffeur' in brief
    assert 'Nassau' not in page.url
    page.locator('#origin-country').select_option('AE')
    page.locator('#origin-city').select_option('dubai')
    assert page.url.endswith('#from-ae-dubai')
    for city, guide, native, requests in (
        ('Miami', 'miami', '/es/contacto/', ('marina', 'charter')),
        ('Dubai', 'dubai', '/ar/contact/', ('family', 'office')),
    ):
        page.goto(origin + '/international-clients/')
        page.locator('#origin-planner').get_by_role('link', name=city, exact=True).click()
        path = f'/{guide}-to-ibiza-concierge/'
        page.wait_for_url(origin + path)
        expect(page.locator('h1')).to_contain_text(city)
        assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com' + path
        assert page.locator('main a[href="' + native + '"]').count() == 1
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (mode, city)
        briefs = []
        for choice in page.locator('details.origin-choice').all():
            if choice.get_attribute('open') is None:
                choice.locator('summary').click()
            cta = choice.locator(':scope > a')
            cta.click(trial=True)
            briefs.append(message(cta))
        assert len(set(briefs)) == len(requests) and all(city in b for b in briefs)
        page.evaluate("window.scrollTo({top:0, behavior:'instant'})")
        page.screenshot(path=str(output / f'origin-{guide}-{mode}.png'), animations='disabled')
    return {'mode': mode, 'localizedHubs': len(cases), 'guides': ['Miami', 'Dubai']}
