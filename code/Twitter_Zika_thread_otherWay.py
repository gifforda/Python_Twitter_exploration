from threading import Thread
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Variables that contain the user credentials to access Twitter Streaming API
consumer_key = '' # Customer key
consumer_secret = '' # Customer secret key
access_token = '' # Access token
access_secret = '' # Access secret token


class StreamListener(StreamListener):
    def __init__(self, keyword, api=None):
        super(StreamListener, self).__init__(api)
        self.keyword = keyword

    def on_status(self, tweet):
        print('Ran on_status')


    def on_error(self, status_code):
        print('Error: ' + repr(status_code))
        return False

    def on_data(self, data):
        print(self.keyword, data)
        print('Ok, this is actually running')


def start_stream(auth, track):
    Stream(auth=auth, listener=StreamListener(track)).filter(track=[track])


# This handles Twitter authentification and the connection to Twitter Streaming API
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

track = ['zika']
for item in track:
    thread = Thread(target=start_stream, args=(auth, item))
    thread.start()
