from typing import Counter
from twitter import create_api
import nltk
# nltk.download('popular')
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
st.image('NLP.jpg')
st.header("")

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
            st.text(pre_tweets)
            # from here we will write logic for generating sentiment and visualizing and storing in database

            btn = st.checkbox('Visualize Result')
            if btn:
                visualize()


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
    return tweets


def generateSetiment():
    pass


def visualize():

    st.header("Sentiment Results")
    sentiments = {
        'positive': 30,
        'negative': 27,
        'neutral': 43
    }

    st.plotly_chart(plotBar(list(sentiments.keys()),
                            list(sentiments.values())))


if selOpt == choices[1]:
    AnalyseSentiment()
st.header("What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user. It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.")
sidebar=st.sidebar
sidebar.title("POLITE-Analyzing sentiments in twitter")
sidebar.header("Choose Your Option")
choices=["Select OPtion","enter a username"]
selOpt = sidebar.selectbox("Choose what to do", choices)



def fetchTweets():
    api= create_api()
    with st.spinner("Loading Viwe..."):
        tweets=st.text_input("enter a username")
        tweets_data=api.search(tweets)
        for tweet in tweets_data:
            st.write(tweet)
            st.write()
            return tweet
        

def cleanTweets():
    twt=fetchTweets()
    tokens = nltk.sent_tokenize(twt)



if selOpt == choices[1]:
    fetchTweets()
