from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api._proxy import GenericProxyConfig
import random

app = Flask(__name__)

PROXIES = [
    "http://156.228.125.161:3129",
    "http://156.228.102.99:3129",
    "http://154.213.166.248:3129",
    "http://156.228.119.178:3129",
    "http://154.213.160.143:3129",
    "http://154.213.167.98:3129",
    "http://154.214.1.10:3129",
    "http://156.228.105.58:3129",
    "http://156.228.93.61:3129",
    "http://156.242.36.156:3129",
]

@app.route("/")
def index():
    return jsonify({
        "message": "YouTube Transcript API is live",
        "usage": "/transcript?video_id=YOUR_VIDEO_ID"
    })

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing 'video_id' parameter"}), 400

    proxy_url = random.choice(PROXIES)
    proxy_config = GenericProxyConfig(proxy_url=proxy_url)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)
        return jsonify(transcript)
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
