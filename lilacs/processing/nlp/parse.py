from builtins import str
from lilacs.processing.nlp import get_nlp
from lilacs.processing.nlp.inflect import singularize as make_singular
from lilacs.util import NUM_STRING_EN
from lilacs.processing.comprehension import replace_coreferences
from spacy.parts_of_speech import NOUN, VERB
import requests


def normalize(text, remove_articles=True, solve_corefs=True, coref_nlp=None, nlp=None):
    """ English string normalization """
    text = str(text.lower())
    text = singularize(text, nlp=nlp)
    words = text.split()  # this also removed extra spaces
    normalized = ""
    # split punctuation into individual words
    punctuation = [",", ".", ";", "!", "#", "$", "%", "&", "/", "(", ")", "=", "?", "«",
                   "»", "<", ">", "[", "]", "{", "}", "@", '"', "'"]
    symbols_to_remove = ["(", ")", "[", "]", "#", "<", ">", "{", "}"]
    new_words = []
    for s in punctuation:
        for word in words:
            if word.startswith(s):
                if s not in symbols_to_remove:
                    new_words.append(s)
                new_words.append(word[1:])
            elif word.endswith(s):
                new_words.append(word[:-1])
                if s not in symbols_to_remove:
                    new_words.append(s)
            else:
                new_words.append(word)
    words = new_words

    for word in words:
        if remove_articles and word in ["the", "a", "an"]:
            continue

        # Expand common contractions, e.g. "isn't" -> "is not"
        contraction = ["ain't", "aren't", "can't", "could've", "couldn't",
                       "didn't", "doesn't", "don't", "gonna", "gotta",
                       "hadn't", "hasn't", "haven't", "he'd", "he'll", "he's",
                       "how'd", "how'll", "how's", "I'd", "I'll", "I'm",
                       "I've", "isn't", "it'd", "it'll", "it's", "mightn't",
                       "might've", "mustn't", "must've", "needn't",
                       "oughtn't",
                       "shan't", "she'd", "she'll", "she's", "shouldn't",
                       "should've", "somebody's", "someone'd", "someone'll",
                       "someone's", "that'll", "that's", "that'd", "there'd",
                       "there're", "there's", "they'd", "they'll", "they're",
                       "they've", "wasn't", "we'd", "we'll", "we're", "we've",
                       "weren't", "what'd", "what'll", "what're", "what's",
                       "whats",  # technically incorrect but some STT outputs
                       "what've", "when's", "when'd", "where'd", "where's",
                       "where've", "who'd", "who'd've", "who'll", "who're",
                       "who's", "who've", "why'd", "why're", "why's", "won't",
                       "won't've", "would've", "wouldn't", "wouldn't've",
                       "y'all", "ya'll", "you'd", "you'd've", "you'll",
                       "y'aint", "y'ain't", "you're", "you've"]
        if word in contraction:
            expansion = ["is not", "are not", "can not", "could have",
                         "could not", "did not", "does not", "do not",
                         "going to", "got to", "had not", "has not",
                         "have not", "he would", "he will", "he is",
                         "how did",
                         "how will", "how is", "I would", "I will", "I am",
                         "I have", "is not", "it would", "it will", "it is",
                         "might not", "might have", "must not", "must have",
                         "need not", "ought not", "shall not", "she would",
                         "she will", "she is", "should not", "should have",
                         "somebody is", "someone would", "someone will",
                         "someone is", "that will", "that is", "that would",
                         "there would", "there are", "there is", "they would",
                         "they will", "they are", "they have", "was not",
                         "we would", "we will", "we are", "we have",
                         "were not", "what did", "what will", "what are",
                         "what is",
                         "what is", "what have", "when is", "when did",
                         "where did", "where is", "where have", "who would",
                         "who would have", "who will", "who are", "who is",
                         "who have", "why did", "why are", "why is",
                         "will not", "will not have", "would have",
                         "would not", "would not have", "you all", "you all",
                         "you would", "you would have", "you will",
                         "you are not", "you are not", "you are", "you have"]
            word = expansion[contraction.index(word)]

        # Convert numbers into digits, e.g. "two" -> "2"
        text_numbers = {}
        for k in NUM_STRING_EN:
            text_numbers[NUM_STRING_EN[k]] = k

        if word in text_numbers:
            word = str(text_numbers[word])

        normalized += " " + word

    if solve_corefs:
        normalized = replace_coreferences(normalized[1:], coref_nlp)
    # strip the initial space
    return normalized


def is_negated_verb(token):
    """
    Returns True if verb is negated by one of its (dependency parse) children,
    False otherwise.

    Args:
        token (``spacy.Token``): parent document must have parse information

    Returns:
        bool

    TODO: generalize to other parts of speech; rule-based is pretty lacking,
    so will probably require training a model; this is an unsolved research problem
    """
    if token.doc.is_parsed is False:
        raise ValueError('token is not parsed')
    if token.pos == VERB and any(c.dep_ == 'neg' for c in token.children):
        return True
    # if (token.pos == NOUN
    #         and any(c.dep_ == 'det' and c.lower_ == 'no' for c in token.children)):
    #     return True
    return False


def singularize(text, nlp=None):
    nlp = nlp or get_nlp()
    doc = nlp(text)
    ignores = ["this", "data", "my", "was"]
    replaces = {"are": "is"}
    words = []
    for tok in doc:
        if tok.pos == NOUN and str(tok) not in ignores:
            words.append(make_singular(str(tok)))
        elif str(tok) in replaces:
            words.append(replaces[str(tok)])
        else:
            words.append(str(tok))
    return " ".join(words)


def dependency_tree(text, nlp=None):
    text = normalize(text, remove_articles=False, nlp=nlp)
    data = {"collapse_phrases": "1", "collapse_punctuation": "1", "model": "en_core_web_lg", "text": text}
    r = requests.post("https://api.explosion.ai/displacy/dep", data)
    return r.json()


if __name__ == "__main__":
    print(singularize("dogs are awesome animals"))
    #print(extract_entities("i ate cheese earlier this week, i hate it"))
