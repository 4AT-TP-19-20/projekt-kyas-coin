from flask import Flask, jsonify, request
# for test server -->
# import blockchain as bc
import threading
import time
from Python import masternode_blockchain as bc

first_time = True
node = Flask("__name__")
nächster_beweis = 0


def blocktime():
    while True:
        global first_time
        global nächster_beweis
        if first_time:
            if (int(time.time()) % 120) <= 5:
                print((int(time.time()) % 120))
                global blockchain
                blockchain = bc.Blockchain()
                first_time = False
                nächster_beweis = 0
                print("genesis")
                time.sleep(10)
        elif (int(time.time()) % 120) <= 5:
            print("new block")
            if nächster_beweis == 0:
                vorheriger_block = blockchain.letzter_block
                nächster_beweis = blockchain.pow(vorheriger_block=vorheriger_block)
                # Keine Belohnung
            else:
                # Belohnung für Miner
                pass
            aktuell_letzter_block = blockchain.chain[-1]
            blockchain.neuer_block(nächster_beweis, blockchain.block_hashen(aktuell_letzter_block))
            nächster_beweis = 0
            time.sleep(10)


# Only for testing purposes
@node.route('/mine', methods=['GET'])
def minen():
    # Berechnung des nächsten Beweises
    vorheriger_block = blockchain.letzter_block
    global nächster_beweis
    nächster_beweis = blockchain.pow(vorheriger_block=vorheriger_block)
    return jsonify("Okay"), 200


@node.route('/update/chain', methods=['POST'])
def update_chain():
    neuer_beweis_json = request.get_json(force=True)
    global nächster_beweis
    nächster_beweis = neuer_beweis_json['beweis']
    aktuell_letzter_block = blockchain.chain[-1]
    if blockchain.beweise_validieren(aktuell_letzter_block['beweis'], nächster_beweis,
                                     blockchain.block_hashen(aktuell_letzter_block)) is False:
        print("bad value")
        return jsonify("Block nicht valide."), 400
    else:
        return jsonify(
            "Block valide. Block wird zur Blockchain hinzugefügt. Belohnung wird im nächsten Block ausgezahlt"), 200
        # Transaktion mit Belohnung für Miner einbauen
        # Update an andere Nodes schicken


threading.Thread(target=blocktime).start()


@node.route('/full/chain', methods=['GET'])
def full_chain():
    return jsonify(blockchain.chain), 200


@node.route('/aktuelle/transaktionen', methods=['GET'])
def transaktionen():
    return jsonify(blockchain.aktuelle_transaktionen), 200


# Only for testing purposes
@node.route('/chain', methods=['GET'])
def rückgabe_ganze_blockchain():
    antwort = {
        'chain': blockchain.chain,
        'länge': len(blockchain.chain)
    }
    return jsonify(antwort), 200


# Only for testing purposes
@node.route('/transaktionen/neu', methods=['POST'])
def neue_transaktion():
    transaktion_inputs = request.get_json(force=True)

    index_transaktion = blockchain.neue_transaktion(absender=transaktion_inputs['absender'],
                                                    empfänger=transaktion_inputs['empfänger'],
                                                    betrag=transaktion_inputs['betrag'])
    antwort = {'nachricht': f'Transaktion wird zum Block hinzugefügt mit dem index {index_transaktion}'}
    return jsonify(antwort), 201


@node.route('/update/transaktionen', methods=['POST'])
def update_transactions():
    neue_transaktionen = request.get_json(force=True)
    blockchain.neue_transaktion(absender=neue_transaktionen['absender'],
                                empfänger=neue_transaktionen['empfänger'],
                                betrag=neue_transaktionen['betrag'])
    # Update an andere Nodes schicken
    return jsonify(), 200
