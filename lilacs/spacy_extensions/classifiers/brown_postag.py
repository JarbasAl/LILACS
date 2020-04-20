from os.path import join, exists
from pickle import dump, load
from lilacs.settings import MODELS_DIR
import nltk
from nltk.corpus import brown


def _train_brown_tagger():
    """Train a tagger from the Brown Corpus. This should not be called very
    often; only in the event that the tagger pickle wasn't found."""
    train_sents = brown.tagged_sents()

    # These regexes were lifted from the NLTK book tagger chapter.
    t0 = nltk.RegexpTagger(
        [(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),  # cardinal numbers
         (r'(The|the|A|a|An|an)$', 'AT'),  # articles
         (r'.*able$', 'JJ'),  # adjectives
         (r'.*ness$', 'NN'),  # nouns formed from adjectives
         (r'.*ly$', 'RB'),  # adverbs
         (r'.*s$', 'NNS'),  # plural nouns
         (r'.*ing$', 'VBG'),  # gerunds
         (r'.*ed$', 'VBD'),  # past tense verbs
         (r'.*', 'NN')  # nouns (default)
         ])
    t1 = nltk.UnigramTagger(train_sents, backoff=t0)
    t2 = nltk.BigramTagger(train_sents, backoff=t1)
    t3 = nltk.TrigramTagger(train_sents, backoff=t2)
    return t3


class BrownPOSTag:
    model_path = join(MODELS_DIR, "brown_tagger.pkl")

    if exists(model_path):
        with open(model_path, 'rb') as data:
            tagger = load(data)
        tagger = tagger
    else:
        tagger = _train_brown_tagger()
        with open(model_path, 'wb') as output:
            dump(tagger, output, -1)

    @staticmethod
    def tag(tokens):
        """Take a sentence as a string and return a list of
        (word, tag) tuples."""
        return BrownPOSTag.tagger.tag(tokens)
