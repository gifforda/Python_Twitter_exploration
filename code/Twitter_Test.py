# Import the necessary methods from the tweepy library
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

# Variables that contain the user credentials to access Twitter Streaming API
ckey = 'lW1gGhAuLVv87XaLEtp1X7r3N' # Customer key
csecret = 'vevuQEqfLuXbWJbXp1OBZeUU6OrfPg6KFEc5F516eaTs7i1P8V' # Customer secret key
atoken = '954657146-KKtvbrhDVRDeIJ0lPatYZ8DnHisXi63S7iFxJNB2' # Access token 
asecret = 'HtPjBArnCUcuuwOJ7euZ8XezxoffkRcrcnxj1j8pzqcJd' # Access secret token

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
