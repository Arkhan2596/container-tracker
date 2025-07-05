# trackers/msc_api.py
import aiohttp
import asyncio

async def track_msc(bl_number: str) -> dict:
    url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/",
    }
    payload = {
        "SearchBy": "B",  # BL number
        "Numbers": [bl_number]
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, headers=headers) as resp:
            if resp.status != 200:
                return {"success": False, "error": f"HTTP {resp.status} error"}
            data = await resp.json()

    # Əsas məlumatları çıxar
    containers = data.get("Containers", [])
    if not containers:
        return {"success": False, "error": "No container data found."}

    events = containers[0].get("Events", [])
    etd_pol = next((e["EventDate"] for e in events if e["EventName"] == "Export Loaded"), "")
    eta_pod = next((e["EventDate"] for e in events if "Discharged" in e["EventName"]), "")
    feeder  = next((e.get("VesselName", "") for e in events), "")

    return {
        "success": True,
        "etd_pol": etd_pol,
        "eta_transshipment": "",
        "etd_transshipment": "",
        "feeder": feeder,
        "eta_pod": eta_pod
    }
