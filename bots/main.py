import tweet
import check_mentions
import threading
import followfollowers

tweet_side = threading.Thread(target=tweet.main)
mentions_side = threading.Thread(target=check_mentions.mentions_main)
follow_side = threading.Thread(target=followfollowers.main)

tweet_side.start()
mentions_side.start()
follow_side.start()
tweet_side.join()
mentions_side.join()
follow_side.join()