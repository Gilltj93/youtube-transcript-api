from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript
)
from youtube_transcript_api._transcript_api import _TranscriptFetcher
import requests

app = Flask(__name__)

# Inject cookies here (important!)
COOKIES = {
    "HSID": "AlXdqFyvxX6WX7oaf",
    "SSID": "A7O0DLhE3B3oJjQbb",
    "APISID": "aBYkNaZWL9b_bTt8/AUKJ8bXUW2cUzEXN_",
    "SAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
    "__Secure-1PAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
    "__Secure-3PAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
    "SID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0NnNHESihn4EmTkMGBcw_tAACgYKAdgSARUSFQHGX2MimJSXmkT1BzfIBtVcfl18ZBoVAUF8yKo7_vjwMkflmcaHZbNC-GY90076",
    "__Secure-1PSID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0P22H-6Kqh_qXdI8ASxTRPAACgYKAX4SARUSFQHGX2MiqalMGcovJwhQuTThGQZpQBoVAUF8yKplpZ3cQ57iguQeK9SaNKDq0076",
    "__Secure-3PSID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0oPlTqbR9cMrTOxlA2jdJ9gACgYKAVUSARUSFQHGX2MiUBheKVLH4f4TSS6N63n5ExoVAUF8yKqI75hmw_HVHnxuifx-M5lg0076"
}

# Custom fetcher to inject cookies
class CustomFetcher(_TranscriptFetcher):
    def _make_request(self, url: str):
        response = requests.get(url, cookies=COOKIES, headers={"User-Agent": "Mozilla/5.0"})
        if not response.ok:
            raise CouldNotRetrieveTranscript(url)
        return response.text

# Replace the default fetcher with the custom one
YouTubeTranscriptApi._YouTubeTranscriptApi__transcript_fetcher = CustomFetcher()

@app.route('/')
def home():
    return 'YouTube Transcript API with Cookie Support is running!'

@app.route('/transcript')
def transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return jsonify(transcript)
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except VideoUnavailable:
        return jsonify({'error': 'Video is unavailable'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
