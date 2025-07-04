import aiohttp
import json

async def track_msc(bl_number):
    try:
        url = "https://www.msc.com/api/feature/tools/TrackingInfo"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
            "Content-Type": "application/json",
            "Origin": "https://www.msc.com",
            "Referer": "https://www.msc.com/",
        }

        payload = {
            "SearchBy": "BOL",
            "Number": bl_number
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=headers, json=payload) as resp:
                if resp.status != 200:
                    return {"success": False, "error": f"HTTP {resp.status} error"}
                
                data = await resp.json()

                # sənədləri burdan çıxart
                containers = data.get("Containers", [])
                if not containers:
                    return {"success": False, "error": "No container data found."}

                events = containers[0].get("Events", [])

                # AYRILMIŞ məlumat çıxarış — nümunə üçün
                etd_pol = next((e["EventDate"] for e in events if e["EventName"] == "Export Loaded"), "")
                eta_pod = next((e["EventDate"] for e in events if "Discharged" in e["EventName"]), "")
                feeder = next((e["VesselName"] for e in events if e.get("VesselName")), "")

                return {
                    "success": True,
                    "etd_pol": etd_pol,
                    "eta_pod": eta_pod,
                    "feeder": feeder,
                    "eta_transshipment": "",  # Əgər varsa çıxara bilərsən
                    "etd_transshipment": ""
                }

    except Exception as e:
        return {"success": False, "error": str(e)}
