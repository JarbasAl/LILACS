from afinn import Afinn
# http://neuro.compute.dtu.dk/wiki/AFINN


def get_sentiment(text, lang="en", emoticons=True, emoji=True):
    afinn = Afinn(language=lang, emoticons=emoticons, emoji=emoji)
    return afinn.score(text)

