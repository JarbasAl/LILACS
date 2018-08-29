# DO NOT ABUSE, this is using the web demo for dev purposes
# you should instead run your own instance
# https://github.com/collab-uniba/Emotion_and_Polarity_SO/tree/master/python/CalculatePoliteAndImpolite


import requests


def get_politness(text):
    # http://www.cs.cornell.edu/~cristian//Politeness.html
    data = {"text": text}
    r = requests.post("http://politeness.cornell.edu/score-politeness", data=data)
    return r.json()


if __name__ == "__main__":
    # word level emotion tagging based on lexicon lookup
    TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      'This is shit',  # angry
                      'This is the shit']  # excited
    for t in TEST_SENTENCES:
        print("\n"+t)
        get_politness(t)