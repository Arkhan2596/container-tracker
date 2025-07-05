from flask import Flask, request, Response
import requests
from lxml import html

app = Flask(__name__)

@app.route('/')
def index():
    return 'MSC HTML Debug API is running.'

@app.route('/debug', methods=['POST'])
def debug():
    """
    POST JSON: { "bl_number": "MEDUJB511593" }
    Cavab: səhifənin HTML-i statik olaraq geri qaytarır, 
    həmçinin konsola pars edilmiş hissəni log edəcək.
    """
    data = request.json or {}
    bl = data.get("bl_number", "").strip()
    if not bl:
        return Response("`bl_number` tələb olunur", status=400)

    # 1) Statik səhifəni çəkmək
    #    (JavaScript olmasa, bizə lazım gələn məlumat burada deyil)
    url = "https://www.msc.com/en/tools/track-a-shipment"  
    resp = requests.get(url, timeout=15)
    raw_html = resp.text

    # 2) `bl` göndərilən POST sorğusunu da təqlid edək
    api_url = "https://www.msc.com/api/feature/tools/TrackingInfo"
    api_payload = {
        "SearchBy": "B",
        "Numbers": [bl]
    }
    api_headers = {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://www.msc.com",
        "Referer": "https://www.msc.com/",
    }
    api_resp = requests.post(api_url, json=api_payload, headers=api_headers, timeout=15)

    # 3) LXML ilə pars edək
    tree = html.fromstring(raw_html)
    # Məsələn: səhifə başlığını götürək
    title = tree.xpath('//title/text()')
    print("PAGE <title>:", title)

    # 4) JSON cavabı da konsola yaz
    print("API raw JSON snippet:", api_resp.status_code, api_resp.text[:500])

    # 5) Cavab kimi bütün statik HTML qaytaraq
    return Response(raw_html, mimetype="text/html")
