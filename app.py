from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/transcript', methods=['POST'])
def get_transcript():
    data = request.get_json()
    video_id = data.get('videoId')

    if not video_id:
        return jsonify({'error': 'Missing videoId'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify({'transcript': transcript})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 404
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)  # <- Render expects open port
