import requests

def track(container_number, bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/en/track-a-shipment",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "SearchBy": "BL",
        "SearchValue": bl_number.strip()
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=20)

        if response.status_code != 200:
            return {
                "error": f"MSC API status code: {response.status_code}",
                "payload": payload
            }

        data = response.json()
        if not data.get("Shipments"):
            return {"error": "MSC: Heç bir shipment tapılmadı.", "payload": payload}

        shipment = data["Shipments"][0]
        events = shipment.get("Events", [])
        result = {
            "etd_pol": "",
            "eta_transshipment": "",
            "etd_transshipment": "",
            "feeder": "",
            "eta_pod": "",
            "raw_result": data
        }

        for event in events:
            event_name = event.get("EventName", "").lower()
            location = event.get("Location", {}).get("DisplayName", "")
            event_date = event.get("ActualDate", "") or event.get("EstimatedDate", "")
            vessel = event.get("VesselName", "") or ""

            if "export loaded" in event_name and not result["etd_pol"]:
                result["etd_pol"] = event_date
            elif "transshipment discharged" in event_name:
                result["eta_transshipment"] = event_date
            elif "transshipment loaded" in event_name:
                result["etd_transshipment"] = event_date
            elif "discharged from vessel" in event_name:
                result["eta_pod"] = event_date
                result["feeder"] = vessel

        return result

    except Exception as e:
        return {"error": f"MSC API exception: {str(e)}", "payload": payload}
