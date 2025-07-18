import scr.db.sqlserver as sql
import pandas as pd
import datetime
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt


conn=sql.create_connection()
df=sql.read_all_data(conn)
conn.close()



def analyze_hourly_sentiment(df):

    df['hour'] = df['CommentDateTime'].dt.hour
    hourly_avg = df.groupby('hour')['SentimentScore'].mean().reset_index()

    plt.figure(figsize=(10, 5))
    plt.plot(hourly_avg['hour'], hourly_avg['SentimentScore'], marker='o')
    plt.title('Average Sentiment Score by Hour', fontsize=18)
    plt.xlabel('Hour of Day (0-23)')
    plt.ylabel('Average Sentiment Score')
    plt.grid(True)
    plt.xticks(range(0, 24))
    plt.tight_layout()
    plt.show()

    return hourly_avg

analyze_hourly_sentiment(df)