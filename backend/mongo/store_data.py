import tweepy
from pymongo import MongoClient
from fastapi import FastAPI
import uvicorn
import os

app = FastAPI()

MONGO_CONNECTION_STR = os.environ['MONGO_CONNECTION_STR']
TWEEPY_CLIENT = tweepy.Client(os.environ['TWEEPY_CLIENT'])

def connect_mongo():
    client = MongoClient(MONGO_CONNECTION_STR)
    db = client.twitter_db
    collection = db.tweets   

    return collection

@app.post("/scrape")
def scrape_and_store_tweets():
    to_be_insert_tweets = []

    resp = TWEEPY_CLIENT.search_recent_tweets(query='Mike Tyson', max_results=10, tweet_fields=['text', 'lang'])

    for tweet in resp.data:
        if tweet['lang'] == 'en' and len(tweet['text']) > 10:
            to_be_insert_tweets.append({
                "text": tweet['text']
            })

    collection = connect_mongo()
    collection.insert_many(to_be_insert_tweets)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8087)