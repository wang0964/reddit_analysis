import pyodbc
import datetime
import pandas as pd


def create_connection():
    return pyodbc.connect("DSN=sentiment;UID=w;PWD=1234;DATABASE=sentiment")

def append_db(conn, df, reddit_comments):
    topic_id=reddit_comments.id

    c = conn.cursor()

    c.execute("SELECT 1 FROM topic WHERE TopicID = ?", (reddit_comments.id,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO topic (TopicID, Title, url) VALUES (?, ?, ?)",
            (
                reddit_comments.id,
                reddit_comments.title,
                "https://www.reddit.com" + reddit_comments.permalink
            )
        )
 
    c.execute("""
                SELECT TOP 1 *
                FROM dbo.CrawlData
                WHERE TopicID = ?
                ORDER BY CrawlDateTime DESC
                """, (topic_id,))

    row = c.fetchone()

    if row is None:
        df1=df
    else:
        df1=df[df['create_dt']>row[4]]

    sql = """
            INSERT INTO dbo.CrawlData (TopicID, CommentID, SentimentScore, 
                CrawlDateTime, CommentDateTime)
            VALUES (?, ?, ?, ?, ?)
        """

    now=datetime.datetime.now()
    data = [
        (topic_id, row['id'], row['compound'], now, row['create_dt'])
        for _, row in df1.iterrows()
    ]
    c.executemany(sql, data)
    conn.commit()
    c.close()
    print(f'Complete inserting {df1.shape[0]} rows.')
    return


def read_all_data(conn):
    c = conn.cursor()
    c.execute("""
                SELECT CommentDateTime, SentimentScore
                FROM dbo.CrawlData
            """)

    rows = c.fetchall()

    data=[]
    
    for row in rows:
        data.append({'CommentDateTime': row[0], 'SentimentScore': row[1]})

    df = pd.DataFrame(data)
    c.close()
    return df
