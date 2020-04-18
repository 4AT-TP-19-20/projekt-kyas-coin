from Python import blockchain as bc
from flask import Flask, jsonify
from uuid import uuid4

knotenpunkt = Flask(__name__)
einzigartiger_name_knotenpunkt = str(uuid4()).replace('-', '')
blockchain = bc.Blockchain


@knotenpunkt.route('/mine')
def minen():
    pass


@knotenpunkt.route('/chain')
def rückgabe_ganze_blockchain():
    antwort = {
        'chain': blockchain.chain,
        'länge': len(blockchain.chain)
    }
    return jsonify(antwort), 200

@knotenpunkt.route('/transaktionen/neu')
def neue_transaktion():
    pass
