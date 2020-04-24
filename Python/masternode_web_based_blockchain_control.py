from flask import Flask, jsonify, request
# for test server -->
# import blockchain as bc
import threading
import time
from Python import masternode_blockchain as bc
import math
import random

first_time = True
node = Flask("__name__")
next_proof = 0
last_miner = ""
block_reward = 5000
already_mined = False
block_count = 0
next_halving = 7200
total_supply = 1000000000
max_ledger_burn_percentage = 0.5
registered_users = []


def blocktime():
    while True:
        global first_time
        global next_proof
        global block_reward
        global already_mined
        global registered_users
        global block_count
        global total_supply
        global max_ledger_burn_percentage
        global next_halving
        # Block reward halving
        if block_count == next_halving:
            block_reward = block_reward / 2
            next_halving = next_halving * 2
        # Generate genesis block at blocktime (2 minutes)
        if first_time:
            if (int(time.time()) % 120) <= 5:
                global blockchain
                blockchain = bc.Blockchain()
                total_supply = total_supply - blockchain.genesis_distributed_money
                for user in blockchain.genesis_initial_users:
                    registered_users.append(user)

                first_time = False
                next_proof = 0
                block_count = block_count + 1
                time.sleep(10)
        # Generate new block at blocktime (2 minutes)
        elif (int(time.time()) % 120) <= 5:
            if next_proof == 0:
                previous_block = blockchain.last_block
                next_proof = blockchain.pow(previous_block=previous_block)
            else:
                global last_miner
                blockchain.add_transaction(sender="masternode", recipient=last_miner, amount=block_reward)
                total_supply = total_supply - block_reward
                pass

            # Burn
            number_of_selected_users = math.ceil(len(registered_users) * 10 / 100)
            selected_users = []
            balance_selected_users = []
            usable_registered_users = registered_users.copy()
            summed_up_balance = 0

            # Choose all the users to burn currency from
            while number_of_selected_users > 0:
                # Choose random name from registered_users list
                unconfirmed_selected_user = random.choice(usable_registered_users)
                # Remove client from list so he can't be picked again
                usable_registered_users.remove(unconfirmed_selected_user)

                # Get clients current spendable balance
                unconfirmed_balance_user = 0
                for block in blockchain.chain:
                    block_transactions = block['transactions']
                    for t in block_transactions:
                        if t['sender'] == unconfirmed_selected_user:
                            unconfirmed_balance_user = unconfirmed_balance_user - t['amount']
                        elif t['recipient'] == unconfirmed_selected_user:
                            unconfirmed_balance_user = unconfirmed_balance_user + t['amount']
                for m in blockchain.mempool:
                    if m['sender'] == unconfirmed_selected_user:
                        unconfirmed_balance_user = unconfirmed_balance_user - m['amount']
                # If clients balance is zero get a new random client
                if unconfirmed_balance_user <= 0:
                    continue
                # If clients balance is greater than zero add client to selected users
                selected_users.append(unconfirmed_selected_user)
                # Append clients balance to the balances of the selected users
                balance_selected_users.append(unconfirmed_balance_user)
                number_of_selected_users = number_of_selected_users - 1
            # Get summed up balance of all chosen users
            for b in balance_selected_users:
                summed_up_balance = summed_up_balance + b

            # Burn value is 10% of summed up balance of selected users
            to_be_burned = summed_up_balance * 10 / 100
            if to_be_burned > (max_ledger_burn_percentage * total_supply / 100):
                to_be_burned = max_ledger_burn_percentage * total_supply / 100

            counter = 0
            while counter < len(selected_users):
                # Percentage client has to burn is calculated
                client_burn_percentage = balance_selected_users[counter] * 100 / summed_up_balance
                # Value each client has to burn is calculated
                client_burn_value = client_burn_percentage * to_be_burned / 100
                # Currency is burned
                blockchain.add_transaction(sender=selected_users[counter], recipient="Burner",
                                           amount=client_burn_value)
                counter = counter + 1

            # Burned currency is removed from total supply
            total_supply = total_supply - to_be_burned

            # New Block
            current_last_block = blockchain.chain[-1]
            blockchain.forge_block(next_proof, blockchain.hash_block(current_last_block))
            block_count = block_count + 1
            already_mined = False
            next_proof = 0

            time.sleep(10)


