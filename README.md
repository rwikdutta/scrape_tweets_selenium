# Scraping tweets from Twitter Profile using selenium

## Requirements:
 - Anaconda or Miniconda ( for creating a conda virtual env)
 - mongodb for storing the tweets

## Steps to run this ( on Ubuntu 18.04 ):
 - Run $conda env create --file env_selenium_data_coll.yml
 - Run $source activate env_selenium_data_coll
 - Install mongodb from this article: https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-18-04
 - Modify the values in the selenium_tweets.py where "modify this" is commented  
 - Run $python selenium_tweets.py
