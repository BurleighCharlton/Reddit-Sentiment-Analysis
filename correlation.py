#!/usr/bin/python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import os
import ast

ticker_data = {}

def extract_data():
  ticker_data = {"ticker": [], "date": [], "pos": [], "neg": [], "neu": [], "compound": []}
  _file = Path(os.path.abspath(__file__)).parent/"files"
  files = [f for f in os.listdir(_file) if (_file/f).is_file()]
  for f in files:
    if f[-3:] != 'txt' or f == "history.txt":
      continue
    print(f)
    ticker, date = f.split('.')[0].split('_')
    with open(_file/f, "r") as fp:
      for n, line in enumerate(fp):
        if n % 2 == 1:
          d = ast.literal_eval(line)
          ticker_data["ticker"].append(ticker)
          ticker_data["date"].append(date)
          ticker_data["pos"].append(d["pos"])
          ticker_data["neg"].append(d["neg"])
          ticker_data["neu"].append(d["neu"])
          ticker_data["compound"].append(d["compound"])
  ticker_data = pd.DataFrame(ticker_data)
  ticker_data.to_csv("ticker_data.csv")

def load_data():
  ticker_data = pd.read_csv("ticker_data.csv")

if __name__ == "__main__":
  extract_data()

