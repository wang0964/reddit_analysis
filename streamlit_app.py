import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
import streamlit as st
import praw
import datetime

# Set the page title and description
st.title('Sentiment Analysis for Reddit')
st.write('''
This app collects live Reddit posts and comments and analyzes their sentiment in real time.
''')




reddit = praw.Reddit(
    client_id='d6PhF1j_wq2xvhOWhpZ7kA',
    client_secret='dmFNcPLk1XsMlP1tsqvaNAki-pOjNw',
    password='Elaine-xgz@0309',
    user_agent='my user agent for college project, by Xinwei',
    username='Born-Medicine-4623'
)
reddit.read_only = True



if 'topics_loaded' not in st.session_state:
    st.session_state['topics_loaded'] = False

if 'topic_title_list' not in st.session_state:
    st.session_state['topic_title_list'] = []

if 'topic_link_list' not in st.session_state:
    st.session_state['topic_link_list'] = []




with st.form('user_inputs'):
    st.subheader('Select a Reddit Category:')
    
    category = st.selectbox('Category:', options=['Hot', 'New', 'Top', 'Controversial', 'Rising', 'Random'] )
    time_filter = st.selectbox('Time Filter:', options=['Last Year', 'Last Month', 'Last Week', 'Last Day'] )
    top_n = st.selectbox( 'Top n:', options=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] )

    submitted = st.form_submit_button('Get Topic List')

time_filter_dict = {
    'Last Year': 'year',
    'Last Month': 'month',
    'Last Week': 'week',
    'Last Day': 'day'
}

topic_title_list=[]
topic_link_list=[]

if submitted:
    subreddit = reddit.subreddit('all')

    if category == 'Hot':
        topics = subreddit.hot(limit=int(top_n))
    elif category == 'New':
        topics = subreddit.new(limit=int(top_n))
    elif category == 'Top':
        topics = subreddit.top(
            time_filter=time_filter_dict[time_filter],
            limit=int(top_n)
        )
    elif category == 'Controversial':
        topics = subreddit.controversial(
            time_filter=time_filter_dict[time_filter],
            limit=int(top_n)
        )
    elif category == 'Rising':
        topics = subreddit.rising(limit=int(top_n))
    elif category == 'Random':
        topics = [subreddit.random() for _ in range(int(top_n))]
    else:
        topics = []

    for topic in topics:
        topic_title_list.append(topic.title)
        topic_link_list.append("https://www.reddit.com" + topic.permalink)

    # save search content to session_state
    st.session_state['topic_title_list'] = topic_title_list
    st.session_state['topic_link_list'] = topic_link_list
    st.session_state['topics_loaded'] = True

# determine whether 'Get Topic List' has been excuted
if st.session_state['topics_loaded']:
    with st.form('specify a topic'):
        st.subheader('Select a topic to analyse:')
        selected_topic = st.selectbox('Specify a topic:', options=st.session_state['topic_title_list'])
        analyze = st.form_submit_button('Analyze Topic Sentiment')

        if analyze:

            idx = st.session_state['topic_title_list'].index(selected_topic)
            st.write(f"[{selected_topic}]({st.session_state['topic_link_list'][idx]})")