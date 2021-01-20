import tweepy
import logging
from twitterAPI import TwitterAPI
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def follow_followers(api):
    logger.info('Retrieving and following followers')
    for follower in tweepy.Cursor(api.followers).items():
        if not follower.following:
            logger.info(f"Folliwing {follower.name}")
            follower.follow()

def main():
    api = TwitterAPI()
    while True:
        follow_followers(api)
        logger.info("Waiting...")
        time.sleep(60)

if __name__ == "__main__":
    main()