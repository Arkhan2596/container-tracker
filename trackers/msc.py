import requests

def track(container_number, bl_number):
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
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
        if not data.get("Shipments"):
            return {"error": "MSC: Heç bir shipment tapılmadı."}

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

            if "loaded" in event_name and not result["etd_pol"]:
                result["etd_pol"] = event_date
            elif "transshipment" in event_name:
                if "eta" in event_name:
                    result["eta_transshipment"] = event_date
                elif "etd" in event_name:
                    result["etd_transshipment"] = event_date
            elif "discharged" in event_name and not result["eta_pod"]:
                result["eta_pod"] = event_date

        return result

    except Exception as e:
        return {"error": f"MSC API istisna: {str(e)}"}
