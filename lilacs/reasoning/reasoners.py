from numpy import dot
from numpy.linalg import norm
import requests


from lilacs.reasoning.solvers import TextualEntailmentSolver, \
    WordVectorSimilaritySolver
from lilacs.reasoning.reading import machine_comprehension
from lilacs.reasoning.entailment import textual_entailment
from lilacs.parse import SentenceParser
from lilacs.reasoning import LILACSTextAnalyzer
from wikipedia_for_humans import ask_about
from lilacs.settings import ALLENNLP_URL
from lilacs import nlp


def dependency_tree(text):
    text = SentenceParser.normalize(text, remove_articles=False)
    # TODO implement for realz
    data = {"collapse_phrases": "1", "collapse_punctuation": "1",
            "model": "en_core_web_lg", "text": text}
    r = requests.post("https://api.explosion.ai/displacy/dep", data)
    return r.json()


def semantic_role_labeling(sentence):
    #TODO  DO NOT ABUSE, dev purposes only
    """
    Semantic Role Labeling (SRL) recovers the latent predicate argument structure of a sentence,
    providing representations that answer basic questions about sentence meaning,
    including “who” did “what” to “whom,” etc.
    The AllenNLP toolkit provides the following SRL visualization, which can be used for any SRL model in AllenNLP.
    This page demonstrates a reimplementation of a deep BiLSTM model (He et al, 2017),
    which is currently state of the art for PropBank SRL (Newswire sentences).
    :param sentence:
    :return:
    """
    url = ALLENNLP_URL + "semantic-role-labeling"
    data = {"sentence": sentence}
    r = requests.post(url, json=data).json()
    roles = {}
    words = r["words"]
    verbs = r["verbs"]
    for v in verbs:
        arg0 = []
        arg1 = []
        verb = v["verb"]
        tags = v["tags"]
        for idx, t in enumerate(tags):
            if "I-ARGM" in t:
                arg0.append(words[idx])
            elif "I-ARG1" in t:
                arg1.append(words[idx])
        if not len(arg0):
            continue
        arg0 = " ".join(arg0)
        arg1 = " ".join(arg1)
        roles[verb] = [arg0, arg1]
    return roles


def constituency_parse(sentence):
    # TODO DO NOT ABUSE, dev purposes only
    """
    A constituency parse tree breaks a text into sub-phrases, or constituents. Non-terminals in the tree are types of phrases, the terminals are the words in the sentence. This demo is an implementation of a minimal neural model for constituency parsing based on an independent scoring of labels and spans described in Extending a Parser to Distant Domains Using a Few Dozen Partially Annotated Examples (Joshi et al, 2018). This model uses ELMo embeddings, which are completely character based and improves single model performance from 92.6 F1 to 94.11 F1 on the Penn Treebank, a 20% relative error reduction.
    :param sentence:
    :return:
    """
    url = ALLENNLP_URL + "constituency-parsing"
    data = {"sentence": sentence}
    r = requests.post(url, json=data).json()
    r.pop('class_probabilities')
    r.pop('spans')
    r.pop("slug")
    r.pop("num_spans")
    return r


def information_extraction(sentence):
    """
    Given an input sentence, Open Information Extraction (Open IE) extracts a list of propositions,
    each composed of a single predicate and an arbitrary number of arguments.
    These often simplify syntactically complex sentences, and make their
    predicate-argument structure easily accessible for various downstream tasks

    """
    url = ALLENNLP_URL + "open-information-extraction"
    data = {"sentence": sentence}
    r = requests.post(url, json=data).json()
    data["propositions"] = {}
    for v in r["verbs"]:
        verb = v["verb"]
        data["propositions"][verb] = {}
        data["propositions"][verb]["tags"] = v["tags"]
        data["propositions"][verb]["args"] = [
            a.split("]")[0].split(":")[1].strip()
            for a in v["description"].split("[")
            if a.startswith("ARG")]
    return data


