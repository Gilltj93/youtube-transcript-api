from youtube_transcript_api import YouTubeTranscriptApi
import requests

video_id = "dQw4w9WgXcQ"  # Replace with your desired YouTube video ID
api_url = "https://your-service-name.onrender.com/upload_transcript"  # Replace with your actual Render app URL

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    response = requests.post(api_url, json={
        "video_id": video_id,
        "transcript": transcript
    })

    print("Upload response:", response.text)

except Exception as e:
    print("Error:", str(e))
