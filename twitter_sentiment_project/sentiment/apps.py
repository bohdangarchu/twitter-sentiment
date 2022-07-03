from django.apps import AppConfig
import pickle
import os


class SentimentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sentiment'
    path = os.path.join(os.getcwd(), 'sentiment', 'model', 'twitter_classifier.pickle')
    f = open(path, 'rb')
    classifier = pickle.load(f)
    f.close()
