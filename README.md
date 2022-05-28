# Reddit Portfolio

## Project Description

Determine if there exists a correlation between r/maxjustrisk sentiment on stocks/daytrading choices and true performance. This will be done by performing lexicon sentiment analysis on data scraped from the subreddit. 

## Solution Diagram

1. Set up Reddit scraper, sentiment analysis, database. 
2. Collect daily data from the daily discussion threads on r/maxjustrisk.
3. Compare sentiment on tickers in daily thread to ticker movement over the next few days.
4. Quantize the performance of a mention.

## Deliverables

Script that takes a Reddit post as input that will scrape comments from the post, associate comments with a ticker, perform sentiment analysis on comments associated with a ticker, and save the comment with the results of the sentiment analysis. 

Script that takes a date range as input that will use the sentiment associated with each ticker in that date range to create a projection for each ticker, and will compare this projection with date in the week following the date range. The input date range must end more than a week before the current date. 

## Data Collection

From r/maxjustrisk, look at comments in daily discussion thread and analyze comments. Associate comments with ticker in top level comment in their thread, and if the top level comment has no ticker, ignore the thread. 

We can do this continuously as new threads are being created as well as working with past data. 

We also need closing prices for stocks associated with the tickers. 

## Tools

Python
- PRAW
- NLTK
- VADER

Database (postgreSQL, mySQL, or filesystem)

Reddit account

## Timeline

Week 4: Data collection started

Week 5: Begin analysis of accuracy

Week 6: By now figure out how to use historical data

Week 7: Focus on writing

Week 8:

Week 9: Finish

Week 10:

## Challenges

No training data, so we will be working with a lexicon based SA approach

Cleaning data

Potentially obfuscated commends due to targets being unaware of our scraper's approach

Difficult to determine what the sentiment is on (which ticker, buy or sell)

## Possible Expansions

We are keeping the project simple, but there are other possibilities we could explore. 

1. Automate data collection in specified subreddits. 
2. Combine data from multiple subreddits. 
3. Make predictions for the future, then wait and check how well the prediction did. 
