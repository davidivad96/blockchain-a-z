# Module 2 - Create a Cryptocurrency

# To be installed:
# Flask==1.1.2
# Postman HTTP Client
# requests==2.25.1

# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify, request
import requests
from uuid import uuid4
from urllib.parse import urlparse


# Part 1 - Building a Blockchain

# Implementing the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.transactions = []
        self.mine_block()

    def __create_block(self, block):
        self.chain.append(block)
        self.transactions = []

    def __proof_of_work(self):
        nonce = 0
        nonce_found = False
        block = {
            'index': len(self.chain),
            'previous_hash': self.__get_last_block()['hash'] if len(self.chain) > 0 else '0' * 64,
            'transactions': self.transactions
        }
        while nonce_found is False:
            block['timestamp'] = str(datetime.datetime.now())
            block['nonce'] = nonce
            hashed_block = self.__hash_block(block)
            if hashed_block[:self.difficulty] == '0' * self.difficulty:
                block['hash'] = hashed_block
                nonce_found = True
            else:
                nonce = (nonce + 1) % (2 ** 32)
        return block

    def __get_last_block(self):
        return self.chain[-1]

    @staticmethod
    def __hash_block(block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def mine_block(self):
        block = self.__proof_of_work()
        self.__create_block(block)
        return block

    def is_chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            block = self.chain[block_index]
            hashed_block = self.__hash_block({key: block[key] for key in block if key != 'hash'})
            # Conditions to verify that the chain is valid
            hash_is_not_correct = block['hash'] != hashed_block
            hash_leading_zeros_is_not_correct = hashed_block[:self.difficulty] != '0' * self.difficulty
            linking_is_not_good = block['previous_hash'] != previous_block['hash']
            if hash_is_not_correct or hash_leading_zeros_is_not_correct or linking_is_not_good:
                return False
            previous_block = block
            block_index += 1
        return True

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return len(self.chain)


# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)

# Instantiating the Blockchain
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    block = blockchain.mine_block()
    response = {
        'message': 'Congratulations, you just mined a block!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'nonce': block['nonce'],
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


# Part 3 - Decentralizing our Blockchain


# Running the app
app.run(host='0.0.0.0', port=5000)
