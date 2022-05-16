#!/usr/bin/env python
# coding: utf-8

#Dean Stirrat

import googletrans
import twitter
from googletrans import Translator
from textblob import TextBlob
import re
import matplotlib.pyplot as plt
import json
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)
#Authentication
twitter_api = twitter.Twitter(auth=auth)
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

translator = Translator()

#functions to process tweets
def sentiment_scores(sentence):
    cleaned_tweet = clean_tweet(sentence)
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(cleaned_tweet)

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        return "positive"

    elif sentiment_dict['compound'] <= - 0.05:
        return "negative"

    else:
        return "neutral"

def clean_tweet(tweet):
    '''
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    '''
    print("Uncleaned tweet")
    print(tweet)
    tokenizedTweet =  ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ / \ / \S+)", " ", tweet).split())
    print("Tokenized tweet")
    print(tokenizedTweet)
    tranlatedTweet = translator.translate(tokenizedTweet)
    print("Tranlated tweet")
    print(tranlatedTweet.text)
    return tranlatedTweet.text



def get_tweet_sentiment(tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'
numTimesToRun = 1
numOfTweets = 50
searchParams = {
    "locations" : {
#        "Helsinki Finland" : '24.840226, 60.146301, 25.068389, 60.243535',
#        "Minsk Belarus" : '27.452519,53.844522,27.692357,53.966406',
        "Bengaluru" : '77.522668,12.925527,77.691964,13.035670',
#        "Moscow Russia" : '37.460891, 55.627444, 37.776366, 55.870121',
#        "Washington DC" : '-77.162969,38.823328,-76.945040,38.973292',
#        "San Francisco" : '-122.515622,37.712600,-122.382400,37.812839',
#        "Bay Area" : '-122.542074,37.121963,-121.813992,38.171283',
#        "Sacramento" : '-121.571318,38.398293,-121.288856,38.693626',
#        "Los Angeles" : '-118.405629,33.889110,-118.021678,34.165535',
#        "Lassen County" : '-121.229516,40.147150,-120.022058,41.172865',
#        "Central Valley" : '-120.010066,35.318959,-118.817885,36.919114'
        "United States" : '-122.986677,25.847657,-58.636563,44.852504',
#        "Southern states" : '-101.567989,27.323442,-75.382242,36.519984',
#        "West coast" : '-125.097450,32.270996,-117.283131,48.858659',
#        "East coast" : '-77.949263,36.603825,-67.942736,44.914868'
#        "Buffalo New York" : '-78.906832,42.839550,-78.790353,42.959176',
#        "Lafayette Louisiana" : '-92.094541,30.153526,-91.977013,30.284586',
#        "Tyler Texas" : '-95.337517,32.255186,-95.272889,32.378907',
#        "Knoxville Tennesse" : '-84.010900,35.932272,-83.844445,36.049789'
    },
    "searchGroups" : {
#        "left-wing" : 'biden,democrat,liberal',
#        "right-wing" : 'trump,GOP,republican,conservative'
        "pro-russian" : 'Russia,Putin',
        "pro-ukrainin" : 'Ukraine,nato,zelensky'
#        "Matt Haney" : 'matt haney,matthaneysf',
#        "David Campos" : 'david campos,DavidCamposSF',
#        "Gavin Newsom" : 'gavin newsom,GavinNewsom,newsom',
#        "Nancy Pelosi" : 'nancy pelosi,SpeakerPelosi,pelosi',
#        "Joe Biden" : 'biden,joe biden,potus',
#        "Donald Trump" : 'trump,donal trump,DonaldTrump',
#        "Kamala Harris" : 'KamalaHarris,kamala harris,kamala',
#        "Pete Buttigieg" : 'PeteButtigieg,buttigieg',
#        "Bernie Sander" : 'BernieSanders,bernie'
#        "Biden" : 'Joe biden,biden,potus',
#        "Trump" : 'trump,donald trump,donaldtrump'
    }
}

runCount = 0
while(runCount != numTimesToRun):
    data = {}
    if(runCount != 0):
        print("Sleeping for 15 minutes")
        time.sleep(900)
    file2 = open('run' + str(runCount) + 'Tweets.txt', 'w+')
    for locationName, coords in searchParams['locations'].items():
        data[locationName] = {}
        for searchGroup, values in searchParams['searchGroups'].items():
            print("searching for "+searchGroup +" tweets in "+ locationName)
            stream = twitter_stream.statuses.filter(track=values, locations=coords)
            tweets = []
            count = 0
            posCount = 0
            negCount = 0
            neutral = 0
            analyizedTweets = []
            for tweet in stream:
                print(count)
                count+=1
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}
                # saving text of tweet
                parsed_tweet['text'] = tweet['text']
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = sentiment_scores(tweet['text'])

                # appending parsed tweet to tweets list
                if tweet['retweet_count'] > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)

                        if(parsed_tweet['sentiment']=='negative'):
                            negCount+=1
                        elif(parsed_tweet['sentiment']=='positive'):
                            posCount+=1
                        else:
                            neutral+=1

                        analyizedTweets.append(parsed_tweet)
                else:
                    if (parsed_tweet['sentiment'] == 'negative'):
                        negCount += 1
                    elif (parsed_tweet['sentiment'] == 'positive'):
                        posCount += 1
                    else:
                        neutral += 1

                    analyizedTweets.append(parsed_tweet)

                if(count == numOfTweets):
                    #remove neutral and normalize
                    posAndNeg = (posCount/numOfTweets + negCount/numOfTweets)
                    posPercent = ((posCount/numOfTweets)/posAndNeg)*100
                    negPercent = ((negCount / numOfTweets)/posAndNeg)*100
                    data[locationName][searchGroup] = [posPercent, negPercent]
                    print("Positive tweet percentage: "+str(posPercent)+"\n")
                    print("Negative tweet percentage: "+str(negPercent)+"\n\n")
                    print("pos: "+str(posCount)+", neg: "+str(negCount)+", neut: "+str(neutral)+"\n")
                    for tweet in analyizedTweets:
                        file2.write(searchGroup)
                        file2.write(json.dumps(tweet))
                        file2.write("\n")
                    break
    print('run '+str(runCount)+' completed')
    print(data)

    x = len(data.items())
    y = len(list(data.values())[0])
    print(str(x)+","+str(y))
    fig, ax1 = plt.subplots(x, y,squeeze=False)
    x = 0
    y = 0
    for locationName, results in data.items():
        for searchGroupName, percentages in data[locationName].items():
            ax1[x,y].pie(percentages, labels=["Positive", "Negative"], autopct='%1.1f%%')
            ax1[x,y].set_title(locationName + " "+ searchGroupName)
            ax1[x,y].axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            y+=1
        y=0
        x+=1

    plt.show()
    runCount +=1