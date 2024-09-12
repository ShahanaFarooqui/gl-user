# 1: Save these new phrase and seed into node_security.json to use
# 2: Register the new node with new seed via register.py
# 3: Add signer.node_id() as node_id to the node_security.json file
# 4: Add response.device_cert, response.device_key to the node_security.json file
# 5: Run the node with start.py for further operations

import bip39
import secrets

rand = secrets.randbits(256).to_bytes(32, 'big')

phrase = bip39.encode_bytes(rand)
print (f'PHRASE: {phrase}\n\n')

seed = bip39.phrase_to_seed(phrase)[:32]
print (f'SEED: {seed.hex()}\n\n')
