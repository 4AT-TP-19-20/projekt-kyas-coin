from Python import client_blockchain as bc
from flask import Flask, jsonify, request
from uuid import uuid4
from urllib.parse import urlparse
import requests
import threading

knotenpunkt = Flask(__name__)
einzigartiger_name_knotenpunkt = str(uuid4()).replace('-', '')
blockchain = bc.Blockchain()
masternode = urlparse("http://173.212.211.222:2169").netloc
name = ""


@knotenpunkt.route('/mine', methods=['GET'])
def minen():
    # Bevor man mit dem Minen eines neuen Blocks anfängt wird die lokale Blockchain geupdated
    sync_status = init_sync()
    status = requests.get(f'http://{masternode}/mining/status')
    if status.status_code == 200:
        mining_status = status.json()
        if not mining_status:
            # Berechnung des nächsten Beweises
            vorheriger_block = blockchain.letzter_block
            nächster_beweis = blockchain.pow(vorheriger_block=vorheriger_block)
            global name
            masternode_antwort = requests.post(f'http://{masternode}/update/chain',
                                               json={"beweis": nächster_beweis, "miner": name})
            if masternode_antwort.status_code == 200:
                antwort = {
                    'nachricht': "Neuer Block wird zu Blocktime erstellt",
                }
                return jsonify(antwort), 200
            else:
                return jsonify("Fehler"), 500
        else:
            return jsonify("POW wurde schon errechnet"), 500


@knotenpunkt.route('/chain', methods=['GET'])
def rückgabe_ganze_blockchain():
    antwort = {
        'chain': blockchain.chain,
        'länge': len(blockchain.chain)
    }
    return jsonify(antwort), 200


@knotenpunkt.route('/transaktionen/neu', methods=['POST'])
def neue_transaktion():
    # Bevor eine neue Transaktion erstellt wird, muss die Transaktions Liste geupdated werden
    update_status = init_sync()
    balance = 0
    global name
    nachricht = {
        "name": name
    }
    transaktion_inputs = request.get_json(force=True)
    empfänger = transaktion_inputs['empfänger']
    betrag = transaktion_inputs['betrag']

    antwort = requests.post(f'http://{masternode}/client/balance', json=nachricht)
    if antwort.status_code == 200:
        antwort_payload = antwort.json()
        balance = antwort_payload['balance']
        if balance < betrag:
            return jsonify("Balance nicht ausreichend"), 500
    t = {
        'absender': name,
        'empfänger': empfänger,
        'betrag': betrag
    }
    masternode_transaktionen_antwort = requests.post(f'http://{masternode}/update/transaktionen',
                                                     json=t)
    if (masternode_transaktionen_antwort.status_code) == 200:
        index_transaktion = blockchain.neue_transaktion(absender=name,
                                                        empfänger=transaktion_inputs['empfänger'],
                                                        betrag=transaktion_inputs['betrag'])
        antwort = {'nachricht': f'Transaktion wird zum Block hinzugefügt mit dem index {index_transaktion}'}
        return jsonify(antwort), 201
    else:
        return jsonify("Transaktion konnte nicht ausgeführt werden"), 500


@knotenpunkt.route('/get/full/update', methods=['GET'])
def init_sync(only_transactions=False):
    if (only_transactions) is False:
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
    else:
        t = requests.get(f'http://{masternode}/aktuelle/transaktionen')
        blockchain.aktuelle_transaktionen = t.json()


@knotenpunkt.route('/spezifische/transaktionen', methods=['GET'])
def spezifische_transaktionen():
    global name
    nachricht = {
        "name": name
    }
    antwort = requests.post(f'http://{masternode}/client/transactions', json=nachricht)
    if antwort.status_code == 200:
        return jsonify(antwort.json()), 200
    else:
        return jsonify(), 500


@knotenpunkt.route('/spezifische/balance', methods=['GET'])
def spezifische_balance():
    global name
    nachricht = {
        "name": name
    }
    antwort = requests.post(f'http://{masternode}/client/balance', json=nachricht)
    if antwort.status_code == 200:
        return jsonify(antwort.json()), 200
    else:
        return jsonify(), 500


@knotenpunkt.route('/set/name', methods=['POST'])
def set_name():
    nachricht = request.get_json(force=True)
    global name
    name = nachricht['name']
    senden = {
        "name": name
    }
    register = requests.post(f'http://{masternode}/register', json=senden)
    return jsonify("Name wurde auf " + name + " gesetzt"), 200


def periodic_update():
    # TODO: Add periodic (Blocktime) updates using threads
    pass
