from os.path import join, exists, dirname
import random
from lilacs.spacy_extensions.classifiers.naive import NaiveBayes
from lilacs.parse.features import LILACSFeaturizer
import nltk
import string
from nltk.corpus import movie_reviews
from lilacs import nlp


class NaiveMovieSentiment(NaiveBayes):
    def __init__(self, model_path=join(dirname(__file__),
                                       "naive_movie_sentiment.pkl")):
        super().__init__()
        stopwords_english = nlp.Defaults.stop_words
        all_words = [word.lower() for word in movie_reviews.words()]
        all_words = [w for w in all_words if w not in stopwords_english and
                     w not in string.punctuation and len(w) > 3]

        # TODO adjectives and verbs only ?
        self.keywords = list(nltk.FreqDist(all_words).most_common(1000))

        if exists(model_path):
            # Accuracy: 0.7675
            print("loading")
            self.load(model_path)
        else:
            print("training")
            pos_reviews = []
            for fileid in movie_reviews.fileids('pos'):
                words = movie_reviews.words(fileid)
                words = [w for w in words if w not in stopwords_english and
                         w not in string.punctuation and len(w) > 3]
                pos_reviews.append(words)

            neg_reviews = []
            for fileid in movie_reviews.fileids('neg'):
                words = movie_reviews.words(fileid)
                words = [w for w in words if w not in stopwords_english and
                         w not in string.punctuation and len(w) > 3]
                neg_reviews.append(words)

            # positive reviews feature set
            pos_reviews_set = []
            for words in pos_reviews:
                pos_reviews_set.append((self.get_features(words), 'pos'))

            # negative reviews feature set
            neg_reviews_set = []
            for words in neg_reviews:
                neg_reviews_set.append((self.get_features(words), 'neg'))

            random.shuffle(pos_reviews_set)
            random.shuffle(neg_reviews_set)

            test_set = pos_reviews_set[:200] + neg_reviews_set[:200]
            train_set = pos_reviews_set[200:] + neg_reviews_set[200:]

            self.train(train_set)
            print("Accuracy:", self.test(test_set))
            self.save(model_path)

    def get_features(self, document):
        text = " ".join(document)
        features = LILACSFeaturizer.lexicon_features(text, self.keywords)
        features.update(LILACSFeaturizer.bow_features(text))
        return features


if __name__ == "__main__":
    senti = NaiveMovieSentiment()
    senti.show_most_informative_features(10)
    """
Most Informative Features
    contains(bad movie) = True            neg : pos    =     22.3 : 1.0
    contains(plod) = True                 neg : pos    =     12.3 : 1.0
    contains(joel schumacher) = True      neg : pos    =     11.0 : 1.0
    contains(outstanding) = True          pos : neg    =     11.0 : 1.0
    contains(schumacher) = True           neg : pos    =     11.0 : 1.0
    contains(unintentional) = True        neg : pos    =     11.0 : 1.0
    contains(great thing) = True          pos : neg    =     10.3 : 1.0
    contains(immerse) = True              pos : neg    =     10.3 : 1.0
    contains(misfire) = True              neg : pos    =     10.3 : 1.0
    contains(unintereste) = True          neg : pos    =      9.4 : 1.0
    """

    TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      "You are awesome!",
                      'This is shit',  # angry
                      'This is the shit']  # excited
    for t in TEST_SENTENCES:
        print("\n" + t)
        print(senti.predict(t))
    exit()
