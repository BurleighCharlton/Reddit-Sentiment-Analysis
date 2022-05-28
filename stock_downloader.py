#!/usr/bin/python
import pandas as pd
import yfinance as yf
import datetime

if __name__ == "__main__":
  df = pd.read_csv('ticker_data.csv')
  grouped = df.groupby('ticker')['date']
  max_date = grouped.max()
  min_date = grouped.min()
  time_format = "%Y-%m-%d"
  bounds_list = zip(min_date.index, map(lambda x : datetime.datetime.strftime(datetime.datetime.strptime(x, time_format)-datetime.timedelta(days=14), time_format), min_date), map(lambda x : datetime.datetime.strftime(datetime.datetime.strptime(x, time_format)+datetime.timedelta(days=14), time_format), max_date)) 
  df_list = list()
  for x in bounds_list:
    data = yf.download(x[0], group_by="Ticker", period="1d", start=x[1], end=x[2])
    data['ticker'] = x[0]
    df_list.append(data)
    print(x)
  df = pd.concat(df_list)
  df.to_csv('stock_data.csv')
