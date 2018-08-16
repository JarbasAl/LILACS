#from builtins import str
#from os.path import join
#from lilacs.nlp import get_nlp
#from lilacs.settings import MODELS_DIR, SENSE2VEC_MODEL
#import sense2vec
import requests

"""

def init_s2v(nlp=None):
    nlp = nlp or get_nlp(False)
    try:
        from sense2vec import Sense2VecComponent
        s2v = Sense2VecComponent(join(MODELS_DIR, SENSE2VEC_MODEL))
        nlp.add_pipe(s2v)
    except ImportError:
        pass
    return nlp


def extract_s2vec_connections(subject, num=5, nlp=None):
    nlp = nlp or init_s2v()
    ents = similar_entities(subject, num, nlp)
    connections = [] # concept : [{type : con, strength: score}]
    for t in ents:
        target = t["concept"]
        strength = t["strength"]
        connections.append({"related": target, "con_strength": strength})
    return connections


def similar_entities(text, num=5, nlp=None):
    nlp = nlp or init_s2v()
    doc = nlp(str(text))
    ents = []
    for token in doc:
        similar = [(s[0][0], s[1]) for s in token._.s2v_most_similar(num)]
        ents.extend([{"strength": int(s[1] * 100), "concept": str(s[0])} for s in similar if s[0] != text])
    return ents


def similar(node, pos="NOUN", num=5, s2v=None):

    s2v = s2v or sense2vec.load(join(MODELS_DIR, SENSE2VEC_MODEL))
    cons = []
    try:
        freq, vector = s2v[node+'|'+pos]
        words, scores = s2v.most_similar(vector, n=num)
        for word, score in zip(words, scores):
            cons.append([word.split("|")[0].lower(), score])
    except KeyError:
        print("Invalid node:", node)
    return cons

"""


def get_similar(text, sense="auto"):
    data = {"word": text, "sense": sense}
    r = requests.post("https://api.explosion.ai/sense2vec/find", data)
    return r.json()

