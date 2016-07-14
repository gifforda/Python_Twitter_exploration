# Import the necessary methods from the tweepy library
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Variables that contain the user credentials to access Twitter Streaming API
ckey = ''  # Customer key
csecret = ''  # Customer secret key
atoken = ''  # Access token
asecret = ''  # Access secret token

class listener(StreamListener):

    def on_data(self, data):
        print(data)
        return True

    def on_error(self, status):
        print(status)

# This handles Twitter authentification and the connection to Twitter Streaming API

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
twitterStream = Stream(auth, listener())
    
# This line filters Twitter Stream to capture data by the keywords: 'python','learning'
twitterStream.filter(track=['Zika'])
