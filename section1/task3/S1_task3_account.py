from etherscan.accounts import Account
import json
import pandas as pd

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']


def get_all_blocks_mined(address, blocktype):
    api = Account(address=address, api_key=key)
    blocks = api.get_all_blocks_mined(offset=10000, blocktype=blocktype)
    print(blocks)
#get_all_blocks_mined('0x9dd134d14d1e65f84b706d6f205cd5b1cd03a46b', 'uncles')


def get_all_transactions(address, offset, sort, internal):
    api = Account(address=address, api_key=key)
    transactions = api.get_all_transactions(offset=offset, sort=sort,
                                            internal=internal)
    print(transactions[0])
#get_all_transactions('0x49edf201c1e139282643d5e7c6fb0c7219ad1db7', 10000, 'asc', False)


def get_balance(address):
    api = Account(address=address, api_key=key)
    balance = api.get_balance()
    print(balance)
# get_balance('0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a')


def get_balance_multiple(address):
    api = Account(address=address, api_key=key)
    balances = api.get_balance_multiple()
    balances = pd.DataFrame(balances)
    balances.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\S1_task3_accounts_balancemultiple.csv', index=False)
# get_balance_multiple(['0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
#          '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a'])


def get_blocks_mined_page(address, page, offset, blocktype):
    api = Account(address=address, api_key=key)
    blocks = api.get_blocks_mined_page(
        page=page, offset=offset, blocktype=blocktype)
    blocks = pd.DataFrame(blocks)
    blocks.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\S1_task3_accounts_minedpage.csv', index=False)
#get_blocks_mined_page('0x2a65aca4d5fc5b5c859090a6c34d164135398226', 1, 10000, 'blocks')


def get_transaction_page(address, page, offset, sort):
    api = Account(address=address, api_key=key)
    transactions = api.get_transaction_page(
        page=page, offset=offset, sort=sort)
    transactions = pd.DataFrame(transactions)
    transactions.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\S1_task3_accounts_transactionpage.csv', index=False)
#get_transaction_page('0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a', 1, 10000, 'des')


def get_transaction_page_erc20(address, page, offset,
                               sort, erc20):
    api = Account(address=address, api_key=key)
    transactions = api.get_transaction_page(
        page=1, offset=10000, sort='des', erc20=True)
    transactions = pd.DataFrame(transactions)
    transactions.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\pageerc20.csv', index=False)
# get_transaction_page_erc20('0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a',
#   1, 10000, 'des', True)
