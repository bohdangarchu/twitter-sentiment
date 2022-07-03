import re
import string
import os
import requests

from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from collections import Counter

from sentiment.apps import SentimentConfig


def remove_noise(tweet_tokens, stop_words=stopwords.words('english')):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        token = re.sub('(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+)|(@[A-Za-z0-9_]+)|((//)?t\.co/.*)|(\'..?)', '', token)
        # token = re.sub("(@[A-Za-z0-9_]+)", '', token)
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 \
                and token not in string.punctuation \
                and token.lower() not in stop_words \
                and token.lower() not in ['rt', 'http']:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens


class TweetClassifier:
    def __init__(self, classifier, tweets):
        self.classifier = classifier
        self.tweets = tweets

    def classify(self, text: str):
        tokenized = word_tokenize(text)
        clean_data = remove_noise(tokenized)
        return self.classifier.classify(
            dict([token, True] for token in clean_data)
        )

    # get dict with number of positive and negative tweets
    def classify_tweets(self):
        sentiment_dict = {
            'Positive': 0,
            'Negative': 0
        }
        for t in self.tweets:
            sentiment = self.classify(t)
            sentiment_dict[sentiment] += 1
        return sentiment_dict

    def get_dict(self):
        d = {}
        for t in self.tweets:
            d[t] = self.classify(t)
        return d

    def most_common(self, n=10):
        text = ' '.join(self.tweets)
        tokenized = word_tokenize(text)
        clean_data = remove_noise(tokenized)
        print('clean data=', clean_data)
        counter = Counter(clean_data)
        return dict(counter.most_common(n))


def load_tweets(keyword: str, max_results=100):
    json = query(keyword, max_results)
    if 'data' not in json:
        return []
    tweets = list(json['data'])
    return list(map(lambda tweet: tweet['text'], tweets))


def get_token():
    return os.getenv('TOKEN')


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def query(keyword, max_results):
    bearer_token = get_token()
    headers = create_headers(bearer_token)
    search_url = 'https://api.twitter.com/2/tweets/search/recent'
    query_params = {'query': keyword + ' lang:en', 'max_results': max_results}
    return connect_to_endpoint(search_url, headers, query_params)


def connect_to_endpoint(url, headers, params):
    response = requests.request('GET', url, headers=headers, params=params)
    print("Endpoint Response Code: " + str(response.status_code))
    return response.json()


if __name__ == '__main__':
    # s = SentimentConfig.classifier
    # cl = TweetClassifier(s)
    # print(cl.classify('happy'))
    print(os.getenv('TOKEN'))
