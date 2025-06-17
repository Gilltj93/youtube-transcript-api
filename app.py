from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    VideoUnavailable,
    NoTranscriptFound
)
import json

app = Flask(__name__)

# Raw cookie string you copied from your browser
raw_cookie_string = """
HSID=AlXdqFyvxX6WX7oaf; SSID=A7O0DLhE3B3oJjQbb; APISID=aBYkNaZWL9b_bTt8/AUKJ8bXUW2cUzEXN_; SAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; __Secure-1PAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; __Secure-3PAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; SID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0NnNHESihn4EmTkMGBcw_tAACgYKAdgSARUSFQHGX2MimJSXmkT1BzfIBtVcfl18ZBoVAUF8yKo7_vjwMkflmcaHZbNC-GY90076; __Secure-1PSID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0P22H-6Kqh_qXdI8ASxTRPAACgYKAX4SARUSFQHGX2MiqalMGcovJwhQuTThGQZpQBoVAUF8yKplpZ3cQ57iguQeK9SaNKDq0076; __Secure-3PSID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0oPlTqbR9cMrTOxlA2jdJ9gACgYKAVUSARUSFQHGX2MiUBheKVLH4f4TSS6N63n5ExoVAUF8yKqI75hmw_HVHnxuifx-M5lg0076
"""

# Parse the cookie string into a dictionary
def parse_cookie_string(cookie_str):
    cookie_dict = {}
    for part in cookie_str.strip().split("; "):
        if "=" in part:
            key, value = part.split("=", 1)
            cookie_dict[key] = value
    return cookie_dict

cookies = parse_cookie_string(raw_cookie_string)

@app.route('/')
def home():
    return 'YouTube Transcript API with browser cookie support is running!'

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
