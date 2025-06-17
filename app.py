from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from youtube_transcript_api.proxy import GenericProxyConfig
import random
import re

app = Flask(__name__)

# ✅ Free HTTP proxies to rotate through
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

# ✅ Helper: Extract video ID from full URL or raw ID
def extract_video_id(input_str):
    if not input_str:
        return None
    # Matches ?v=VIDEO_ID or youtu.be/VIDEO_ID
    match = re.search(r"(?:v=|youtu\.be/)([A-Za-z0-9_-]{11})", input_str)
    if match:
        return match.group(1)
    # Accept raw 11-char video IDs directly
    if len(input_str) == 11:
        return input_str
    return None

@app.route("/transcript", methods=["GET"])
def get_transcript():
    # Accept either video_id or full url
    raw_input = request.args.get("video_id") or request.args.get("url")
    video_id = extract_video_id(raw_input)

    if not video_id:
        return jsonify({"error": "Missing or invalid video ID or URL"}), 400

    random.shuffle(PROXY_LIST)  # Shuffle the proxies on each request

    for proxy_url in PROXY_LIST:
        try:
            proxy_config = GenericProxyConfig(proxies=[proxy_url], proxy_timeout=10)
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)
            return jsonify(transcript)
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable):
            return jsonify({"error": "Transcript not available for this video"}), 404
        except Exception as e:
            # Try next proxy if this one fails
            continue

    # All proxies failed
    return jsonify({"error": "All proxies failed or were blocked by YouTube"}), 502

# For local testing
if __name__ == "__main__":
    app.run(debug=True)
