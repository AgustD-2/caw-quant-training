from etherscan.contracts import Contract
import json
import pandas as pd

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']
address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
api = Contract(address=address, api_key=key)


def get_abi():
    abi = api.get_abi()
    text_file = open("S1_task3_contracts_abi_text.txt", "w")
    n = text_file.write(abi)
    text_file.close()


#get_abi()


def get_sourcecode():
    sourcecode = api.get_sourcecode()
    text_file = open("S1_tsak3_contracts_sourcecode_text.txt", "w")
    n = text_file.write(sourcecode[0]['SourceCode'])
    text_file.close()


#get_sourcecode()
