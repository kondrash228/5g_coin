import hashlib
import json

from textwrap import dedent
from time import time
from uuid import uuid4
from urllib.parse import urlparse

from flask import Flask, jsonify, request



class Blockchain(object):
    def __init__(self) -> None:
        self.chain = []
        self.current_transactions = []
        self.add_new_block(prev_hash=1, proof=100)
        self.nodes = set()
    

    def register_node(self, address: str) -> None:

        parse_url = urlparse(address)
        self.nodes.add(parse_url.netloc)

    
    def valid_chain(self, chain: list) -> bool:

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):

            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n------------\n")

            if block['prev_hash'] != self.hash(last_block):
                return False
            
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False
            
            last_block = block
            current_index += 1
        
        return True
    

    def resolve_conflicts(self) -> bool:
        neighbours = self.nodes
        new_chain = None

        max_length = len(self.chain)

        for node in neighbours:

            response = request.get(f'http://{node}//chain')

            if response.status_code == 200:
                length = response.json()['lenght']
                chain = response.json()['chain']

                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True
        
        return False


    def add_new_block(self, prev_hash: int, proof: int) -> dict:
        block = {
            'index': len(self.chain) + 1, 
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash or self.hash(self.chain[-1])
        }
        self.current_transactions = []

        self.chain.append(block)
        return block


    def new_transaction(self, sender: str, recipient: str, amount: int) -> int:
        self.current_transactions.append(
            {
                'sender': sender,
                'recipient': recipient,
                'amount': amount
            }
        )

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block: dict) -> str:
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self) -> None:
        return self.chain[-1]


    def proof_of_woork(self, last_proof: int) -> int:
        proof = 0

        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        
        return proof


    @staticmethod
    def valid_proof(last_proof: int, proof: int) -> bool:

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"
    

app = Flask(__name__)
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_woork(last_proof)

    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )

    prev_hash = blockchain.hash(last_block)
    block = blockchain.add_new_block(proof, prev_hash)

    response = {
        'message': 'New block forged',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'prev_hash': block['prev_hash']
    }

    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    required = ['sender', 'recipient', 'amount']


    if not all(k in values for k in required):
        return 'Missed values', 400

    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {
        'message': f'Transaction will be added to Block {index}'
    }
    

    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain)
    }

    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')

    print(nodes)
    print(values)

    if nodes is None:
        return 'Error:  Please supply a valid list of nodes', 400
    
    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }

    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
 
    return jsonify(response), 200



if __name__ == "__main__":
    app.run(port=5002)


