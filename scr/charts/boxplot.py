import pandas as pd
import matplotlib.pyplot as plt

# Draws a bar chart showing hourly average sentiment scores with standard deviation as error bars
def draw_boxplot(st,df):
    df1=df.copy()

    # Extract the hour of each comment's creation time (0–23)
    df1['hour'] = df1['create_dt'].dt.hour

    # Group by hour and calculate mean and standard deviation of compound sentiment scores
    grouped = df1.groupby('hour')['compound'].agg(['mean', 'std']).reset_index()


    plt.figure(figsize=(12, 6))
    plt.bar(grouped['hour'], grouped['mean'], yerr=grouped['std'], capsize=5, color='skyblue')

    plt.axhline(0, color='gray', linestyle='--', alpha=0.8)

    plt.title('Hourly Sentiment Score with Variability', fontsize=18)
    plt.xlabel('Hour of Day')
    plt.ylabel('Average Compound Score')
    plt.xticks(range(0, 24)) 
    st.pyplot(plt) 