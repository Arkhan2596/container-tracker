import requests

def track(container_number, bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/en/track-a-shipment",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {"SearchBy": "BL", "SearchValue": bl_number.strip()}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"error": f"MSC API status code: {response.status_code}"}

        data = response.json()
        shipments = data.get("Shipments", [])
        if not shipments:
            return {"error": "MSC: Heç bir shipment tapılmadı."}

        events = shipments[0].get("Events", [])

        result = {
            "ETD from POL": "",
            "ETA Transshipment port": "",
            "ETD Transshipment port": "",
            "Feeder name": "",
            "ETA Vessel at POD": "",
            "raw_result": data
        }

        for event in events:
            name = event.get("EventName", "").lower()
            date = event.get("ActualDate", "") or event.get("EstimatedDate", "")
            location = event.get("Location", {}).get("DisplayName", "")
            vessel = event.get("VesselName", "")

            # ETD from POL
            if "export loaded" in name and not result["ETD from POL"]:
                result["ETD from POL"] = date

            # ETA Transshipment
            elif "transshipment discharged" in name and not result["ETA Transshipment port"]:
                result["ETA Transshipment port"] = date

            # ETD Transshipment
            elif "transshipment loaded" in name and not result["ETD Transshipment port"]:
                result["ETD Transshipment port"] = date

            # ETA at POD
            elif "import discharged" in name and not result["ETA Vessel at POD"]:
                result["ETA Vessel at POD"] = date

            # Feeder name
            if vessel and "med" in vessel.lower():
                result["Feeder name"] = vessel

        return result

    except Exception as e:
        return {"error": f"MSC API istisna: {str(e)}"}
