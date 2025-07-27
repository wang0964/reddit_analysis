from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

# Draws a word cloud
def draw_wordcloud(st,text):

    # ellipse mask
    x, y = np.ogrid[:400, :600]  # height/width
    mask = (x - 150)**2 / 150**2 + (y - 300)**2 / 300**2 > 1
    mask = 255 * mask.astype(int)

    # Generate word cloud (remove outer frame)
    wordcloud = WordCloud(
        background_color='white',
        mask=mask,
        width=600,
        height=300
    # ).generate(' '.join(words))
    ).generate(text)

    # display
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Most Frequent Words in Comments\n', fontsize=18)
    st.pyplot(fig)