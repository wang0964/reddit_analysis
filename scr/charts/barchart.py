import matplotlib.pyplot as plt
from collections import Counter



def draw_barchart(st, df, nlp , color, title):
    all_text = " ".join(df['comment'].astype(str).tolist()).lower()


    doc = nlp(all_text)
    # print(doc)

    # summary noun / adj / verb
    tokens = [
        token.lemma_   # Use the lemmatized form of the word (e.g., "running" to "run")
        for token in doc
        if not token.is_stop  # Exclude stopwords like "the", "is", "and"
        and token.is_alpha # Keep only alphabetic tokens (exclude punctuation and numbers)
        and token.pos_ in ["NOUN", "ADJ", "VERB"]  # Keep only nouns, adjectives, and verbs
    ]


    word_counts = Counter(tokens)
    top_n = 20  # Top 20 words
    top_words = word_counts.most_common(top_n)


    words, counts = zip(*top_words)


    plt.figure(figsize=(12, 6))
    plt.bar(words, counts, color=color)
    plt.xticks(rotation=45, ha='right')
    plt.title(title.format(top_n), fontsize=18)
    plt.xlabel('Word')
    plt.tight_layout()
    st.pyplot(plt)  