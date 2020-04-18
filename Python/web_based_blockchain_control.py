from Python import blockchain as bc
from flask import Flask, jsonify, request
from uuid import uuid4

knotenpunkt = Flask(__name__)
einzigartiger_name_knotenpunkt = str(uuid4()).replace('-', '')
blockchain = bc.Blockchain()


@knotenpunkt.route('/mine')
def minen():
    vorheriger_block = blockchain.letzter_block
    beweis = blockchain.pow(vorheriger_block=vorheriger_block)

    # Belohnung für Mining einbauen

    vorheriger_hash = blockchain.block_hashen(vorheriger_block)
    neuer_block = blockchain.neuer_block(beweis=beweis, vorheriger_hash=vorheriger_hash)
    antwort = {
        'nachricht': "Neuer Block wurde erstellt",
        'index': neuer_block['index'],
        'transaktionen': neuer_block['transaktionen'],
        'beweis': neuer_block['beweis'],
        'vorheriger_hash': neuer_block['vorheriger_hash']
    }
    return jsonify(antwort), 200


@knotenpunkt.route('/chain')
def rückgabe_ganze_blockchain():
    antwort = {
        'chain': blockchain.chain,
        'länge': len(blockchain.chain)
    }
    return jsonify(antwort), 200


@knotenpunkt.route('/transaktionen/neu')
def neue_transaktion():
    transaktion_inputs = request.get_json()

    index_transaktion = blockchain.neue_transaktion(absender=transaktion_inputs['absender'],
                                                    empfänger=transaktion_inputs['empfänger'],
                                                    betrag=transaktion_inputs['betrag'])
    antwort = {'nachricht': f'Transaktion wird zum Block hinzugefügt mit dem index {index_transaktion}'}
    return jsonify(antwort), 201

