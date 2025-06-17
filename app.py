from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import requests

app = Flask(__name__)

@app.route("/myip")
def get_ip():
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@app.route("/transcript")
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    # Fetch proxy list from ProxyScrape API
    proxy_api_url = "https://proxy.scrapeops.io/v1/proxies?protocol=http&anonymity=elite&country=US"
    try:
        proxy_response = requests.get(proxy_api_url)
        proxy_data = proxy_response.json().get("proxies", [])
    except Exception as e:
        return jsonify({"error": f"Failed to fetch proxies: {str(e)}"}), 500

    # Try each proxy until one works
    for proxy in proxy_data:
        proxy_url = f"http://{proxy['ip']}:{proxy['port']}"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxies)
            return jsonify(transcript)
        except Exception as e:
            print(f"Failed with proxy {proxy_url}: {str(e)}")
            continue

    return jsonify({"error": "All proxies failed or no transcript found"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
