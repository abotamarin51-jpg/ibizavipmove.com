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
        assert page.locator('#origin-planner .origin-guides a').count() == 9
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), (mode, path)
    assert page.locator('html').get_attribute('dir') == 'rtl'
    page.goto(origin + '/international-clients/?utm_source=qa#from-gb-london')
    expect(page.locator('#origin-city')).to_have_value('london')
    # Use a stub clipboard so automated checks do not change the runner clipboard.
    page.evaluate("""Object.defineProperty(navigator, 'clipboard', {configurable:true,
        value:{writeText: async text => { window.originCopiedInTest = text; }}})""")
    page.locator('#origin-share').click()
    expect(page.locator('#origin-share-status')).to_have_text('Link copied')
    assert page.evaluate('window.originCopiedInTest') == origin + '/international-clients/#from-gb-london'
    page.evaluate("""Object.defineProperty(navigator, 'clipboard', {configurable:true,
        value:{writeText: () => Promise.reject(new Error('denied'))}})""")
    page.locator('#origin-country').select_option('CH')
    page.locator('#origin-share').click()
    expect(page.locator('#origin-share-url')).to_be_visible()
    assert page.locator('#origin-share-url').input_value() == origin + '/international-clients/#from-ch'
    page.goto(origin + '/international-clients/#from-us')
    expect(page.locator('#origin-city')).to_have_value('')
    expect(page.locator('#origin-local-clock')).to_be_hidden()
    assert 'United States' in message(page.locator('#origin-whatsapp'))
    page.locator('#origin-country').select_option('other')
    expect(page.locator('#origin-share')).to_be_hidden()
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
    for label, language, path, form, main_copy, request_city in (
        ('London', 'en', '/london-to-ibiza-concierge/', '/contact/?service=travel-concierge', 'weekend', 'London'),
        ('Paris', 'fr', '/fr/conciergerie-ibiza-depuis-paris/', '/fr/contact/', 'depuis Paris', 'Paris'),
        ('Munich', 'de', '/de/concierge-ibiza-ab-muenchen/', '/de/kontakt/', 'München', 'München'),
        ('Amsterdam', 'en', '/amsterdam-to-ibiza-concierge/', '/contact/?service=villas', 'Amsterdam', 'Amsterdam'),
        ('Milan', 'en', '/milan-to-ibiza-concierge/', '/contact/?service=access', 'Milan', 'Milan'),
        ('Zürich', 'de', '/de/concierge-ibiza-ab-zuerich/', '/de/kontakt/', 'Zürich', 'Zürich'),
    ):
        page.goto(origin + '/international-clients/')
        page.locator('#origin-planner').get_by_role('link', name=label, exact=True).click()
        page.wait_for_url(origin + path)
        assert page.locator('html').get_attribute('lang') == language
        expect(page.locator('h1')).to_contain_text(main_copy)
        assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com' + path
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        assert request_city in message(page.locator('main .ny-button').first)
        link = page.locator('main a[href="' + form + '"]').first
        link.click()
        page.wait_for_url(origin + form)
        assert page.locator('html').get_attribute('lang') == language
        if form.endswith('service=villas'):
            expect(page.locator('#fService')).to_have_value('Luxury Villas & Private Stays')
        if form.endswith('service=access'):
            expect(page.locator('#fService')).to_have_value('Restaurants, Beach Clubs & Nightlife')

    for service, city, destination in (
        ('/de/private-events-ibiza/', 'munich', '/de/concierge-ibiza-ab-muenchen/'),
        ('/luxury-villas-ibiza/', 'amsterdam', '/amsterdam-to-ibiza-concierge/'),
        ('/vip-tables-club-access-ibiza/', 'milan', '/milan-to-ibiza-concierge/'),
        ('/de/luxusvillen-ibiza/', 'zurich', '/de/concierge-ibiza-ab-zuerich/'),
    ):
        page.goto(origin + service)
        link = page.locator(f'main [data-origin-reference="{city}"] a')
        expect(link).to_have_count(1)
        assert link.get_attribute('href') == destination
        link.click()
        page.wait_for_url(origin + destination)
        expect(page.locator('main a[href="' + service + '"]').first).to_be_visible()
    return {'mode': mode, 'localizedHubs': len(cases), 'newServiceLinks': 4,
            'guides': ['Miami', 'Dubai', 'London', 'Paris', 'Munich', 'Amsterdam', 'Milan', 'Zurich']}
