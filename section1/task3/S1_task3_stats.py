from etherscan.stats import Stats
import pandas as pd
import json

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

api = Stats(api_key=key)


def get_ether_last_price(api):
    last_price = api.get_ether_last_price()
    last_price = pd.DataFrame(last_price.items())
    last_price = pd.DataFrame.transpose(last_price)
    last_price = last_price.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\S1_task3_stats_lastprice.csv')
# get_ether_last_price(api)


def get_total_ether_supply(api):
    supply = api.get_total_ether_supply()
    print(supply)
# get_total_ether_supply(api)
