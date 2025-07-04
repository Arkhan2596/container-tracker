import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from bs4 import BeautifulSoup

async def track_msc(bl_number):
    try:
        async with async_playwright() as playwright:
            chrome_path = "/opt/render/.cache/ms-playwright/chromium-1179/chrome-linux/chrome"
            browser = await playwright.chromium.launch(executable_path=chrome_path, headless=True)
            page = await browser.new_page()

            await page.goto("https://www.msc.com/en/tools/track-a-shipment")
            await page.fill('input[name="reference"]', bl_number)
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(6000)

            html = await page.content()
            await browser.close()

            # ✅ HTML parse et
            soup = BeautifulSoup(html, "lxml")

            def get_event(text):
                el = soup.find("div", string=lambda t: t and text.lower() in t.lower())
                if el:
                    parent = el.find_parent("div", class_="shipment-event") or el.parent
                    date_el = parent.find("div", class_="date")
                    port_el = parent.find("div", class_="port")
                    vessel_el = parent.find("div", class_="vessel")
                    return {
                        "date": date_el.text.strip() if date_el else "",
                        "port": port_el.text.strip() if port_el else "",
                        "vessel": vessel_el.text.strip() if vessel_el else ""
                    }
                return {}

            # Bu hissədə uyğunlaşdırma edə bilərik
            etd_pol = get_event("Export Loaded")
            trans = get_event("Transshipment")
            discharged = get_event("Discharged from Vessel")

            return {
                "success": True,
                "etd_pol": etd_pol.get("date", ""),
                "eta_transshipment": trans.get("date", ""),
                "etd_transshipment": trans.get("date", ""),
                "feeder": trans.get("vessel", ""),
                "eta_pod": discharged.get("date", "")
            }

    except Exception as e:
        print("🔥 MSC scraping error:", str(e))  # bunu əlavə et
        return {
            "success": False,
            "error": str(e)
        }
