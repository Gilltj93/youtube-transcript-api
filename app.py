from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is Live!'

@app.route('/ip')
def get_ip():
    return jsonify({'ip': request.remote_addr})

@app.route('/transcript')
def transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'video_id is required'}), 400
    # Example stub
    return jsonify({'video_id': video_id, 'transcript': 'This is a fake transcript for testing.'})

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
