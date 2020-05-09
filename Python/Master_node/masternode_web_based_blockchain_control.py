from flask import Flask, jsonify, request
# for test server -->
# import blockchain as bc
import threading
import time
import requests
from Python.Master_node import masternode_blockchain as bc
import math
import random
import os
import signal

# Set own static IP address
master_node_pool = []
local_node = "192.168.1.150:2169"
lookup_server_pool = ["192.168.1.200:6921", "192.168.1.201:6921", "192.168.1.202:6921", "192.168.1.203:6921"]
first_time = True
node = Flask("__name__")
next_proof = 0
last_miner = ""
block_reward = 5000
block_count = 0
next_halving = 7200
total_supply = 1000000000
max_ledger_burn_percentage = 0.5
registered_users = []
current_miners = []


def blocktime():
    while True:
        global first_time
        global next_proof
        global block_reward
        global registered_users
        global block_count
        global blockchain
        global total_supply
        global max_ledger_burn_percentage
        global next_halving
        # Block reward halving
        if block_count == next_halving:
            block_reward = block_reward / 2
            next_halving = next_halving * 2

        if first_time:
            blockchain = bc.Blockchain()
            total_supply = total_supply - blockchain.genesis_distributed_money
            for user in blockchain.genesis_initial_users:
                registered_users.append(user)

            first_time = False
            next_proof = 0
            block_count = block_count + 1
            return
        else:
            global last_miner
            blockchain.add_transaction(sender="masternode", recipient=last_miner, amount=block_reward)
            total_supply = total_supply - block_reward

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
            next_proof = 0
            return


def startup_sequence():
    global master_node_pool
    global first_time
    global blockchain
    global block_count
    global registered_users
    global local_node
    chosen_lookup_server = random.choice(lookup_server_pool)
    response = requests.get(f'http://{chosen_lookup_server}/get/masternodes')
    for m in response.json()['masternodes']:
        master_node_pool.append(m)
    # If there are no master nodes currently online, create a new block chain with new genesis block
    if len(master_node_pool) == 0:
        # Start thread to create blocks at block time asynchronously
        threading.Thread(target=blocktime).start()
        master_node_pool.append(local_node)
    else:
        first_time = False
        sync_from = random.choice(master_node_pool)

        blockchain = bc.Blockchain()
        response = requests.get(f'http://{sync_from}/full/chain')
        blockchain.chain = response.json()
        response = requests.get(f'http://{sync_from}/current/transactions')
        blockchain.mempool = response.json()
        master_node_pool.append(local_node)
        response = requests.get(f'http://{sync_from}/register/print')
        registered_users = response.json()
        response = requests.get(f'http://{sync_from}/block/count')
        block_count = response.json()
    message = {
        'masternode': local_node
    }
    requests.post(f'http://{chosen_lookup_server}/new/masternode', json=message)


def shutdown_sequence(signal, frame):
    while True:
        chosen_lookup_server = random.choice(lookup_server_pool)
        message = {
            'masternode': local_node
        }
        requests.post(f'http://{chosen_lookup_server}/remove/masternode', json=message)
        os._exit(os.EX_OK)


@node.route('/new/masternode', methods=['POST'])
def new_masternode():
    message = request.get_json(force=True)
    master_node_pool.append(message['masternode'])
    return jsonify(), 200


@node.route('/block/count', methods=['GET'])
def ret_block_count():
    return jsonify(block_count), 200


@node.route('/master/add/miner', methods=['POST'])
def master_add_miner():
    global current_miners
    message = request.get_json(force=True)
    current_miners.append(message['miner'])
    return jsonify(), 200


@node.route('/master/remove/miner', methods=['POST'])
def master_remove_miner():
    global current_miners
    message = request.get_json(force=True)
    current_miners.remove(message['miner'])
    return jsonify(), 200


@node.route('/add/miner', methods=['POST'])
def add_miner():
    global current_miners
    message = request.get_json(force=True)
    current_miners.append(message['miner'])
    tmp_master_nodes = master_node_pool.copy()
    tmp_master_nodes.remove(local_node)
    for m in tmp_master_nodes:
        requests.post(f'http://{m}/master/add/miner', json=message)
    return jsonify(), 200


@node.route('/remove/miner', methods=['POST'])
def rem_miner():
    global current_miners
    message = request.get_json(force=True)
    current_miners.remove(message['miner'])
    tmp_master_nodes = master_node_pool.copy()
    tmp_master_nodes.remove(local_node)
    for m in tmp_master_nodes:
        requests.post(f'http://{m}/master/remove/miner', json=message)
    return jsonify(), 200


