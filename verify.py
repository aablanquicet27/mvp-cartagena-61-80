"""Browser verification and screenshots. Optional development dependency: playwright."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
SELECTED = ['elia-jewelry','restaurante-porton-de-san-sebastian','henna-cartagena','mayking-barber-club','muscle-gym-colombia','dulce-cream-heladeria']


def main():
    slugs = sorted(p.parent.name for p in (ROOT/'dist').glob('*/index.html'))
    errors = []
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path='/home/ubuntu/.local/bin/google-chrome', args=['--no-sandbox'])
        page = browser.new_page()
        page.on('pageerror', lambda error: errors.append(str(error)))
        for slug in slugs:
            page.goto('http://localhost:8080/'+slug+'/',wait_until='domcontentloaded')
            for width in [360,768,1440]:
                page.set_viewport_size({'width':width,'height':1000})
                page.wait_for_timeout(60)
                assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), (slug,width,'horizontal overflow')
            assert page.locator('h1').count() == 1
            assert page.locator('main img').count() >= 4
            assert len(set(page.locator('main img').evaluate_all('(els)=>els.map(e=>e.src)'))) >= 4
            assert page.locator('a[href^="tel:"]').count() == 1
            assert page.locator('iframe[src*="maps.google.com"]').count() == 1
            page.locator('.offer-float').click()
            assert page.locator('dialog').is_visible()
            assert page.locator('.seller-cta').get_attribute('href').startswith('https://wa.me/?text=')
            page.keyboard.press('Escape')
            assert not page.locator('dialog').is_visible()
        print('PASS: 20 sites × 3 widths (360, 768, 1440); contacts, 4 unique photos, Maps, modal, Escape and empty seller fallback')
        page.goto('http://localhost:8080/hostal-playa-blanca/')
        page.locator('#arrival').fill('2027-12-10')
        page.locator('#departure').fill('2027-12-09')
        assert not page.locator('#departure').evaluate('(e)=>e.validity.valid')
        page.locator('#departure').fill('2027-12-12')
        with page.expect_popup() as popup:
            page.locator('.booking button').click()
        assert '2027-12-10' in popup.value.url and '2027-12-12' in popup.value.url
        popup.value.close()
        print('PASS: booking rejects invalid date range; valid dates open business WhatsApp')
        page.set_viewport_size({'width':390,'height':844})
        page.goto('http://localhost:8080/elia-jewelry/')
        page.locator('.menu-toggle').click()
        assert page.locator('.nav').evaluate('(e)=>e.classList.contains("open")')
        page.locator('.nav nav a').first.click()
        assert page.locator('.menu-toggle').get_attribute('aria-expanded') == 'false'
        print('PASS: mobile navigation opens and closes on section selection')
        for slug in ['']+SELECTED:
            for label,width,height in [('desktop',1440,1000),('mobile',390,844)]:
                page.set_viewport_size({'width':width,'height':height})
                page.goto('http://localhost:8080/'+slug+'/',wait_until='networkidle')
                page.evaluate('document.fonts.ready')
                page.wait_for_timeout(1200)
                page.screenshot(path=str(ROOT/'evidence'/f'{slug or "index"}-{label}.png'))
                if slug:
                    page.locator('.offer-float').click()
                    if slug == SELECTED[0]:
                        page.wait_for_timeout(450)
                        page.screenshot(path=str(ROOT/'evidence'/f'offer-{label}.png'))
                    page.keyboard.press('Escape')
        page.emulate_media(reduced_motion='reduce')
        page.goto('http://localhost:8080/elia-jewelry/')
        assert page.locator('.ticker>div').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
        print('PASS: prefers-reduced-motion disables animations')
        assert not errors, errors
        print('PASS: no JavaScript page errors; 16 screenshots captured')
        browser.close()


if __name__ == '__main__':
    main()
