# import flask_test
from Python.Master_node import masternode_web_based_blockchain_control

if __name__ == "__main__":
    # Start flask server
    masternode_web_based_blockchain_control.node.run(host='173.212.211.222', port=2169)
