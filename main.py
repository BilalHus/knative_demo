import json
import os

import requests
from flask import Flask, request

from cloudevents.http import from_http

app = Flask(__name__)


@app.route("/", methods=["POST"])
def home():
    event = from_http(request.headers, request.get_data())
    print(
        f"Found {event['id']} from {event['source']} with type "
        f"{event['type']} and specversion {event['specversion']}"
    )

    url = os.getenv("MOCK_URL")
    body = {"key": event['id']}


    response = requests.post(url,
                             data=json.dumps(body),
                             headers={"Content-Type": "application/json"})

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    return "", 204


if __name__ == "__main__":
    app.run(port=3000)
