from Python import blockchain as bc
from flask import Flask
from uuid import uuid4

knotenpunkt = Flask(__name__)
einzigartiger_name_knotenpunkt = str(uuid4()).replace('-', '')
blockchain = bc.Blockchain


