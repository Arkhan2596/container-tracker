import requests
from lxml import html

def track_msc(bl_number: str) -> dict:
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/",
    }
    payload = {
        "SearchBy": "B",         # "B" = BL number, "C" = Container no.
        "Numbers": [bl_number]
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code != 200:
            return {"success": False, "error": f"HTTP {response.status_code} error"}

        data = response.json()

        # Əgər cavab boşdursa
        containers = data.get("Containers", [])
        if not containers:
            return {"success": False, "error": "No container data found."}

        events = containers[0].get("Events", [])
        etd_pol = next((e["EventDate"] for e in events if e["EventName"] == "Export Loaded"), "")
        eta_pod = next((e["EventDate"] for e in events if "Discharged" in e["EventName"]), "")
        feeder = next((e.get("VesselName", "") for e in events if e.get("VesselName")), "")

        return {
            "success": True,
            "etd_pol": etd_pol,
            "eta_transshipment": "",
            "etd_transshipment": "",
            "feeder": feeder,
            "eta_pod": eta_pod
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
