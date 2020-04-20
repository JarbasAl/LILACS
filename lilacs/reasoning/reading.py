import requests
from lilacs.settings import ALLENNLP_URL
from lilacs import nlp
from lilacs.parse import SentenceParser
from jarbas_utils.parse import extract_sentences, split_sentences
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textacy.spacier import utils as spacy_utils


# allenai nlp server
def allen_elmo_bidaf(question, passage):
    # TODO DO NOT ABUSE, dev purposes only
    # curl 'http://demo.allennlp.org/predict/machine-comprehension' -H 'Origin: http://demo.allennlp.org' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Referer: http://demo.allennlp.org/machine-comprehension/MzIzOTM2' -H 'Connection: keep-alive' -H 'DNT: 1' --data-binary '{"passage":"Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. These technologies are used to develop machines that can substitute for humans. Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive. Robots can take on any form but some are made to resemble humans in appearance. This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people. Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do.","question":"What do robots that resemble humans attempt to do?"}' --compressed
    """
    Machine Comprehension (MC) answers natural language questions by selecting an answer span within an evidence text.
    The AllenNLP toolkit provides the following MC visualization, which can be used for any MC model in AllenNLP.
    This page demonstrates a reimplementation of BiDAF (Seo et al, 2017), or Bi-Directional Attention Flow,
    a widely used MC baseline that achieved state-of-the-art accuracies on the SQuAD dataset (Wikipedia sentences) in early 2017.

    :param question:
    :param passage:
    :return:
    """
    url = ALLENNLP_URL + "elmo-reading-comprehension"
    data = {"passage": passage, "question": question}
    r = requests.post(url, json=data).json()
    return r["best_span_str"]


def allen_bidaf(question, passage):
    """
    Machine Comprehension (MC) answers natural language questions by selecting an answer span within an evidence text.
    The AllenNLP toolkit provides the following MC visualization, which can be used for any MC model in AllenNLP.
    This page demonstrates a reimplementation of BiDAF (Seo et al, 2017), or Bi-Directional Attention Flow,
    a widely used MC baseline that achieved state-of-the-art accuracies on the SQuAD dataset (Wikipedia sentences) in early 2017.

    :param question:
    :param passage:
    :return:
    """
    url = ALLENNLP_URL + "reading-comprehension"
    data = {"passage": passage, "question": question}
    r = requests.post(url, json=data).json()
    return r["best_span_str"]


def allen_naqanet(question, passage):
    # TODO DO NOT ABUSE, dev purposes only
    """
    Machine Comprehension (MC) answers natural language questions by selecting an answer span within an evidence text.
    The AllenNLP toolkit provides the following MC visualization, which can be used for any MC model in AllenNLP.
    This page demonstrates a reimplementation of BiDAF (Seo et al, 2017), or Bi-Directional Attention Flow,
    a widely used MC baseline that achieved state-of-the-art accuracies on the SQuAD dataset (Wikipedia sentences) in early 2017.

    :param question:
    :param passage:
    :return:
    """
    url = ALLENNLP_URL + "naqanet-reading-comprehension"
    data = {"passage": passage, "question": question}
    r = requests.post(url, json=data).json()
    return r["answer"]["value"]


# baselines, retrieve sentence with more overlapping words
def best_sentence(question, passage):
    doc = nlp(question)
    question = doc._.enrich()
    question = question.replace("|", " ").replace("(", "").replace(")", "")
    return extract_sentences(question, passage)[0][0]


def bow_retrieve(question, passage):
    question = question.lower()
    sents = split_sentences(passage)

    norm_sents = [SentenceParser.normalize(s, make_singular=True,
                                           remove_stop_words=True,
                                           remove_pronouns=True).lower()
                  for s in sents]
    cv = CountVectorizer()

    feats = cv.fit_transform(norm_sents + [
        SentenceParser.normalize(question, make_singular=True,
                                 remove_stop_words=True,
                                 remove_pronouns=True).lower()])

    vals = cosine_similarity(feats[-1], feats)

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    score = flat[-2]
    if score == 0:
        return "?"
    else:
        return sents[idx]


def tfidf_retrieve(question, passage):
    sents = split_sentences(passage)
    norm_sents = [SentenceParser.normalize(s, make_singular=True,
                                           remove_stop_words=True,
                                           remove_pronouns=True).lower()
                  for s in sents]
    tfidf = TfidfVectorizer()

    feats = tfidf.fit_transform(norm_sents + [
        SentenceParser.normalize(question, make_singular=True,
                                 remove_stop_words=True,
                                 remove_pronouns=True).lower()])

    vals = cosine_similarity(feats[-1], feats)

    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    score = flat[-2]
    if score == 0:
        return "?"
    else:
        return sents[idx]


# default methods
def machine_comprehension(question, passage):
    return allen_elmo_bidaf(question, passage)


def generate_questions(text):
    """
    Generates a few simple questions by slot filling pieces from sentences
    """
    doc = nlp(text)

    results = {}
    for sentence in doc.sents:
        root = sentence.root
        ask_about = spacy_utils.get_subjects_of_verb(root)
        answers = [str(s) for s in spacy_utils.get_objects_of_verb(root)]
        if len(ask_about) > 0 and len(answers) > 0:
            if root.lemma_ == "be":
                question = f'What is {ask_about[0]}?'
            else:
                question = f'What does {ask_about[0]} {root.lemma_}?'
            if question not in results:
                results[question] = []
            results[question] += answers
    return [{"question": k, "answers": results[k]} for k in results]


if __name__ == "__main__":
    question = "what is the capital of the uk"
    question = "what is the area of london"
    #question = "who discovered london"
    passage = """London is the capital and most populous city of England and the United Kingdom.
       standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
       It was founded by the Romans, who named it Londinium. 
       London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. 
       Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""

    #print(generate_questions(passage))
    """
    [{
        'question': 'What is London?', 
        'answers': [capital, city, Kingdom, settlement]
     },
     {
        'question': 'What does core retain?', 
        'answers': [boundaries]
     }]
    """

    print(allen_elmo_bidaf(question, passage))
    #  print(allen_bidaf(question, passage))
    #  print(allen_naqanet(question, passage))

    print(best_sentence(question, passage))
    print(bow_retrieve(question, passage))
    print(tfidf_retrieve(question, passage))
