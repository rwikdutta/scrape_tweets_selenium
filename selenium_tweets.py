from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json
from datetime import datetime
from pymongo import MongoClient
import numpy as np
import pandas as pd
i=1
j=1
url='https://twitter.com/cnn' #modify_this
browser=webdriver.Chrome(executable_path='./chromedriver')
browser.get(url)
client = MongoClient('mongodb://localhost:27017') #modify_this
db = client.news_data #modify_this
db_cnn_collection=client.news_data.cnn_12 #modify_this
time.sleep(3)
tweets_html=pd.Series(browser.find_elements_by_class_name('tweet'))
new_entries=tweets_html
#print(tweets_html)
out=[]
old_tweets_html=pd.Series([],dtype='object')
body=browser.find_element_by_tag_name('body')
while new_entries.shape[0]>0:
    for tweet in new_entries:
        id=tweet.get_attribute('data-tweet-id')
        tweet_timestamp_html=tweet.find_element_by_class_name('tweet-timestamp')
        tweet_link=tweet_timestamp_html.get_attribute('href')
        tweet_timestamp=tweet_timestamp_html.find_element_by_tag_name('span').get_attribute('data-time')
        tweet_text_html=tweet.find_element_by_class_name('tweet-text')
        tweet_text=tweet_text_html.text
        tweet_urls=[]
        for a_html in tweet_text_html.find_elements_by_tag_name('a'):
            tweet_urls.append(a_html.get_attribute('href'))
        out_dict={'tweet_id':id,
                    'tweet_timestamp':tweet_timestamp,
                    'tweet_link':tweet_link,
                    'tweet_text':tweet_text,
                    'tweet_urls':tweet_urls,}
        res=db_cnn_collection.insert_one(out_dict)
        if not res.acknowledged:
            print('{} ack for entry {}'.format(res.acknowledged,i))
        if i%100==0:
            print("Entry:{},ack:{},insert_id:{}".format(i,res.acknowledged,res.inserted_id))
        i+=1
    old_tweets_html=tweets_html
    for _ in range(3):
        print('Pressing END for {}th time'.format(j))
        j += 1
        body.send_keys(Keys.END)
        time.sleep(3)
        tweets_html = pd.Series(browser.find_elements_by_class_name('tweet'))
        new_entries=tweets_html[tweets_html.isin(old_tweets_html)==False]
        if new_entries.shape[0]>0:
            break
