from typing import Counter
from twitter import create_api
import nltk
# nltk.download('popular')
from textblob import TextBlob
import streamlit as st
import pandas as pd
from streamlit.elements.image import _format_from_image_type
from tweepy_init import create_api

api = create_api()
st.title("Sentiment Analysis For Tweets ")
st.image('NLP.jpg')
st.header("")

sidebar = st.sidebar
sidebar.header("Choose Your Option")
choices = ["Select any option below", "Analyse Tweets"]
selOpt = sidebar.selectbox("Choose what to do", choices)


def AnalyseSentiment():
    with st.spinner("Loading View... "):
        user_input = st.text_input("Enter the Twitter Handle or Hashtag")

        if user_input:
            pre_tweets = fetchTweets(user_input)

            # from here we will write logic for generating sentiment and visualizing and storing in database
            

def fetchTweets(keyword, c = 100):
    tweets_data = api.search(keyword, count = c)
    print(tweets_data[0])

    raw_tweets = []
    for tweet in tweets_data:
        raw_tweets.append(tweet.text)

    cleaned_tweets = cleanTweets(raw_tweets)

    return cleaned_tweets

def cleanTweets(tweets):
    pass


def generateSetiment():
    pass


def visualize():
    pass


if selOpt == choices[1]:
    AnalyseSentiment()
