import requests
import random
from lilacs.processing.comprehension import textual_entailment, comprehension
from lilacs.processing.comprehension.extraction import LILACSextractor
import wikipedia
import spacy
import math
from lilacs.memory.data_sources import LILACSKnowledge
from lilacs.processing import LILACSTextAnalyzer
from lilacs.processing.nlp.word_vectors import similar_turkunlp_demo, similar_sense2vec, similar_sense2vec_demo

from numpy import dot
from numpy.linalg import norm


# DO NOT ABUSE
def ask_euclid(text):
    url = "http://euclid.allenai.org/api/solve?query=" + text
    return requests.get(url).text


# DO NOT ABUSE
# use the source https://github.com/allenai/aristo-mini
def ask_aristo(text, raw=False):
    url = "http://aristo-demo.allenai.org/api/ask?text=" + text
    data = requests.get(url).json()
    if raw:
        return data
    answers = data["response"]["success"]["answers"]

    response = {}
    for a in answers:
        # 'confidence', 'analyses', 'selection', 'selected'
        if a["selected"]:
            response["answer"] = a["selection"]["directAnswer"]["answer"]
            response["confidence"] = a["confidence"]
            data = a["analyses"][0]["analysis"]["analyses"][0]
            response["expectedAnswerType"] = data['expectedAnswerType']
            response['questionSentence'] = data['questionSentence']
            response['questionType'] = data['questionType']
            response['questionTheme'] = data['questionTheme']
            response['questionSetup'] = data['questionSetup']
            response["dataSource"] = data["sourceFriendlyName"]
            response["top20"] = data['top20ThisCluster']
    return response


def EYE_rest(data, rules="", query="{ ?a ?b ?c. } => { ?a ?b ?c. }.", server_url="http://eye.restdesc.org/"):
    if rules:
        data = data + "\n" + rules
    r = requests.post(server_url, json={"data": data, "query": query}).text
    return r


class LILACSReasoner(object):
    coref_nlp = None
    analyzer = LILACSTextAnalyzer

    def __init__(self, bus=None, coref_nlp=None):
        self.bus = bus
        if LILACSReasoner.coref_nlp is None and coref_nlp is not None:
            LILACSReasoner.coref_nlp = coref_nlp

    @staticmethod
    def is_math_question(question):
        # check for number references
        if LILACSextractor.extract_number(question):
            # check for math operation vocabulary
            math_qualifier = ["plus", "+", "-", "minus", "divid", "/", "multipl", "times",
                              "*", "exp", "integral", "root", "^", "percent", "%"]
            for m in math_qualifier:
                if m in question:
                    # seems a math question
                    return True
        return False

    @staticmethod
    def related_nodes(concept, n=5, engine="sense2vec_demo"):
        if engine == "sense2vec_demo":
            return similar_sense2vec_demo(concept)
        elif engine == "sense2vec":
            return similar_sense2vec(concept, num=n, nlp=LILACSReasoner.coref_nlp)
        elif engine == "turkunlp_demo":
            return similar_turkunlp_demo(concept, n=n)
        return []

    @staticmethod
    def answer_choice(question, choices, engine="allennlp_demo"):
        # use textual entailment to select best choice
        best = random.choice(choices)
        best_entailment = 0
        for c in choices:
            data = textual_entailment(question, c)
            e = data["entailment"]
            if e > best_entailment:
                best = c
                best_entailment = e
        return best

    @staticmethod
    def answer_corpus(question, corpus):
        # machine comprehension, look for answers in text corpus
        return comprehension(question, corpus)

    @staticmethod
    def answer_wikipedia(question, concept):
        wiki_name = wikipedia.search(concept)
        if wiki_name:
            page = wikipedia.page(wiki_name[0])
            corpus = page.content
            return LILACSReasoner.answer_corpus(question, corpus)
        return None

    @staticmethod
    def analogy(a, b, c, nlp=None):
        parser = nlp or spacy.load('en_core_web_md')
        # cosine similarity
        cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))
        # Let's see if it can figure out this analogy
        # Man is to King as Woman is to ??
        a = parser.vocab[a]
        b = parser.vocab[b]
        c = parser.vocab[c]

        result = b.vector - a.vector + c.vector

        # gather all known words, take only the lowercased versions
        allWords = list({w for w in parser.vocab if
                         w.has_vector and w.orth_.islower() and w.lower_ != "king" and w.lower_ != "man" and w.lower_ != "woman"})
        # sort by similarity to the result
        allWords.sort(key=lambda w: cosine(w.vector, result), reverse=True)

        print(allWords[0].orth_, allWords[1].orth_, allWords[2].orth_)
        return allWords[:3]

    # WIP
    def answer(self, question):
        if LILACSReasoner.is_math_question(question):
            ans = LILACSReasoner.euclid(question)
            if len(ans):
                return ans[0]
        # TODO LILACS question parser
        # TODO wolfram etc
        return LILACSReasoner.aristo(question)["answer"]

    def what(self, node):
        pass

    def sci_tail(self, question, choices):
        # multiple choice
        # https://github.com/allenai/scitail
        return None

    # external
    @staticmethod
    def EYE(data, rules="", query="{ ?a ?b ?c. } => { ?a ?b ?c. }."):
        return EYE_rest(data, rules, query)

    @staticmethod
    def aristo(query, engine="aristo_demo"):
        # TODO support https://github.com/allenai/aristo-mini
        return ask_aristo(query)

    @staticmethod
    def euclid(query):
        return ask_euclid(query)


