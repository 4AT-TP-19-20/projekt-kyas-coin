from Python.Client_node import client_blockchain as bc
from flask import Flask, jsonify, request
from urllib.parse import urlparse
import requests
import signal
import os
import multiprocessing

node = Flask(__name__)
blockchain = bc.Blockchain()
masternode = "192.168.1.169:2169"
name = "alexander"
first_time = True
static_ip = "192.168.1.21:21569"


def minen():
    # Blockchain is updated before pow is calculated
    init_sync()
    # Calculation of next pow
    try:
        previous_block = blockchain.last_block
    except IndexError:
        minen()
    next_proof = blockchain.pow(previous_block=previous_block)
    global name
    # Send pow to master node for confirmation
    requests.post(f'http://{masternode}/update/chain',
                  json={"proof": next_proof, "miner": name, "address": static_ip})
    minen()


p = multiprocessing.Process(target=minen)


@node.route('/mine', methods=['GET'])
def initiate_mining():
    global p
    p = multiprocessing.Process(target=minen)
    p.start()
    requests.post(f'http://{masternode}/add/miner', json={"miner": static_ip})
    return jsonify(), 200


@node.route('/update/miner', methods=['GET'])
def miner_update():
    global p
    p.terminate()
    p = multiprocessing.Process(target=minen)
    p.start()
    return jsonify(), 200


@node.route('/stop/miner', methods=['GET'])
def kill_miner():
    global p
    p.terminate()
    requests.post(f'http://{masternode}/remove/miner', json={"miner": static_ip})
    return jsonify(), 200


# Return entire chain
@node.route('/chain', methods=['GET'])
def return_entire_chain():
    reply = {
        'chain': blockchain.chain,
        'lenght': len(blockchain.chain)
    }
    return jsonify(reply), 200


@node.route('/transactions/new', methods=['POST'])
def new_transaction():
    balance = 0
    global name
    message = {
        "name": name
    }
    request_input = request.get_json(force=True)
    recipient = request_input['recipient']
    amount = request_input['amount']

    # Balance is checked before transaction is made
    reply = requests.post(f'http://{masternode}/client/balance', json=message)
    if reply.status_code == 200:
        reply_payload = reply.json()
        balance = reply_payload['balance']
        # If balance is not sufficient stop transaction
        if balance < float(amount):
            return jsonify("Balance not sufficient"), 403
    t = {
        'sender': name,
        'recipient': recipient,
        'amount': amount
    }
    # If balance is sufficient send transaction to mempool
    masternode_reply = requests.post(f'http://{masternode}/update/transactions',
                                     json=t)
    # If masternode http reply status code is 200 add transaction to own mempool
    if (masternode_reply.status_code) == 200:
        index_transaction = blockchain.add_transaction(sender=name,
                                                       recipient=request_input['recipient'],
                                                       amount=request_input['amount'])
        reply = {'message': f'Transaction will be added to block with index {index_transaction}'}
        return jsonify(reply), 201
    else:
        return jsonify("Transaction failed"), 500


@node.route('/get/full/update', methods=['GET'])
def init_sync(only_transactions=False):
    global blockchain
    # If get only transactions is false get update of chain and transactions
    if only_transactions is False:
        resp = requests.get(f'http://{masternode}/full/chain')
        if resp.status_code == 200:
            new_chain = resp.json()
            resp = (requests.get(f'http://{masternode}/block/count')).json()
            print(resp)
            if resp > 1:
                if blockchain.validate_new_chain(new_chain) is False:
                    requests.get(f'http://{masternode}/prime/chain/sync')
                    return jsonify("Invalid chain"), 500
                else:
                    blockchain.chain = new_chain
                    t = requests.get(f'http://{masternode}/current/transactions')
                    blockchain.mempool = t.json()
                    return jsonify("Chain replaced"), 200
            else:
                blockchain.chain = new_chain
                t = requests.get(f'http://{masternode}/current/transactions')
                blockchain.mempool = t.json()
                return jsonify("Chain replaced"), 200
    # Get only update of transactions
    else:
        t = requests.get(f'http://{masternode}/current/transactions')
        blockchain.mempool = t.json()


@node.route('/specific/transactions', methods=['GET'])
def specific_transactions():
    global name
    message = {
        "name": name
    }
    # Ask masternode for list of all transactions where user is involved
    reply = requests.post(f'http://{masternode}/client/transactions', json=message)
    if reply.status_code == 200:
        return jsonify(reply.json()), 200
    else:
        return jsonify(), 500


@node.route('/specific/balance', methods=['GET'])
def specific_balance():
    global name
    message = {
        "name": name
    }
    # Ask masternode for current users balance
    reply = requests.post(f'http://{masternode}/client/balance', json=message)
    if reply.status_code == 200:
        return jsonify(reply.json()['balance']), 200
    else:
        return jsonify(), 500


@node.route('/set/name', methods=['POST'])
def set_name():
    # Set users name for future transactions and mining rewards
    message = request.get_json(force=True)
    global name
    name = message['name']
    send = {
        "name": name
    }
    #  Register user to masternode to add him to burn pool
    register = requests.post(f'http://{masternode}/register', json=send)
    return jsonify("Name has been set to " + name), 200


@node.route('/set/masternode', methods=['POST'])
def set_masternode():
    # Set masternodes address, future proofing for when there will be more than 1 masternode
    message = request.get_json(force=True)
    global masternode
    global first_time
    masternode = urlparse(message['masternode']).netloc
    if first_time:
        init_sync(False)
        first_time = False
    return jsonify("Masternode set to: " + masternode), 200

# TODO: If chain not valid, update chain until it is valid
# TODO: Add try except
