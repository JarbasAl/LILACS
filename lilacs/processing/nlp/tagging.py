import nltk

nltk.download('brown')
nltk.download('punkt')
from nltk.corpus import brown
from itertools import dropwhile
import string
import os
from pickle import dump, load
from lilacs.processing.nlp import get_nlp
from pattern.en import conjugate, PAST, PRESENT, SINGULAR, PLURAL
from spacy.symbols import NOUN

SUBJ_DEPS = {'agent', 'csubj', 'csubjpass', 'expl', 'nsubj', 'nsubjpass'}


class SentenceTagger:
    def __init__(self, nlp=None):
        self._nlp = nlp
        if os.path.exists("tagger.pkl"):
            with open('tagger.pkl', 'rb') as data:
                tagger = load(data)
            self.tagger = tagger
        else:
            tagger = self.train()
            self.tagger = tagger
            self.save()

    @staticmethod
    def train():
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

    def save(self):
        with open('tagger.pkl', 'wb') as output:
            dump(self.tagger, output, -1)

    def tag(self, sent):
        return self.tagger.tag(sent)

    def tag_sentence(self, sent):
        """Take a sentence as a string and return a list of (word, tag) tuples."""
        tokens = nltk.word_tokenize(sent)
        return self.tag(tokens)

    def is_passive(self, sent):
        return is_passive(self, sent)

    def get_conjuncts(self, tok):
        """
        Return conjunct dependents of the leftmost conjunct in a coordinated phrase,
        e.g. "Burton, [Dan], and [Josh] ...".
        """
        return [right for right in tok.rights
                if right.dep_ == 'conj']

    def is_plural_noun(self, token):
        """
        Returns True if token is a plural noun, False otherwise.
        Args:
            token (``spacy.Token``): parent document must have POS information
        Returns:
            bool
        """
        if token.doc.is_tagged is False:
            raise ValueError('token is not POS-tagged')
        return True if token.pos == NOUN and token.lemma != token.lower else False

    def get_subjects_of_verb(self, verb):
        if verb.dep_ == "aux" and list(verb.ancestors):
            return self.get_subjects_of_verb(list(verb.ancestors)[0])
        """Return all subjects of a verb according to the dependency parse."""
        subjs = [tok for tok in verb.lefts
                 if tok.dep_ in SUBJ_DEPS]
        # get additional conjunct subjects
        subjs.extend(tok for subj in subjs for tok in self.get_conjuncts(subj))
        if not len(subjs):
            return self.get_subjects_of_verb(list(verb.ancestors)[0])
        return subjs

    def is_plural_verb(self, token):
        if token.doc.is_tagged is False:
            raise ValueError('token is not POS-tagged')
        subjects = self.get_subjects_of_verb(token)
        if not len(subjects):
            return False
        plural_score = sum([self.is_plural_noun(x) for x in subjects]) / len(
            subjects)

        return plural_score > .5

    @property
    def nlp(self):
        if self._nlp is None:
            self._nlp = get_nlp()
        return self._nlp

    def change_tense(self, text, to_tense, nlp=None):
        """Change the tense of text.
        Args:
            text (str): text to change.
            to_tense (str): 'present','past', or 'future'
            npl (SpaCy model, optional):
        Returns:
            str: changed text.
        """
        nlp = nlp or self.nlp
        tense_lookup = {'future': 'inf', 'present': PRESENT, 'past': PAST}
        tense = tense_lookup[to_tense]

        doc = nlp(text)

        out = list()
        out.append(doc[0].text)
        words = []
        for word in doc:
            words.append(word)
            if len(words) == 1:
                continue
            if (words[-2].text == 'will' and words[-2].tag_ == 'MD' and words[
                -1].tag_ == 'VB') or \
                    words[-1].tag_ in ('VBD', 'VBP', 'VBZ', 'VBN') or \
                    (not words[-2].text in ('to', 'not') and words[
                        -1].tag_ == 'VB'):

                if words[-2].text in ('were', 'am', 'is', 'are', 'was') or \
                        (words[-2].text == 'be' and len(words) > 2 and words[
                            -3].text == 'will'):
                    this_tense = tense_lookup['past']
                else:
                    this_tense = tense

                subjects = [x.text for x in self.get_subjects_of_verb(words[
                                                                          -1])]
                if ('I' in subjects) or ('we' in subjects) or (
                        'We' in subjects):
                    person = 1
                elif ('you' in subjects) or ('You' in subjects):
                    person = 2
                else:
                    person = 3
                if self.is_plural_verb(words[-1]):
                    number = PLURAL
                else:
                    number = SINGULAR
                if (words[-2].text == 'will' and words[-2].tag_ == 'MD') or \
                        words[
                            -2].text == 'had':
                    out.pop(-1)
                if to_tense == 'future':
                    if not (out[-1] == 'will' or out[-1] == 'be'):
                        out.append('will')
                    # handle will as a noun in future tense
                    if words[-2].text == 'will' and words[-2].tag_ == 'NN':
                        out.append('will')
                # if word_pair[0].dep_ == 'auxpass':
                out.append(
                    conjugate(words[-1].text, tense=this_tense, person=person,
                              number=number))
            else:
                out.append(words[-1].text)

            # negation
            if words[-2].text + words[-1].text in (
                    'didnot', 'donot', 'willnot'):
                if tense == PAST:
                    out[-2] = 'did'
                elif tense == PRESENT:
                    out[-2] = 'do'
                else:
                    out.pop(-2)

            # future perfect, and progressives, but ignore for "I will have cookies"
            if words[-1].text in ('have', 'has') and len(
                    list(words[-1].ancestors)) and words[-1].dep_ == 'aux':
                out.pop(-1)

        text_out = ' '.join(out)

        for char in string.punctuation:
            if char in """(<['""":
                text_out = text_out.replace(char + ' ', char)
            else:
                text_out = text_out.replace(' ' + char, char)

        text_out = text_out.replace(" 's", "'s")  # fix posessive 's

        return text_out


def _passivep(tags):
    """Takes a list of tags, returns true if we think this is a passive
    sentence.
    Particularly, if we see a "BE" verb followed by some other, non-BE
    verb, except for a gerund, we deem the sentence to be passive.
    """

    after_to_be = list(dropwhile(lambda tag: not tag.startswith("BE"), tags))
    nongerund = lambda tag: tag.startswith("V") and not tag.startswith("VBG")

    filtered = filter(nongerund, after_to_be)
    out = any(filtered)

    return out


def is_passive(tagger, sent):
    tagged = tagger.tag_sentence(sent)
    tags = map(lambda tup: tup[1], tagged)
    return bool(_passivep(tags))


if __name__ == '__main__':
    t = SentenceTagger()
    assert t.is_passive('Mistakes were made.')
    assert not t.is_passive('I made mistakes.')
    # Noteable fail case. Fix me. I think it is because the 'to be' verb is
    # omitted.
    # assert t.is_passive('guy shot by police')
    assert t.change_tense("I am making dinner",
                          "past") == "I was making dinner"
    assert t.change_tense("I am making dinner",
                          "future") == "I will be making dinner"
    assert t.change_tense("I am making dinner",
                          "present") == "I am making dinner"
