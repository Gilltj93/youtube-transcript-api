from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from youtube_transcript_api._utils import CookieFetcher

app = Flask(__name__)

# ✅ Your full YouTube cookie goes here
YOUTUBE_COOKIE = """
HSID=AlXdqFyvxX6WX7oaf; SSID=A7O0DLhE3B3oJjQbb; APISID=aBYkNaZWL9b_bTt8/AUKJ8bXUW2cUzEXN_; SAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; __Secure-1PAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; __Secure-3PAPISID=Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU; SID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0NnNHESihn4EmTkMGBcw_tAACgYKAdgSARUSFQHGX2MimJSXmkT1BzfIBtVcfl18ZBoVAUF8yKo7_vjwMkflmcaHZbNC-GY90076; __Secure-1PSID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0P22H-6Kqh_qXdI8ASxTRPAACgYKAX4SARUSFQHGX2MiqalMGcovJwhQuTThGQZpQBoVAUF8yKplpZ3cQ57iguQeK9SaNKDq0076; __Secure-3PSID=g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0oPlTqbR9cMrTOxlA2jdJ9gACgYKAVUSARUSFQHGX2MiUBheKVLH4f4TSS6N63n5ExoVAUF8yKqI75hmw_HVHnxuifx-M5lg0076; LOGIN_INFO=AFmmF2swRQIhAKR5etip8W6R9_lInVSkIloqlryYZLLROKkGiJaxx-ceAiBuCc4JM48Ncwa955BtEVglfUBIzfkKbCexoHC5mdofZg:QUQ3MjNmd25XNG5EcVhXRm1yNjlYeGhBMURWMjZ3RVh4SG1FeW5mTlllWTQ5QnR5RlV2U2JOWHkyTzJTdjFPaVprdHBVUGlzUVlEWkJpRVMxRHJjbHAzbzd0WVpHNkZwX2xrQmdxZnhDTzVGbVB3TGRfNGdiZGdwTTlWSXhfRkdGZmR2bEVhY0Y5c2diOW9wc196M1ViVGs1QmNmbEVWeDdn; YSC=8h784BRfVE4; VISITOR_INFO1_LIVE=vvIweTBXHN4; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgKQ%3D%3D; __Secure-ROLLOUT_TOKEN=CLXkj-vQl72NLhCG5pfF0PaNAxj78cLF0PaNAw%3D%3D; PREF=f6=40000000&tz=America.New_York&f7=100; wide=0; __Secure-1PSIDTS=sidts-CjIB5H03P9KFURBsGxjr06YdE8-V_U1uC4TABK3iBooJJoF8ugcDQX1v61o0wjHARl0bzxAA; __Secure-3PSIDTS=sidts-CjIB5H03P9KFURBsGxjr06YdE8-V_U1uC4TABK3iBooJJoF8ugcDQX1v61o0wjHARl0bzxAA; SIDCC=AKEyXzWE_RsiZ8lzKvRSeOq5XH1E_crjdHL_S4RMJ7Dmj_vxoGRaInuuDYMYmpZduqkR8i4vlw; __Secure-1PSIDCC=AKEyXzWlcDZZ_eqbWDdqU6cC7KRzHd7pIVx4PTtdPKg5lbXoA1j-7k67Ho9bQDF2jHTe46FAtA; __Secure-3PSIDCC=AKEyXzU1q_MBCKQk9ZHe4tCYDl4MJX4uoVmNU3dYx7DOxE8AfULUhDlzhZLT1cM_5-v8OyXjOw
""".strip()

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, cookies=YOUTUBE_COOKIE)
        return jsonify(transcript)
    except VideoUnavailable:
        return jsonify({'error': 'Video unavailable'}), 404
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
