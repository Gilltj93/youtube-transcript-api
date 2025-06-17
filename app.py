from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound
)
import os
import json

app = Flask(__name__)

# Load cookies once on startup
def load_cookies():
    cookies_path = os.path.join(os.path.dirname(__file__), 'cookies.txt')
    if not os.path.exists(cookies_path):
        return {}
    cookies = {}
    with open(cookies_path, 'r') as f:
        for line in f:
            if not line.strip() or line.strip().startswith('#'):
                continue
            parts = line.strip().split('\t')
            if len(parts) >= 7:
                domain, _, path, secure, expiry, name, value = parts
                cookies[name] = value
    return cookies

cookies = load_cookies()

@app.route('/')
def home():
    return 'YouTube Transcript API with Cookie Support is running!'

@app.route('/transcript', methods=['GET'])
def transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=cookies)
        formatter = JSONFormatter()
        json_formatted = formatter.format_transcript(transcript)
        return jsonify(json.loads(json_formatted))

    except VideoUnavailable:
        return jsonify({'error': 'Video is unavailable'}), 404
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        if '429' in str(e):
            return jsonify({'error': 'Too many requests to YouTube (rate limited)'}), 429
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
