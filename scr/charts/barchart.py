import matplotlib.pyplot as plt
from collections import Counter


# Draw a bar chart of the top 20 most frequent words in the comment column
def draw_barchart(st, df, color, title):
    all_text = " ".join(df['comment'].astype(str).tolist()).lower()

    tokens=all_text.split()

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