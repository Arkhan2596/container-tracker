from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

app = Flask(__name__)

def get_searates_tracking(container_number: str, sealine: str = None):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
            ])
        page = browser.new_page()
        url = f"https://www.searates.com/container/tracking/?number={container_number}&type=CT"
        if sealine:
            url += f"&sealine={sealine}"
        page.goto(url)
        try:
            page.wait_for_selector('div.tracking-info', timeout=15000)
        except PlaywrightTimeoutError:
            browser.close()
            return None

        data = page.evaluate('() => window.__INITIAL_STATE__')
        browser.close()
        return data

@app.route('/track', methods=['GET'])
def track():
    container = request.args.get('container')
    if not container:
        return jsonify({'error': 'container param is required'}), 400
    sealine = request.args.get('sealine')

    data = get_searates_tracking(container.strip(), sealine.strip() if sealine else None)
    if not data or 'containerTracking' not in data:
        return jsonify({'error': 'No tracking data found'}), 404

    tracking_info = data['containerTracking'].get('trackingInfo', {})

    events = tracking_info.get('events', [])
    vessel = tracking_info.get('vesselName', '')
    destination = tracking_info.get('destination', '')

    return jsonify({
        'container': container,
        'sealine': sealine,
        'events': events,
        'vessel': vessel,
        'destination': destination
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
