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
from urllib.parse import urlparse


# Part 1 - Building a Blockchain

# Implementing the Blockchain class
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4
        self.transactions = []
        self.nodes = set()
        self.mine_block()

    def __create_block(self, block):
        self.chain.append(block)
        self.transactions = [{
            'sender': None,
            'receiver': 'David',
            'amount': 10
        }]

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

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response_1 = requests.get(f'http://{node}/get_chain')
            response_2 = requests.get(f'http://{node}/is_valid')
            if response_1.status_code == 200 and response_2.status_code == 200:
                data_1 = response_1.json()
                data_2 = response_2.json()
                length = data_1['length']
                chain = data_1['chain']
                valid_chain = data_2['is_valid']
                if length > max_length and valid_chain:
                    max_length = length
                    longest_chain = chain
        if longest_chain:
            self.chain = longest_chain
            return True
        return False

    def add_transaction(self, sender, receiver, amount):
        self.transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        return len(self.chain)

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)


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
        'previous_hash': block['previous_hash'],
        'transactions': block['transactions']
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


# Adding a new transaction to the Blockchain
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    data = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']
    if not all(key in data for key in transaction_keys):
        response = {'message': 'Some elements of the transaction are missing'}
        return jsonify(response), 400
    index = blockchain.add_transaction(data['sender'], data['receiver'], data['amount'])
    response = {'message': f'This transaction will be added to Block {index}'}
    return jsonify(response), 201


# Part 3 - Decentralizing our Blockchain

# Connecting new nodes
@app.route('/connect_node', methods=['POST'])
def connect_node():
    data = request.get_json()
    nodes = data.get('nodes')
    if nodes is None:
        response = {'message': 'There is no node'}
        return jsonify(response), 400
    for node in nodes:
        blockchain.add_node(node)
    response = {
        'message': 'All the nodes are now connected',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


# Replacing the chain by the longest chain if needed
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    chain_is_replaced = blockchain.replace_chain()
    response = {
        'message': 'Chain has been replaced by the longest one',
        'new_chain': blockchain.chain
    } if chain_is_replaced is True else {
        'message': 'The chain is all good, no need to replace it',
        'actual_chain': blockchain.chain
    }
    return jsonify(response), 200


# Running the app
port = 5001
app.run(host='0.0.0.0', port=port)
