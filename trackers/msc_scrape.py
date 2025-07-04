# trackers/msc_scrape.py

from playwright.sync_api import sync_playwright

def track_msc(bl_number):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.msc.com/en/track-a-shipment")

            # BL nömrəsini daxil et və axtar
            page.fill('input[name="SearchValue"]', bl_number)
            page.click('button:has-text("Track")')

            page.wait_for_selector('.shipment-events', timeout=15000)
            html_content = page.inner_html('.shipment-events')
            print("🔍 HTML content from MSC:")
            print(html_content)  # <-- Bunu log üçün əlavə etdik

            browser.close()
            return {
                "success": True,
                "html": html_content
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
