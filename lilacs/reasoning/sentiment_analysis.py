from afinn import Afinn
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests


def get_politness(text):
    # DO NOT ABUSE, this is using the web demo for dev purposes
    # you should instead run your own instance
    # https://github.com/collab-uniba/Emotion_and_Polarity_SO/tree/master/python/CalculatePoliteAndImpolite
    # http://www.cs.cornell.edu/~cristian//Politeness.html
    data = {"text": text}
    r = requests.post("http://politeness.cornell.edu/score-politeness", data=data)
    return r.json()


def get_affin_sentiment(text, lang="en", emoticons=True):
    afinn = Afinn(language=lang, emoticons=emoticons)
    return afinn.score(text)


def get_vader_sentiment(text):
    return SentimentIntensityAnalyzer().polarity_scores(text)


def get_sentiment(text, lang="en", emoticons=True):
    return get_vader_sentiment(text)


