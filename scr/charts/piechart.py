import pandas as pd
import matplotlib.pyplot as plt


           

def draw_piechart(st, df):
    sentiment_counts = df['sentiment'].value_counts()
    sentiment_counts = sentiment_counts.reindex(['Positive', 'Neutral', 'Negative'], fill_value=0)
    import matplotlib.pyplot as plt

    colors = ["green", "gray", "red"]  

    plt.figure(figsize=(7, 7))
    plt.pie(
        sentiment_counts,
        labels=sentiment_counts.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=140,
        explode=(0.05, 0.05, 0.05)
    )
    plt.title("Sentiment Distribution of Comments", fontsize=18)
    plt.axis('equal')
    st.pyplot(plt) 