from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk.stem import PorterStemmer

import pandas as pd

# Create a DataFrame from a list of comments with VADER sentiment scores and timestamps
def create_DataFrame(text_list, all_comments):
# initialize VADER
    analyzer = SentimentIntensityAnalyzer()
    results = []
    id = 0

    # Compute sentiment scores for each cleaned comment
    for comment in text_list:
        score = analyzer.polarity_scores(comment)
        results.append({
            'id' : id,                                      # Sequential numeric ID
            "comment": comment,                             # Cleaned comment text
            "neg": score["neg"],                            # Negative sentiment score
            "neu": score["neu"],                            # Neutral sentiment score
            "pos": score["pos"],                            # Positive sentiment score
            "compound": score["compound"],                  # Compound sentiment score
            "create_dt": all_comments[id]['created_dt']     # Original comment timestamp
        })
        id += 1

    df = pd.DataFrame(results)

    # Add sentiment label column based on compound score
    df['sentiment'] = df['compound'].apply(get_sentiment_label)

     # Sort by create datetime on ascending
    df = df.sort_values(by='create_dt') 
    return df

# Clean and preprocess
def clean_words(text,nlp):
     # Lowercase and tokenize the input text using spaCy
    doc = nlp(text.lower())

    # Lemmatize tokens and filter out stopwords, punctuation, and unwanted POS
    words_token = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'ADJ', 'VERB']]
    
    # Apply stemming using NLTK's PorterStemmer
    stemmer = PorterStemmer()
    words_token = [stemmer.stem(token) for token in words_token]

    return ' '.join(words_token)

# Remove comments that have been marked as deleted or removed
def remove_deleted_data(df):
    df = df[~df['comment'].isin(['[deleted]', '[removed]'])].copy()
    return df

# Convert compound score to sentiment label
def get_sentiment_label(compound):
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"
    

