import datetime
import json
import os
from hashlib import sha256

import requests
from flask import Flask, render_template, redirect, request

# New instance app
app = Flask(__name__)

# Node in the blockchain
NODE_ADDRESS = "http://127.0.0.1:8000"

@app.route('/')
def index():
  app.logger.debug("Variable mia")
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def login_user():
  node_endpoint = f"{NODE_ADDRESS}/validate_user"
  hash_pass = sha256(request.form['userPass'].encode()).hexdigest()
  username = request.form['userName']

  response = requests.post(
    node_endpoint,
    headers={'Content-Type': "application/json"},
    data={
      'user': username,
      'pass': hash_pass
    }
  )

  if response.status_code == 200:
    return render_template('login.html')
  
  elif response.status_code == 404:
    # User not fund
    return redirect('/')


@app.route('/register')
def register_user():
  return render_template('register.html')

@app.route('/register_new')
def register__new_user():
  node_endpoint = f"{NODE_ADDRESS}/validate_user"
  hash_pass = sha256(request.form['userPass'].encode()).hexdigest()
  username = request.form['userName']

  response = requests.post(
    node_endpoint,
    headers={'Content-Type': "application/json"},
    data={
      'user': username,
      'pass': hash_pass
    }
  )

  if response.status_code == 200:
    return render_template('login.html')
  
  elif response.status_code == 404:
    # User not fund
    return redirect('/')
