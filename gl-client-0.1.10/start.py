# 1: Save these new phrase and seed into node_security.json to use
# 2: Register the new node with new seed via register.py
# 3: Add signer.node_id() as node_id to the node_security.json file
# 4: Add response.device_cert, response.device_key to the node_security.json file
# 5: Run the node with start.py for further operations

import json
from glclient import TlsConfig, Scheduler

with open('node_security.json', 'r') as f:
    security_data = json.load(f)

tls = TlsConfig().identity(security_data['device_cert'], security_data['device_key'])

scheduler = Scheduler(bytes.fromhex(security_data['node_id']), security_data['network'], tls)
print(f'SCHEDULER: {scheduler}\n\n')

node = scheduler.node()
getinfo = node.get_info()
print(f'NODE: {node}\n\n')
print(f'NODE INFO: {getinfo}\n\n')
print(f'Fee Collected: {getinfo.fees_collected_msat}\n\n')
print(f'Features: {getinfo.our_features.node}\n\n')
print(f'Runes: {node.showrunes()}\n\n')

# print(f'RUNE: {node.showrunes()}\n\n')
# print(f'COMMANDO: {node.commando(security_data['node_id'], 'getinfo', '[]', security_data['rune'])}\n\n')


