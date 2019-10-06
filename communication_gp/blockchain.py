# Paste your version of blockchain.py from the client_mining_p
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

import sys

from urllib.parse import urlparse

import requests


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        # self.new_block(previous_hash=1, proof=100)
        self.create_genesis_block() 

    def create_genesis_block(self):
        """
        Create genesis block
        These are hardcoded into most if not all blockchain protocols
        """

        block = {
            'index': 1,
            'timestamp': 1,
            'transactions': [],
            'proof': 1,
            'previous_hash': 1
        }

        # Reset the current list of transactions
        # self.current_transactions = []

        self.chain.append(block)
        # return block

    # new block
    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        # Reset the current list of transactions
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Creates a new transaction to go into the next mined Block

        :param sender: <str> Address of the Recipient
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the BLock that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    #register node ##
    def register_node(self, node):
        parsed_url = urlparse(node)
        self.nodes.add(parsed_url.netloc)


    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """


        # json.dumps converts json into a string
        # hashlib.sha246 is used to createa hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.  It convertes the string to bytes.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        block_string = json.dumps(block, sort_keys=True).encode()

        # By itself, this function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string using hexadecimal characters, which is
        # easer to work with and understand.  
        return hashlib.sha256(block_string).hexdigest()

    #  boradcast_new_block ##
    def broadcast_new_block(self,block):
        """
        Alert neighbors that a new block has been mined and they should add it to their
        chain as well
        """
        neighbors = self.nodes
        post_data = {"block": block}
        for node in neighbors:
            response = requests.post(f'http://{node}/block/new', json=post_data)
            if response.status_code != 200:
                # TODO error handling
                pass

    # add block ##
    def add_block(self,block):
        """
        Add a received block to the end of the chain
        """
        # Reset our pending transactions
        self.current_transactions = []
        self.chain.append(block)

    @property
    def last_block(self):
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Simple Proof of Work Algorithm
        Find a number p such that hash(last_block_string, p) contains 6 leading
        zeroes
        :return: A valid proof for the provided block
        """
        # TODO
        # pass
        # return proof
        # block_string = json.dumps(self.last_block, sort_keys=True).encode()
        block_string = json.dumps(block, sort_keys=True).encode()
        proof = 0
        while self.valid_proof(block_string, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 6
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # TODO
        # pass
        # return True or False
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == "00000"
        # return guess_hash[:2] == "00"

    def valid_chain(self, chain):
        """
        Determine if a given blockchain is valid.  We'll need this
        later when we are a part of a network.

        :param chain: <list> A blockchain
        :return: <bool> True if valid, False if not
        """

        prev_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{prev_block}')
            print(f'{block}')
            print("\n-------------------\n")
            # Check that the hash of the block is correct
            # TODO: Return false if hash isn't correct
            if block['previous_hash'] != self.hash(prev_block):
                return False

            # Check that the Proof of Work is correct
            # TODO: Return false if proof isn't correct
            block_string = json.dumps(prev_block, sort_keys=True).encode()
            if not self.valid_proof(block_string, block['proof']):
                breakpooint()
                print("Found invalid proof of work")
                return False

            prev_block = block
            current_index += 1

        return True


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


# @app.route('/mine', methods=['GET'])
# def mine():
#     # We run the proof of work algorithm to get the next proof...
#     # proof = blockchain.proof_of_work()
#     proof = blockchain.proof_of_work(blockchain.last_block)

#     # We must receive a reward for finding the proof.
#     # TODO:
#     # The sender is "0" to signify that this node has mine a new coin
#     # The recipient is the current node, it did the mining!
#     # The amount is 1 coin as a reward for mining the next block
#     blockchain.new_transaction(
#         sender="0",
#         recipient=node_identifier,
#         amount=1
#     )

#     # Forge the new Block by adding it to the chain
#     # TODO
#     previous_hash = blockchain.hash(blockchain.last_block)
#     block = blockchain.new_block(proof, previous_hash)

#     # Send a response with the new block
#     response = {
#         'message': "New Block Forged",
#         'index': block['index'],
#         'transactions': block['transactions'],
#         'proof': block['proof'],
#         'previous_hash': block['previous_hash'],
#     }
#     return jsonify(response), 200

@app.route('/mine', methods=['POST'])
def mine():
    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True).encode()
    values = request.get_json()
    submitted_proof = values.get('proof')
    print(last_block_string)
    print(submitted_proof)
    print(blockchain.valid_proof(last_block_string, submitted_proof))
    if blockchain.valid_proof(last_block_string, submitted_proof):
        blockchain.new_transaction(
            sender="0",
            recipient=node_identifier,
            amount=1
        )
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(submitted_proof, previous_hash)
        # broadcast new block
        blockchain.broadcast_new_block(block)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200
    else:
        response = {
            'message' : "Proof was invalid or already submitted"
        }
        return jsonify(response), 400




@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing Values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'],
                                       values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200

# add an endpoint returns the last block in the chain
@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200

# @app.route('/block/new', methods=['POST'])
# def new_block():
#     values = request.get_json()

#     # Check that the required fields are in the POST'ed data
#     required = ['block']
#     if not all(k in values for k in required):
#         return 'Missing Values', 400

#     # TODO: Verify that the sender is one of our peers

#     # TODO: Check that the new block index is 1 higher than our last block
#     # that it has a valid proof

#     # TODO: Otherwise, check for consensus
#     # Don't forget to send a response before asking for the full
#     # chain from a server awaiting a response.

#     return response, 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    print(values)
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/block/new', methods=['POST'])
def receive_block():
    values = request.get_json()
    new_block = values['block']
    old_block = blockchain.last_block
    if new_block['index'] == old_block['index'] + 1:
        # index is correct
        if new_block['previous_hash'] == blockchain.hash(old_block):
            # hashes are correct
            block_string = json.dumps(old_block, sort_keys=True).encode()
            if blockchain.valid_proof(block_string, new_block['proof']):
                # proof is valid
                blockchain.add_block(new_block)
                return 'Block Accepted'
            else:
                # bad proof, handle case
                pass
        else:
            # hashes don't match, handle error
            pass
    else:
        # their index is one greater
        # block could be invalid
        # we could be behind
        
        # do the consensus process:
        # poll all the nodes in our chain, and get the biggest one:
        pass

# params:
# key nodes / value [{'address':'localhost:5001'}]
# headers
# key Contnet-type / value application/json
# body
# { "nodes": ["http://localhost:5001"]}

# Run the program on port 5000
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)

# TODO: Get rid of the previous if __main__ and use this so we can change
# ports via the command line.  Note that this is not robust and will
# not catch errors
if __name__ == '__main__':
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000
    app.run(host='0.0.0.0', port=port)




#############Additional Code Added by our Colleagues################




