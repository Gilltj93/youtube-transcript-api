from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._proxy import GenericProxyConfig
from youtube_transcript_api.formatters import JSONFormatter

app = Flask(__name__)

# Set up proxy rotation (you can add more proxies here)
proxies = [
    "http://scraperapi:<kezvt8im3kx8ak7ywwvk>@proxy-server.scraperapi.com:8001"
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
