import matplotlib.pyplot as plt
import base64
from io import BytesIO
from wordcloud import WordCloud


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', transparent=True)
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_word_cloud(freq: dict, percentage_dict: dict, keyword: str):
    positive = percentage_dict['Positive']
    negative = percentage_dict['Negative']
    title = f'positive tweets: {positive}%, negative tweets: {negative}%'\
            f'\n\nmost frequent words for \'{keyword}\' keyword '
    plt.switch_backend('Agg')
    wordcloud = WordCloud().generate_from_frequencies(freq)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=20, color='green')
    graph = get_graph()
    return graph
