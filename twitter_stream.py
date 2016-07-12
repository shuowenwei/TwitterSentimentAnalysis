# -*- coding: utf-8 -*-

# Simple example of using the twitter stream API
# Usage:  python twitter_stream.py or
#         python twitter_stream.py > streamFile.txt
#  NOTE:  IN EITHER CASE YOU WILL NEED TO USE CTRL-C TO CLOSE THE STREAM	  

from twython import TwythonStreamer

# insert your app developer keys here
CONSUMER_KEY = your key 
CONSUMER_SECRET = your secret
ACCESS_TOKEN_KEY = your TOKEN_KEY
ACCESS_TOKEN_SECRET = your TOKEN_SECRET

class MyStreamer(TwythonStreamer):
    # on_success is a callback for every tweet that gets through the filter
	# then we decide what to do with it; printing out key values for now
    def on_success(self, data):
        if 'text' in data and data['coordinates'] != None:
		    # reporting id, originating time, location, and text of the tweet
		    print data['id'],                       \
                    data['created_at'][:19],                \ 
                  data['coordinates']['coordinates'],     \
                  data['text'].encode('utf-8')

    # on_error is a callback for errors; we print the status code and disconnect
    def on_error(self, status_code, data):
        print status_code
        # stop trying to get data if there is an error
        self.disconnect()

if __name__=="__main__":	
    # establish a streaming connection as an ojbect of type TwythonStreamer
	# then create a filter on the stream
    stream = MyStreamer( CONSUMER_KEY, CONSUMER_SECRET,
                         ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET ) 
	# get tweets containing breakfast				 
    #stream.statuses.filter(track="breakfast", language='en')
	# get tweets originating in the continental US - roughly
    stream.statuses.filter(language='en', locations='-125, 25, -65, 50')
		
       

