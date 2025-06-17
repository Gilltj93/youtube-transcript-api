from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
import os

app = Flask(__name__)

# Set your proxy IP here (for example: http://123.456.789.101:8080)
PROXIES = {
    "http": os.environ.get("PROXY_URL"),
    "https": os.environ.get("PROXY_URL")
}

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=PROXIES)
        full_text = " ".join([entry["text"] for entry in transcript])
        return jsonify({"transcript": full_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
