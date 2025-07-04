from playwright.async_api import async_playwright

async def track_msc(bl_number):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://www.msc.com/track-a-shipment", timeout=60000)
            await page.get_by_role("textbox").fill(bl_number)
            await page.get_by_role("button", name="Track").click()

            await page.wait_for_selector(".shipment-container", timeout=20000)

            # Məlumatı parslamaq üçün HTML götür (bu sadə testdir, real datanı parse edə bilərik)
            content = await page.content()
            await browser.close()

            return {
                "success": True,
                "html": content[:1000]
            }

    except Exception as e:
        return {"success": False, "error": str(e)}
