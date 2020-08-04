from binance.client import Client
import keys
from pandas import DataFrame as df
from datetime import datetime
import trading_key

client=Client(api_key=keys.Pkeys, api_secret=keys.Skeys)

#get candle data
def candle_data(symbols, intervals):
    
    candles=client.get_klines(symbol=symbols, interval=intervals)

    #create (date) dataframe
    candles_data_frame=df(candles)
    candles_data_frame_date=candles_data_frame[0]

    #create the empty date list
    final_date=[]

    #convert timestamp to readable date and append it to the list
    for time in candles_data_frame_date.unique():
        readable=datetime.fromtimestamp(int(time/1000))
        final_date.append(readable)

    #drop the first and last columns of the dateframe
    candles_data_frame.pop(0)
    candles_data_frame.pop(len(candles_data_frame.columns))
    
    dataframe_final_date=df(final_date)
    dataframe_final_date.columns=['date']
    final_data_frame=candles_data_frame.join(dataframe_final_date)
    
    #index by date
    final_data_frame.set_index('date', inplace=True)
    final_data_frame.columns=["open", "high", "low", "close", "volumn", "close time", "quote asset volumn", "number of trades", "taker buy base asset volumn", "taker buy quote assest volumn"]
    final_data_frame.to_csv(r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task2\S1_task2_candle data', index=True)

#candle_data('BTCUSDT',Client.KLINE_INTERVAL_30MINUTE)


#get transaction/trades data
def trades_data(symbols):
    trades=client.get_recent_trades(symbol=symbols)
    trades_df=df(trades)

    #convert time to readable date
    trades_df_date=trades_df['time']
    
    final_date=[]
    for time in trades_df_date:
        readable=datetime.fromtimestamp(int(time/1000))
        final_date.append(readable)
        
    df_final_date=df(final_date)
    df_final_date.columns=['date']
    final_df=trades_df.join(df_final_date)
    final_df.set_index('date', inplace=True)
    final_df.pop('time')

    final_df.to_csv(r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task2\S1_task2_trades data', index=True)

#trades_data('BTCUSDT')


def market_depth(symbols):
    market_depth=client.get_order_book(symbol=symbols)
    market_depth_df=df(market_depth)

    market_depth_df.columns=['lastUpdatedId', 'bids[price, quantity]', 'asks']

    market_depth_df.to_csv(r'C:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\S1\task2\S1_task2_market_depth', index=False)
    
#market_depth("BTCUSDT")


#Optional

tradingClient=Client(api_key=trading_key.Pkey1, api_secret=trading_key.Skey1)
order=tradingClient.create_test_order(symbol="BTCUSDT", side=Client.SIDE_BUY, type=Client.ORDER_TYPE_MARKET, quantity=100)
print(order)