import os

from flask import Flask
from checker.monitor import query_once

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def root():
    query_once()
    return "Hello!"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))