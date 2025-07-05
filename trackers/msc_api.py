# trackers/msc_api.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import html
import time

def track_msc(bl_number: str) -> dict:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("https://www.msc.com/track-a-shipment")

        input_box = driver.find_element("id", "trackingNumber")
        input_box.clear()
        input_box.send_keys(bl_number)

        button = driver.find_element("xpath", '//button[contains(text(), "Track")]')
        button.click()

        time.sleep(10)

        tree = html.fromstring(driver.page_source)
        shipment_info = tree.xpath('//div[contains(@class,"shipment-container")]//text()')

        return {
            "success": True,
            "result": ''.join(shipment_info)[:500]
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        driver.quit()
