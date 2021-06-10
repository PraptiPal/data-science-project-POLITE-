from os import fdopen, name
from typing import Container, Counter
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
import re
from numpy import negative, positive
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer, WordNetLemmatizer
# from nltk.tokenize import RegexpTokenizer
from textblob import TextBlob, sentiments
import streamlit as st
import pandas as pd
from textblob.blob import Word
# from streamlit.elements.image import _format_from_image_type
from tweepy_init import create_api
import matplotlib.pyplot as plt
from visualization import *
from database import Search
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///db.sqlite3')

Session = sessionmaker(bind=engine)
session = Session()


@st.cache(allow_output_mutation=True)
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
    st.image('sentiment_analysis.jpg')
    st.markdown("""
    ## Reviewing the sentiments 
    Polite?
    :What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user.
    It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.
    """, unsafe_allow_html=True)
    st.header('Flowchart that represents the detailed process to handle the tweets')
    st.markdown('#')
    st.image('Flow-Chart-Sentiment-Analysis.png')

    st.markdown(f"""
    ![alt text for screen readers](E:\data-science-project(POLITE)\sentiment_analysis.jpg "Text to show on mouseover")
    ### Features of Project
    1. Fetch the tweets from twitter using api
    2. Cleaning the tweets so as to accurately so that sentiment analyzing takes place accurately
    3. Counting the positive, negative and neutral tweets and also determining the subjectivity of the tweets.
    **Parameters used to determin the sentiments are -- POLARITY and SUBJECTIVITY**
    4. The best way to understand the analysis is through visualization. The results are displayed in form of graphs
    for a better understanding. 
    """, unsafe_allow_html=True)


def AnalyseSentiment():
    with st.spinner("Loading View... "):
        user_input = st.text_input("Enter the Twitter Handle or Hashtag")
        tweet_count = st.text_input(
            "Enter the number of tweets you want to analyze")
        btn = st.checkbox('Submit')
        if user_input and btn:
            user_details = getuser(user_input)
            # st.markdown(f"""
            # <img style="border-radius: 100%;" src="{user_details['avatar']}">
            # <h2>{user_details['name']}</h2>
            # """, unsafe_allow_html=True)

            st.markdown(f"""
                <h1><b>User Account Details</b></h1>
                <hr/>
                <img style="border-radius: 100%;" src="{user_details['avatar']}">
                <table style = "width:100%">
                <tr><td>Account Name : {user_details['name']}</td></tr>
                <tr><td>Handle Name {user_details['screen_name']}</td></tr>          
                <tr><td>Account Description {user_details['description']}</td></tr>
                <tr><td>Account created on {user_details['created']}</td></tr>
                <tr><td>Number Of Followers {user_details['followers']}</td></tr>
                </table>
                """, unsafe_allow_html=True)

            # st.write(user_details)
            pre_tweets = fetchTweets(user_input, tweet_count)
            st.write(pre_tweets)
            # from here we will write logic for generating sentiment and visualizing and storing in database

            btn = st.checkbox('Visualize Result')
            if btn:
                sentiments, subjectivity = generateSentiment(pre_tweets)
                visualize(sentiments, subjectivity)

                saveData = st.checkbox('Save Data')
                if saveData:
                    try:
                        search = Search(
                            keyword=user_input, sentiment=f"{sentiments}", subjectivity=f"{subjectivity}")
                        session.add(search)
                        session.commit()
                        st.success('Data Saved')
                    except Exception as e:
                        st.error('Something went wrong')
                        print(e)


@st.cache()
def getuser(username):

    profile = {}
    user_details = api.get_user(username)
    profile['name'] = user_details._json['name']
    profile['avatar'] = user_details._json['profile_image_url_https']
    profile['screen_name'] = user_details._json['profile_image_url_https']
    profile['description'] = user_details._json['description']
    profile['created'] = user_details._json['created_at']
    profile['followers'] = user_details._json['followers_count']
    return profile


@st.cache()
def fetchTweets(keyword, c):
    print('tweets fetched')
    tweets_data = api.search(keyword, count=c)
    # print(tweets_data[0])

    raw_tweets = []
    for tweet in tweets_data:
        raw_tweets.append(tweet.text)
    cleaned_Tweets = cleanTweets(raw_tweets)

    return cleaned_Tweets
    


def cleanTweets(tweets):
    cleanedtweets = []
    for twt in tweets:
        tweet = list()
        Word = twt.split()
        for w in Word:
            tweet.append(w)
        tweet = [re.sub(r' [^A-Za-z0-9]+' , '', x)for x in tweet]  
        cleanedtweets.append(''.join(tweet))
    return cleanedtweets      

            

def generateSentiment(tweets):
    sentimentList = {}.fromkeys(['positive', 'neutral', 'negative'], 0)
    subjctivity = []
    for tweet in tweets:
        st.write(tweet)
        analysis=TextBlob(tweet)
        st.write(analysis.sentiment)
        if analysis.sentiment[0]>0:
            st.write('positive')

        else:
            st.write('negative')    


        blob = TextBlob(tweet)
        subjctivity.append(blob.subjectivity)
        if(blob.sentiment.polarity > 0):
            sentimentList['positive'] += 1
        elif(blob.sentiment.polarity < 0):
            sentimentList['negative'] += 1
        elif(blob.sentiment.polarity == 0):
            sentimentList['neutral'] += 1

    if sentimentList['positive'] > sentimentList['neutral'] & sentimentList['positive'] > sentimentList['negative']:
        st.write('mostly tweets are positive')

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
    fig= plotHistogram(df, 'Subjectivity')

    # fig, ax = plt.subplots()
    # ax.hist(subjctivity, bins=20)
    # st.pyplot(fig)
    # df1 = pd.DataFrame(sentiments)
    # st.dataframe(df1)

    pie_fig2 = plotpie(tuple(sentiments.keys()), list(
        sentiments.values()), 'My title')
    st.plotly_chart(pie_fig2)
    col1, col2 =st.beta_columns([3,1])
    col1.subheader("A wide column with  a chart")
    col1.plotly_chart(fig)

    col2.subheader("A narrow column with the data")
    col2.plotly_chart(pie_fig2)

    # fig2=piechart(df,'sentimentList')









if selOpt == choices[1]:
    ProjectOverview()
if selOpt == choices[2]:
    AnalyseSentiment()
