from flask import Flask, jsonify, request
import requests

server = Flask("__name__")

# Change local address to own static ip
local_address = "192.168.1.200:6921"
server_pool = ["192.168.1.200:6921", "192.168.1.201:6921", "192.168.1.202:6921", "192.168.1.203:6921"]
registered_masternodes = []

server_pool.remove(local_address)


# Choosing random server for initial syncing
# chosen_server = random.choice(server_pool)
# Syncing from chosen server --> not needed because there is only fixed amount of lookup servers
# and they start at same time
# response = requests.get(f'http://{chosen_server}/get/masternodes')
# registered_masternodes = []

@server.route("/get/masternodes", methods=['GET'])
def get_masternodes():
    reply = {
        'masternodes': registered_masternodes
    }
    return jsonify(reply), 200


@server.route("/new/masternode", methods=['POST'])
def new_masternode():
    message = request.get_json(force=True)
    for m in registered_masternodes:
        if m == message['masternode']:
            return jsonify(), 400
    for m in registered_masternodes:
        requests.post(f'http://{m}/new/masternode', json=message)
    registered_masternodes.append(message['masternode'])
    for s in server_pool:
        requests.post(f'http://{s}/lookup/sync/new/masternode', json=message)
    return jsonify(), 200


@server.route("/update/trustfactor", methods=['POST'])
def update_trustfactor():
    # Message structure:
    # { 'old_masternode': "ip:port, old_trust factor",
    #   'new_masternode': "ip:port, new_trust_factor"
    # }
    message = request.get_json(force=True)
    for index, m in enumerate(registered_masternodes):
        if m == message['old_masternode']:
            registered_masternodes[index] = message['new_masternode']
    for s in server_pool:
        requests.post(f'http://{s}/lookup/sync/update/trustfactor', json=message)
    return jsonify(), 200


# Called when master node goes offline
@server.route("/remove/masternode", methods=['POST'])
def remove_masternode():
    message = request.get_json(force=True)
    for m in registered_masternodes:
        if m == message['masternode']:
            registered_masternodes.remove(m)
    for m in registered_masternodes:
        requests.post(f'http://{m}/remove/masternode', json=message)
    for s in server_pool:
        requests.post(f'http://{s}/lookup/sync/remove/masternode', json=message)
    return jsonify(), 200


@server.route("/lookup/sync/new/masternode", methods=['POST'])
def lookup_sync_new_masternode():
    message = request.get_json(force=True)
    for m in registered_masternodes:
        if m == message['masternode']:
            return jsonify(), 400
    registered_masternodes.append(message['masternode'])
    return jsonify(), 200


@server.route("/lookup/sync/remove/masternode", methods=['POST'])
def lookup_sync_remove_masternode():
    message = request.get_json(force=True)
    for m in registered_masternodes:
        if m == message['masternode']:
            registered_masternodes.remove(m)
    return jsonify(), 200


@server.route("/lookup/sync/update/trustfactor", methods=['POST'])
def lookup_sync_update_trustfactor():
    message = request.get_json(force=True)
    for index, m in enumerate(registered_masternodes):
        if m == message['old_masternode']:
            registered_masternodes[index] = message['new_masternode']
    return jsonify(), 200


