# Lexicons Used
# NRC Emotion Lexicon - http://www.saifmohammad.com/WebPages/lexicons.html
# Bing Liu's Opinion Lexicon - http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
# MPQA Subjectivity Lexicon - http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
# Harvard General Inquirer - http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
# NRC Word-Colour Association Lexicon - http://www.saifmohammad.com/WebPages/lexicons.html

from lilacs.nlp.lexicons import LEXICON


# http://www.saifmohammad.com/WebDocs/ACL2011-word-colour-associations-poster.pdf
def get_color(word):
    if word in LEXICON:
        return LEXICON[word]["color"]
    return None


def get_emotion(word):
    if word in LEXICON:
        return LEXICON[word]["emotion"]
    return None


def get_sentiment(word):
    if word in LEXICON:
        return LEXICON[word]["sentiment"]
    return None


def get_subjectivity(word):
    if word in LEXICON:
        return LEXICON[word]["subjectivity"]
    return None


def get_orientation(word):
    if word in LEXICON:
        return LEXICON[word]["orientation"]
    return None
