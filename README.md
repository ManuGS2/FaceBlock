# FaceBlock
Blockchain based social network that allows people to interact each others
This application is based on this repo [Blockchain](https://github.com/ManuGS2/Blockchain)

## Purpose
Main purpose of this *dapp* is to allow users whithin the network post messages into the app.

## Pow algorithm
The proof of work for this blockchain is based on the hash of each Block as well as a sentimental analysis about the comment posted.
For this app each block contains a single transaction. Each transaction is defined by the next info:
* Author
* Content
* Timestamp

Each block is defined by the next:
* Index
* Transaction
* Timestamp
* Previous block (defined by its hash)

Algorithm consists in look for such a *Nonce* value that when calculating hash function for that block, result begin with "00".
Sentimental analysis consists in detect spam or bad words in the comment 

## Consensus algorithm
The consensus for this blockchain is as simple as just select the larger chain as the valid chain

## Running
It's possible to run this *Dapp* (Descentralized Application) by two ways

This tutorial is assuming you have python installed and running on a Linux-based OS

### Locally 

If you go by this way, I suggest you to use virtual environment

  1. Clone this repo
  
  `git clone https://github.com/ManuGS2/Blockchain.git`

  2. Go to the folder

  `cd Blockchain`

  3. Install the dependencies

  ```
  pip install -r server/requirements.txt
  pip install -r front/requirements.txt
  ```

  4. Run the node server for connecting to blockchain network with the next commands

  ```
  export FLASK_APP=server/blockchain_api.py
  flask run --port 8000
  ```
  
  5. Run the web application with the next commands

  ```
  export FLASK_APP=front/views.py
  flask run --port 5000
  ```

  6. If you want to run more nodes, just follow the samen in step 4 but changing the port

  ```
  export FLASK_APP=server/blockchain_api.py
  flask run --port 8001
  ```

Your web application will be running on http://127.0.0.1:5000/

**NOTE: for each instance of the web app or node server it's necessary to open new console window**

### Docker compose

If you go by this way, you need to have [docker](https://docs.docker.com/engine/) installed in your machine  as well as [docker-compose](https://docs.docker.com/compose/) in onder to run this *Dapp* in containers.

If you don't have docker neither docker-compose installed follow the instructions from official page.
  * [docker](https://docs.docker.com/engine/install/ubuntu/)
  * [docker-compose](https://docs.docker.com/compose/install/)

Once you have docker compose installed follow the next steps

  1. Clone this repo
  
  `git clone https://github.com/ManuGS2/Blockchain.git`

  2. Go to the folder

  `cd Blockchain`

  3. Build, crate and run the containers

  `docker-compose up --build`

  This last command will run the services defined in docker-compose.yml file. You can modify it in order to create more nodes or instances

  By default this will create 1 web app instance, 1 node and 1 redis instance.

Your web application will be running on http://127.0.0.1:5000/

