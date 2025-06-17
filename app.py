from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable
from youtube_transcript_api._errors import NoTranscriptFound
from youtube_transcript_api._proxy import GenericProxyConfig

import youtube_transcript_api
print("✅ Running local version from:", youtube_transcript_api.__file__)

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id parameter"}), 400

    # Optional: set up a proxy to bypass region/IP blocks
    proxy_config = GenericProxyConfig(
        proxy_url="http://scraperapi:kezvt8im3kx8ak7ywwvk@proxy.scraperapi.com:8001"  # Replace with your proxy credentials
    )

    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            proxies=proxy_config.get_next_proxy()
        )
        return jsonify({"transcript": transcript})

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except VideoUnavailable:
        return jsonify({"error": "Video is unavailable"}), 404
    except NoTranscriptFound:
        return jsonify({"error": "Transcript not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def health_check():
    return "YouTube Transcript API is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
