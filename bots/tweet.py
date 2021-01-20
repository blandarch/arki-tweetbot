from models import Store_Word
from configs import db
import tweepy
from twitterAPI import TwitterAPI
import logging
import re
import time
from check_mentions import mentions_main, check_mentions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Tweet_and_AddWord(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
    def tweet_words(self):
        sw = Store_Word.query.order_by(Store_Word.every_word).all()
        for u in sw:
            tweet_word = u.__dict__['every_word']
            logger.info(f"The word {tweet_word} is to be tweeted.\nFrom dict: {u} ")
            try:
                self.api.update_status(status=tweet_word)
                logger.info(f"Word \"{tweet_word}\" has been tweeted.")
            except tweepy.error.TweepError:
                logger.info(f'The word "{tweet_word}" has been most likely tweeted recently.')
                pass
            time.sleep(3600)
    def on_error(self, status):
        logger.error(status)
        

def main():
    api = TwitterAPI()
    tweet_and_word = Tweet_and_AddWord(api)
    tweet_and_word.tweet_words()


if __name__ == "__main__":
    main()
