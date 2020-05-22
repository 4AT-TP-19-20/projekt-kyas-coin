import json
import hashlib
import requests

chosen_lookup_server = "192.168.1.200:6921"
master_node_pool = []
chain_hashes = []
ledgers = []


def hash_chain(k_chain):
    # Hash a block and return hash value
    name_chain = json.dumps(k_chain, sort_keys=True).encode()
    ret_hash = hashlib.sha256(name_chain).hexdigest()
    return ret_hash


def all_same(items):
    return all(x == items[0] for x in items)


if __name__ == "__main__":
    response = requests.get(f'http://{chosen_lookup_server}/get/masternodes')
    for m in response.json()['masternodes']:
        master_node_pool.append(m)
    for node in master_node_pool:
        chain = (requests.get(f'http://{node}/chain')).json()
        chain_hashes.append(hash_chain(chain))
        led = (requests.get(f'http://{node}/ledger')).json()
        ledgers.append(led)
    print(all_same(chain_hashes))
    print(all_same(ledgers))
