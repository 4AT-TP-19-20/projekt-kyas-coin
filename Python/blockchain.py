class Blockchain:
    def __init__(self):
        self.chain = []
        self.aktuelle_transaktion = []

        self.neuer_block(beweis=100, vorheriger_hash=)

    def neuer_block(self, beweis, vorheriger_hash=None):
        pass

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
