from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound,
    TooManyRequests
)

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is running!'

@app.route('/transcript', methods=['GET'])
def transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    # Optional headers or cookies for future use
    cookies = request.headers.get('Cookie')
    user_agent = request.headers.get('User-Agent')

    try:
        # Optional: Add headers/cookies if you're using a proxy strategy
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({'transcript': transcript})
    
    except VideoUnavailable:
        return jsonify({'error': 'Video is unavailable'}), 404
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except TooManyRequests:
        return jsonify({'error': 'Too many requests to YouTube'}), 429
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