@node.route('/update/chain', methods=['POST'])
def update_chain():
    # Check if given proof of work is valid and masternodes pow
    new_proof_json = request.get_json(force=True)
    global next_proof
    next_proof = new_proof_json['proof']
    current_last_block = blockchain.chain[-1]
    if blockchain.validate_pow(current_last_block['proof'], next_proof,
                               blockchain.hash_block(current_last_block)) is False:
        return jsonify("Block not valid."), 400
    else:
        global last_miner
        global already_mined
        last_miner = new_proof_json['miner']
        already_mined = True
        return jsonify(
            "Block valid. Block will be added to chain."), 200


# Start thread to create blocks at blocktime asynchronously
threading.Thread(target=blocktime).start()


# Return full chain
@node.route('/full/chain', methods=['GET'])
def full_chain():
    return jsonify(blockchain.chain), 200


# Return transactions that are currently in mempool
@node.route('/current/transactions', methods=['GET'])
def transactions():
    return jsonify(blockchain.mempool), 200


# Only for testing purposes
# Return current chain
@node.route('/chain', methods=['GET'])
def rückgabe_ganze_blockchain():
    try:
        reply = {
            'chain': blockchain.chain,
            'lenght': len(blockchain.chain)
        }
        return jsonify(reply), 200
    except:
        return jsonify("No genesis block created"), 500


# Only for testing purposes
# Create a new transaction
@node.route('/transactions/new', methods=['POST'])
def add_transaction():
    input = request.get_json(force=True)

    index_transaktion = blockchain.add_transaction(sender=input['sender'],
                                                   recipient=input['recipient'],
                                                   amount=input['amount'])
    reply = {'message': f'Transaction will be added to block with index {index_transaktion}'}
    return jsonify(reply), 201


@node.route('/update/transactions', methods=['POST'])
def update_transactions():
    # Get new transaction from node and add it to mempool
    # Return confirmation status code 200
    add_transactions = request.get_json(force=True)
    blockchain.add_transaction(sender=add_transactions['sender'],
                               recipient=add_transactions['recipient'],
                               amount=add_transactions['amount'])
    return jsonify(), 200


# Return mining status (Has the next pow already been mined?)
@node.route('/mining/status', methods=['GET'])
def mining_status():
    global already_mined
    return jsonify(already_mined), 200


# Return a specific users transaction history
@node.route('/client/transactions', methods=['POST'])
def client_transactions():
    message = request.get_json(force=True)
    client_name = message['name']
    returned_transactions = []
    for block in blockchain.chain:
        block_transactions = block['transactions']
        for t in block_transactions:
            if t['sender'] == client_name:
                returned_transactions.append(t)
            elif t['recipient'] == client_name:
                returned_transactions.append(t)
    for m in blockchain.mempool:
        if m['sender'] == client_name:
            returned_transactions.append(m)
    finale_reply = {
        "transactions": returned_transactions
    }
    return jsonify(finale_reply), 200


# Return a specific users balance
@node.route('/client/balance', methods=['POST'])
def client_balance():
    message = request.get_json(force=True)
    client_name = message['name']
    balance = 0
    for block in blockchain.chain:
        block_transactions = block['transactions']
        for t in block_transactions:
            if t['sender'] == client_name:
                balance = balance - t['amount']
            elif t['recipient'] == client_name:
                balance = balance + t['amount']
    for m in blockchain.mempool:
        if m['sender'] == client_name:
            balance = balance - m['amount']
    new_balance = {
        "balance": balance
    }
    return jsonify(new_balance), 200


# Register a new user and give him a signup bonus
@node.route('/register', methods=['POST'])
def register():
    message = request.get_json(force=True)
    global registered_users
    global total_supply
    for user in registered_users:
        if user == message['name']:
            return jsonify("User already registered"), 200
    registered_users.append(message['name'])
    signup_bonus = 0.0001 * total_supply / 100
    total_supply = total_supply - signup_bonus
    blockchain.add_transaction(sender="SignupBonus", recipient=message['name'], amount=signup_bonus)
    return jsonify("User registered"), 200


# Only for testing purposes
# Return all currently registered users
@node.route('/register/print', methods=['GET'])
def r():
    global registered_users
    return jsonify(registered_users), 200
