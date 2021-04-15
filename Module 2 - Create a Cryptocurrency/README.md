# Create a cryptocurrency

Starting from the previous module where we implemented a basic blockchain, added transactions logic and
decentralization to create our own cryptocurrency: the Davidcoin. We will have several nodes running at the same
time, each one with its own copy of the blockchain.

## Dependencies

Apart from the already mentioned <a href="https://flask.palletsprojects.com/en/1.1.x/">Flask</a> (version 1.1.2), we
will also need another external dependency: <a href="https://docs.python-requests.org/en/master/">requests</a>,
specifically the version 2.25.1.

## Usage

We will run 3 nodes in this example (you can add more if you want), so we need to run the 3 scripts at the same time:
```davidcoin_node_1.py```, ```davidcoin_node_2.py``` and ```davidcoin_node_3.py```. I recommend using
<a href="https://www.jetbrains.com/es-es/pycharm/">PyCharm</a> to do this because you can add a compound configuration
that will launch the 3 nodes simultaneously. The nodes will run at http://localhost:5001, http://localhost:5002 and
http://localhost:5003, respectively.

Then, we will run the ```synchronizer.py``` script that will be constantly checking the blockchains of all the nodes in
the network and updating them accordingly so that all the system is consistent.

After that, we can play with the blockchain using <a href="https://www.postman.com/">Postman</a>. You still can use the
requests we saw in the previous module: ```/get_chain```, ```/mine_block``` and ```/is_valid```; and there's a new one
that will allow us to add transactions. To do this, just send a POST request to ```/add_transaction``` and send a body
JSON with the keys **sender**, **receiver** and **amount**. The next time a block is mined and added to the blockchain,
you will see the added transactions in the new block.

Have fun!
