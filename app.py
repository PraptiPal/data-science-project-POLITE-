from os import fdopen, name
from typing import Container, Counter
import nltk
import re
from numpy import average, negative, positive
from textblob import TextBlob, sentiments
import streamlit as st
import pandas as pd
from textblob.blob import Word
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
choices = ["Project Overview", "Analyse Tweets", "View Previous Searches"]
selOpt = sidebar.selectbox("Choose what to do", choices)


def ProjectOverview():

    st.markdown("""
    ## Reviewing the sentiments 
    Polite?
    :What does Polite Do? The project is designed and developed to analyze the sentiments mentioned in the tweet of an user.
    It analyzes whether a tweet is written to send positive message or negative message or is a neutral sentence.
    """, unsafe_allow_html=True)
    st.image('sentiment-analysis.gif')
    st.write('')
    st.markdown(f"""
    ### Features of Project
    1. Fetch the tweets from twitter using api
    2. Cleaning the tweets so as to accurately so that sentiment analyzing takes place accurately
    3. Counting the positive, negative and neutral tweets and also determining the subjectivity of the tweets.
    **Parameters used to determine the sentiments are -- POLARITY and SUBJECTIVITY**
    4. The best way to understand the analysis is through visualization. The results are displayed in form of graphs
    for a better understanding. 
    """, unsafe_allow_html=True)

    st.header('Flowchart that represents the detailed process to handle the tweets')
    st.write('')
    st.image('Flow-Chart-Sentiment-Analysis.png')


def AnalyseSentiment():
    with st.spinner("Loading View... "):
        show_tweets = sidebar.checkbox('Show Tweets')
        user_input = st.text_input(
            "Enter the Twitter Handle or Hashtag", value="@Kurz_Gesagt")
        tweet_count = st.number_input(
            "Enter the number of tweets you want to analyze", step=1, min_value=1, max_value=500, value=50)
        btn = st.checkbox('Submit')
        if user_input and btn:
            user_details = getuser(user_input)
            st.write('Profile picture')
            st.markdown(f"""
            <img style="border-radius: 100%;" src="{user_details['avatar']}">
            <h2>{user_details['name']}</h2>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <table border = "3">
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
                <tr>
                <td>Profile Verified</td>
                <td>{user_details['verified']}</td>
                </tr>
                </table>
                """, unsafe_allow_html=True)

            # st.write(user_details)
            pre_tweets = fetchTweets(user_input, tweet_count)
            st.write(pre_tweets)
            #displaytweets = pre_tweets
            for i in range(0, int(tweet_count-1)):
                st.markdown(f""" 
                <table border = "2">  
                <tr>{pre_tweets[i]}</tr>
                </table>
                """, unsafe_allow_html=True)

            # from here we will write logic for generating sentiment and visualizing and storing in database

            btn = st.checkbox('Visualize Result')
            if btn:
                sentiments, subjectivity = generateSentiment(
                    pre_tweets, tweet_count)
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
    profile['description'] = user_details._json['description']
    profile['created'] = user_details._json['created_at']
    profile['followers'] = user_details._json['followers_count']
    profile['verified'] = user_details._json['verified']
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
        Word = twt.split()
        for w in Word:
            tweet.append(w)
        tweet = [re.sub(r'[^A-Za-z0-9]+', '', x) for x in tweet]
        cleanedtweets.append(' '.join(tweet))
    return cleanedtweets


def generateSentiment(tweets, count):
    n = float(count)
    sentimentList = {}.fromkeys(['positive', 'neutral', 'negative'], 0)
    subjctivity = []
    btn = st.checkbox('View Sentiment by Tweets')
    for tweet in tweets:
        if btn:
            st.write(tweet)
            analysis = TextBlob(tweet)
            st.write(analysis.sentiment)
            if analysis.sentiment[0] > 0:
                st.write('positive')
            elif analysis.sentiment[0] < 0:
                st.write('negative')
            else:
                st.write('neutral')

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
    elif sentimentList['negative'] > sentimentList['neutral'] & sentimentList['negative'] > sentimentList['positive']:
        st.write('mostly tweets are negative')
    else:
        st.write('Mostly tweets are neutral')
    total = 0
    for s in subjctivity:
        total += float(s)
    average = float(total/n)
    st.write(f'The average subjectivity for the tweets are {average}')
    return sentimentList, subjctivity


def visualize(sentiments, subjctivity):

    df = pd.DataFrame(subjctivity).rename(columns={0: 'Subjectivity'})
    fig = plotHistogram(df, 'Subjectivity')

    fig1 = plotBar(tuple(sentiments.keys()), list(
        sentiments.values()), 'Showing the count of positive negative and neutral tweets ')

    pie_fig2 = plotpie(tuple(sentiments.keys()), list(
        sentiments.values()), 'Pie Chart')

    st.header("Subjectivity Results")
    col1, col2 = st.beta_columns(2)
    col1.subheader("A histogram showing the subjectivity of the tweets")
    col1.plotly_chart(fig)
    col2.subheader("Dataframe showing the subjectivity")
    col2.dataframe(df)

    st.header("Sentiment Results")
    col1, col2 = st.beta_columns(2)
    col1.subheader(
        "Line chart showing the count of positive, negative and neutral tweets")
    col1.plotly_chart(fig1)
    col2.subheader("Pie chart to show it in percentage form")
    col2.plotly_chart(pie_fig2)


def viewPrevious():
    try:
        searches = session.query(Search).all()
        keywords = [search.keyword for search in searches]

        selKeyword = st.selectbox(options=keywords, label="Select Keyword")

        selObj = session.query(Search).filter_by(keyword=selKeyword).first()

        st.markdown(f"""
            ### Date : {selObj.date}
        """)

        st.markdown(f"""
            ### Sentiment : {selObj.sentiment}
        """)

        st.markdown(f"""
            ### Subjectivity : {selObj.subjectivity}
        """)

    except Exception as e:
        st.error('Something went wrong')
        print(e)


if selOpt == choices[0]:
    ProjectOverview()
elif selOpt == choices[1]:
    AnalyseSentiment()
elif selOpt == choices[2]:
    viewPrevious()
