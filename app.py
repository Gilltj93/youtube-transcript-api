from flask import Flask, request, jsonify
import subprocess
import uuid
import os
from pathlib import Path

app = Flask(__name__)

PROXIES = [
    "http://156.228.125.161:3129",
    "http://156.228.102.99:3129",
    "http://154.213.166.248:3129"
]

@app.route("/transcript", methods=["GET"])
def get_transcript():
    video_id = request.args.get("video_id")
    if not video_id:
        return jsonify({"error": "Missing video_id"}), 400

    video_url = f"https://www.youtube.com/watch?v={video_id}"
    temp_dir = Path(f"/tmp/{uuid.uuid4()}")
    temp_dir.mkdir(parents=True, exist_ok=True)

    proxy = PROXIES[0]  # Rotate if needed
    cmd = [
        "yt-dlp",
        "--proxy", proxy,
        "--write-auto-sub",
        "--sub-lang", "en",
        "--skip-download",
        "-o", str(temp_dir / "%(id)s.%(ext)s"),
        video_url
    ]

    try:
        subprocess.run(cmd, check=True)
        vtt_file = next(temp_dir.glob("*.vtt"))
        with open(vtt_file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        transcript = []
        for line in lines:
            if "-->" not in line and line.strip():
                transcript.append(line.strip())

        return jsonify({"transcript": transcript})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # Clean up temp
        for f in temp_dir.glob("*"):
            f.unlink()
        temp_dir.rmdir()

if __name__ == "__main__":
    app.run(debug=True)
