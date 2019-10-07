# Paste your version of miner.py from the communication_gp
# or client_mining_p folder here (we don't make any changes)
import hashlib
import requests

import sys
import json

from uuid import uuid4

def proof_of_work(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof +=1
    return proof

def valid_proof(block_string, proof):
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:5] == "00000"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"
    coins_mined = 0
    # load or create id
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is: ", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # generate globally unique id
        id = str(uuid4()).replace('-', '')
        print("created new id: " + id)
        f.write(id)
        f.close()
    # run forever until interupted
    while True:
        # get last proof from server
        r = requests.get(url=node + "/last_block")
        data = r.json()
        new_proof = proof_of_work(data.get('last_block'))
        print("submitting proof: " + str(new_proof))
        post_data = {
            "proof": new_proof,
            "id": id
            }
        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
