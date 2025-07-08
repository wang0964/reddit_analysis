from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd


def create_DataFrame(text_list, all_comments):
# initialize VADER
    analyzer = SentimentIntensityAnalyzer()
    results = []
    id = 0


    for comment in text_list:
        score = analyzer.polarity_scores(comment)
        results.append({
            'id' : id,
            "comment": comment,
            "neg": score["neg"],
            "neu": score["neu"],
            "pos": score["pos"],
            "compound": score["compound"],
            "create_dt": all_comments[id]['created_dt']
        })
        id += 1

    df = pd.DataFrame(results)
    df['sentiment'] = df['compound'].apply(get_sentiment_label)
    return df

def clean_date(df):
    return df[~((df['comment'] == '[deleted]') | (df['comment'] == '[removed]'))]


def get_sentiment_label(compound):
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    

