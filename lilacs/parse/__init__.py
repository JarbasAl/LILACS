from jarbas_utils.parse import singularize, split_sentences
from lilacs import nlp
import textacy
import textacy.ke
from lingua_franca.parse import normalize


class SentenceParser:
    @staticmethod
    def tokenize(text, stopwords=None):
        stopwords = stopwords or []
        return [singularize(token) for token in text.split(" ")
                if token not in stopwords]

    @staticmethod
    def singularize(text):
        doc = nlp(text)
        singularized = " ".join([tok._.lemma() for tok in doc])
        return singularized

    @staticmethod
    def remove_pronouns(text):
        doc = nlp(text)
        result = [token.text for token in doc if token.lemma_ != '-PRON-']
        return " ".join(result)

    @staticmethod
    def replace_coreferences(text):
        from lilacs.reasoning.coreference import replace_coreferences
        return replace_coreferences(text)

    @staticmethod
    def process_text(text):
        doc = nlp(text.lower())
        result = []
        for token in doc:
            if token.text in nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return [t.strip() for t in " ".join(result).split("\n") if t.strip()]

    @staticmethod
    def normalize(text, solve_corefs=False, make_singular=False,
                  remove_articles=False, remove_stop_words=False,
                  remove_pronouns=False):
        if solve_corefs:
            text = SentenceParser.replace_coreferences(text)
        text = normalize(text, remove_articles=remove_articles)
        if remove_pronouns:
            text = SentenceParser.remove_pronouns(text)
        if make_singular:
            text = SentenceParser.singularize(text)
        if remove_stop_words:
            stop_words = nlp.Defaults.stop_words
            text = " ".join(SentenceParser.tokenize(text, stop_words))
        return text

    @staticmethod
    def split_sentences(text, solve_corefs=False):
        if solve_corefs:
            text = SentenceParser.replace_coreferences(text)
        return split_sentences(text)

    @staticmethod
    def chunk(text, solve_corefs=False):
        if solve_corefs:
            text = SentenceParser.replace_coreferences(text)
        candidates = []
        for text in split_sentences(text):
            candidates += text.split(",")
        sentences = []
        for text in candidates:
            sentences += text.split(" and ")
        return [c.strip() for c in sentences if c.strip()]

    @staticmethod
    def text_rank(text, normalize="lemma", topn=5):
        doc = nlp(text)
        return textacy.ke.textrank(doc, normalize=normalize, topn=topn)

    @staticmethod
    def ngram_rank(text, ngrams=(1, 2, 3, 4), normalize="lemma", topn=0.1):
        doc = nlp(text)
        return textacy.ke.sgrank(doc,
                                 ngrams=ngrams,
                                 normalize=normalize,
                                 topn=topn)

    # word counting
    @staticmethod
    def count(text):
        doc = nlp(text)
        ts = textacy.TextStats(doc)
        return ts.basic_counts

    @staticmethod
    def count_unique_words(text):
        return SentenceParser.count(text)["n_unique_words"]

    @staticmethod
    def count_sentences(text):
        return SentenceParser.count(text)["n_sents"]

    @staticmethod
    def count_words(text):
        return SentenceParser.count(text)["n_words"]

    @staticmethod
    def count_chars(text):
        return SentenceParser.count(text)["n_chars"]

    @staticmethod
    def count_syllables(text):
        return SentenceParser.count(text)["n_syllables"]

    @staticmethod
    def count_long_words(text):
        return SentenceParser.count(text)["n_long_words"]

    @staticmethod
    def count_monosyllable_words(text):
        return SentenceParser.count(text)["n_monosyllable_words"]

    @staticmethod
    def count_polysyllable_words(text):
        return SentenceParser.count(text)["n_polysyllable_words"]

    @staticmethod
    def bag_of_words(text, ngrams=(1, 2, 3), weighting="count", entities=True):
        doc = nlp(text)
        bag = doc._.to_bag_of_terms(ngrams=ngrams, entities=entities,
                                    weighting=weighting, as_strings=True)
        return sorted(bag.items(), key=lambda x: x[1], reverse=True)

    # part of speech
    @staticmethod
    def postag(sent):
        doc = nlp(sent)
        return [(token.text, token.tag_) for token in doc]

    @staticmethod
    def brown_postag(sent):
        doc = nlp(sent)
        return doc._.brown_tags

    @staticmethod
    def tag_sentence(sent):
        doc = nlp(sent)
        return [(token.text, token.pos_) for token in doc]

    @staticmethod
    def dependency_labels(sent):
        doc = nlp(sent)
        return [(token.text, token.dep_) for token in doc]

    # verbs
    @staticmethod
    def is_passive(sent):
        """Takes a list of tags, returns true if we think this is a passive
        sentence.
        Particularly, if we see a "BE" verb followed by some other, non-BE
        verb, except for a gerund, we deem the sentence to be passive.
        """
        doc = nlp(sent)
        return doc._.is_passive

    @staticmethod
    def change_tense(text, to_tense):
        """Change the tense of text.
        Args:
            text (str): text to change.
            to_tense (str): 'present','past', or 'future'
            npl (SpaCy model, optional):
        Returns:
            str: changed text.
        """
        doc = nlp(text)
        return doc._.change_tense(to_tense)

