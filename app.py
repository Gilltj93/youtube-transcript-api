from flask import Flask, request, jsonify
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    url = f"https://www.youtube.com/watch?v={video_id}"
    
    try:
        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitlesformat": "vtt",
            "subtitleslangs": ["en"],
            "outtmpl": f"{video_id}.%(ext)s",
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        vtt_file = f"{video_id}.en.vtt"
        if not os.path.exists(vtt_file):
            return jsonify({"error": "Transcript not available"}), 404

        with open(vtt_file, "r", encoding="utf-8") as f:
            content = f.read()

        os.remove(vtt_file)

        return jsonify({"transcript_vtt": content})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
