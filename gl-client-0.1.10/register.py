# 1: Save these new phrase and seed into node_security.json to use
# 2: Register the new node with new seed via register.py
# 3: Add signer.node_id() as node_id to the node_security.json file
# 4: Add response.device_cert, response.device_key to the node_security.json file
# 5: Run the node with start.py for further operations

import json
from glclient import TlsConfig, Signer, Scheduler

with open('node_security.json', 'r') as f:
    security_data = json.load(f)

tls = TlsConfig().identity(security_data['device_cert'], security_data['device_key'])

signer = Signer(security_data['seed'], network=security_data['network'], tls=tls)
print(f'SIGNER NODE ID: {signer.node_id().hex()}\n\n')

scheduler = Scheduler(node_id=signer.node_id(), network=security_data['network'], tls=tls)
print(f'SCHEDULER: {scheduler}\n\n')

response = scheduler.register(signer)
print(f'REGISTER: {response}\n\n')

new_tls = TlsConfig().identity(response.device_cert, response.device_key)

signer = Signer(security_data['seed'], network=security_data['network'], tls=new_tls)
print(f'SIGNER NODE ID: {signer.node_id().hex()}\n\n')

node = Scheduler(node_id=signer.node_id(), network=security_data['network'], tls=new_tls).node()
print(f'NODE: {node}\n\n')
print(f'NODE INFO: {node.get_info()}\n\n')
