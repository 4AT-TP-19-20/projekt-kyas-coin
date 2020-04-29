from Python import client_blockchain as bc
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests
import threading

node = Flask(__name__)
blockchain = bc.Blockchain()
masternode = ""
name = ""
first_time = True


@node.route('/mine', methods=['GET'])
def minen():
    # Blockchain is updated before pow is calculated
    sync_status = init_sync()
    # Current mining status (Has someone else already mined next pow?) is checked from the masternode
    status = requests.get(f'http://{masternode}/mining/status')
    if status.status_code == 200:
        mining_status = status.json()
        # If next pow has not been calculated already by someone else go on
        if not mining_status:
            # Calculation of next pow
            previous_block = blockchain.last_block
            next_proof = blockchain.pow(previous_block=previous_block)
            global name
            # Send pow to masternode for confirmation
            masternode_response = requests.post(f'http://{masternode}/update/chain',
                                                json={"proof": next_proof, "miner": name})
            if masternode_response.status_code == 200:
                reply = {
                    'message': "New block will be forged at blocktime",
                }
                return jsonify(reply), 200
            else:
                return jsonify("Error"), 500
        else:
            return jsonify("POW has already been calculated"), 403


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
    # If get only transactions is false get update of chain and transactions
    if only_transactions is False:
        resp = requests.get(f'http://{masternode}/full/chain')
        if resp.status_code == 200:
            new_chain = resp.json()
            if blockchain.validate_new_chain(new_chain) is False:
                return jsonify(), 500
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
