import streamlit as st

import datetime
import spacy

# Import custom Reddit initialization modules
import scr.initialization.initpraw as init_reddit

# Import preprocessing modules
import scr.preprocess.preprocess as pp

# Import chart rendering modules
import scr.charts.wordcloud as wordcloud
import scr.charts.slidewindow as slidewindow
import scr.charts.piechart as piechart
import scr.charts.barchart as barchart
import scr.charts.scatterplot as scatterplot
import scr.charts.scatter_comment_len as comment_len
import scr.charts.boxplot as boxplot
import scr.charts.histogram as histogram
import scr.charts.comparison as compare_chart

# Import SQL Server database interaction module
import scr.db.sqlserver as sql


# Initialize authentication state, it stores the login status information.
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Login function
def login():
    st.title('Login in')
    username = st.text_input('User Name:')
    password = st.text_input('Password', type='password')
    login_btn = st.button('Login in')

    # Validate user credentials
    if login_btn:
        if sql.check_account(username,password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success(f'Welcome {username}!')
            st.rerun()
        else:
            st.error('Wrong user name or password')



# Main app section (after login)
if st.session_state['authenticated']:

    # Set the page title and description
    st.title('Sentiment Analysis for Reddit')
    st.write('''
    This app collects live Reddit posts and comments and analyzes their sentiment in real time.
    ''')


    reddit=init_reddit.get_reddit()

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
            topic_link_list.append('https://www.reddit.com' + topic.permalink)

        # Save search content to session_state
        st.session_state['topic_title_list'] = topic_title_list
        st.session_state['topic_link_list'] = topic_link_list
        st.session_state['topics_loaded'] = True

    # Determine whether 'Get Topic List' has been excuted
    if st.session_state['topics_loaded']:
        with st.form('specify a topic'):
            st.subheader('Select a topic to analyze:')
            selected_topic = st.selectbox('Specify a topic:', options=st.session_state['topic_title_list'])
            analyze = st.form_submit_button('Analyze Topic Sentiment')

            if analyze:

                idx = st.session_state['topic_title_list'].index(selected_topic)
                st.write(f'[{selected_topic}]({st.session_state['topic_link_list'][idx]})')

                # Fetch comments from the selected topic
                reddit_comments =  reddit.submission(url=st.session_state['topic_link_list'][idx])
                reddit_comments.comments.replace_more(limit=None)

                # Collect all comments with timestamps
                all_comments = []
                id = 0
                for comment in reddit_comments.comments.list():
                    created = comment.created_utc
                    dt = datetime.datetime.fromtimestamp(created)
                    all_comments.append({'id':comment.id, 'body':comment.body,'created_dt':dt})
                    id += 1

                # print('Title:', reddit_comments.title)
                # print('URL:', 'https://www.reddit.com' + reddit_comments.permalink)
                # for item in all_comments:
                #     print(item)

                # Load spaCy model
                nlp = spacy.load(r'./en_core_web_sm/en_core_web_sm-3.8.0')


                # Clean and process comment text
                text_list = []
                for item in all_comments:
                    text_list.append(pp.clean_words(item['body'], nlp))
                text = ' '.join(text_list)

                # create DataFrame
                df=pp.create_DataFrame(text_list, all_comments)
                # print(df)
                df=pp.remove_deleted_data(df)


                print(f'topicID: {reddit_comments.id}')


                # Store to database
                conn=sql.create_connection()
                sql.append_db(conn, df, reddit_comments )
                conn.close()

                # Render charts
                print('1. wordcloud')
                wordcloud.draw_wordcloud(st,text)

                print('2. slidewindow')
                slidewindow.draw_slidewindow_trend(st,df)

                print('3. histogram')
                histogram.draw_histogram(st,df)

                print('4. piechart')
                piechart.draw_piechart(st, df)

                print('5. barchart1')
                barchart.draw_barchart(st, df,  'cornflowerblue','Top {} Most Frequent Words')

                print('6. barchart2')
                df_neg = df[df['compound'] <= -0.05]
                barchart.draw_barchart(st, df_neg,  'red', 'Top {} Words in Negative Sentiment Comments')

                print('7. barchart3')
                df_pos = df[df['compound'] >= 0.05]
                barchart.draw_barchart(st, df_pos,  'green', 'Top {} Words in Positive Sentiment Comments')

                print('8. scatterplot')
                scatterplot.draw_scatterplot(st, df)

                print('9. comment_len')
                comment_len.draw_scatter_comment_length(st, df)

                print('10. boxplot')
                boxplot.draw_boxplot(st, df)


                print('Load data from database')
                conn=sql.create_connection()
                database_df=sql.read_all_data(conn)
                conn.close()

                print('11. Average Sentiment Chart')
                compare_chart.comparison_chart(st,df,database_df)
                
                print('end of render')
                print('\n')
else:
    login()
            




