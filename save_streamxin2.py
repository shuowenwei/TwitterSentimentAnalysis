# -*- coding: utf-8 -*-

from twython import TwythonStreamer
import mysql.connector
import string
from datetime import date

# connect to the database server
connection = mysql.connector.connect(user='DBproj', password='W#akesale2013@',
                                     host='50.63.244.18', database='DBproj')
# we use a cursor to reference specific values in the database
cursor = connection.cursor()

# secret keys
CONSUMER_KEY = 'vDZ5rjMi7yYlUSE455X2hg'
CONSUMER_SECRET = 'EG09Ubi0skswNaKDYgwxhVYRiQhR1hpf6mVBkuFUj4'
ACCESS_TOKEN_KEY = '2314628120-HqxPNjlZz8dCVQ3KU5qCb9qVh0CS99EEBGb7UBf'
ACCESS_TOKEN_SECRET = 'adGPU7MoMeRx6N0gTmpjaCnDC4PUVA6kjrykELotQtkhm'

# used later in program to replace punctuation characters by spaces using translate()
REPLACEMENTS = string.maketrans( string.punctuation, ' '*len( string.punctuation ))

# dictionary to translate Month names to numbers
MONTHDICT = {'':0, 'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
    'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10,'Nov':11, 'Dec':12}

# template for the SQL INSERT statement
SQLInsert = ("INSERT INTO tweets2 " 
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)") 

def doInsert( data ):
    # Break out the interesting fields from the data
    ID = data['id_str'].encode('utf-8')
    creation = data['created_at'].encode('utf-8')
    creationDay  = creation[0:3]
    creationDate = date(int(creation[26:30]), MONTHDICT[creation[4:7]], int(creation[8:10]))
    creationTime = creation[11:19]
    # convert tweet text from unicode to printable ascii
    asciiText    = filter(lambda x: x in string.printable, data['text']).encode('utf-8', errors='ignore')    
    
    if  data['coordinates'] != None:	# a lot of tweets have no localization data    	    
        lon = data['coordinates']['coordinates'][0]
        lat = data['coordinates']['coordinates'][1]
        if (int(lat) >= 40) & (int(lat)<= 41) & (int(lon) >= -74 ) & (int(lon)<= -73):     
            tweetData = (ID, creationDay, creationDate, creationTime, lon, lat, asciiText, 'NY')
            
        elif (int(lat) >= 35) & (int(lat)<= 36) & (int(lon) >= -81) & (int(lon)<= -75):  
            tweetData = (ID, creationDay, creationDate, creationTime, lon, lat, asciiText, 'NC')
        else:
            tweetData = (ID, creationDay, creationDate, creationTime, lon, lat, asciiText, None)
    else:
        tweetData = (ID, creationDay, creationDate, creationTime, None, None, asciiText, None)


    # twitter occasionally sends duplicate IDs in their streaming data, so be careful
    try:
        cursor.execute( SQLInsert, tweetData)
    except mysql.connector.IntegrityError as err:
        print err

    connection.commit()

# Required class for providing callbacks for handling twitter stream
class MyStreamer(TwythonStreamer):
    
    def on_success(self, data):
        if 'text' in data:
            doInsert( data )
    
    def on_error(self, status_code, data):
        print status_code
        # stop trying to get data if there is an error
        self.disconnect()

# main
if __name__=="__main__":	
    stream = MyStreamer( CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET ) 
    # get tweets containing breakfast				 
    #stream.statuses.filter(track="football", language='en')
    # get tweets originating in the continental US - roughly
    #stream.statuses.filter(track="movie",language='en', locations='-74, 40, -73, 41,-84,35,-75,36')
    #track = ['dinner','restaurant','food','eat']
    stream.statuses.filter(language='en', locations='-74, 40, -73, 41,-84,35,-75,36')

    
