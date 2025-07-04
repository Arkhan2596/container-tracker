import aiohttp
import json

async def track_msc(bl_number):
    try:
        url = "https://www.msc.com/api/feature/tools/TrackingInfo"
        headers = {
            "Content-Type": "application/json",
            "Origin": "https://www.msc.com",
            "Referer": "https://www.msc.com/en/tools/track-a-shipment",
            "User-Agent": "Mozilla/5.0"
        }
        payload = {
            "containerNumber": None,
            "isLiveTracking": False,
            "searchBy": "B",
            "searchNumber": bl_number
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as response:
                if response.status != 200:
                    return {"success": False, "error": f"HTTP {response.status} error"}

                data = await response.json()

                if not data.get("shipments"):
                    return {"success": False, "error": "No shipment found"}

                shipment = data["shipments"][0]
                events = shipment.get("events", [])

                # Boş dəyişənlər
                etd_pol = ""
                eta_trans = ""
                etd_trans = ""
                eta_pod = ""
                feeder = ""

                for event in events:
                    event_type = event.get("eventType", "").lower()
                    event_date = event.get("eventDate", "")
                    vessel = event.get("vesselName", "")

                    if "export loaded" in event_type and not etd_pol:
                        etd_pol = event_date
                    elif "transshipment" in event_type:
                        if not eta_trans:
                            eta_trans = event_date
                        if not etd_trans:
                            etd_trans = event_date
                        if vessel and not feeder:
                            feeder = vessel
                    elif "discharged from vessel" in event_type and not eta_pod:
                        eta_pod = event_date

                return {
                    "success": True,
                    "etd_pol": etd_pol,
                    "eta_transshipment": eta_trans,
                    "etd_transshipment": etd_trans,
                    "feeder": feeder,
                    "eta_pod": eta_pod
                }

    except Exception as e:
        return {"success": False, "error": str(e)}
