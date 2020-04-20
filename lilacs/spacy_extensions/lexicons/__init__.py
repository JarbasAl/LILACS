from os.path import join
from lilacs.settings import LEXICONS_DIR


def _load_lexicon():
    bucket = {}

    lexicon_path = join(LEXICONS_DIR, "word_emotion_lexicon.csv")
    with open(lexicon_path, "r") as f:
        lines = f.readlines()
        for l in lines[1:]:
            l = l.replace("\n", "")
            word, emotion, color, orientation, sentiment, subjectivity, source = l.split(",")
            bucket[word] = {"emotion": emotion,
                            "color": color,
                            "orientation": orientation,
                            "sentiment": sentiment,
                            "subjectivity": subjectivity,
                            "source": source}
    return bucket


LEXICON = _load_lexicon()


def lexicon_color(token):
    """
    http://www.saifmohammad.com/WebDocs/ACL2011-word-colour-associations-poster.pdf
    """
    word = token.text
    if word in LEXICON:
        return LEXICON[word]["color"]
    return None


def lexicon_emotion(token):
    word = token.text
    if word in LEXICON:
        return LEXICON[word]["emotion"]
    return None


def lexicon_sentiment(token):
    word = token.text
    if word in LEXICON:
        return LEXICON[word]["sentiment"]
    return None


def lexicon_subjectivity(token):
    word = token.text
    if word in LEXICON:
        return LEXICON[word]["subjectivity"]
    return None


def lexicon_orientation(token):
    word = token.text
    if word in LEXICON:
        return LEXICON[word]["orientation"]
    return None


def lexicon_colors(doc):
    lexicon_lookup = []
    for token in doc:
        atr = lexicon_color(token)
        if atr and atr not in lexicon_lookup:
            lexicon_lookup.append(atr)
    return lexicon_lookup


def lexicon_emotions(doc):
    lexicon_lookup = []
    for token in doc:
        atr = lexicon_emotion(token)
        if atr and atr not in lexicon_lookup:
            lexicon_lookup.append(atr)
    return lexicon_lookup


def lexicon_sentiments(doc):
    lexicon_lookup = []
    for token in doc:
        atr = lexicon_sentiment(token)
        if atr and atr not in lexicon_lookup:
            lexicon_lookup.append(atr)
    return lexicon_lookup


def lexicon_subjectivities(doc):
    lexicon_lookup = []
    for token in doc:
        atr = lexicon_subjectivity(token)
        if atr and atr not in lexicon_lookup:
            lexicon_lookup.append(atr)
    return lexicon_lookup


def lexicon_orientations(doc):
    lexicon_lookup = []
    for token in doc:
        atr = lexicon_orientation(token)
        if atr and atr not in lexicon_lookup:
            lexicon_lookup.append(atr)
    return lexicon_lookup


if __name__ == "__main__":
    from pprint import pprint

    pprint(LEXICON)