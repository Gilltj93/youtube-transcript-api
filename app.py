from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._proxy import GenericProxyConfig
from youtube_transcript_api.formatters import JSONFormatter

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is live!', 200

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    try:
        # Replace with your real proxy URL and credentials
        proxy_config = GenericProxyConfig([
            "http://scraperapi:kezvt8im3kx8ak7ywwvk@proxy.scraperapi.com:8001"
        ])

        transcript = YouTubeTranscriptApi.get_transcript(video_id, proxies=proxy_config)
        formatter = JSONFormatter()
        return formatter.format_transcript(transcript), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
