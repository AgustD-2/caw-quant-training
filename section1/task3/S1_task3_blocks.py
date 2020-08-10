from etherscan.blocks import Blocks
import json
import pandas as pd

with open('C:/Yiru Xiong-Professional/实习/CryptoAlgoWheel/S1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

api = Blocks(api_key=key)


def get_block_reward():
    reward = api.get_block_reward(2165403)
    reward = pd.DataFrame(reward)
    reward.to_csv(
        r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task3\S1_task3_blocks_output.csv', index=False)


get_block_reward()
