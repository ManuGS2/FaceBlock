import time
import json

from flask import Flask, request
import requests
import redis

from Blockchain import Blockchain
from Block import Block


app = Flask(__name__)

blockchain = Blockchain()
blockchain.create_genesis_block()

# Opening connection pool to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

@app.route("/new_transaction", methods=["POST"])
def new_transaction():
    txn_data = request.get_json()
    required_fields = ["author", "content"]

    if all(not txn_data.get(field) for field in required_fields):
        return "Invalid transaction data", 404

    txn_data["timestamp"] = time.time()
    blockchain.add_new_transaction(txn_data)

    return "Transaction added", 201


@app.route("/chain", methods=["GET"])
def get_chain():
    chain_data = [block.__dict__ for block in blockchain.chain]
    peers = [peer.decode("ASCII") for peer in r.smembers("peers")]

    return json.dumps({
        "length": len(chain_data), 
        "chain": chain_data, 
        "peers": peers
    })
    
@app.route("/mine", methods=["GET"])
def mine_txns():
    result = blockchain.mine()
    
    if not result:
        return "Nothing to mine", 200
    
    else:
        chain_length = len(blockchain.chain)
        consensus()

        if chain_length == len(blockchain.chain):
            announce_new_block(blockchain.last_block)

        return "Block #{} is mined.".format(blockchain.last_block.index)


@app.route("/pending_txn", methods=["GET"])
def get_pending_txns():
    return json.dumps(blockchain.unconfirmed_transactions), 200


@app.route("/register_node", methods=["POST"])
def register_new_peer():
    node_address = request.get_json()["node_address"]
    if not node_address:
        return "Invalid node address", 400

    r.sadd("peers", node_address)

    return get_chain()


@app.route("/register_with", methods=["POST"])
def register_with_existing_node():
    node_address = request.get_json().get("node_address")

    if not node_address:
        return "Invalid node address", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    response = requests.post(
        node_address + "/register_node", 
        data=json.dumps(data),  
        headers=headers
    )

    if response.status_code == 200:
        global blockchain
        
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)

        r.sadd("peers", *response.json()['peers'])
        r.sadd("peers", node_address+"/")
        r.srem("peers", request.host_url)

        return "Registration successful", 200

    else:
        return response.content, response.status_code


@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    block_data = request.get_json()
    block = Block(
        block_data["index"],
        block_data["transactions"],
        block_data["timestamp"],
        block_data["previous_hash"],
        block_data["nonce"]
    )

    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


def announce_new_block(block):
    for peer in r.smembers("peers"):
        requests.post(
            "{}add_block".format(peer.decode("ASCII")), 
            data=json.dumps(block.__dict__, sort_keys=True),
            headers={'Content-Type': "application/json"}
        )


def create_chain_from_dump(chain_dump):
    new_blockchain = Blockchain()
    new_blockchain.create_genesis_block()

    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            continue  # Skip gen block

        block = Block(
            block_data["index"],
            block_data["transactions"],
            block_data["timestamp"],
            block_data["previous_hash"],
            block_data["nonce"]
        )
        proof = block_data['hash']
        added = new_blockchain.add_block(block, proof)

        if not added:
            raise Exception("The chain dump is tampered!!")
            
    return new_blockchain


def consensus():
    global blockchain
    
    longest_chain = None
    current_len = len(blockchain.chain)

    for node in r.smembers("peers"):
        response = requests.get("{}chain".format(node.decode("ASCII")))
        length = response.json().get("length")
        chain = response.json().get("chain")

        if length > current_len and blockchain.validate_chain(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False
