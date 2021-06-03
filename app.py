from typing import Counter
from tweepy_init import create_api
import nltk
import re
# nltk.download('popular')
from textblob import TextBlob
import streamlit as st
import pandas as pd
from streamlit.elements.image import _format_from_image_type
#from tweepy_init import create_api
#from visualization import *


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
        #btn = st.checkbox('Submit')
        if user_input:
           fetchTweets(user_input) 
        
            #raw_tweets = []
            #for tweet in tweets_data:
                # raw_tweets.append(tweet.text)
            #pre_tweets = fetchTweets(user_input)
                 #st.write(raw_tweets)
            # from here we will write logic for generating sentiment and visualizing and storing in database

            #btn = st.checkbox('Visualize Result')
            #if btn:
             #   visualize()


def fetchTweets(user_input, count=100):
    tweets_data = api.search(user_input=user_input, count=count)
    #print(tweets_data[0])

  #  raw_tweets = []
    
    for tweet in tweets_data:
        st.write(tweet.text)

    return tweets_data

    

    #print()


#def cleanTweets():
    #pass


#def generateSetiment():
#    pass


#def visualize():

   # st.header("Sentiment Results")
    #sentiments = {
     #   'positive': 30,
      #  'negative': 27,
       # 'neutral': 43
    #}

    #st.plotly_chart(plotBar(list(sentiments.keys()),
     #                       list(sentiments.values())))


if selOpt == choices[1]:
    AnalyseSentiment()
#st.header("What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user. It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.")
#sidebar=st.sidebar
#sidebar.title("POLITE-Analyzing sentiments in twitter")
#sidebar.header("Choose Your Option")
#choices=["Select OPtion","enter a username"]
#selOpt = sidebar.selectbox("Choose what to do", choices)

def visualize(sentiments, subjctivity):

    st.header("Sentiment Results")


    
