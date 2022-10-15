# Twitter Streaming

# Create a simple application that plots out the popularity of tags associated with incoming tweets streamed live from Twitter
# 
# Steps:
# 
# 1. Start going to <https://developer.twitter.com> and create a Twitter Developer Account to get our access codes
#   1. Click: Create and App
#   2. Get get the `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET`
# 2. Install the tweepy library as well as matplotlib and seaborn
#   1. In you virtual environment or virtual box, run 
#     1. `pip install tweepy`
#     2. `pip install matplotlib`
#     3. `pip install seaborn`
#     4. `pip install pandas`
# 

# import needed libraries
import tweepy
from tweepy import OAuthHandler,Stream
from tweepy.streaming import Stream
import socket
import json

# define secure access
api_key = ''
api_secret = ''
access_token = ''
access_secret = ''

# listen for basic streaming events
class TweetListener(Stream):
    
    def __init__(self,c_socket):
        self.client_socket = c_socket
        
    def on_data(self,data):
        try:
            msg = json.loads(data)
            encoded_msg = msg['text'].encode('utf-8')
            print(encoded_msg)
            self.client_socketsend(encoded_msg)
            return True
        except BaseException as e:
            print('Error on_data: %s' % str(e))
        return True
    
    def on_error(self,status):
        print(status)
        return True

# authenticate and get the stream and filter out the tracks
def sendData(c_socket):
    auth = OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    
    twitter_stream = Stream(auth,TweetListener(c_socket))
    twitter_stream.filter(track=['blockchain'])

# run the app connecting to socket (host + port)
if __name__ == '__main__':
    s = socket.socket()
    host = '127.0.0.1'
    port = 5555
    s.bind((host, port))
    
    print('listening on {}:{}'.format(host, port))
    s.listen(5)
    c,addr = s.accept()
    
    # send the data to the client socket
    sendData(c)
