# gl-user-testing
Testing Greenlight client v0.2.0


# User Personas(?):
- App Developer + App Users: One developer application registered with client credentials + multiple users using different instances of the application on multiple devices with separate device credentials.
- End user/node operator: End user will register + can connect multiple devices to same node with different device credentials.


# GL setup steps
- Download the developer certificate and key from https://greenlight.blockstream.com/ and save them in the `gl-certs` directory
- Create seed phrase for a new node
- Register the new node
- Node is ready to use


# How to test
- Start peotry shell with `poetry shell`.
- `poetry install` in dependencies are not installed already.
- Run `python gl-developer.py --metadata=./metadata.json` to create seed phrase, register a signer and use the node with device creds.
