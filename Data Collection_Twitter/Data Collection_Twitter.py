#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 00:38:46 2022

@author: buluo
"""

'''import all necessary packages'''

from bs4 import BeautifulSoup
import requests as rq
import pandas as pd
import tweepy
from AppCred import CONSUMER_KEY, CONSUMER_SECRET
from AppCred import ACCESS_TOKEN, ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

url = 'https://www.tradingview.com/markets/cryptocurrencies/prices-all/'
res = rq.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

'''make data structured and only take top 100 cryptocurrencies based on market_capitalization'''

coin = []
count = 0
for i in soup.find_all('tr',{'class':'tv-data-table__row tv-data-table__stroke tv-screener-table__result-row'}):
    if count < 100: 
        coin.append(i.find('a').text)
        count += 1
        
'''collect search results according to the coin list gained from the website Tradingview'''

# count = 0
Tw_coin = []
for i in coin:
    Tw_coin.append(api.search_tweets(q = i, count = 100, tweet_mode = "extended"))
#     count += 1
#     print(count)

'''another way to collect more tweets: results = [status._json for status in tweepy.Cursor(API.search, q="$EURUSD", count=1000, tweet_mode='extended', lang='en').items()]'''

'''make data structured'''

tweet_created_at = []
text = []
screen_name = []
location = []
description = []
followers_count = []
friends_count = []
user_created_at = []
statuses_count = []
coin_name = []

help_ = 0
for result in Tw_coin:
    for i in result:
        tweet_created_at.append(i._json['created_at'])
        text.append(i._json['full_text'])
        screen_name.append(i._json['user']['screen_name'])
        location.append(i._json['user']['location'])
        description.append(i._json['user']['description'])
        followers_count.append(i._json['user']['followers_count'])
        friends_count.append(i._json['user']['friends_count'])
        user_created_at.append(i._json['user']['created_at'])
        statuses_count.append(i._json['user']['statuses_count'])
        coin_name.append(coin[help_])
    help_ += 1
    
'''turn the data into DataFrame'''

tweet_coin = {'tweet_created_at':tweet_created_at, 'text':text, 'screen_name':screen_name, 'location':location,
              'description':description, 'followers_count':followers_count, 
              'friends_count':friends_count, 'user_created_at':user_created_at, 
              'statuses_count':statuses_count, 'coin_name':coin_name}
tweet_coin = pd.DataFrame(tweet_coin)
tweet_coin.head()

tweet_coin.to_csv('tweet_coin_21012022.csv',index = False)