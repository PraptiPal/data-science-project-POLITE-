from typing import Counter
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer, WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
import streamlit as st
import pandas as pd
from streamlit.elements.image import _format_from_image_type
from tweepy_init import create_api
from visualization import *


@st.cache()
def init():
    return create_api()


api = init()

st.title("Sentiment Analysis For Tweets ")
st.header("What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user. It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.")
st.image('NLP.jpg')

sidebar = st.sidebar
sidebar.header("Choose Your Option")
choices = ["Select any option below", "Analyse Tweets"]
selOpt = sidebar.selectbox("Choose what to do", choices)


def AnalyseSentiment():
    with st.spinner("Loading View... "):
        user_input = st.text_input("Enter the Twitter Handle or Hashtag")
        btn = st.checkbox('Submit')
        if user_input and btn:
            pre_tweets = fetchTweets(user_input)
            st.write(pre_tweets)
            # from here we will write logic for generating sentiment and visualizing and storing in database

            btn = st.checkbox('Visualize Result')
            if btn:
                sentiments = generateSentiment(pre_tweets)
                visualize(sentiments)


@st.cache()
def fetchTweets(keyword, c=100):
    print('tweets fetched')
    tweets_data = api.search(keyword, count=c)
    # print(tweets_data[0])

    raw_tweets = []
    for tweet in tweets_data:
        raw_tweets.append(tweet.text)
    cleaned_tweets = cleanTweets(raw_tweets)

    return cleaned_tweets


def cleanTweets(tweets):

    cleanedtweets = []
    for twt in tweets:
        tweet = list()
        word = twt.split()
        for w in word:
            tweet.append(w)
        tweet = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in tweet]
        cleanedtweets.append(' '.join(tweet))

    return cleanedtweets


def generateSentiment(tweets):
    sentimentList = {}.fromkeys(['positive', 'neutral', 'negative'], 0)

    for tweet in tweets:
        blob = TextBlob(tweet)
        if(blob.sentiment.polarity > 0):
            sentimentList['positive'] += 1
        elif(blob.sentiment.polarity < 0):
            sentimentList['negative'] += 1
        elif(blob.sentiment.polarity == 0):
            sentimentList['neutral'] += 1

    st.write(sentimentList)
    return sentimentList


def visualize(sentiments):

    st.header("Sentiment Results")

    st.plotly_chart(plotBar(list(sentiments.keys()),
                            list(sentiments.values())))


if selOpt == choices[1]:
    AnalyseSentiment()
