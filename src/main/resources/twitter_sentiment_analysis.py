import sys, tweepy
import matplotlib.pyplot as plt 
from textblob import TextBlob
from pymongo import MongoClient
from datetime import datetime
import json
try:
#    conn = MongoClient()
    conn = MongoClient("localhost",27017)
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")
db = conn.kpro_tweet_analysis
collection = db.tweet_collection
def percentage(part, whole):
	return 100 * float(part)/float(whole)
access_token = "2428571131-38eTGbUqxW1t7kobx4mvd0PJ82bH0tfedBwwc6c"
access_token_secret = "Ldh0qwmNC7b0AaKpho5cTLErO20lvh1oQ1yjjnEIZMk5P"
consumer_key =  "8Lzk2BPOjlINHfTPb99jLuamW"
consumer_secret =  "nxOvL4Qavg149XeXcyXVPzrPuk6k0QrUghVdpC66eSP5sb8QsM"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,  access_token_secret)
api = tweepy.API(auth)
searchTerm = input("Enter keyword to search about :")
noOfSearchTerms = int(input("Enter how many tweets to analyze: "))
tweets = tweepy.Cursor(api.search, q=searchTerm).items(noOfSearchTerms)
positive = 0
negative = 0
neutral = 0
polarity =0
#public_tweets = api.search('Modi')
for tweet in tweets:

 	#analysis = TextBlob(tweet.text)
 	#print(analysis.sentiment)

 	analysis = TextBlob(tweet.text)
 	sentiment = analysis.polarity
 	# print(analysis.polarity)
 	if analysis.polarity < 0.00:
 		negative_twitt="Negative"
 	elif analysis.polarity > 0.00:
 	    negative_twitt="positive"
 	elif analysis.polarity == 0.00:
 	    negative_twitt="neutral"
 	tweettext = tweet.text
 	id_str = tweet.id_str
 	tweetlocation = tweet.author.location
 	tweet = tweet.author.location.city
 	name = tweet.user.screen_name
 	retweet = tweet.retweet_count
 	user_created = tweet.user.created_at
 	created = tweet.created_at 
 	followers = tweet.user.followers_count
 	#result = db.objects.insert_one({"last_modified": datetime.utcnow()})
 	tweet_data={'topic_name':searchTerm,'status_text':tweettext, 'status_id':id_str, 'location':tweetlocation,
 	'user_screen_name':name, 'user_retweet':retweet, 'tweet_sent':created, 'User_followers':followers,
 	'tweet_sentiment':sentiment,'status_twitt':negative_twitt}
 	print(tweet_data)
 	#datajson = json.loads(tweet_data)
 	#print(datajson)
 	collection.insert(tweet_data)
 	polarity += analysis.sentiment.polarity
 	if analysis.sentiment.polarity == 0:
 		neutral += 1
 	elif analysis.sentiment.polarity < 0.00:
 	    negative += 1
 	elif analysis.sentiment.polarity > 0.00:
 	    positive += 1	
positive = percentage(positive, noOfSearchTerms)
negative = percentage(negative, noOfSearchTerms)
neutral = percentage(neutral, noOfSearchTerms)
positive_per = format(positive, '.2f')
neutral_per = format(neutral, '.2f')
negative_per = format(negative, '.2f')
# print(positive_per)
# print(neutral_per)
# print(negative_per)
# print("How people are reaction on" + searchTerm + " by analysis " + str(noOfSearchTerms) + " Tweets.")	

overall={'positive%':positive_per, 'neutral%':neutral_per, 'negative%':negative_per}
#  	'user_screen_name':name, 'user_retweet':retweet, 'tweet_sent':created, 'User_followers':followers,
#  	'tweet_sentiment':sentiment}
db.percentage_sentiment.insert(overall)
# if(polarity == 0):
#  	print("Neutral")
# elif(polarity < 0):
#     print("Negative")
# elif(polarity > 0):
#     print("Positive")

#percentage_sentiment = ['Positive ['+str(positive)+'%]', 'Neutral [' + str(neutral) + '%]', 'Negative [' + str(negative) + '%]'] 
#print(percentage_sentiment)    
