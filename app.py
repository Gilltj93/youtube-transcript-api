from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._proxy import GenericProxyConfig
from youtube_transcript_api.formatters import JSONFormatter

app = Flask(__name__)

# Paste your ProxyScrape HTTP proxies here
proxies = [
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

proxy_config = GenericProxyConfig(proxies)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)
        formatter = JSONFormatter()
        return formatter.format_transcript(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
