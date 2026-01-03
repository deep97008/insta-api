from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, re

app = Flask(__name__)
CORS(app)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def extract_video(url):
    try:
        api_url = url.rstrip("/") + "/?__a=1&__d=dis"
        r = requests.get(api_url, headers=HEADERS, timeout=10)
        data = r.json()
        media = data["graphql"]["shortcode_media"]

        if media["is_video"]:
            return media["video_url"]
    except:
        pass

    html = requests.get(url, headers=HEADERS).text
    match = re.search(r'"video_url":"([^"]+)"', html)
    if match:
        return match.group(1).replace("\\/", "/")

    return None

@app.route("/api/download", methods=["POST"])
def download():
    url = request.json.get("url")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    video = extract_video(url)

    if not video:
        return jsonify({"error": "Video not found or private"}), 404

    return jsonify({
        "success": True,
        "download_url": video
    })
