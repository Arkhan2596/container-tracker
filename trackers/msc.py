import requests
from bs4 import BeautifulSoup

def track_msc(container_number, bl_number):
    session = requests.Session()
    tracking_number = bl_number or container_number
    url = f"https://www.msc.com/en/track-a-shipment?trackingNumber={tracking_number}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = session.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, "lxml")

        # Aşağıdakı hissə demo məqsədlidir
        # Real scraping üçün HTML strukturuna uyğunlaşdırılacaq
        result = {
            "etd_pol": "2024-07-05",  # Example
            "eta_transit": "2024-07-10",
            "etd_transit": "2024-07-11",
            "feeder": "FEEDER-X",
            "eta_pod": "2024-07-15",
            "status": "Success"
        }

        return result

    except Exception as e:
        return {
            "etd_pol": "",
            "eta_transit": "",
            "etd_transit": "",
            "feeder": "",
            "eta_pod": "",
            "status": f"Error: {str(e)}"
        }