@node.route('/add/block', methods=['POST'])
def add_latest_block():
    global next_proof
    global block_count
    global total_supply
    message = request.get_json(force=True)
    current_last_block = blockchain.chain[-1]
    next_proof = message['proof']
    print(next_proof)
    sender_node = message['node']
    if blockchain.validate_pow(current_last_block['proof'], next_proof,
                               blockchain.hash_block(current_last_block)) is False:
        return jsonify("Proof not valid!"), 400
    else:
        blockchain.chain.append(message['block'])
        block_count = block_count + 1
        total_supply = (requests.get(f'http://{sender_node}/ledger')).json()
        print("Ledger: " + str(total_supply))
        for b in blockchain.chain:
            print(blockchain.hash_block(b))
        return jsonify(), 200


@node.route('/remove/masternode', methods=['POST'])
def remove_master_node():
    message = request.get_json(force=True)
    master_node_pool.remove(message['masternode'])
    return jsonify(), 200


@node.route('/ledger')
def ret_ledger():
    return jsonify(total_supply), 200


@node.route('/active/masternodes', methods=['GET'])
def active_masternodes():
    return jsonify(master_node_pool), 200


@node.route('/update/chain', methods=['POST'])
def update_chain():
    global next_proof
    # Check if given proof of work is valid and masternodes pow
    new_proof_json = request.get_json(force=True)
    next_proof = new_proof_json['proof']
    current_last_block = blockchain.chain[-1]
    if blockchain.validate_pow(current_last_block['proof'], next_proof,
                               blockchain.hash_block(current_last_block)) is False:
        return jsonify("Block not valid."), 400
    else:
        global last_miner
        last_miner = new_proof_json['miner']
        blocktime()
        tmp_master_nodes = master_node_pool.copy()
        tmp_master_nodes.remove(local_node)
        for m in tmp_master_nodes:
            requests.post(f'http://{m}/add/block',
                          json={"node": local_node, "proof": new_proof_json['proof'], "block": blockchain.last_block})
        tmp_miners = current_miners.copy()
        tmp_miners.remove(new_proof_json['address'])
        for mr in tmp_miners:
            requests.get(f'http://{mr}/update/miner')
        print("Ledger: " + str(total_supply))
        for b in blockchain.chain:
            print(blockchain.hash_block(b))
        return jsonify(
            "Block valid. Block will be added to chain."), 200


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
def return_entire_blockchain():
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
    temp_send_list = master_node_pool.copy()
    temp_send_list.remove(local_node)
    for t in temp_send_list:
        requests.post(f'http://{t}/transactions/new/masternodes', json=input)
    return jsonify(reply), 201


@node.route('/transactions/new/masternodes', methods=['POST'])
def new_transaction_masternode():
    input = request.get_json(force=True)

    blockchain.add_transaction(sender=input['sender'],
                               recipient=input['recipient'],
                               amount=input['amount'])
    return jsonify(), 200


@node.route('/update/transactions', methods=['POST'])
def update_transactions():
    # Get new transaction from node and add it to mempool
    # Return confirmation status code 200
    add_transactions = request.get_json(force=True)
    blockchain.add_transaction(sender=add_transactions['sender'],
                               recipient=add_transactions['recipient'],
                               amount=add_transactions['amount'])
    return jsonify(), 200


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
    for s in master_node_pool:
        requests.post(f'http://{s}/add/user', json=message)
    signup_bonus = 0.0001 * total_supply / 100
    total_supply = total_supply - signup_bonus
    blockchain.add_transaction(sender="SignupBonus", recipient=message['name'], amount=signup_bonus)
    return jsonify("User registered"), 200


@node.route('/add/user', methods=['POST'])
def add_user():
    message = request.get_json(force=True)
    global registered_users
    for user in registered_users:
        if user == message['name']:
            return jsonify(), 200
    registered_users.append(message['name'])
    return jsonify(), 200


# Only for testing purposes
# Return all currently registered users
@node.route('/register/print', methods=['GET'])
def r():
    return jsonify(registered_users), 200


@node.route('/update/masternodes', methods=['POST'])
def update_masternodes():
    pass


print("Press CTRL + C to stop master node\n")
startup_sequence()
signal.signal(signal.SIGINT, shutdown_sequence)
