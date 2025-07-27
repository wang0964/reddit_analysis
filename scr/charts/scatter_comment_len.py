import matplotlib.pyplot as plt


# Draws a scatter plot showing the relationship between comment length and sentiment score
def draw_scatter_comment_length(st, df):

    df['length'] = df['comment'].apply(len)

    color_map = {'Positive': 'green', 'Negative': 'red', 'Neutral': 'gray'}

    plt.figure(figsize=(12, 6))

    for sentiment, color in color_map.items():
        subset = df[df['sentiment'] == sentiment]
        plt.scatter(
            subset['length'],
            subset['compound'],
            alpha=0.5,
            s=50,
            c=color,
            label=sentiment
        )

    plt.title('Sentiment vs. Comment Length (by Sentiment)', fontsize=18)
    plt.xlabel('Comment Length (chars)')
    plt.ylabel('Compound Score')
    plt.legend()
    st.pyplot(plt) 