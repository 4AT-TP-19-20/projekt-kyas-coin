from Python import client_blockchain as bc
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests

knotenpunkt = Flask(__name__)
einzigartiger_name_knotenpunkt = str(uuid4()).replace('-', '')
blockchain = bc.Blockchain()
masternode = urlparse("http://173.212.211.222:2169").netloc


@knotenpunkt.route('/mine', methods=['GET'])
def minen():
    # Berechnung des nächsten Beweises
    vorheriger_block = blockchain.letzter_block
    nächster_beweis = blockchain.pow(vorheriger_block=vorheriger_block)
    masternode_antwort = requests.post(f'http://{masternode}/update/chain', json={"beweis": nächster_beweis})
    if masternode_antwort.status_code == 200:
        vorheriger_hash = blockchain.block_hashen(vorheriger_block)
        neuer_block = blockchain.neuer_block(beweis=nächster_beweis, vorheriger_hash=vorheriger_hash)
        antwort = {
            'nachricht': "Neuer Block wurde erstellt",
            'index': neuer_block['index'],
            'transaktionen': neuer_block['transaktionen'],
            'beweis': neuer_block['beweis'],
            'vorheriger_hash': neuer_block['vorheriger_hash']
        }
        return jsonify(antwort), 200
    else:
        return jsonify(), 500


@knotenpunkt.route('/chain', methods=['GET'])
def rückgabe_ganze_blockchain():
    antwort = {
        'chain': blockchain.chain,
        'länge': len(blockchain.chain)
    }
    return jsonify(antwort), 200


@knotenpunkt.route('/transaktionen/neu', methods=['POST'])
def neue_transaktion():
    transaktion_inputs = request.get_json(force=True)
    masternode_transaktionen_antwort = requests.post(f'http://{masternode}/update/transaktionen',
                                                     json=transaktion_inputs)
    if (masternode_transaktionen_antwort.status_code) == 200:
        index_transaktion = blockchain.neue_transaktion(absender=transaktion_inputs['absender'],
                                                        empfänger=transaktion_inputs['empfänger'],
                                                        betrag=transaktion_inputs['betrag'])
        antwort = {'nachricht': f'Transaktion wird zum Block hinzugefügt mit dem index {index_transaktion}'}
        return jsonify(antwort), 201
    else:
        return jsonify("Transaktion konnte nicht ausgeführt werden"), 500


@knotenpunkt.route('/get/chain', methods=['GET'])
def init_sync():
    resp = requests.get(f'http://{masternode}/full/chain')
    if resp.status_code == 200:
        neue_chain = resp.json()
        if blockchain.neue_blockchain_validieren(neue_chain) is False:
            return jsonify(), 500
        else:
            blockchain.chain = neue_chain
            t = requests.get(f'http://{masternode}/aktuelle/transaktionen')
            blockchain.aktuelle_transaktionen = t.json()
    return jsonify("Chain replaced"), 200


@knotenpunkt.route('/registrieren', methods=['POST'])
def reg():
    # sich bei masternode registrieren
    pass
