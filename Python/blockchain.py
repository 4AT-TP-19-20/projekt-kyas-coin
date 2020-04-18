from time import time


class Blockchain:
    def __init__(self):
        self.chain = []
        self.aktuelle_transaktion = []

        self.neuer_block(beweis=100)

    def neuer_block(self, beweis):
        struktur_block = {
            'index': len(self.chain) + 1,
            'zeit_erstellung': time(),
            'beweis': beweis,
            'vorheriger_hash': self.block_hashen(self.chain[len(self.chain)-1])
        }
        self.aktuelle_transaktion.clear()
        self.chain.append(struktur_block)
        return struktur_block

    def neue_transaktion(self, absender, empfänger, betrag):
        self.aktuelle_transaktion.append({
            'absender': absender,
            'empfänger': empfänger,
            'betrag': betrag,
        })
        index = self.letzter_block['index']
        return index + 1

    def block_hashen(self):
        pass

    def letzter_block(self):
        lenght = len(self.chain) - 1
        return lenght
