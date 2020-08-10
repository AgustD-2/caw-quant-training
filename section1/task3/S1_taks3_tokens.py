from etherscan.tokens import Tokens
import json

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']
    api = Tokens(contract_address='0x57d90b64a1a57749b0f932f1a3395792e12e7055',
                 api_key=key)


def get_token_balance(address):
    balance = api.get_token_balance(address=address)
    print(balance)


#get_token_balance('0xe04f27eb70e025b78871a2ad7eabe85e61212761')


def get_total_supply():
    supply = api.get_total_supply()
    print(supply)


#get_total_supply()
