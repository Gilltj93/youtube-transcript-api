from flask import Flask, request
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return "Deploy successful. Go to /myip to get public IP."

@app.route("/myip")
def get_public_ip():
    # Use external service to determine your public IP (Render's outbound IP)
    try:
        ip = requests.get('https://ifconfig.me', timeout=5).text
        return f"Your public IP is: {ip}"
    except Exception as e:
        return f"Error retrieving IP: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
