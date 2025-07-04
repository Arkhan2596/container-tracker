import requests
from bs4 import BeautifulSoup
from datetime import datetime

def track(container_number: str, bl_number: str = None):
    try:
        tracking_number = bl_number if bl_number else container_number
        url = f"https://www.msc.com/en/track-a-shipment?tracking_number={tracking_number}"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return {"error": "MSC saytı cavab vermədi."}

        soup = BeautifulSoup(response.text, "lxml")
        rows = soup.find_all("div", class_="event-tracking__event")
        print("Saytdan alınan event sayı:", len(rows))  # log üçün

        if not rows:
            return {"error": "Heç bir izləmə məlumatı tapılmadı."}

        etd_from_pol = None
        eta_trans = None
        etd_trans = None
        feeder_name = None
        eta_pod = None

        for row in rows:
            text = row.get_text(separator="|", strip=True).lower()

            # Tarixi oxu
            date_raw = row.find("div", class_="event-tracking__date")
            if not date_raw:
                continue

            try:
                date_str = date_raw.text.strip()
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                formatted_date = date_obj.strftime("%d.%m.%Y")
            except:
                continue

            # Əlavə et - şərtlərə əsasən
            if "export loaded on vessel" in text and not etd_from_pol:
                etd_from_pol = formatted_date

            elif "transshipment discharged" in text and not eta_trans:
                eta_trans = formatted_date

            elif "transshipment loaded" in text and not etd_trans:
                etd_trans = formatted_date
                feeder = row.find("div", class_="event-tracking__vessel")
                feeder_name = feeder.text.strip() if feeder else ""

            elif "import discharged from vessel" in text and not eta_pod:
                eta_pod = formatted_date

        return {
            "etd_pol": etd_from_pol or "not found",
            "eta_transit": eta_trans or "not found",
            "etd_transit": etd_trans or "not found",
            "feeder_name": feeder_name or "",
            "eta_pod": eta_pod or "not found"
        }

    except Exception as e:
        return {"error": f"Xəta baş verdi: {str(e)}"}
