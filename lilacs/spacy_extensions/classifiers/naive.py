import nltk
from lilacs.exceptions import NotTrained
from os.path import exists
from pickle import dump, load


class NaiveBayes:
    clf = None

    def __init__(self, model_path=None):
        if model_path is not None:
            self.load(model_path)

    def save(self, model_path):
        if self.clf is None:
            raise NotTrained
        with open(model_path, 'wb') as output:
            dump(self.clf, output, -1)

    def load(self, model_path):
        if exists(model_path):
            with open(model_path, 'rb') as data:
                self.clf = load(data)
        else:
            raise NotTrained

    def train(self, train_data):
        self.clf = nltk.NaiveBayesClassifier.train(train_data)
        return self.clf

    def test(self, test_data):
        return nltk.classify.accuracy(self.clf, test_data)

    def get_features(self, text):
        raise NotImplementedError

    def predict(self, text):
        if self.clf is None:
            raise NotTrained
        return self.clf.classify(self.get_features(text))

    def show_most_informative_features(self, n=5):
        return self.clf.show_most_informative_features(n)

