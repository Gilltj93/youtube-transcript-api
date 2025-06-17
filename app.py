import requests

@app.route('/ip')
def get_ip():
    ip = requests.get("https://api.ipify.org").text
    return jsonify({"server_ip": ip})
