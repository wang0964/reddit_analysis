from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def draw_wordcloud(st,nlp,text):
    doc = nlp(text)
    words = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'ADJ', 'VERB']]

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
    ).generate(' '.join(words))

    # display
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    ax.set_title('Most Frequent Words in Comments\n', fontsize=18)
    st.pyplot(fig)