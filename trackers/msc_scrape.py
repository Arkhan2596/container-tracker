import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import json

async def track_msc(bl_number):
    try:
        async with async_playwright() as playwright:
            # ✅ Render-də yüklənmiş brauzerin tam yolu
            chrome_path = "/opt/render/.cache/ms-playwright/chromium-1179/chrome-linux/chrome"
            
            browser = await playwright.chromium.launch(executable_path=chrome_path, headless=True)
            page = await browser.new_page()

            # MSC tracking səhifəsinə POST vasitəsilə keçid (əgər API varsa, onu istifadə et)
            await page.goto("https://www.msc.com/en/tools/track-a-shipment")

            await page.fill('input[name="reference"]', bl_number)
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(6000)

            content = await page.content()
            await browser.close()

            # Parse ediləcək hissəni burada əlavə edirsən:
            # events = parse_events(content)  # öz parse funksiyanı çağır
            return {
                "success": True,
                "raw_html": content,
                # "parsed_events": events
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Test üçün (lokalda işlədilirsə)
if __name__ == "__main__":
    bl = "MEDUJB511593"
    result = asyncio.run(track_msc(bl))
    print(json.dumps(result, indent=2))
