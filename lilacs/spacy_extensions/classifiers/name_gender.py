import csv
import random
from lilacs.settings import LEXICONS_DIR, MODELS_DIR
from lilacs.spacy_extensions.classifiers.naive import NaiveBayes
from os.path import join, exists
from pickle import dump, load
import nltk


def get_features(name):
    return {
        'prefix1': name[1],
        'prefix2': name[:2],
        'prefix3': name[:3],
        'suffix1': name[-1],
        'suffix2': name[-2:],
        'suffix3': name[-3:]
    }


def _train_gender():
    with open(join(LEXICONS_DIR, "names.csv")) as f:
        names = [tuple(line) for line in csv.reader(f)]
    random.shuffle(names)
    train_data = [(get_features(n), g) for
                  (n, g) in names[20000:]]
    return nltk.NaiveBayesClassifier.train(train_data)


class NaiveNameGender(NaiveBayes):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

    model_path = join(MODELS_DIR, "naive_gender.pkl")

    if exists(model_path):
        with open(model_path, 'rb') as data:
            clf = load(data)
    else:
        clf = _train_gender()
        with open(model_path, 'wb') as output:
            dump(clf, output, -1)

    def __init__(self, model_path=model_path):
        super().__init__(model_path)

    def get_features(self, name):
        return get_features(name)

    def predict(self, word):
        pred = super().predict(word)
        if pred == "male":
            return NaiveNameGender.MALE
        elif pred == "female":
            return NaiveNameGender.FEMALE
        return NaiveNameGender.NEUTRAL


if __name__ == "__main__":
    gender = NaiveNameGender()
    gender.show_most_informative_features(5)
    """
    Most Informative Features
                 suffix3 = 'sia'          female : male   =    219.5 : 1.0
                 suffix3 = 'cia'          female : male   =    167.1 : 1.0
                 suffix3 = 'mes'            male : female =    161.0 : 1.0
                 suffix3 = 'ena'          female : male   =    109.2 : 1.0
                 suffix3 = 'ita'          female : male   =     99.0 : 1.0
    """
    assert gender.predict("Maria") == NaiveNameGender.FEMALE
    assert gender.predict("Linda") == NaiveNameGender.FEMALE
    assert gender.predict("Joanna") == NaiveNameGender.FEMALE
    assert gender.predict("Sarah") == NaiveNameGender.FEMALE
    assert gender.predict("Justin") == NaiveNameGender.MALE
    assert gender.predict("Gerard") == NaiveNameGender.MALE
