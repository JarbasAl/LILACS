import requests
from functools import lru_cache
import math
from typing import Iterable, List

from gensim.parsing.preprocessing import STOPWORDS
from gensim.parsing.porter import PorterStemmer
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess

import numpy as np

stemmer = PorterStemmer()


@lru_cache(maxsize=1024)
def stem(word: str) -> str:
    """stemming words is not cheap, so use a cache decorator"""
    return stemmer.stem(word)


def tokenizer(sentence: str) -> List[str]:
    """use gensim's `simple_preprocess` and `STOPWORDS` list"""
    return [stem(token) for token in simple_preprocess(sentence) if token not in STOPWORDS]


def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """https://en.wikipedia.org/wiki/Cosine_similarity"""
    num = np.dot(v1, v2)
    d1 = np.dot(v1, v1)
    d2 = np.dot(v2, v2)

    if d1 > 0.0 and d2 > 0.0:
        return num / math.sqrt(d1 * d2)
    else:
        return 0.0


class WordTwoVec(object):
    """
    a wrapper for gensim.Word2Vec with added functionality to embed phrases and compute the
    "goodness" of a question-answer pair based on embedding-vector similarity
    """
    def __init__(self, model_file: str) -> None:
        if model_file.endswith(".bin"):
            self.model = Word2Vec.load_word2vec_format(model_file, binary=True)
        else:
            self.model = Word2Vec.load(model_file)

    def embed(self, words: Iterable[str]) -> np.ndarray:
        """given a list of words, find their vector embeddings and return the vector mean"""
        # first find the vector embedding for each word
        vectors = [self.model[word] for word in words if word in self.model]

        if vectors:
            # if there are vector embeddings, take the vector average
            return np.average(vectors, axis=0)
        else:
            # otherwise just return a zero vector
            return np.zeros(self.model.vector_size)

    def cosine_similarity(self, question_stem: str, choice_text: str) -> float:
        """how good is the choice for this question?"""
        question_words = {word for word in tokenizer(question_stem)}
        choice_words = {word for word in tokenizer(choice_text) if word not in question_words}
        return cosine_similarity(self.embed(question_words), self.embed(choice_words))


def similar_sense2vec_demo(text, sense="auto"):
    data = {"word": text, "sense": sense}
    r = requests.post("https://api.explosion.ai/sense2vec/find", data)
    return r.json()


def similar_sense2vec(text, nlp, num=5):
    doc = nlp(str(text))
    ents = []
    for token in doc:
        similar = [(s[0][0], s[1]) for s in token._.s2v_most_similar(num)]
        ents.extend([{"strength": int(s[1] * 100), "concept": str(s[0])} for s in similar if s[0] != text])
    return ents


# WIP - scrapping failing

# DO NOT ABUSE, de purposes only
# run from source https://github.com/fginter/w2v_demo

def similar_turkunlp_demo(text, n=10, model="Finnish+4B+wordforms+skipgram"):
    models = ["Suomi24 wordforms skipgram",
              "Finnish 4B wordforms skipgram",
              "Suomi24 lemmas skipgram",
              "English GoogleNews Negative300"]
    model = model.replace(" ", "+")
    text = text.replace(" ", "+")
    url = "http://bionlp-www.utu.fi/wv_demo/nearest"
    data = {
        "form[0][name]": "word",
        "form[0][value]": text,
        "form[1][name]": "topn",
        "form[1][value]": n,
        "model_name": model
    }
    headers = {"Host": "bionlp-www.utu.fi",
        "Connection": "keep-alive",
        "Content-Length": "148",
        "Origin": "http://bionlp-www.utu.fi",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Referer": "http://bionlp-www.utu.fi/wv_demo/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"}
    r = requests.post(url, data=data)
    print(r.text)


