import argparse
import bip39
import secrets
import json
import os
from glclient import Signer, Scheduler, Credentials


developer_path = 'gl-certs'
metadata_path = './metadata.json'
metadata = {}


def read_metadata():
  global metadata, metadata_path
  if os.path.exists(metadata_path):
    with open(metadata_path, 'r') as file:
      try:
        metadata = json.load(file)
      except json.JSONDecodeError:
        print(f"Invalid JSON in {metadata_path}. Returning empty dictionary.")
        metadata = {}
  else:
    metadata = {
      "network": "testnet",
      "phrase": "",
      "seed": "",
      "node_id": "",
      "rune": "",
      "device_cert": "",
      "device_key": ""
    }
    with open(metadata_path, 'w') as file:
      json.dump(metadata, file, indent=2)
      print(f"{metadata_path} did not exist. Created new file.")


def update_metadata(key, value):
  global metadata, metadata_path
  if 'key' in metadata:
    metadata[key] = value
  else:
    metadata.update({key: value})

  with open(metadata_path, 'w') as file:
    json.dump(metadata, file, indent=2)
    print(f"Appended {key} to {metadata_path}")


def get_seed_phrase():
  print("\nGenerating seed phrase...\n")
  rand = secrets.randbits(256).to_bytes(32, 'big')
  phrase = bip39.encode_bytes(rand)
  update_metadata('phrase', phrase)
  seed = bip39.phrase_to_seed(phrase)[:32]
  update_metadata('seed', seed.hex())


def register_user():
  global metadata
  print("\nInitializing signer...\n")
  developer_cert = ''
  developer_key = ''
  cert_path = os.path.join(developer_path, 'client.crt')
  with open(cert_path, mode="rb") as file:
      developer_cert = file.read()
  key_path = os.path.join(developer_path, 'client-key.pem')
  with open(key_path, mode="rb") as file:
      developer_key = file.read()
  developer_creds = Credentials.nobody_with(developer_cert, developer_key)
  signer = Signer(metadata['seed'].encode('utf-8'), metadata['network'], developer_creds)
  update_metadata('node_id', signer.node_id().hex())

  print("\nRegistering user...\n")
  scheduler = Scheduler(metadata['network'], developer_creds)
  registration = scheduler.register(signer=signer, invite_code=None)
  device_creds = Credentials.from_bytes(registration.creds)
  update_metadata('rune', registration.rune)
  update_metadata('device_cert', registration.device_cert)
  update_metadata('device_key', registration.device_key)
  return scheduler, device_creds


def schedule_node():
  global metadata
  print("\nScheduling Node...\n")
  device_creds = Credentials.from_parts(metadata['device_cert'].encode('utf-8'), metadata['device_key'].encode('utf-8'), metadata['rune'])
  scheduler = Scheduler(metadata['network'], device_creds)  
  return scheduler, None


def use_node(scheduler, device_creds=None):
  global metadata
  print("\nCalling node methods...\n")
  if device_creds is not None:
    scheduler = scheduler.authenticate(device_creds)
  node = scheduler.node()
  info = node.get_info()
  print(f'NODE INFO: {info}\n\n')


def main():
  global metadata, metadata_path
  parser = argparse.ArgumentParser(description=['Run Greenlight developer client'])
  parser.add_argument('--metadata', help='Location of the metadata file', default='./metadata.json')
  metadata_path = parser.parse_args().metadata
  print(f"\nMetadata file path: {metadata_path}\n")
  read_metadata()
  scheduler, device_creds = None, None
  if 'seed' in metadata and metadata['seed'] == '':
    get_seed_phrase()
  if ('node_id' in metadata and metadata['node_id'] == '') or ('device_cert' in metadata and metadata['device_cert'] == '') or ('device_key' in metadata and metadata['device_key'] == ''):
    scheduler, device_creds = register_user()
  else:
    scheduler, device_creds = schedule_node()
  use_node(scheduler, device_creds)


if __name__ == '__main__':
    main()
