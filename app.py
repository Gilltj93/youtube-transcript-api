from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    video_id = data.get("videoId")

    if not video_id:
        return jsonify({"error": "Missing videoId"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({"transcript": transcript})

    except VideoUnavailable:
        return jsonify({"error": "Video unavailable"}), 404
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found"}), 404
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

@app.route('/')
def home():
    return "Transcript API is running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
