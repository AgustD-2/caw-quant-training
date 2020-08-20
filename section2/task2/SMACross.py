from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
                        
import os
import datetime

import backtrader as bt
import pandas as pd
from matplotlib import pyplot as plt

from S1_task1 import *
obj = CryptoCompare('BTC', 'USDT', 'binance')
obj.download_histohour('2020-01-01', '2020-04-01')

# declear all environment params / global variables
datadir = 'E:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\Month1\S2\data'  # data path
logdir = 'E:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\Month1\S2\log'  # log path
reportdir = 'E:\Yiru Xiong-Professional\实习\CryptoAlgoWheel\Month1\S2\\report'  # report path
datafile = 'BTC_USDT_1h.csv'  # data file
from_datetime = '2020-01-01 00:00:00'  # start time
to_datetime = '2020-04-01 00:00:00'  # end time
logfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.csv'
figfile = 'BTC_USDT_1h_SMACross_10_20_2020-01-01_2020-04-01.png'

# define strategy class
class SMACross(bt.Strategy):

    params = (
        ('pfast', 10),
        ('pslow', 20),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        self.smafast = bt.indicators.SMA(
            self.datas[0], period=self.p.pfast)
        self.smaslow = bt.indicators.SMA(
            self.datas[0], period=self.p.pslow)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        self.log('Close, %.2f' % self.dataclose[0])
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            # Not yet ... we MIGHT BUY if ...
            if self.smafast[0] > self.smaslow[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.order = self.buy()

        else:

            if self.smafast[0] < self.smaslow[0]:
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                self.order = self.sell()


if __name__ == '__main__':

    # initiate cerebro instance:
    cerebro = bt.Cerebro()

    # feed data:
    data = pd.read_csv(os.path.join(datadir, datafile),
                       index_col='datetime', parse_dates=True)
    data = data.loc[
        (data.index >= pd.to_datetime(from_datetime)) &
        (data.index <= pd.to_datetime(to_datetime))]
    datafeed = bt.feeds.PandasData(dataname=data)
    cerebro.adddata(datafeed)

    # feed strategy:
    cerebro.addstrategy(SMACross)

    # additional backtest setting:
    cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.broker.setcash(1000)
    cerebro.broker.setcommission(commission=0.0)

    # add logger:
    cerebro.addwriter(
        bt.WriterFile,
        out=os.path.join(logdir, logfile),
        csv=True)

    # run:
    cerebro.run()

    print(cerebro.strats[0][0][0])
    print(cerebro.strats[0][0][0].params.__dict__)

    # save report:
    plt.rcParams['figure.figsize'] = [13.8, 10]
    fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
    fig[0][0].savefig(
        os.path.join(reportdir, figfile),
        dpi=480)