if __name__ == "__main__":
    LILACS = LILACSReasoner()

    parser = spacy.load('en_core_web_lg')

    # genders
    #assert LILACS.analogy("man", "king", "woman", parser)[0] == "queen"

    # capitals
    LILACS.analogy('Paris', 'France', 'Rome', parser)

    #assert LILACS.analogy('walk', 'walked', 'go', parser)[0] == "went"

    # tenses
    LILACS.analogy('quick', 'quickest', 'smart', parser)


    LILACS.analogy('dog', 'mammal', 'chicken', parser)
    #dog - mammal is like
    #eagle - bird

    t = "Elon Musk"
    q = "where was Elon Musk born"
    #print(LILACSReasoner.answer_wikipedia(q, t))
    # Pretoria, South Africa

    p = "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. These technologies are used to develop machines that can substitute for humans. Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive. Robots can take on any form but some are made to resemble humans in appearance. This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people. Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do."
    q = "What do robots that resemble humans attempt to do?"
    # print(LILACS.answer_corpus(q, p))
    # replicate walking, lifting, speech, cognition

    t = "Which tool should a student use to compare the masses of two small rocks?"
    c = ["balance", "hand lens", "ruler", "measuring cup"]
    # print(LILACS.answer_choice(t, c))
    # balance
    # print(LILACS.is_math_question(t))
    # False

    t = "If 30 percent of 48 percent of a number is 288, what is the number?"
    # print(LILACS.is_math_question(t))
    # True
    # print(LILACS.euclid(t))
    # ["2000"]

    t = """Which tool should a student use to compare the masses of two small rocks?
    (A) balance
    (B) hand lens
    (C) ruler
    (D) measuring cup
    """
    # print(LILACS.aristo(t))
    # {'expectedAnswerType': 'tool', 'questionSetup': '', 'questionTheme': 'None', 'answer': 'A metric ruler and a balance will measure the size and mass of an object.', 'top20': [{'matchedText': 'A metric ruler and a balance will measure the size and mass of an object.', 'answerText': 'A metric ruler and a balance will measure the size and mass of an object.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.979915201663971, 'index': 'barrons-2016-09-21'}, {'matchedText': 'Scientists need balances that can measure very small amounts of mass.', 'answerText': 'Scientists need balances that can measure very small amounts of mass.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.6653347611427307, 'index': 'websentences-2016-09-08'}, {'matchedText': 'Balance : used to measure the mass of an object to a know unit of mass. Compass : a tool that uses a magnetized pointer to show magnetic north.', 'answerText': 'Balance : used to measure the mass of an object to a know unit of mass. Compass : a tool that uses a magnetized pointer to show magnetic north.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.6450331807136536, 'index': 'websentences-2016-09-08'}, {'matchedText': 'Mass is usually measured with a balance.', 'answerText': 'Mass is usually measured with a balance.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.6091084480285645, 'index': 'ck12-flexbook-gr5-sentences-2016-10-19'}, {'matchedText': 'A balance is used to measure mass.', 'answerText': 'A balance is used to measure mass.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.6091084480285645, 'index': 'websentences-2016-09-08'}, {'matchedText': 'A balance measures mass.', 'answerText': 'A balance measures mass.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.6091084480285645, 'index': 'barrons-2016-09-21'}, {'matchedText': 'A balance compares the mass of an object with an object of known mass.', 'answerText': 'A balance compares the mass of an object with an object of known mass.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.590347170829773, 'index': 'websentences-2016-09-08'}, {'matchedText': "To properly determine mass, you could use a balancing scale and compare an object's mass to another object, whose mass is known, such as measured weights.", 'answerText': "To properly determine mass, you could use a balancing scale and compare an object's mass to another object, whose mass is known, such as measured weights.", 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5843542218208313, 'index': 'websentences-2016-09-08'}, {'matchedText': 'The scale measures weight relevant to the force of gravity while the balance is used to compare the mass of two different objects .', 'answerText': 'The scale measures weight relevant to the force of gravity while the balance is used to compare the mass of two different objects .', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5748049020767212, 'index': 'websentences-2016-09-08'}, {'matchedText': 'An instrument used to measure mass is a balance.', 'answerText': 'An instrument used to measure mass is a balance.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5329698920249939, 'index': 'virginiaflashcard-sentences-2016-10-12'}, {'matchedText': 'A balance is used to measure the mass of an object.', 'answerText': 'A balance is used to measure the mass of an object.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5329698920249939, 'index': 'websentences-2016-09-08'}, {'matchedText': 'To measure mass scientists use a balance.', 'answerText': 'To measure mass scientists use a balance.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5329698920249939, 'index': 'barrons-2016-09-21'}, {'matchedText': 'A balance can measure weight and mass.', 'answerText': 'A balance can measure weight and mass.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5329698920249939, 'index': 'websentences-2016-09-08'}, {'matchedText': 'However, there are several designs of the anemometer and the cup version is not the only measuring tool available.', 'answerText': 'However, there are several designs of the anemometer and the cup version is not the only measuring tool available.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.507074236869812, 'index': 'websentences-2016-09-08'}, {'matchedText': 'An example of a ruler is a wooden tool used to measure the length of a piece of paper.', 'answerText': 'An example of a ruler is a wooden tool used to measure the length of a piece of paper.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5027037262916565, 'index': 'websentences-2016-09-08'}, {'matchedText': 'Tools for measuring length range from simple rulers to lasers.', 'answerText': 'Tools for measuring length range from simple rulers to lasers.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5027037262916565, 'index': 'websentences-2016-09-08'}, {'matchedText': 'A metric ruler is a tool used to measure objects using the metric system.', 'answerText': 'A metric ruler is a tool used to measure objects using the metric system.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5027037262916565, 'index': 'websentences-2016-09-08'}, {'matchedText': 'The standard ruler is the most common tool used to measure in inches.', 'answerText': 'The standard ruler is the most common tool used to measure in inches.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.5027037262916565, 'index': 'websentences-2016-09-08'}, {'matchedText': 'Balance used for measurement Mass is measured using a pan balance, a triple-beam balance, lever balance or electronic balance.', 'answerText': 'Balance used for measurement Mass is measured using a pan balance, a triple-beam balance, lever balance or electronic balance.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.49989789724349976, 'index': 'websentences-2016-09-08'}, {'matchedText': 'The measurement of mass in the laboratory is performed using balances.', 'answerText': 'The measurement of mass in the laboratory is performed using balances.', 'luceneQuery': 'tool compare masses small rocks balance hand lens ruler measuring cup ', 'luceneScore': 0.45683130621910095, 'index': 'websentences-2016-09-08'}], 'questionType': 'Which', 'dataSource': 'Barrons 4th Grade Study Guide', 'questionSentence': 'Which tool should a student use to compare the masses of two small rocks?', 'confidence': 0.09799152016639709}

    data = """@prefix ppl: <http://example.org/people#>.
    @prefix foaf: <http://xmlns.com/foaf/0.1/>.

    ppl:Cindy foaf:knows ppl:John.
    ppl:Cindy foaf:knows ppl:Eliza.
    ppl:Cindy foaf:knows ppl:Kate.
    ppl:Eliza foaf:knows ppl:John.
    ppl:Peter foaf:knows ppl:John."""

    rules = """@prefix foaf: <http://xmlns.com/foaf/0.1/>.

    {
        ?personA foaf:knows ?personB.
    }
    =>
    {
        ?personB foaf:knows ?personA.
    }."""

    # print(LILACS.EYE(data, rules))
    # PREFIX ppl: <http://example.org/people#>
    # PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #
    # ppl:Cindy foaf:knows ppl:John.
    # ppl:Cindy foaf:knows ppl:Eliza.
    # ppl:Cindy foaf:knows ppl:Kate.
    # ppl:Eliza foaf:knows ppl:John.
    # ppl:Peter foaf:knows ppl:John.
    # ppl:John foaf:knows ppl:Cindy.
    # ppl:Eliza foaf:knows ppl:Cindy.
    # ppl:Kate foaf:knows ppl:Cindy.
    # ppl:John foaf:knows ppl:Eliza.
    # ppl:John foaf:knows ppl:Peter.
