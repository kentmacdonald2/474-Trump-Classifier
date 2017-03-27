#!/usr/bin/env python
# encoding: utf-8
# -*- coding: utf-8 -*-

import tweepy  # https://github.com/tweepy/tweepy
import random
import string
import re

# Twitter API credentials
consumer_key = "91AHqTh4QNcWnu6PNHYMRorxs"
consumer_secret = "N68gf9HDiOnhRILj4ncZTKOvdazUaDwkfF6xzp5A5hL6dqwDCS"
access_key = "188460439-G3KzsXZnbq6eYxYasU7lVPfkNXUv5iwMtqQfWCLj"
access_secret = "IHhrUATJrkuxH6rcBU22Oq3gQi7X7jtvkhYYKiEYwCFwT"

non_trump_tweets = []
trump_tweets = []

def get_all_tweets(screen_names, is_trump):
    for screen_name in screen_names:
        print("Getting Tweets from: \"@"+ screen_name + "\"")
        # Twitter only allows access to a users most recent 3240 tweets with this method

        # authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        # initialize a list to hold all the tweepy Tweets
        alltweets = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name=screen_name, count=200)

        # save most recent tweets
        alltweets.extend(new_tweets)

        # save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)

            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1


        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
        tweets = []
        for tweet in outtweets:
            tweets.append(tweet[2].__str__()[2:-1])
        punct = [",", ".", "\"", "!", "\'","(",")",":","-"]
        if is_trump:
            for tweet in outtweets:
                current_tweet = tweet[2].__str__()[2:-1]
                current_tweet = current_tweet.translate(string.punctuation)
                current_tweet = current_tweet.lower()
                for curr in punct:
                    current_tweet = current_tweet.replace(curr, "")
                re.sub('(\\...)', ' ', current_tweet)
                trump_tweets.append(current_tweet)
        else:
            for tweet in outtweets:
                current_tweet = tweet[2].__str__()[2:-1]
                current_tweet = current_tweet.translate(string.punctuation)
                current_tweet = current_tweet.lower()
                for curr in punct:
                    current_tweet = current_tweet.replace(curr, "")
                re.sub('(\\...)', ' ', current_tweet)
                non_trump_tweets.append(current_tweet)


def concat_files(filenames, outfilename):
    with open(outfilename, 'w') as outfile:
        for fname in filenames:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)


def write_files():
    train_data = open("traindata.txt", "w")
    train_labels = open("trainlabels.txt", "w")
    test_data = open("testdata.txt", "w")
    test_labels = open("testlabels.txt", "w")

    raw_data = open("data.txt", "w")
    raw_labels = open("labels.txt", "w")

    random.shuffle(non_trump_tweets)
    random.shuffle(trump_tweets)

    print("Writing Files for K-Folding")
    for i in range(3000):
        raw_data.write(trump_tweets[i] + "\n")
        raw_labels.write("1\n")
        raw_data.write(non_trump_tweets[i] + "\n" )
        raw_labels.write("0\n")

    print("Writing Training Files ")
    for _ in range(1000):
        train_data.write(trump_tweets[0] + "\n")
        trump_tweets.pop(0)
        train_labels.write("1\n")

        train_data.write(non_trump_tweets[0] + "\n")
        non_trump_tweets.pop(0)
        train_labels.write("0\n")

    print("Writing Testing Files ")
    for _ in range(1000):
        test_data.write(trump_tweets[0] + "\n")
        trump_tweets.pop(0)
        test_labels.write("1\n")

        test_data.write(non_trump_tweets[0] + "\n")
        non_trump_tweets.pop(0)
        test_labels.write("0\n")


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets(["realDonaldTrump"], True)
    get_all_tweets(["BarackObama"], False)
    write_files()
