import matplotlib.pyplot as plt


def draw_scatterplot(st,df):
    color_map = {"Positive": "green", "Neutral": "gray", "Negative": "red"}
    colors = df['sentiment'].map(color_map)


    plt.figure(figsize=(14, 6))
    plt.scatter(df['create_dt'], df['compound'], c=colors, alpha=0.6)


    plt.axhline(y=0, color='black', linestyle='--', alpha=0.7)

    plt.title("Sentiment Scatter Plot Over Time", fontsize=18)
    plt.xlabel("Time")
    plt.ylabel("Compound Score")
    st.pyplot(plt)   