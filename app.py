from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api import GenericProxyConfig
from youtube_transcript_api.formatters import JSONFormatter

app = Flask(__name__)

# Set up proxies to bypass Google blocking
proxy_config = GenericProxyConfig(
    proxies=[
        "http://scraperapi:kezvt8im3kx8ak7ywwvk@scraperapi.com:8001",
        "http://user:password@156.228.125.161:3129",
        "http://user:password@156.228.102.99:3129"
    ],
    proxy_selection_method="round_robin",
)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy_config=proxy_config)
        return jsonify(transcript)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def index():
    return "YouTube Transcript API with Proxy is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
