# -*- coding: utf-8 -*-

import mysql.connector
import string

# read the AFINN_111 wordlist and store in a Python dictionary
# format:   word or phrase  sentiment value (-5 .. 5)

worddict = {}
filehandle = open("AFINN_111.txt", "rt")
for aline in filehandle:
    fields = aline.split()             # split line into a list of words
    mood = int(fields[len(fields)-1])  # the last one is the mood rating
    key = ' '.join(fields[0:len(fields)-1]) # join the other fields back together as a string
    worddict[key] = int(mood)          # create a dictionary entry (key,val)
    

# connect to the database server
connection = mysql.connector.connect(user='DBproj', password='W#akesale2013@',
                                     host='50.63.244.18', database='DBproj',
                                     use_unicode=False)

# we use a cursor to reference specific values in the database
cursor = connection.cursor()

# template for the SQL SELECT statement
CountQuery = ("SELECT COUNT(*) as count "
              "FROM tweets2"     ) 
getallQuery = ("SELECT rawtext, info, creationTime "
               "FROM tweets2 " 
               "WHERE creationDay = %s" )
     
# main
if __name__=="__main__":	
    
    cursor.execute( CountQuery )
    size = cursor.fetchone()
    print "There are currently", size[0] , "tweets in the database."
    
    NY=[]
    NC=[]
    
    begintime = 18*3600
    gap = 30
    k = 6
    timerange = []
    plotrange = []
    slotcount = 0
    for i in range(k):
        timerange.append(i+1)
        
    
    for timeslot in timerange:
        overallMoodSum = 0 
        overallMoodSum2 = 0
        tweetCount= 0
        tweetCount2= 0
        cursor.execute( getallQuery, ('Sun',) )
        for (tweet) in cursor:
            tweetText = tweet[0].lower()                  # lower case
            tweetText2 = tweet[1]
            creationtime = tweet[2]
            creationsecs = tweet[2].seconds
            
            
            if (creationsecs >(begintime+(timeslot-1)*gap*60)) & (creationsecs<(begintime+timeslot*gap*60)):

                # going to read tweets from the database and calculate the mood/sentiment values
                
                tweetText = tweetText.translate(None, string.punctuation)  # remove punctuation
                wordlist  = tweetText.split(' ')   # split on blanks to create a list of words
                moodsum = 0
                moodsum2 = 0
                keywordFound = False 
                
                if tweetText2 == 'NY':
                    for w in wordlist:                          # iterate over words in the tweet
                        if w in worddict:                       # if the word is in the dictionary
                            keywordFound = True
                            moodsum = moodsum + worddict[w]     # add in the mood value 
                
                    if keywordFound:
                                tweetCount = tweetCount + 1
                                overallMoodSum = overallMoodSum + moodsum
                                #print moodsum, tweetText, tweetText2 
                else:
                    for w in wordlist:                          # iterate over words in the tweet
                        if w in worddict:                       # if the word is in the dictionary
                            keywordFound = True
                            moodsum2 = moodsum2 + worddict[w]     # add in the mood value 
            
                    if keywordFound:
                        tweetCount2 = tweetCount2 + 1
                        overallMoodSum2 = overallMoodSum2 + moodsum2
                        #print moodsum2, tweetText, tweetText2  
                        #import pdb
                        #pdb.set_trace() 
        if (tweetCount>0) & (tweetCount2>0):
            print "NY", timeslot, overallMoodSum/float(tweetCount)
            print "NC", timeslot, overallMoodSum2/float(tweetCount2)
            NY.append(overallMoodSum/float(tweetCount))
            NC.append(overallMoodSum2/float(tweetCount2))
            slotcount = slotcount +1
    
    for i in range(slotcount):
        plotrange.append(i+1)
    print "\n\n", tweetCount, "tweets processed."
    import matplotlib.pyplot as plt
    
    plt.plot(plotrange,NC,'-r',plotrange,NY,'-b')
    plt.title('Tweets')
    plt.ylabel('Mood')
    plt.xlabel('Time')
    plt.legend(('NC','NY'))
    plt.savefig('plot.png')
    plt.show()

 
    connection.close()   
