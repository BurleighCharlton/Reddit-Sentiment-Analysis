#!/usr/bin/python3
from pathlib import Path
import os
import sys
import json
import re
from datetime import datetime
import praw
import nltk.sentiment.vader as vader

_root = Path(os.path.abspath(__file__)).parent/"files"
SA = vader.SentimentIntensityAnalyzer()
with open("company_tickers.json", "r") as f:
  tickers_json = json.load(f)
tickers = [x["ticker"] for x in tickers_json.values() if x["ticker"] != "A"]
tickers_re = [re.compile(r'\b{0}\b'.format(x)).search for x in tickers]

def init(dir):
  """Initialize the files module in a specific directory.

  dir is a string of the absolute path to the directory the module should work
  in.
  """
  root = Path(dir)/"files"

def save_comment(ticker, time, text, sent):
  """Save a comment associated with ticker made on a post associated with the
  day of time that contains text and has sentiment sent. 

  """
  date = datetime.utcfromtimestamp(time).strftime("%Y-%m-%d")
  if not _root.exists():
    _root.mkdir(parents=True, exist_ok=True)
  with open(_root/f"{ticker}_{date}.txt", "a") as f:
    f.write(re.sub("\s+", " ", text) + f"\n{sent}\n")

def check_crawled(id):
  """Checks if we have already crawled a post with this id"""
  with open(_root/"history.txt", "r") as f:
    for line in f:
      if id in line:
        print("Post already crawled")
        exit()

def store_crawled(id):
  """Saves id of post in history file"""
  with open(_root/"history.txt", "a") as f:
    f.write(id)

def check_ticker(text):
  for idx, ticker_re in enumerate(tickers_re):
    if ticker_re(text):
      return tickers[idx]
  return None

def crawl_submission(reddit, url=None, id=None, period=129600):
  """Crawl the comments on a Reddit post. 

  Crawls through the comments on a Reddit post given by url or id. Any comments
  created more than period seconds after the post will be skipped. 

  Either url or id must be specified. If id is specified, url will be ignored.

  Will not run if post has already been crawled. 
  """
  def crawl():
    comment_tree = submission.comments
    comment_tree.replace_more(limit=None)
    for top_level_comment in comment_tree:
      if top_level_comment.created_utc - time < period:
        ticker = check_ticker(top_level_comment.body)
        if ticker:
          sent = SA.polarity_scores(top_level_comment.body)
          save_comment(ticker, time, top_level_comment.body, sent)
          replies = top_level_comment.replies
          replies.replace_more(limit=None)
          for comment in replies.list():
            if comment.created_utc - time < period:
              sent = SA.polarity_scores(comment.body)
              save_comment(ticker, time, comment.body, sent)
  if id == None:
    id = url.split("/")[-3]
  check_crawled(id)
  submission = reddit.submission(id=id)
  time = submission.created_utc
  crawl()
  store_crawled(id)

if __name__ == '__main__':
  if len(sys.argv) > 1 and sys.argv[1] == "-h":
    help(crawl_submission)
    exit()
  with open("bot.details", 'r') as f:
    ls = list(f.readlines())
    reddit = praw.Reddit(
      client_id = ls[0][:-1],
      client_secret = ls[1][:-1],
      user_agent = ls[2][:-1]
    )
    print(ls[2][:-1])
  if len(sys.argv) > 1 and sys.argv[1] == "-t":
    url = "https://www.reddit.com/r/Warframe/comments/udn1ha/zariman_spoon/"
    crawl_submission(reddit, url=url)
    exit()
  uri = input()
  while uri:
    crawl_submission(reddit, url=uri)
    print(uri)
    uri = input()

