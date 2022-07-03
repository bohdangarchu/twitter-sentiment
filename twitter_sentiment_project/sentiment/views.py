import matplotlib.pyplot as plt
from io import StringIO

from django.shortcuts import render

from .apps import SentimentConfig
from .utils import get_word_cloud
from .models import TweetClassifier, load_tweets


def get_start_page(request):
    if request.method == 'GET':
        return render(request, "index.html")


def get_sentiment(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword')
        tweets = load_tweets(keyword)
        if len(tweets) == 0:
            return render(request, "index.html", context={'response': 'keyword not found'})
        classifier = TweetClassifier(SentimentConfig.classifier, tweets)
        response = classifier.classify_tweets()
        # d = classifier.get_dict(tweets)
        most_common_dict = classifier.most_common(20)
        wordcloud = get_word_cloud(most_common_dict, percentage_dict=response, keyword=keyword)
        return render(request, "index.html", context={'wordcloud': wordcloud})


def get_pie_chart(my_dict: dict):
    labels = 'Positive', 'Negative'
    sizes = [my_dict['Positive'], my_dict['Negative']]

    fig1, ax1 = plt.subplots()
    imgdata = StringIO()
    fig1.savefig(imgdata, format='svg')
    imgdata.seek(0)

    return imgdata.getvalue()


# todo add more filters and increase number of tweets





