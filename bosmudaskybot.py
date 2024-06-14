import tweepy
import schedule
import time
import logging
from dotenv import load_dotenv
import os
import sqlite3
import random

# Load environment variables
load_dotenv()

# Your Twitter API credentials
consumer_key = os.getenv('CONSUMER_KEY')
consumer_secret = os.getenv('CONSUMER_SECRET')
access_token = os.getenv('ACCESS_TOKEN')
access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

# Authenticate to Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Create API object
api = tweepy.API(auth)

# Set up logging
logging.basicConfig(filename='twitter_auto_poster.log', level=logging.INFO)

# Function to post a tweet
def post_tweet(message, image_path=None):
    try:
        if image_path:
            api.update_with_media(image_path, status=message)
        else:
            api.update_status(message)
        logging.info(f"Tweet posted successfully: {message}")
        print("Tweet posted successfully!")
    except tweepy.TweepError as e:
        logging.error(f"Error: {e.reason}")
        print(f"Error: {e.reason}")

# Function to read messages from a SQLite database
def read_messages_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT message, image_path FROM tweets")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Function to schedule tweets with random intervals
def schedule_tweets(messages):
    for message, image_path in messages:
        interval_minutes = random.randint(30, 180)  # Random interval between 30 minutes and 3 hours
        schedule.every(interval_minutes).minutes.do(post_tweet, message=message, image_path=image_path)

def main():
    messages = read_messages_from_db('tweets.db')
    schedule_tweets(messages)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
