import json

from flask import Flask, request, jsonify


app = Flask(__name__)


@app.route('/', methods=['POST'])
def receive_json():
    # Get JSON data from the POST request
    data = request.get_json()
    print(data)

    with open('data.json', 'w') as f:
        json.dump(data, f)
    # Do something with the data (here we are just printing it)
    print(data)

    # Respond to the client
    return jsonify({'status': 'success', 'data_received': data}), 200


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=80)
