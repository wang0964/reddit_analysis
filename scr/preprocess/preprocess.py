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
    df = df.sort_values(by='create_dt')  # sort in create datetime on ascending
    return df

def clean_words(text,nlp):
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'ADJ', 'VERB']]
    return ' '.join(words)

def remove_deleted_data(df):
    df = df[~df['comment'].isin(['[deleted]', '[removed]'])].copy()
    return df


def get_sentiment_label(compound):
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    

