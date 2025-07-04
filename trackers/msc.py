import requests

def track(container_number: str, bl_number: str = None):
    try:
        # Hansı nömrə varsa onu istifadə edirik
        tracking_number = bl_number or container_number
        if not tracking_number:
            return {"error": "Neither container number nor BL number provided."}

        url = "https://www.msc.com/api/feature/tools/TrackingInfo"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Origin": "https://www.msc.com",
            "Referer": "https://www.msc.com/en/track-a-shipment"
        }

        payload = {
            "TrackingNumber": tracking_number,
            "SearchBy": "B" if bl_number else "C"  # BL varsa B, yoxdursa konteyner üçün C
        }

        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            return {"error": "MSC API cavab vermədi."}

        data = response.json()

        # Əsas izləmə eventləri
        events = data.get("TrackingEvents", [])
        raw_result = events  # Sonra təhlil üçün bütün məlumatları saxlayırıq

        etd_from_pol = None
        eta_transshipment = None
        etd_transshipment = None
        feeder_name = None
        eta_pod = None

        for event in events:
            desc = event.get("EventDescription", "").lower()
            date = event.get("EventDate", "")[:10]  # format: YYYY-MM-DD
            vessel = event.get("VesselName", "")
            location = event.get("LocationName", "")

            if "export loaded" in desc and not etd_from_pol:
                etd_from_pol = date
            elif "transshipment discharged" in desc and not eta_transshipment:
                eta_transshipment = date
            elif "transshipment loaded" in desc and not etd_transshipment:
                etd_transshipment = date
                feeder_name = vessel
            elif "import discharged" in desc and not eta_pod:
                eta_pod = date

        return {
            "etd_pol": etd_from_pol,
            "eta_transit": eta_transshipment,
            "etd_transit": etd_transshipment,
            "feeder": feeder_name,
            "eta_pod": eta_pod,
            "raw_result": raw_result
        }

    except Exception as e:
        return {"error": f"Xəta baş verdi: {str(e)}"}
