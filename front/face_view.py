import datetime
import time
import json
import os
from hashlib import sha256

import requests
from flask import Flask, render_template, redirect, request, make_response, url_for

# New instance app
app = Flask(__name__)

# Node in the blockchain
NODE_ADDRESS = "http://127.0.0.1:8000"

@app.route('/')
def index():
  """username = request.cookies.get('UserFB')

  if not username:
    return render_template(
      'login.html',
      message='Please enter your credentials'
    )

  else:
    posts = fetch_posts()
    return render_template(
      'feed.html',
      user=username,
      posts=posts,
      readable_time=timestamp_to_string
    )"""
  return render_template(
    'feed.html',
    user='Manu',
    posts=[
      {
        'author': "Emma",
        'content': "some content",
        'timestamp': time.time()
      },
      {
        'author': "Manu",
        'content': "Another some content",
        'timestamp': time.time()
      },
      {
        'author': "Emmanuel",
        'content': "Another other some content",
        'timestamp': time.time()
      }
    ],
    readable_time=timestamp_to_string
  )

@app.route('/register')
def register_user():
  return render_template(
    'register.html',
    message='Please enter your info'
  )

@app.route('/login', methods=['POST'])
def login_user():
  node_endpoint = f"{NODE_ADDRESS}/loginUser"
  hash_pass = sha256(request.form['userPass'].encode()).hexdigest()
  username = request.form['userName']

  response = requests.post(
    node_endpoint,
    headers={'Content-Type': "application/json"},
    json={
      'user': username,
      'pass': hash_pass,
      'type': 'login'
    }
  )

  if response.status_code == 200:
    posts = fetch_posts()
    resp = make_response(render_template(
      'feed.html',
      user=username,
      posts=posts,
      readable_time=timestamp_to_string
    ))
    resp.set_cookie('UserFB', username)
    return resp
  
  elif response.status_code == 400:
    return render_template(
      'login.html',
      message='Wrong credentials. Try again!'
    )

  elif response.status_code == 404:
    return render_template(
      'register.html',
      message='User not found. Please register'
    )

@app.route('/registerNew', methods=['POST'])
def register_new_user():
  node_endpoint = f"{NODE_ADDRESS}/loginUser"
  hash_pass = sha256(request.form['colPassword'].encode()).hexdigest()
  username = request.form['colUsername']

  response = requests.post(
    node_endpoint,
    headers={'Content-Type': "application/json"},
    json={
      'user': username,
      'pass': hash_pass,
      'type': 'register'
    }
  )

  if response.status_code == 200:
    return render_template(
      'login.html',
      message='Registered successfully. Please login!'
    )
    
@app.route('/submit', methods=['POST'])
def submit_textarea():
    post_content = request.form.get("textarea1")
    author = request.cookies.get('UserFB')

    post_object = {
      'author': author,
      'content': post_content,
    }

    # Submit a transaction
    new_txn_address = f"{NODE_ADDRESS}/new_transaction"

    requests.post(
        new_txn_address,
        json=post_object,
        headers={'Content-type': 'application/json'}
    )

    return redirect('/')

def fetch_posts():
  chain_endpoint = f"{NODE_ADDRESS}/chain"
  response = requests.get(chain_endpoint)

  if response.status_code == 200:
    content = []
    chain = json.loads(response.content)

    for block in chain["chain"]:
      for txn in block["transactions"]:
        content.append(txn)

    return sorted(
      content,
      key=lambda k: k['timestamp'],
      reverse=True
    )

def timestamp_to_string(epoch_time):
  return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')