import yfinance as yf
import pandas_ta as ta
import pandas as pd
import multiprocessing as mp

"""
@author: Rohan Mendiratta
"""


def screen_ticker(symbol, weekly):
    """
    This function will is the screening function. It will calculate the EMA's and decide if the stock is bullish on
    either the daily or weekly timeframe
    :param symbol: Symbol to screen ('SPY')
    :param weekly: If true checks on the weekly timeframe, else checks on the daily timeframe
    :return: True if 5,8,13,21,50, and 75 EMA are in ascending order and if most recent candle is covering the 5 and 8
    EMA. Else False
    """
    try:
        ticker = yf.Ticker(symbol)

        if weekly:
            df = ticker.history(period='75wk', interval='1wk')
        else:
            df = ticker.history(period='75d', interval='1d')
    except:
        return False

    if len(df) != 75:
        return False

    open = df.iloc[-1]['Open']
    close = df.iloc[-1]['Close']

    ema_5 = ta.ema(df['Close'], length=5).iloc[-1]
    ema_8 = ta.ema(df['Close'], length=8).iloc[-1]
    ema_13 = ta.ema(df['Close'], length=13).iloc[-1]
    ema_21 = ta.ema(df['Close'], length=21).iloc[-1]
    ema_50 = ta.ema(df['Close'], length=50).iloc[-1]
    ema_75 = ta.ema(df['Close'], length=75).iloc[-1]

    if not (ema_5 > ema_8 > ema_13 > ema_21 > ema_50 > ema_75):
        return False

    if not (ema_5 < close and ema_8 > open):
        return False

    return True


if __name__ == '__main__':
    csv = pd.read_csv('tickers.csv')
    tickers = csv['Symbol'].tolist()

    with mp.Pool(processes=8) as pool:
        for ticker in tickers:
            r1 = pool.apply_async(screen_ticker, (ticker, False))
            if r1.get():
                print(f"{ticker} - Daily")

            r2 = pool.apply_async(screen_ticker, (ticker, True))
            if r2.get():
                print(f"{ticker} - Weekly")
