# Module 1 - Create a Blockchain

# To be installed:
# Flask==1.1.2
# Postman HTTP Client

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain

# Implementing the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(proof=1)

    def create_block(self, proof):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': self.chain[-1]['hash'] if len(self.chain) > 0 else '0'
        }
        block_hash = self.hash(block)
        block['hash'] = block_hash
        self.chain.append(block)
        return block

    def proof_of_work(self):
        new_proof = 1
        check_proof = False
        previous_proof = self.chain[-1]['proof']
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            previous_block_without_hash = {key: previous_block[key] for key in previous_block if key != 'hash'}
            if block['previous_hash'] != self.hash(previous_block_without_hash):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Instantiating the Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    proof = blockchain.proof_of_work()
    block = blockchain.create_block(proof)
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'hash': block['hash'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid_blockchain = blockchain.is_chain_valid()
    message = 'The chain is valid!' if valid_blockchain is True else 'Oops! It seems that the chain is not valid...'
    response = {
        'is_valid': valid_blockchain,
        'message': message,
    }
    return jsonify(response), 200


# Running the app
app.run(host='0.0.0.0', port=5000)
