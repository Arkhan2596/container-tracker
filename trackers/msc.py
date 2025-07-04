import requests

def track(container_number, bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/en/track-a-shipment",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {
        "SearchBy": "BL",
        "SearchValue": bl_number.strip()
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        if response.status_code != 200:
            return {"error": f"MSC API status code: {response.status_code}", "payload": payload}

        data = response.json()

        if not data.get("Shipments"):
            return {"error": "MSC: Heç bir shipment tapılmadı.", "payload": payload, "response": data}

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
            name = event.get("EventName", "").lower()
            date = event.get("ActualDate", "") or event.get("EstimatedDate", "")
            vessel = event.get("VesselName", "") or event.get("VesselVoyage", "")

            if "export loaded" in name and not result["etd_pol"]:
                result["etd_pol"] = date
            elif "transshipment discharged" in name and not result["eta_transshipment"]:
                result["eta_transshipment"] = date
            elif "transshipment loaded" in name and not result["etd_transshipment"]:
                result["etd_transshipment"] = date
                result["feeder"] = vessel
            elif "discharged from vessel" in name and not result["eta_pod"]:
                result["eta_pod"] = date

        return result

    except Exception as e:
        return {"error": f"MSC istisna: {str(e)}", "payload": payload}
