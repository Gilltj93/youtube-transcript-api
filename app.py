from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._utils import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api.proxy import GenericProxyConfig

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    # Use a public proxy from ProxyScrape (replace with your real working proxy)
    proxy = GenericProxyConfig(
        https='http://your-proxy-ip:your-port'
    )

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy)
        formatter = JSONFormatter()
        return formatter.format_transcript(transcript)
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
