from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._utils import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.proxy import GenericProxyConfig
import random

app = Flask(__name__)

# List of working HTTP proxies (from ProxyScrape)
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
    "http://156.242.36.156:3129"
]

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    # Try each proxy until one works
    for proxy_url in random.sample(PROXIES, len(PROXIES)):
        proxy = GenericProxyConfig(http=proxy_url)
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
            formatter = JSONFormatter()
            return formatter.format_transcript(transcript)
        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            return jsonify({"error": str(e)}), 404
        except Exception as e:
            continue  # Try next proxy

    return jsonify({"error": "All proxies failed"}), 500

if __name__ == "__main__":
    app.run(debug=True)
