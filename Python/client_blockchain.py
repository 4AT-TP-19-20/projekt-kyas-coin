from time import time
import json
import hashlib


class Blockchain:
    def __init__(self):
        #mempool
        self.aktuelle_transaktionen = []
        self.chain = []

        self.neuer_block(beweis=100, vorheriger_hash='0')

    def neuer_block(self, beweis, vorheriger_hash):
        struktur_block = {
            'index': len(self.chain) + 1,
            'zeit_erstellung': time(),
            'beweis': beweis,
            'vorheriger_hash': vorheriger_hash,
            'transaktionen': self.aktuelle_transaktionen
        }
        self.aktuelle_transaktionen = []
        self.chain.append(struktur_block)
        return struktur_block

    def neue_transaktion(self, absender, empfänger, betrag):
        self.aktuelle_transaktionen.append({
            'absender': absender,
            'empfänger': empfänger,
            'betrag': betrag,
        })
        index = self.letzter_block['index']
        return index + 1

    @staticmethod
    def block_hashen(hashblock):
        name_block = json.dumps(hashblock, sort_keys=True).encode()
        hash = hashlib.sha256(name_block).hexdigest()
        return hash

    @property
    def letzter_block(self):
        return self.chain[-1]

    def pow(self, vorheriger_block):
        vorheriger_beweis = vorheriger_block['beweis']
        vorheriger_hash = self.block_hashen(vorheriger_block)

        aktueller_beweis = 0
        while self.beweise_validieren(vorheriger_beweis, aktueller_beweis, vorheriger_hash) is False:
            aktueller_beweis = aktueller_beweis + 1
        return aktueller_beweis

    @staticmethod
    def beweise_validieren(vorheriger_beweis, aktueller_beweis, vorheriger_hash):
        x = f'{vorheriger_beweis}{aktueller_beweis}{vorheriger_hash}'.encode()
        z = hashlib.sha256(x).hexdigest()

        # Durch das Hinzufügen von mehr 0en an diesem Punkt, kann man die Mining
        # Schwierigkeit stark beeinflussen --> je mehr 0en, desto länger dauert
        # die Suche nach einer Lösung
        return z[:4] == "0000"

    def neue_blockchain_validieren(self, chain):
        vorheriger_block = chain[0]
        stelle = 1
        while stelle < len(chain):
            derzeitiger_block = chain[stelle]
            hash_vorheriger_block = self.block_hashen(vorheriger_block)
            if derzeitiger_block['vorheriger_hash'] != hash_vorheriger_block:
                return False
            if self.beweise_validieren(vorheriger_block['beweis'], derzeitiger_block['beweis'],
                                       hash_vorheriger_block) is False:
                return False

            vorheriger_block = derzeitiger_block
            stelle = stelle + 1

        return True
