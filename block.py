import hashlib
import json
from time import time



class Blockchain(object):
    def __init__(self) -> None:
        self.chain = []
        self.current_transactions = []
        self.add_new_block(prev_hash=1, proof=100)

    def add_new_block(self, prev_hash: int, proof: int) -> dict:
        block = {
            'index': len(self.chain) - 1, 
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'prev_hash': prev_hash or self.hash(self.chain[-1])
        }
        self.current_transactions.remove()

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
    
