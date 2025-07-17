from flask import Flask, request, jsonify
from flask_cors import CORS

from bid_resolution_service import resolve_bids_poc

app = Flask(__name__)
CORS(app)


@app.route("/greet", methods=['POST'])
def greet():
    data = request.get_json()
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    message = f"Hello {first_name} {last_name}!"
    return jsonify({"message": message})


@app.route("/resolvebid", methods=['POST'])
def bid_resolution():
    data = request.get_json()

    return resolve_bids_poc(data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