def documentqa(sentence):
    """
    run a web search on the question, and additionally try to identify
     Wikipedia articles about entities mentioned in the question.
    The resulting documents will be passed to a machine learning algorithm
    which will try to read the text and identify a span of text within one of
    the documents that answers your questions. No knowledge bases or
    other sources of information are used.

    Example Questions
        Who won the World Cup in 2014?
        What is a group of porcupines called?
        Which artist created the sculpture "The Thinker"?
        Where did Harry Potter go to school?
        What has the strongest magnet field in the Universe?
        The reaction where two atoms of hydrogen combine to form an atom of helium is called what?
        Who the president of Spain?
    Weaknesses/Limitations
        The system can answer short answer questions, most other forms of questions are unlikely work, including:
        yes/no questions ("Are tomatoes vegetables?")
        math problems ("What is 21*123?")
        multiple choice questions ("Which is taller, the Space Needle taller or the Empire States building?")
        questions that do not have a concrete answer or require longer output ("What happened during WW2?", "Who is Barrack Obama?")
        questions that ask for a list ("What are some of the uses of aluminum?")
    The system has some weaknesses you might observe
        Time: It tends to return answers that might have once been true, but are not true currently.
        Fact vs. Opinion: It does not have a good sense of when a statement can be trusted as a fact.
        Complex reasoning: It can perform multiple steps of inference (ex "Who won the world Cup during Obama's first term as President?")

    :param sentence:
    :return:
    """
    url = "https://documentqa.allenai.org/answer"
    data = {"question": sentence}
    r = requests.get(url, data).json()

    data = {"sentence": sentence,
            "answers": [],
            "short_answers": [],
            "sources": [],
            "corpus": [],
            "conf": [],
            "raw": r
            }
    for answer in r:
        data["sources"].append(answer["source_url"])
        data["corpus"].append(answer["text"])
        data["conf"].append(answer["answers"][0]["conf"])
        ans = answer["text"][answer["answers"][0]["start"]:answer["answers"][0]["end"]]
        data["short_answers"].append(ans)
        for sent in answer["text"].replace(":", ".").replace("\n", ".").split("."):
            if ans in sent:
                data["answers"].append(sent)
                break
    return data


def EYE_rest(data, rules="", query="{ ?a ?b ?c. } => { ?a ?b ?c. }.", server_url="http://eye.restdesc.org/"):
    if rules:
        data = data + "\n" + rules
    r = requests.post(server_url, json={"data": data, "query": query}).text
    return r


class LILACSReasoner:
    """
    """
    analyzer = LILACSTextAnalyzer

    def __init__(self, bus=None):
        """

        Args:
            bus:
            coref_nlp:
        """
        self.bus = bus

    @staticmethod
    def is_math_question(question):
        """

        Args:
            question:

        Returns:

        """
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
    def answer_web(question):
        return documentqa(question)

    @staticmethod
    def answer_corpus(question, corpus):
        # machine comprehension, look for answers in text corpus
        return machine_comprehension(question, corpus)

    @staticmethod
    def answer_wikipedia(question, concept):
        return ask_about(question, concept)

    @staticmethod
    def analogy(a, b, c):
        # cosine similarity
        cosine = lambda v1, v2: dot(v1, v2) / (norm(v1) * norm(v2))
        # Let's see if it can figure out this analogy
        # Man is to King as Woman is to ??
        a = nlp.vocab[a]
        b = nlp.vocab[b]
        c = nlp.vocab[c]

        result = b.vector - a.vector + c.vector

        # gather all known words, take only the lowercased versions
        allWords = list({w for w in nlp.vocab if
                         w.has_vector and w.orth_.islower() and w.lower_ != "king" and w.lower_ != "man" and w.lower_ != "woman"})
        # sort by similarity to the result
        allWords.sort(key=lambda w: cosine(w.vector, result), reverse=True)

        #print(allWords[0].orth_, allWords[1].orth_, allWords[2].orth_)
        return [a.orth_ for a in allWords[:3]]

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


class LILACSMultipleChoiceReasoner:
    """
    """
    def __init__(self, bus=None):
        """

        Args:
            bus:
        """
        self.bus = bus
        self.entailment_model = TextualEntailmentSolver()
        self.vector_similarity_model = WordVectorSimilaritySolver()

    def textual_entailment(self, question, choices):
        """

        Args:
            question:
            choices:

        Returns:

        """
        scores = self.entailment_model.answer_question(question, choices)
        best = 0
        ans = None
        for s in scores:
            if s["entailment"] > best:
                best = s["entailment"]
                ans = scores.index(s)
        return ans

    def vector_similarity(self, question, choices):
        """

        Args:
            question:
            choices:

        Returns:

        """
        scores = self.vector_similarity_model.answer_question(question, choices)
        best = 0
        ans = None
        for s in scores:
            if s > best:
                best = s
                ans = scores.index(s)
        return ans

    def answer(self, question, choices):
        """

        Args:
            question:
            choices:

        Returns:

        """
        #a1 = self.vector_similarity(question, choices)
        a2 = self.textual_entailment(question, choices)
        return a2



if __name__ == "__main__":

    print(documentqa("what is the speed of light"))

    exit()
    LILACS = LILACSReasoner()

    # genders
    #assert LILACS.analogy("man", "king", "woman", parser)[0] == "queen"

    # capitals
    LILACS.analogy('Paris', 'France', 'Rome')

    #assert LILACS.analogy('walk', 'walked', 'go', parser)[0] == "went"

    # tenses
    LILACS.analogy('quick', 'quickest', 'smart')


    LILACS.analogy('dog', 'mammal', 'chicken')
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
