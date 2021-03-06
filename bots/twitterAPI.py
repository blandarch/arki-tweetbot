from __future__ import unicode_literals
import tweepy
import logging
import os

logger = logging.getLogger()

def TwitterAPI():
    consumer_key = os.getenv('API_KEY')
    consumer_secret = os.getenv('API_SECRETKEY')
    access_token = os.getenv('ACCESS_TOKEN')
    access_token_secret = os.getenv('ACCESS_TOKEN_SECRET')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logging.info("API Created")
    return api