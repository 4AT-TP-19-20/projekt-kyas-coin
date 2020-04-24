from time import time
import json
import hashlib


class Blockchain:
    def __init__(self):
        self.mempool = []
        self.chain = []

    def add_transaction(self, sender, recipient, amount):
        self.mempool.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        index = self.last_block['index']
        return index + 1

    @staticmethod
    def hash_block(hashblock):
        # Encode and hash block
        name_block = json.dumps(hashblock, sort_keys=True).encode()
        hash = hashlib.sha256(name_block).hexdigest()
        return hash

    @property
    def last_block(self):
        # Return last block in chain
        return self.chain[-1]

    def pow(self, previous_block):
        # Calculate next proof of work
        previous_proof = previous_block['proof']
        previous_hash = self.hash_block(previous_block)

        current_proof = 0
        while self.validate_pow(previous_proof, current_proof, previous_hash) is False:
            current_proof = current_proof + 1
        return current_proof

    @staticmethod
    def validate_pow(previous_proof, current_proof, previous_hash):
        x = f'{previous_proof}{current_proof}{previous_hash}'.encode()
        z = hashlib.sha256(x).hexdigest()
        # Check if hash has 4 leading zeros
        return z[:4] == "0000"

    def validate_new_chain(self, chain):
        # Check if new chain is valid
        previous_block = chain[0]
        index = 1
        while index < len(chain):
            current_block = chain[index]
            hash_previous_block = self.hash_block(previous_block)
            if current_block['previous_hash'] != hash_previous_block:
                return False
            if self.validate_pow(previous_block['proof'], current_block['proof'],
                                 hash_previous_block) is False:
                return False
            previous_block = current_block
            index = index + 1
        return True
