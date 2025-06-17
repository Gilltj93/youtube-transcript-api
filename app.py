from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from youtube_transcript_api.proxy import GenericProxyConfig
import random

app = Flask(__name__)

# ✅ Free HTTP proxies from your screenshot
PROXY_LIST = [
    "http://156.228.125.161:3129",
    "http://156.228.102.99:3129",
    "http://154.213.166.248:3129",
    "http://156.228.119.178:3129",
    "http://154.213.160.143:3129",
    "http://154.213.167.98:3129",
    "http://154.214.1.10:3129",
    "http://156.228.105.58:3129",
    "http://156.228.93.61:3129",
    "http://156.242.36.156:3129"
]

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    selected_proxy = random.choice(PROXY_LIST)
    proxy_config = GenericProxyConfig(proxies=[selected_proxy], proxy_timeout=10)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)
        return jsonify(transcript)
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found"}), 404
    except VideoUnavailable:
        return jsonify({"error": "Video is unavailable"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
