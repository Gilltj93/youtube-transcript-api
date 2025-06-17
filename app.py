from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound,
)

# Optional proxy config — uncomment and replace if needed
# from youtube_transcript_api._proxy import GenericProxyConfig
# proxy_config = GenericProxyConfig(
#     proxies=["http://your-proxy.com:port"],  # Replace with a working proxy or pool
#     number_of_retries=3
# )

app = Flask(__name__)

@app.route('/')
def index():
    return "YouTube Transcript API is live!"

@app.route('/upload_transcript', methods=['POST'])
def upload_transcript():
    data = request.get_json()
    video_id = data.get('video_id')

    if not video_id:
        return jsonify({'error': 'Missing video_id'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)  # Use this line if proxy needed
        return jsonify({
            'video_id': video_id,
            'lines': len(transcript),
            'transcript': transcript
        })
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except VideoUnavailable:
        return jsonify({"error": "Video is unavailable"}), 404
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get("video_id")

    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        # transcript = YouTubeTranscriptApi.get_transcript(video_id, proxy=proxy_config)  # Use this line if proxy needed
        return jsonify({
            'video_id': video_id,
            'lines': len(transcript),
            'transcript': transcript
        })
    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video"}), 403
    except VideoUnavailable:
        return jsonify({"error": "Video is unavailable"}), 404
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
