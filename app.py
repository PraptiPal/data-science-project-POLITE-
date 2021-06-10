from os import name
from typing import Counter
import nltk
# nltk.download('stopwords')
# nltk.download('wordnet')
import re
from numpy import negative, positive
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
choices = ["Project Overview", "Analyse Tweets"]
selOpt = sidebar.selectbox("Choose what to do", choices)


def ProjectOverview():
    st.image('sentiment-analysis.gif')
    st.markdown("""
    ## Reviewing the sentiments 
    Polite?
    :What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user.
    It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.
    """, unsafe_allow_html=True)
    st.header('Flowchart that represents the detailed process to handle the tweets')
<<<<<<< HEAD
    st.write('')
=======
    st.markdown('#')
>>>>>>> 3d7bdf20df71a20b1624c5372e2233a652dcb149
    st.image('Flow-Chart-Sentiment-Analysis.png')
 
    st.markdown(f"""
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
<<<<<<< HEAD
            st.markdown(f"""
            <img style="border-radius: 100%;" src="{user_details['avatar']}">
            <h2>{user_details['name']}</h2>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <table border = "1">
            <tr>
            <th>Property</th>
            <th>Value</th>
            </tr>
            <td>Account Name</td>
            <td>{user_details['name']}</td>
            </tr>
            <tr><td> Handle Name </td>
            <td>{user_details['screen_name']}</td>
            </tr>
            <tr>
            <td>Account Description</td>
            <td>{user_details['description']}</td>
            </tr>
            <tr>
            <td>Account created on</td>
            <td>{user_details['created']}</td>
            </tr>
            <tr>
            <td>Followers</td>
            <td>{user_details['followers']}</td>
            </tr>
            </table>
            """,unsafe_allow_html=True)
            
            #st.write(user_details)
=======
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
>>>>>>> 3d7bdf20df71a20b1624c5372e2233a652dcb149
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
    profile['screen_name'] = user_details._json['screen_name']
    profile['description']=user_details._json['description']
    profile['created']=user_details._json['created_at']
    profile['followers']=user_details._json['followers_count']
    return profile


@st.cache()
def fetchTweets(keyword, c):
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

<<<<<<< HEAD
    if sentimentList['positive']> sentimentList['neutral'] & sentimentList['positive'] > sentimentList['negative']:
=======
    if sentimentList['positive'] > sentimentList['neutral'] & sentimentList['positive'] > sentimentList['negative']:
>>>>>>> 3d7bdf20df71a20b1624c5372e2233a652dcb149
        st.write('mostly tweets are positive')

    # st.write(sentimentList)
    # st.write(subjctivity)
    # visualize(sentimentList, subjctivity)
    return sentimentList, subjctivity


def visualize(sentiments, subjctivity):

    df = pd.DataFrame(subjctivity).rename(columns={0: 'Subjectivity'})
    fig = plotHistogram(df, 'Subjectivity')

    fig1 = plotBar(tuple(sentiments.keys()), list(
        sentiments.values()), 'Showing the count of positive negative and neutral tweets ')

    pie_fig = plotpie(tuple(sentiments.keys()), list(
        sentiments.values()), 'My title')


    st.header("Subjectivity Results")
    col1, col2 = st.beta_columns([2, 2])
    col1.subheader("A histogram showing the subjectivity of the tweets")
    col1.plotly_chart(fig)
    col2.subheader("Dataframe showing the subjectivity")
    col2.dataframe(df)
    
    st.header("Sentiment Results")
    col1, col2 = st.beta_columns([3,1])
    col1.subheader("Line chart showing the count of positive, negative and neutral tweets")
    col1.plotly_chart(fig1)
    col2.subheader("Pie chart to show it in percentage form")
    col2.plotly_chart(pie_fig)
    
    
    


if selOpt == choices[0]:
    ProjectOverview()
if selOpt == choices[1]:    
    AnalyseSentiment()


