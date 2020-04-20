from spacy.tokens import Doc, Span, Token
from lilacs.spacy_extensions.lexicons import *
from lilacs.spacy_extensions.classifiers.brown_postag import BrownPOSTag
from lilacs.spacy_extensions.inflection_utils import change_tense, \
    is_passive, past_tense, present_tense, future_tense, is_plural_noun
from lilacs.spacy_extensions.extraction import interesting_triples, \
    svo_triples, extract_semi_structured_statements
from lingua_franca.parse import normalize as _lf_norm
from afinn import Afinn
from nltk.sentiment.vader import SentimentIntensityAnalyzer


# sense2vec extension
def s2v_doc_similarity_match(doc1, doc2):
    scores = []
    for tok in doc1._.s2v_phrases:
        for tok2 in doc2._.s2v_phrases:
            try:
                scores.append(tok._.s2v_similarity(tok2))
            except:
                # TODO upstream bug in sense2vec?
                pass
    if not scores:
        return 0
    # TODO average scores? average vectors and calc cosine similarity?
    return max(scores)


def s2v_related_concepts(doc, n=3):
    related = []
    for tok in doc._.s2v_phrases:
        try:
            for r in tok._.s2v_most_similar(n):
                if r not in related:
                    related.append(r)
        except:
            # TODO upstream bug in sense2vec?
            pass
    return related


def _load_s2v():
    Doc.set_extension("s2v_similarity_match", method=s2v_doc_similarity_match)
    Doc.set_extension("s2v_related_concepts", method=s2v_related_concepts)
    Span.set_extension("s2v_similarity_match", method=s2v_doc_similarity_match)
    Span.set_extension("s2v_related_concepts", method=s2v_related_concepts)


# wordnet
def enrich_sentence(doc, domains=None):
    enriched_sentence = []

    # For each token in the sentence
    for token in doc:

        # We get those synsets within the desired domains
        if domains:
            synsets = token._.wordnet.wordnet_synsets_for_domain(domains)
        else:
            # if auto detecting, only extend verbs
            if not token.tag_.lower().startswith("v"):
                enriched_sentence.append(token.text)
                continue
            # TODO disambiguate, currently just going with 1st synset
            synsets = token._.wordnet.synsets()
            if len(synsets) > 1:
                synsets = synsets[:1]

        if not synsets:
            enriched_sentence.append(token.text)
        else:
            lemmas_for_synset = [lemma for s in synsets for lemma in
                                 s.lemma_names()]
            # If we found a synset in the economy domains
            # we get the variants and add them to the enriched sentence
            enriched_sentence.append('({})'.format('|'.join(set(
                lemmas_for_synset))).replace("_", " "))

    norm = _lf_norm(' '.join(enriched_sentence), remove_articles=False)
    return norm


def _load_wordnet():
    Doc.set_extension("enrich", method=enrich_sentence)
    Span.set_extension("enrich", method=enrich_sentence)


# Brown corpus
def get_brown_postags(doc):
    return [(tok.text, tok._.brown_tag) for tok in doc]


def brown_postags(doc):
    Token.set_extension("brown_tag", default="<UNK>", force=True)
    tokens = [token.text for token in doc]
    tags = BrownPOSTag.tag(tokens)
    for token in doc:
        doc[token.i]._.brown_tag = tags[token.i][1]
    return doc


def _load_brown(nlp):
    # brown corpus
    Doc.set_extension("brown_tags", getter=get_brown_postags)
    nlp.add_pipe(brown_postags)


