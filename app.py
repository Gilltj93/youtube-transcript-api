from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import requests
import random

app = Flask(__name__)

# Optional: use your existing /myip route
@app.route("/myip")
def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@app.route("/transcript")
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    # Get free proxies from ProxyScrape
    proxy_list_url = "https://proxy.scrapeops.io/v1/proxies?protocol=http&anonymity=elite&country=US"
    proxy_response = requests.get(proxy_list_url)
    proxies = proxy_response.json().get("proxies", [])

    for proxy in proxies:
        ip = proxy["ip"]
        port = proxy["port"]
        proxy_url = f"http://{ip}:{port}"

        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies={"http": proxy_url, "https": proxy_url})
            return jsonify(transcript)
        except Exception as e:
            print(f"Proxy failed: {proxy_url} → {str(e)}")
            continue

    return jsonify({"error": "All proxies failed or no transcript found"}), 500
