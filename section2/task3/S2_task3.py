from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import csv

# Import the backtrader platform
import backtrader as bt
import backtrader.analyzers as btanalyzers


datadir = './data'  # data path
datafile = 'BTC_USDT_1h.csv'  # data file
from_datetime = '2020-01-01 00:00:00'  # start time
to_datetime = '2020-04-01 00:00:00'  # end time


# Create a Stratey
class SMACross(bt.Strategy):
    params = (
        ('pfast', 10),
        ('pslow', 20),
        ('printlog', False)
    )

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
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
        self.smafast = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.pfast)
        self.smaslow = bt.indicators.SimpleMovingAverage(
            self.datas[0], period=self.params.pslow)

        self.sma_crossup = bt.ind.CrossUp(self.smafast, self.smaslow)
        self.sma_crossdown = bt.ind.CrossDown(self.smafast, self.smaslow)

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
        if not self.position:
            if self.sma_crossup:
                self.buy()
        elif self.position:
            if self.sma_crossdown:
                self.close()

    def stop(self):
        self.log('(MA Period %2d %2d) Ending Value %.2f' %
                 (self.params.pfast, self.params.pslow, self.broker.getvalue()), doprint=True)
        # add column name
        b = open('S2_task3.csv', 'a', newline='')
        
        # get kpi
        returns = self.analyzers.myreturn.get_analysis()
        max_drawdown = self.analyzers.mydrawdown.get_analysis()[
            'max']['drawdown']
        total_trade = self.analyzers.mytradeanalyzer.get_analysis()[
            'total']['total']
        win_trade = self.analyzers.mytradeanalyzer.get_analysis()[
            'won']['total']
        loss_trade = total_trade-win_trade
        win_ratio = win_trade/total_trade
        average_win = self.analyzers.mytradeanalyzer.get_analysis()[
            'won']['pnl']['average']
        average_loss = self.analyzers.mytradeanalyzer.get_analysis()[
            'lost']['pnl']['average']
        average_wlratio = average_win/(-float(average_loss))
        longest_win_streak=self.analyzers.mytradeanalyzer.get_analysis()[
            'streak']['won']['longest']
        longest_loss_streak=self.analyzers.mytradeanalyzer.get_analysis()[
            'streak']['lost']['longest']
        items = [self.params.pfast, self.params.pslow, returns,
                 max_drawdown, total_trade, win_trade, loss_trade, win_ratio, 
                 average_win, average_loss, longest_win_streak, longest_loss_streak, average_wlratio]
        a = csv.writer(b)
        a.writerow(items)
        b.close()


if __name__ == '__main__':
    # Create a cerebro entity
    cerebro = bt.Cerebro(optreturn=False)

    # Add a strategy

    strats = cerebro.optstrategy(
        SMACross,
        pfast=range(5, 7),
        pslow=range(10, 16)
    )

    # Create a Data Feed
    data = pd.read_csv(os.path.join(datadir, datafile),
                       index_col='datetime', parse_dates=True)
    data = data.loc[
        (data.index >= pd.to_datetime(from_datetime)) &
        (data.index <= pd.to_datetime(to_datetime))]
    datafeed = bt.feeds.PandasData(dataname=data)

    # Add the Data Feed to Cerebro
    cerebro.adddata(datafeed)

    cerebro.addanalyzer(btanalyzers.Returns, _name='myreturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='mydrawdown')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='mytradeanalyzer')
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

    # Set our desired cash start
    cerebro.broker.setcash(1000.0)

    # Add a FixedSize sizer according to the stake
    cerebro.addsizer(bt.sizers.PercentSizer, percents=99)

    # Set the commission
    cerebro.broker.setcommission(commission=0.001)

    # Run over everything
    thestrats = cerebro.run(maxcpus=1)

#format the csv file
cols = ['sma_pfast', 'sma_pslow', 'Returns', 'MaxDrawDown', 'TotalTrades#',
              'WinTrades#', 'LossTrades#', 'WinRatio', 'AverageWin', 'AvergaeLoss',
              'LongestWinStreak', 'LongestLossStreak', 'AverageWinLossRatio']
df = pd.read_csv('S2_task3.csv', names=cols)
#df['RankReturn'] = df['Return'].rank()
df['RankMaxDrawDown'] = df['MaxDrawDown'].rank()
df['RankWinRatio'] = df['WinRatio'].rank()
df['RankAverageWinLossRatio'] = df['AverageWinLossRatio'].rank()
df['Score'] = (df['RankMaxDrawDown'] +
               df['RankWinRatio']+df['RankAverageWinLossRatio'])/3.0
df.to_csv('S2_task3.csv', index=True)
