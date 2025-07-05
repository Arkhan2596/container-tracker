from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
import time

def track_msc(bl_number):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    try:
        driver.get("https://www.msc.com/track-a-shipment")

        # BL nömrəsini inputa yaz
        input_box = driver.find_element("id", "trackingNumber")
        input_box.clear()
        input_box.send_keys(bl_number)

        # Track düyməsini kliklə
        button = driver.find_element("xpath", '//button[contains(text(), "Track")]')
        button.click()

        # Gözlə nəticə gələnə qədər (sadə, 10 saniyə)
        time.sleep(10)

        page_source = driver.page_source

        # HTML-i lxml ilə analiz elə
        tree = html.fromstring(page_source)

        # Məsələn, bir nümunə element seçək
        shipment_info = tree.xpath('//div[contains(@class,"shipment-container")]//text()')

        # İlk 500 simvolu qaytar
        return {
            "success": True,
            "result": ''.join(shipment_info)[:500]
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.quit()
