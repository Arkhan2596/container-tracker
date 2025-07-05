from playwright.async_api import async_playwright

async def track_msc(bl_number):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.msc.com/track-a-shipment", timeout=60000)

            await page.locator("#trackingNumber").fill(bl_number)
            await page.get_by_role("button", name="Track").click()

            # Sadəcə əsas selectoru yoxla, məsələn, nəticə qutusu
            await page.wait_for_selector(".shipment-container", timeout=20000)

            # Ən əsas: JSON şəklində lazım olan məlumatı çıxarmağa çalış
            # Sadəcə səhifədəki bəzi mətnləri götürək misal üçün
            result_text = await page.locator(".shipment-container").inner_text()

            await browser.close()

            return {
                "success": True,
                "result": result_text[:1000]  # İlk 1000 simvolu qaytarırıq
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
