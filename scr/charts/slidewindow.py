import pandas as pd
import matplotlib.pyplot as plt

def draw_slidewindow_trend(st, df):
    df1 = df.copy()
    df1['create_dt'] = pd.to_datetime(df1['create_dt'])
    # create datetime index
    df1.set_index('create_dt', inplace=True)
    df1 = df1.sort_index()

    # # Make a sliding window for 10 minutes
    t=10
    rolling = df1['compound'].rolling(f'{t}min').mean()

    plt.figure(figsize=(12, 6))
    # plt.plot(df.index, df['compound'], alpha=0.3, label='Original')
    plt.plot(rolling.index, rolling, color='purple', label=f'Rolling Mean ({t})')

    plt.axhline(y=0.05, color='grey', linestyle='--', label='Neutral Boundary (+0.05)')
    plt.axhline(y=-0.05, color='grey', linestyle='--', label='Neutral Boundary (-0.05)')

    plt.xlabel('Time', fontsize=14)
    plt.ylabel('Average Compound Score')

    plt.title(f'Sentiment Trend Over Time ({t} min Window)', fontsize=18)

    plt.tick_params(axis='both')
    plt.legend()

    st.pyplot(plt) 
