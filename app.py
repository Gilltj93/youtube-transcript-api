from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/ip')
def get_ip():
    ip = requests.get("https://api.ipify.org").text
    return jsonify({"server_ip": ip})
