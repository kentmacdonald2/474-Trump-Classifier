# toy code, not meaningful

import tweepy

# create api instance
consumer_key = 'EfqaL86DG4IB5S1dByhRe6IDM'
consumer_secret = '30bNKdiL8XAJB9z3RLbETwUSCz5dDiVJ7pi8kGuKmqpQlILTZf'
access_token = '3883647074-tMKNRUxnIusvnG59dEEdr3dtC00O6H5fJPJwJvG'
access_token_secret = 'mfAW95YhLcBOsEGNOEoSDQoZ2DvVcZ3bu6jKpmWtlD7ok'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)