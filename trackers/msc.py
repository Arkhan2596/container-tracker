import requests

def track(container_number, bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/en/track-a-shipment",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "SearchBy": "BL",
        "SearchValue": bl_number.strip()
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)

        if response.status_code != 200:
            return {"error": f"MSC API status code: {response.status_code}", "raw": response.text}

        data = response.json()
        if not data.get("Shipments"):
            return {"error": "MSC: Heç bir shipment tapılmadı.", "raw": data}

        shipment = data["Shipments"][0]
        events = shipment.get("Events", [])
        result = {
            "ETD from POL": "",
            "ETA Transshipment port": "",
            "ETD Transshipment port": "",
            "Feeder name": "",
            "ETA Vessel at POD": "",
            "raw_result": data
        }

        for event in events:
            event_name = event.get("EventName", "").lower()
            event_date = event.get("ActualDate") or event.get("EstimatedDate") or ""
            vessel_name = event.get("VesselName", "")

            if "loaded" in event_name and not result["ETD from POL"]:
                result["ETD from POL"] = event_date
            elif "transshipment" in event_name:
                if "eta" in event_name:
                    result["ETA Transshipment port"] = event_date
                elif "etd" in event_name:
                    result["ETD Transshipment port"] = event_date
            elif "discharged" in event_name and not result["ETA Vessel at POD"]:
                result["ETA Vessel at POD"] = event_date

            if vessel_name and not result["Feeder name"]:
                result["Feeder name"] = vessel_name

        return result

    except Exception as e:
        return {"error": f"MSC API istisna: {str(e)}"}
