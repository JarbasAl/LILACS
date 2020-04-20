from lilacs.reasoning import LILACSWordAnalyzer, LILACSTextAnalyzer
from lilacs.reasoning.sentiment_analysis import get_vader_sentiment, \
    get_affin_sentiment


class LILACSFeaturizer:
    @staticmethod
    def lexicon_features(text, keywords=None):
        keywords = keywords or []
        features = {}
        affin = get_affin_sentiment(text)
        vader = get_vader_sentiment(text)

        features["vader(positive)"] = vader["compound"] > 0
        features["afinn(positive)"] = affin > 0

        text = LILACSTextAnalyzer.normalize(text,
                                        make_singular=True,
                                        remove_stop_words=True,
                                        remove_pronouns=True,
                                        remove_articles=True)

        document = LILACSTextAnalyzer.tokenize(text)

        document_words = set(document)

        for word in keywords:
            features['contains({})'.format(word)] = (word in document_words)

        for word in document_words:
            color = LILACSWordAnalyzer.get_color(word)
            if color:
                features['color({})'.format(color)] = True
            senti = LILACSWordAnalyzer.get_sentiment(word)
            if senti:
                features['senti({})'.format(senti)] = True
            subj = LILACSWordAnalyzer.get_subjectivity(word)
            if subj:
                features['subj({})'.format(subj)] = True
            ori = LILACSWordAnalyzer.get_orientation(word)
            if ori:
                features['ori({})'.format(ori)] = True
            emo = LILACSWordAnalyzer.get_emotion(word)
            if emo:
                features['emotion({})'.format(emo)] = True
        return features

    @staticmethod
    def bow_features(text, entities=True):
        features = {}
        grams = LILACSTextAnalyzer.bag_of_words(text, entities=entities)
        for k, _ in grams:
            features["contains({})".format(k)] = True
        return features


if __name__ == "__main__":
    from pprint import pprint
    TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      'This is shit',  # angry
                      'This is the shit']  # excited
    for t in TEST_SENTENCES:
        print("\n"+t)
        data = LILACSFeaturizer.lexicon_features(t)
        pprint(data)
        data = LILACSFeaturizer.bow_features(t)
        pprint(data)