from etherscan.transactions import Transactions
import json

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']


def get_status(tx_hash):
    api = Transactions(api_key=key)
    status = api.get_status(tx_hash=tx_hash)
    print(status)
# get_status('0x15f8e5ea1079d9a0bb04a4c58ae5fe7654b5b2b4463375ff7ffb490aa0032f3a')


def get_tx_receipt_status(tx_hash):
    api = Transactions(api_key=key)
    receipt_status = api.get_tx_receipt_status(tx_hash=tx_hash)
    print(receipt_status)
# get_tx_receipt_status('0x513c1ba0bebf66436b5fed86ab668452b7805593c05073eb2d51d3a52f480a76')
