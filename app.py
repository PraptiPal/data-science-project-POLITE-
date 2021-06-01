from typing import Counter
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
import re
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer, WordNetLemmatizer
# from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob
import streamlit as st
import pandas as pd
# from streamlit.elements.image import _format_from_image_type
from tweepy_init import create_api
import matplotlib.pyplot as plt
from visualization import *


@st.cache()
def init():
    return create_api()


api = init()

st.title("Sentiment Analysis For Tweets ")
st.image('NLP.jpg')

sidebar = st.sidebar
sidebar.header("Choose Your Option")
choices = ["Select any option below", "Project Overview", "Analyse Tweets"]
selOpt = sidebar.selectbox("Choose what to do", choices)


def ProjectOverview():
    st.markdown("""
    ## Reviewing the sentiments 
    Polite?
    :What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user.
    It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.
    ! Flow-Chart-Sentiment-Analysis.png

    ### Features of Project
    1. Fetch the tweets from twitter using api
    2. Cleaning the tweets so as to accurately so that sentiment analyzing takes place accurately
    3. Counting the positive, negative and neutral tweets and also determining the subjectivity of the tweets.
    ! sentiment_analysis.jpg
    4. The best way to understand the analysis is through visualization. The results are displayed in form of graphs
    for a better understanding.

    
    """)


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
                sentiments, subjectivity = generateSentiment(pre_tweets)
                visualize(sentiments, subjectivity)


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
    subjctivity = []
    for tweet in tweets:
        blob = TextBlob(tweet)
        subjctivity.append(blob.subjectivity)
        if(blob.sentiment.polarity > 0):
            sentimentList['positive'] += 1
        elif(blob.sentiment.polarity < 0):
            sentimentList['negative'] += 1
        elif(blob.sentiment.polarity == 0):
            sentimentList['neutral'] += 1

    # st.write(sentimentList)
    # st.write(subjctivity)
    # visualize(sentimentList, subjctivity)
    return sentimentList, subjctivity


def visualize(sentiments, subjctivity):

    st.header("Sentiment Results")

    fig = plotBar(tuple(sentiments.keys()), list(
        sentiments.values()), 'My title')

    st.plotly_chart(fig)

    st.header("Subjectivity Results")
    df = pd.DataFrame(subjctivity).rename(columns={0: 'Subjectivity'})
    st.dataframe(df)
    fig = plotHistogram(df, 'Subjectivity')
    st.plotly_chart(fig)
    # fig, ax = plt.subplots()
    # ax.hist(subjctivity, bins=20)
    # st.pyplot(fig)


if selOpt == choices[1]:
    ProjectOverview()
if selOpt == choices[2]:
    AnalyseSentiment()
