import tweepy
import config
import logging
from haiku import Haiku

auth = tweepy.OAuthHandler(config.CONSUMER_TOKEN, config.CONSUMER_SECRET)
auth.set_access_token(config.ACCESS_TOKEN, config.ACCESS_SECRET)
api = tweepy.API(auth)

class StreamListener(tweepy.StreamListener):
    def on_status(self, status):
        haiku = Haiku()
        tweeter = status.author.screen_name.encode("utf-8")
        text = haiku.to_str('. ') + ' @' + tweeter
        api.update_status(status=text, in_reply_to_status_id=status.id)

    def on_error(self, status_code):
        logging.error('Status Code: {}'.format(status_code))
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False


stream_listener = StreamListener()
stream = tweepy.Stream(auth=api.auth, listener=stream_listener)
stream.filter(track=['@'+config.USERNAME])