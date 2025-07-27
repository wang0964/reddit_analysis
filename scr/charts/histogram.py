import streamlit as st
import matplotlib.pyplot as plt

# Draws a histogram of compound sentiment scores from the DataFrame
def draw_histogram(st, df):

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(df['compound'], bins=30, color='skyblue', edgecolor='black')
    ax.set_title("Histogram of Compound Sentiment Scores", fontsize=18)
    ax.set_xlabel("Compound Score", fontsize=14)
    ax.set_ylabel("Frequency", fontsize=14)

    st.pyplot(fig)