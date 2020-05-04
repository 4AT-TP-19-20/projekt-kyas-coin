from time import time
import json
import hashlib
import random


class Blockchain:
    def __init__(self):
        self.genesis_initial_users = []
        self.genesis_distributed_money = 0
        self.mempool = []
        self.chain = []

        self.genesis_transactions()
        self.forge_block(proof=100, previous_hash='0')

    def genesis_transactions(self):
        # Generate given number of users and distribute a random amount of coins
        while len(self.genesis_initial_users) < 1000:
            username = "user" + str(len(self.genesis_initial_users))
            self.genesis_initial_users.append(username)
            random_number = random.randrange(100000, 500000)
            self.add_transaction(sender="masternode", recipient=username, amount=random_number)
            self.genesis_distributed_money = self.genesis_distributed_money + random_number

    def forge_block(self, proof, previous_hash):
        # Create new block
        # Add all transactions in mempool to new block
        block = {
            'index': len(self.chain) + 1,
            'forge_time': time(),
            'proof': proof,
            'previous_hash': previous_hash,
            'transactions': self.mempool
        }
        self.mempool = []
        self.chain.append(block)
        return block

    def add_transaction(self, sender, recipient, amount):
        # Create new transaction
        self.mempool.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
            'index_block': len(self.chain)
        })
        if len(self.chain) == 0:
            return
        else:
            index = self.last_block['index']
            return index + 1

    @staticmethod
    def hash_block(hashblock):
        # Hash a block and return hash value
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
        # Check if given proof of work is valid
        x = f'{previous_proof}{current_proof}{previous_hash}'.encode()
        z = hashlib.sha256(x).hexdigest()

        return z[:4] == "0000"


