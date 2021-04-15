# Create a blockchain

Basic blockchain implemented from scratch. This project is basically a Flask server that will allow us to interact
with the blockchain through the following endpoints:

- Getting the blockchain: ```/get_chain```.
- Mining a block: ```/mine_block```.
- Check if the current blockchain is valid: ```/is_valid```.

## Dependencies

The only external dependency we need to install in order to run the project is
<a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a>, specifically the version 1.1.2.

## Usage

Just run the ```blockchain.py``` script with your favourite IDE (I recommend using
<a href="https://www.jetbrains.com/es-es/pycharm/">PyCharm</a>), and the Flask server will be ready to go! It runs at
http://localhost:5000.

After that, you can use <a href="https://www.postman.com/">Postman</a> to send requests to the blockchain. For example,
try sending a GET request to http://localhost:5000/get_chain, and you will see that the current blockchain only have
one block: the genesis block.

Then you can send some GET requests to http://localhost:5000/mine_block so that some blocks
are mined and added to the blockchain.

Finally, try sending another GET request to http://localhost:5000/is_valid to verify that the blockchain is actually
valid and there's no problem with it.
