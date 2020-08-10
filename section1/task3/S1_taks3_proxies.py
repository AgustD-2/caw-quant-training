from etherscan.proxies import Proxies
import json

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']
address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'
api = Proxies(api_key=key)


def gas_price():
    price = api.gas_price()
    print(price)
# gas_price()


def get_block_by_number(number):
    block = api.get_block_by_number(number)
    print(block['number'])
#get_block_by_number(5747732 )


def get_block_transaction_count_by_number(block_number):
    tx_count = api.get_block_transaction_count_by_number(
        block_number=block_number)
    print(int(tx_count, 16))
# get_block_transaction_count_by_number('0x10FB78')


def get_code(address):
    code = api.get_code(address)
    print(code)
# get_code('0xf75e354c5edc8efed9b59ee9f67a80845ade7d0c')


def get_most_recent_block():
    block = api.get_most_recent_block()
    print(int(block, 16))
# get_most_recent_block()


def get_storage_at(address):
    value = api.get_storage_at(address, 0x0)
    print(value)
# get_storage_at('0x6e03d9cce9d60f3e9f2597e13cd4c54c55330cfd')


def get_transaction_by_blocknumber_index(blocknumber, index):
    transaction = api.get_transaction_by_blocknumber_index(block_number=blocknumber,
                                                           index=index)
    print(transaction['transactionIndex'])
# get_transaction_by_blocknumber_index('0x57b2cc', '0x2')


def get_transaction_by_hash(tx_hash):
    transaction = api.get_transaction_by_hash(
        tx_hash=tx_hash)
    print(transaction['hash'])
# get_transaction_by_hash('0x1e2910a262b1008d0616a0beb24c1a491d78771baa54a33e66065e03b1f46bc1')


def get_transaction_count(address):
    count = api.get_transaction_count(address)
    print(int(count, 16))
# get_transaction_count('0x6E2446aCfcec11CC4a60f36aFA061a9ba81aF7e0')


def get_transaction_receipt(address):
    receipt = api.get_transaction_receipt(address)
    print(receipt)
# get_transaction_receipt('0xb03d4625fd433ad05f036abdc895a1837a7d838ed39f970db69e7d832e41205d')


def get_uncle_by_blocknumber_index(blocknumber, index):
    uncles = api.get_uncle_by_blocknumber_index(block_number=blocknumber,
                                                index=index)
    print(uncles['uncles'])
#get_uncle_by_blocknumber_index('0x210A9B', '0x0')
