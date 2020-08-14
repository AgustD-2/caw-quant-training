import requests
import pandas as pd
import io
import json

class CryptoCompare:
    def __init__(self, fsym, tsyms, e):
        self.fsym=fsym
        self.tsyms=tsyms
        self.e=e        

    def download_histohour(self, starting_time, end_time):
        #convert given date parameter to timestamp
        ts_starting=int(pd.to_datetime(starting_time).value/10**9)
        ts_end=int(pd.to_datetime(end_time).value/10**9)

        #initialize old_data with only column name
        old_data=pd.DataFrame(columns=['time', 'close', 'high','low','open', 'volumefrom','volumeto','conversionType','conversionSymbol'])
        
        #extract data for every seven days
        for i in range(ts_starting, ts_end, 168*3600):
            
            if i+168*3600<=ts_end:
                par={"fsym":self.fsym, "tsym": self.tsyms, "e":self.e, "toTs":i+168*3600, "aggregate":1}
            else:
                par={"fsym":self.fsym, "tsym": self.tsyms, "e":self.e, "toTs":ts_end, "aggregate":1}
            r=requests.post('https://min-api.cryptocompare.com/data/v2/histohour',params=par)
            s=requests.get(r.url).content
            data=pd.read_json(io.StringIO(s.decode('utf-8')))
            data=data["Data"]["Data"]
            data=pd.DataFrame(data)
            data["time"]=pd.to_datetime(data["time"], unit='s')
            
            #collapse all data from each time period
            data=pd.concat([data, old_data], axis=0)
            old_data=data

        #remove the last two columns    
        cols_name=['conversionType','conversionSymbol','volumefrom']
        data=data.rename({'volumeto':'baseVolume', 'time':'datetime'}, axis=1)
        data.drop(cols_name, axis=1, inplace=True)
        
        data=data.sort_values(by='datetime')
        data.to_csv("S1_task1", encoding='utf-8', index=False)


    def download_topTradingPairs(self):
        par={"fsym":self.fsym}
        response=requests.post('https://min-api.cryptocompare.com/data/top/pairs', params=par)
        content=requests.get(response.url).content
        data_string=content.decode('utf-8')
              
        data=json.loads(data_string)
        df=pd.DataFrame.from_dict(data['Data'])
        df.to_csv("S1_task1 opt", encoding='utf-8', index=False)
        


obj=CryptoCompare(fsym="BTC",tsyms="USDT",e="binance")
obj.download_histohour("2017-04-01", "2020-04-01")
obj.download_topTradingPairs()
