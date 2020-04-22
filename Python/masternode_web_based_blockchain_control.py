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
nächster_beweis = 0
last_miner = ""
block_reward = 50000
already_mined = False
block_count = 0
next_halving = 7200
total_supply = 1000000000
max_ledger_burn_percentage = 0.5
registered_users = []


def blocktime():
    while True:
        global first_time
        global nächster_beweis
        global block_reward
        global already_mined
        global registered_users
        global block_count
        global total_supply
        global max_ledger_burn_percentage
        global next_halving
        if block_count == next_halving:
            block_reward = block_reward / 2
            next_halving = next_halving * 2
        if first_time:
            if (int(time.time()) % 120) <= 5:
                global blockchain
                print(time.time() % 120)
                blockchain = bc.Blockchain()
                total_supply = total_supply - blockchain.genesis_distributed_money
                for user in blockchain.genesis_initial_users:
                    registered_users.append(user)

                first_time = False
                nächster_beweis = 0
                print("genesis")
                block_count = block_count + 1
                time.sleep(10)
        elif (int(time.time()) % 120) <= 5:
            print(time.time() % 120)
            print("new block")
            if nächster_beweis == 0:
                vorheriger_block = blockchain.letzter_block
                nächster_beweis = blockchain.pow(vorheriger_block=vorheriger_block)
            else:
                global last_miner
                blockchain.neue_transaktion(absender="masternode", empfänger=last_miner, betrag=block_reward)
                total_supply = total_supply - block_reward
                pass

            # Burn
            number_of_selected_users = math.ceil(len(registered_users) * 10 / 100)
            selected_users = []
            balance_selected_users = []
            summed_up_balance = 0

            # Choose all the users to burn currency from
            while number_of_selected_users > 0:
                already_selected = False
                # Choose random name from registered_users list
                unconfirmed_selected_user = random.choice(registered_users)
                # Check if user has already been selected before
                for u in selected_users:
                    # If user has already been selected set already selected to True
                    if unconfirmed_selected_user == u:
                        already_selected = True
                        continue
                # If already selected is True get a new random user
                if already_selected:
                    continue
                # Get clients current spendable balance
                unconfirmed_balance_user = 0
                for block in blockchain.chain:
                    block_transaktionen = block['transaktionen']
                    for t in block_transaktionen:
                        if t['absender'] == unconfirmed_selected_user:
                            unconfirmed_balance_user = unconfirmed_balance_user - t['betrag']
                        elif t['empfänger'] == unconfirmed_selected_user:
                            unconfirmed_balance_user = unconfirmed_balance_user + t['betrag']
                for m in blockchain.aktuelle_transaktionen:
                    if m['absender'] == unconfirmed_selected_user:
                        unconfirmed_balance_user = unconfirmed_balance_user - m['betrag']
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
                blockchain.neue_transaktion(absender=selected_users[counter], empfänger="Burner",
                                            betrag=client_burn_value)
                counter = counter + 1

            # Burned currency is removed from total supply
            total_supply = total_supply - to_be_burned

            # New Block
            aktuell_letzter_block = blockchain.chain[-1]
            blockchain.neuer_block(nächster_beweis, blockchain.block_hashen(aktuell_letzter_block))
            block_count = block_count + 1
            already_mined = False
            nächster_beweis = 0

            time.sleep(10)


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
        global last_miner
        global already_mined
        last_miner = neuer_beweis_json['miner']
        already_mined = True
        return jsonify(
            "Block valide. Block wird zur Blockchain hinzugefügt. Belohnung wird im nächsten Block ausgezahlt"), 200


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
    try:
        antwort = {
            'chain': blockchain.chain,
            'länge': len(blockchain.chain)
        }
        return jsonify(antwort), 200
    except:
        return jsonify("No genesis block created"), 500


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
    return jsonify(), 200


@node.route('/mining/status', methods=['GET'])
def mining_status():
    global already_mined
    return jsonify(already_mined), 200


@node.route('/client/transactions', methods=['POST'])
def client_transactions():
    nachricht = request.get_json(force=True)
    client_name = nachricht['name']
    rückgabe_transaktionen = []
    for block in blockchain.chain:
        block_transaktionen = block['transaktionen']
        for t in block_transaktionen:
            if t['absender'] == client_name:
                rückgabe_transaktionen.append(t)
            elif t['empfänger'] == client_name:
                rückgabe_transaktionen.append(t)
    for m in blockchain.aktuelle_transaktionen:
        if m['absender'] == client_name:
            rückgabe_transaktionen.append(m)
    finale_antwort = {
        "transactions": rückgabe_transaktionen
    }
    return jsonify(finale_antwort), 200


@node.route('/client/balance', methods=['POST'])
def client_balance():
    nachricht = request.get_json(force=True)
    client_name = nachricht['name']
    balance = 0
    for block in blockchain.chain:
        block_transaktionen = block['transaktionen']
        for t in block_transaktionen:
            if t['absender'] == client_name:
                balance = balance - t['betrag']
            elif t['empfänger'] == client_name:
                balance = balance + t['betrag']
    for m in blockchain.aktuelle_transaktionen:
        if m['absender'] == client_name:
            balance = balance - m['betrag']
    new_balance = {
        "balance": balance
    }
    return jsonify(new_balance), 200


@node.route('/register', methods=['POST'])
def register():
    nachricht = request.get_json(force=True)
    global registered_users
    global total_supply
    for user in registered_users:
        if user == nachricht['name']:
            return jsonify("User schon registriert"), 200
    registered_users.append(nachricht['name'])
    signup_bonus = 0.0001 * total_supply / 100
    blockchain.neue_transaktion(absender="SignupBonus", empfänger=nachricht['name'], betrag=signup_bonus)
    print(registered_users)
    return jsonify("User registriert"), 200


@node.route('/register/print', methods=['GET'])
def r():
    global registered_users
    return jsonify(registered_users), 200
