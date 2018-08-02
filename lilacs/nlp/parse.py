from builtins import str
from lilacs.nlp import get_nlp, get_corefnlp
import textacy.extract
from lilacs.nlp.inflect import singularize as make_singular
from lilacs.util import NUM_STRING_EN
from spacy.parts_of_speech import NOUN, PROPN, VERB


def normalize(text, remove_articles=True, solve_corefs=True, coref_nlp=None, nlp=None):
    """ English string normalization """
    text = str(text.lower())
    text = singularize(text, nlp=nlp)
    words = text.split()  # this also removed extra spaces
    normalized = ""
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
        text = replace_coreferences(normalized[1:], coref_nlp)
    # strip the initial space
    return text


def extract_facts(subject, text, nlp=None, coref_nlp=None):
    facts = []
    nlp = nlp or get_nlp()
    # Parse the document with spaCy
    text = normalize(text, remove_articles=False, coref_nlp=coref_nlp)
    doc = nlp(text)
    # Extract semi-structured statements
    statements = textacy.extract.semistructured_statements(doc, subject)
    for statement in statements:
        subject, verb, fact = statement
        facts.append(fact)
    return facts


def extract_entities(text, nlp=None):
    nlp = nlp or get_nlp(False)
    # Parse the text with spaCy. This runs the entire pipeline.
    text = normalize(text, solve_corefs=False)
    doc = nlp(text)

    # 'doc' now contains a parsed version of text. We can use it to do anything we want!
    # For example, this will print out all the named entities that were detected:
    ents = []
    for entity in doc.ents:
        ents.append((entity.text, entity.label_))
    return ents


def replace_coreferences(text, nlp=None):
    # "My sister has a dog. She loves him." -> "My sister has a dog. My sister loves a dog."

    # """
    # London is the capital and most populous city of England and  the United Kingdom.
    # Standing on the River Thames in the south east of the island of Great Britain,
    # London has been a major settlement  for two millennia.  It was founded by the Romans,
    # who named it Londinium.
    # """ -> """
    # London is the capital and most populous city of England and  the United Kingdom.
    # Standing on the River Thames in the south east of the island of Great Britain,
    # London has been a major settlement  for two millennia.  London was founded by the Romans,
    # who named London Londinium.
    # """
    nlp = nlp or get_corefnlp()
    # Parse the text with spaCy. This runs the entire pipeline.
    doc = nlp(text)

    # 'doc' now contains a parsed version of text. We can use it to do anything we want!
    text = doc._.coref_resolved
    return text


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


def singularize(text, nlp = None):
    nlp = nlp or get_nlp()
    doc = nlp(text)
    ignores = ["this", "data", "my", "was"]
    words = []
    for tok in doc:
        if tok.pos == NOUN and str(tok) not in ignores:
            words.append(make_singular(str(tok)))
        else:
            words.append(str(tok))
    return " ".join(words)


if __name__ == "__main__":
    print(singularize("dogs are awesome animals"))