import datetime
import json
import os

import requests
from flask import Flask, render_template, redirect, request

# New instance app
app = Flask(__name__)

# Node in the blockchain network that our application will communicate with
# to fetch and add data.
NODE_ADDRESS = "http://127.0.0.1:8000"

posts = []

def fetch_posts():
    get_chain_endpoint = "{}/chain".format(NODE_ADDRESS)
    response = requests.get(get_chain_endpoint)

    if response.status_code == 200:
        content = []
        chain = json.loads(response.content)

        for block in chain["chain"]:
            for txn in block["transactions"]:
                txn["index"] = block["index"]
                txn["hash"] = block["previous_hash"]
                content.append(txn)

        global posts
        posts = sorted(
            content,
            key=lambda k: k['timestamp'],
            reverse=True
        )


@app.route('/')
def index():
    app.logger.debug("Var %s", os.environ.get("NODE_VAR"))
    fetch_posts()

    return render_template(
        'index.html',
        title='YourNet: Decentralized '
        'content sharing',
        posts=posts,
        node_address=NODE_ADDRESS,
        readable_time=timestamp_to_string
    )


@app.route('/submit', methods=['POST'])
def submit_textarea():
    """
    Endpoint to create a new transaction via our application.
    """
    post_content = request.form["content"]
    author = request.form["author"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    # Submit a transaction
    new_txn_address = "{}/new_transaction".format(NODE_ADDRESS)

    requests.post(
        new_txn_address,
        json=post_object,
        headers={'Content-type': 'application/json'}
    )

    return redirect('/')


def timestamp_to_string(epoch_time):
    return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')