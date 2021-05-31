# stock-screener
## Author: Rohan Mendiratta
## This code is open-source and available for personal and commericial use.

### Required Packages
<li> pandas
<li> yfinance
<li> pandas_ta

This program is a stock screener. The program will read a CSV file named 'tickers.csv'. The CSV file must containa column name 'Symbol', which will contain a column of stock symbols that you want to screen. The program will screen the symbol based on the following critera:
<li> The 5, 8, 13, 21, 50, and 75 EMA must be in ascending order.
<li> The most recent candle must be overlapping the 5 and 8 EMA.