# other stuff
def _load_lexicons():
    # lexicons
    Token.set_extension("lexicon_color", getter=lexicon_color)
    Token.set_extension("lexicon_emotion", getter=lexicon_emotion)
    Token.set_extension("lexicon_sentiment", getter=lexicon_sentiment)
    Token.set_extension("lexicon_subjectivity", getter=lexicon_subjectivity)
    Token.set_extension("lexicon_orientation", getter=lexicon_orientation)

    Doc.set_extension("lexicon_colors", getter=lexicon_colors)
    Span.set_extension("lexicon_colors", getter=lexicon_colors)
    Doc.set_extension("lexicon_emotions", getter=lexicon_emotions)
    Span.set_extension("lexicon_emotions", getter=lexicon_emotions)
    Doc.set_extension("lexicon_sentiments", getter=lexicon_sentiments)
    Span.set_extension("lexicon_sentiments", getter=lexicon_sentiments)
    Doc.set_extension("lexicon_orientations", getter=lexicon_orientations)
    Span.set_extension("lexicon_orientations", getter=lexicon_orientations)
    Doc.set_extension("lexicon_subjectivities", getter=lexicon_subjectivities)
    Span.set_extension("lexicon_subjectivities", getter=lexicon_subjectivities)


def _load_sentiment(nlp):
    def vader(doc):
        return SentimentIntensityAnalyzer().polarity_scores(doc.text)[
            'compound']

    def afinn(doc):
        return Afinn(language=nlp.lang, emoticons=True).score(doc.text)

    Doc.set_extension("afinn_score", getter=afinn)
    Doc.set_extension("vader_score", getter=vader)
    Span.set_extension("afinn_score", getter=afinn)
    Span.set_extension("vader_score", getter=vader)
    Token.set_extension("afinn_score", getter=afinn)
    Token.set_extension("vader_score", getter=vader)


def _load_triples(nlp):
    def interesting(doc):
        return interesting_triples(doc, nlp.vocab)

    Doc.set_extension("interesting_triples", getter=interesting)
    Span.set_extension("interesting_triples", getter=interesting)
    Doc.set_extension("svo_triples", getter=svo_triples)
    Span.set_extension("svo_triples", getter=svo_triples)

    Doc.set_extension("extract_semi_structured_statements",
                      method=extract_semi_structured_statements)
    Span.set_extension("extract_semi_structured_statements",
                       method=extract_semi_structured_statements)

    Doc.set_extension("semi_structured_statements",
                      getter=extract_semi_structured_statements)
    Span.set_extension("semi_structured_statements",
                       getter=extract_semi_structured_statements)


def _load_inflection():
    Doc.set_extension("change_tense", method=change_tense)
    Doc.set_extension("past_tense", getter=past_tense)
    Doc.set_extension("present_tense", getter=present_tense)
    Doc.set_extension("future_tense", getter=future_tense)
    Doc.set_extension("is_passive", getter=is_passive)
    Token.set_extension("is_plural_noun", getter=is_plural_noun)


def _load_lingua_franca(nlp):
    def normalize(doc, remove_articles=False):
        return _lf_norm(doc.text,
                        remove_articles=remove_articles,
                        lang=nlp.lang)

    # lingua_franca integration
    Doc.set_extension("normalized", getter=normalize)
    Doc.set_extension("normalize", method=normalize)

    #  TODO this goes against spacy priciple of doc.text == text
    #  nlp.tokenizer = Normalizer(nlp)


# misc utils
def better_boundaries(doc):
    # improve sentencizer
    for token in doc[:-1]:
        if token.text == "...":
            doc[token.i + 1].is_sent_start = True
    return doc


def overlap_tokens(doc, other_doc):
    """
    Get the tokens from the original Doc that are also in the comparison Doc.
    """
    overlap = []
    other_tokens = [token.text for token in other_doc]
    for token in doc:
        if token.text in other_tokens:
            overlap.append(token)
    return overlap


def _load_utils(nlp):
    Doc.set_extension("overlap", method=overlap_tokens)
    Span.set_extension("overlap", method=overlap_tokens)
    nlp.add_pipe(better_boundaries, before="parser")
    nlp.vocab["s"].is_stop = True
    # Adding s to the list of stop words


def load_extensions(nlp):
    _load_lexicons()
    _load_s2v()
    _load_sentiment(nlp)
    _load_triples(nlp)
    _load_inflection()
    _load_lingua_franca(nlp)
    _load_brown(nlp)
    _load_wordnet()
    _load_utils(nlp)


