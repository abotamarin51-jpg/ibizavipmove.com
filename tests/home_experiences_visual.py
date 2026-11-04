"""Review the Home experiences and real editable Contact handoffs without sending."""
from urllib.parse import urlsplit
from PIL import Image

CASES = (
    ('villa', '/contact/?service=villas', 'Luxury Villas & Private Stays'),
    ('yacht', '/contact/?service=yacht', 'Yachts & Charters'),
    ('nightlife', '/contact/?service=access', 'Restaurants, Beach Clubs & Nightlife'),
)


def review_home_experiences(page, origin, mode, width, height, output):
    response = page.goto(origin + '/', wait_until='load')
    assert response.status == 200
    page.evaluate('document.fonts.ready')
    assert page.locator('h1').inner_text() == 'Luxury concierge in Ibiza,\npersonally arranged.'
    assert page.locator('.ivm-home-tagline').inner_text() == 'IBIZA · PRIVATE CLIENTS & TRAVEL PROFESSIONALS'
    assert page.locator('.ivm-ref-service-rail .ivm-ref-service').count() == 6
    assert page.locator('.ivm-exp-card').count() == 3
    assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com/'
    assert page.locator('h1').count() == 1
    assert 'noindex' not in page.locator('meta[name="robots"]').get_attribute('content')
    assert page.locator('main a[href="/private-office/"]').count() >= 1
    assert page.locator('main a[href="/ibiza-intelligence/"]').count() >= 1
    assert page.locator('.ivm-home-case a').get_attribute('href') == '/case-studies/weekend-concierge-two-guests/'
    page.screenshot(path=str(output / f'home-experiences-hero-{mode}.png'), animations='disabled')
    measurements = []
    for name, href, expected in CASES:
        card = page.locator(f'.ivm-exp-card[data-experience="{name}"]')
        image = card.locator('img')
        image.evaluate('e=>e.scrollIntoView({block:"center",behavior:"instant"})')
        image.evaluate('e=>e.decode()')
        assert image.evaluate('e=>e.complete && e.naturalWidth > 0')
        assert image.get_attribute('loading') == 'lazy'
        assert image.evaluate('(e)=>e.currentSrc').startswith(origin + '/assets/images/experience-' + name)
        button = card.locator('a.ivm-exp-plan')
        assert button.get_attribute('href') == href
        button.evaluate('e=>e.scrollIntoView({block:"center",behavior:"instant"})')
        button.focus()
        state = button.evaluate('''e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e),t=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);return {width:r.width,height:r.height,font:parseFloat(s.fontSize),inside:r.left>=0&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1,unobstructed:t===e||e.contains(t),focused:document.activeElement===e,overflow:document.documentElement.scrollWidth>innerWidth+1}}''')
        assert state['height'] >= 44 and state['font'] >= 14
        assert state['inside'] and state['unobstructed'] and state['focused'] and not state['overflow'], (mode, name, state)
        button.click(trial=True)
        measurements.append({'experience': name, 'button': state})
    proof = page.locator('.ivm-phase105-proof')
    contrast = proof.evaluate('''e=>{
      const rgb=s=>(s.match(/[\\d.]+/g)||[]).map(Number);
      const luminance=c=>c.slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
      let node=e,bg;
      while(node){let c=rgb(getComputedStyle(node).backgroundColor);if(c.length===3||c[3]>=.99){bg=c;break;}node=node.parentElement;}
      bg=bg||[255,255,255];
      const ratio=node=>{const a=luminance(rgb(getComputedStyle(node).color)),b=luminance(bg);return(Math.max(a,b)+.05)/(Math.min(a,b)+.05);};
      return{heading:ratio(e.querySelector('h2')),paragraph:ratio(e.querySelector('p')),background:bg};
    }''')
    assert contrast['heading'] >= 4.5 and contrast['paragraph'] >= 4.5, (mode, contrast)
    proof.screenshot(path=str(output / f'home-experiences-proof-{mode}.png'), animations='disabled')
    # Capture from the page top so fixed navigation is shown at its real
    # initial position rather than repeated inside a tall element screenshot.
    page.evaluate("document.activeElement.blur();window.scrollTo({top:0,behavior:'instant'})")
    section = page.locator('#experiences')
    bounds = section.bounding_box()
    full = output / f'home-experiences-full-{mode}.png'
    page.screenshot(path=str(full), full_page=True, animations='disabled')
    with Image.open(full) as screenshot:
        x,y,w,h=(bounds[k] for k in ('x','y','width','height'))
        screenshot.crop((int(x),int(y),round(x+w),round(y+h))).save(output / f'home-experiences-cards-{mode}.png')
    for name, href, expected in CASES:
        page.goto(origin + '/', wait_until='load')
        button = page.locator(f'.ivm-exp-card[data-experience="{name}"] a.ivm-exp-plan')
        button.evaluate('e=>e.scrollIntoView({block:"center",behavior:"instant"})')
        with page.expect_navigation(wait_until='load'):
            button.click()
        assert page.url == origin + href
        service = page.locator('#fService')
        assert service.input_value() == expected, (mode, name, service.input_value())
        assert service.is_enabled() and service.locator('option').count() == 19
        for identity in ('fName', 'fPhone', 'fArrival', 'fDeparture', 'fBrief'):
            assert page.locator('#' + identity).input_value() == '', (mode, name, identity)
        assert page.locator('link[rel="canonical"]').get_attribute('href') == 'https://ibizavipmove.com/contact/'
        # A representative can change the selection; no form is submitted.
        service.select_option('Full Concierge')
        assert service.input_value() == 'Full Concierge'
    print(f'PASS: Home experiences photos, layout and all three editable contact handoffs: {mode}')
    return {'mode': mode, 'viewport': [width, height], 'cards': measurements,
            'operationalProofContrast': contrast,
            'contactHandoffs': 'all three passed; no enquiry submitted'}
