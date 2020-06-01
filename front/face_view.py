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
  return render_template(
    'login.html',
    message='Please enter your credentials'
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
    return "Logged in succesfully"
  
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
    