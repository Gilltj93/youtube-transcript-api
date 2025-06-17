from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return 'YouTube Transcript API is live!'

@app.route('/upload_transcript', methods=['POST'])
def upload_transcript():
    data = request.get_json()

    video_id = data.get("video_id")
    transcript = data.get("transcript")

    if not video_id or not transcript:
        return jsonify({"error": "Missing video_id or transcript"}), 400

    # Here, you'd normally process or store it
    return jsonify({"message": f"Transcript for {video_id} received.", "lines": len(transcript)})
