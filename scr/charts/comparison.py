import matplotlib.pyplot as plt

def comparison_chart(st, df,database_df):
    database_df['hour'] = database_df['CommentDateTime'].dt.hour
    df['hour'] = df['create_dt'].dt.hour

    # calculate the average sentiment score per hour
    db_hourly_avg = database_df.groupby('hour')['SentimentScore'].mean().reset_index()
    crawl_hourly_avg = df.groupby('hour')['compound'].mean().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(db_hourly_avg['hour'], db_hourly_avg['SentimentScore'], marker='o', label='Database')
    plt.plot(crawl_hourly_avg['hour'], crawl_hourly_avg['compound'], marker='s', label='Crawled Data')
    plt.title('Average Sentiment Score by Hour', fontsize=18)
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True)
    plt.xticks(range(0, 24))
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt) 