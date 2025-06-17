from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "YouTube Transcript API with Cookie Support is running!"

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400

    # YouTube API URL for transcript
    url = f"https://www.youtube.com/api/timedtext?lang=en&v={video_id}"

    # Set your actual cookies here
    cookies = {
        "HSID": "AlXdqFyvxX6WX7oaf",
        "SSID": "A7O0DLhE3B3oJjQbb",
        "APISID": "aBYkNaZWL9b_bTt8/AUKJ8bXUW2cUzEXN_",
        "SAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
        "__Secure-1PAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
        "__Secure-3PAPISID": "Omkh9UqVWUyzWyaL/ABCEPiY6d_GKFGsNU",
        "SID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0NnNHESihn4EmTkMGBcw_tAACgYKAdgSARUSFQHGX2MimJSXmkT1BzfIBtVcfl18ZBoVAUF8yKo7_vjwMkflmcaHZbNC-GY90076",
        "__Secure-1PSID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0P22H-6Kqh_qXdI8ASxTRPAACgYKAX4SARUSFQHGX2MiqalMGcovJwhQuTThGQZpQBoVAUF8yKplpZ3cQ57iguQeK9SaNKDq0076",
        "__Secure-3PSID": "g.a000yAhIKn58CppcZu-TceFdg4O7HQL9gR6tsVdMLjFPoq9o2Jh0oPlTqbR9cMrTOxlA2jdJ9gACgYKAVUSARUSFQHGX2MiUBheKVLH4f4TSS6N63n5ExoVAUF8yKqI75hmw_HVHnxuifx-M5lg0076",
        # Add more cookies if needed
    }

    try:
        headers = {
            "User-Agent": "Mozilla/5.0",
        }
        response = requests.get(url, cookies=cookies, headers=headers)
        response.raise_for_status()

        return jsonify({
            "video_id": video_id,
            "transcript_xml": response.text
        })

    except requests.exceptions.HTTPError as e:
        return jsonify({'error': f'HTTP error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
