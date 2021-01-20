import tweepy
import logging
from twitterAPI import TwitterAPI
import time
import re
from models import Store_Word
from configs import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
bring_out_word = Store_Word.query.all()
word_sto = [u.__dict__['every_word'] for u in bring_out_word]

def check_mentions(api, keyword, since_id):
    logging.info('Retrieving mentions')
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline, since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if not tweet.favorited:
            if keyword in tweet.text.lower():
                fin_word = search_keyword(tweet)
                #search keyword
                if fin_word.lower() in word_sto: #if keyword in database
                    word_already_in_database(api, fin_word, tweet)
                else:
                    add_word_database(api, fin_word, tweet)
            try:
                tweet.favorite()
            except Exception as e:
                while Exception:
                    logger.error("Error on fav", exc_info=True)
                    tweet.favorite()
        else:
            logging.info(f"{tweet.id} already favourited.")
    return new_since_id

def search_keyword(tweet):
    regex = re.compile(r'arkiword: (.*)')
    regex_search = regex.findall(tweet.text.lower()) 
    if len(regex_search) > 1:
        fin_word = ' '.join(regex_search)
    else:
        fin_word = regex_search[0]
    logging.info(f'A keyword "{fin_word}" found.')
    return fin_word

def add_word_database(api, wrd, tweet):
    logging.info(f'The keyword "{wrd}" is not in the database. Adding...')
    db.create_all()
    add_word = Store_Word(every_word=wrd.lower())
    db.session.add(add_word)
    db.session.commit()
    try:
        api.update_status(status=f"The word \"{wrd}\" has been successfully added to our database.\
            Thank you for your contribution!", in_reply_to_status_id=tweet.id)
    except tweepy.error.TweepError as e:
        logging.info(f"TweepError: {e.reason}")

def word_already_in_database(api, wrd, tweet):
    logging.info(f'The keyword "{wrd}" is already in the database!')
    try:
        api.update_status(status=f"The word \"{wrd}\" already exists in the database.", in_reply_to_status_id=tweet.id)
    except tweepy.error.TweepError as e:
        logging.info(f"TweepError: {e.reason}")

def mentions_main():
    api = TwitterAPI()
    since_id = 1
    while True:
        since_id = check_mentions(api, "arkiword", since_id)
        logger.info("Waiting for mentions...")

if __name__ == "__main__":
    mentions_main()
