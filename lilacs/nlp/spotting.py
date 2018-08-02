import spotlight
from lilacs.settings import SPOTLIGHT_URL
from padaos import IntentContainer
from lilacs.nlp import get_nlp
from lilacs.nlp.parse import normalize
from spacy.parts_of_speech import NOUN, PROPN, VERB


class BasicQuestionParser(object):
    """
    Poor-man's english question parser. Not even close to conclusive, but
    appears to construct some decent w|a queries and responses.

    """

    def __init__(self):
        self.container = IntentContainer()
        self.container.add_entity('question', ['what', 'when', 'where', 'why', 'how', 'which', 'whose', 'who'])

        self.container.add_intent('what of', ['what (is|are|were|was|did|does|do) {first_query} of {second_query}'])
        self.container.add_intent('what', ['what (is|are|were|was|did|does|do) {query}', 'tell me about {query}'])

        self.container.add_intent('when', ['when (is|are|were|was|did|does|do) {query}'])
        self.container.add_intent('where', ['where (is|are|were|was|did|does|do) {query}'])

        self.container.add_intent('why', ['why (is|are|were|was|did|does|do) {query}'])
        self.container.add_intent('how to', ['how (to|do) {query}'])
        self.container.add_intent('how much', ['how (much|many) {query}'])
        self.container.add_intent('how long', ['how long {query}'])
        self.container.add_intent('which', ['which {query}'])
        self.container.add_intent('whose', ['whose {query}'])
        self.container.add_intent('who', ['who {query}'])

        self.container.add_intent('example',
                                  ['(are|is) {first_query} (a|an|an example of|an instance of) {second_query}',
                                   "{sometext} example of {query}"])

        self.container.add_intent('common',
                                  ['{first_query} and {second_query} in common'])

        self.container.add_intent('should', ['should (i|we) {query}'])

        self.container.add_intent('will you', ['(are|will|do) you {query}'])
        self.container.add_intent('have you', ['(have|were|did) you {query}'])

    def parse(self, utterance):
        match = self.container.calc_intent(utterance)
        data = {"Query": utterance}
        data["QuestionWord"] = match["name"]
        entities = match["entities"]
        if "query" in entities:
            data["Query"] = entities["query"]
        if "first_query" in entities and "second_query" in entities:
            data["Query"] = entities["first_query"] + " " + entities["second_query"]
            data["Query1"] = entities["first_query"]
            data["Query2"] = entities["second_query"]
        return data


class LILACSQuestionParser(object):
    # these are mostly hand picked by trial and error, may need tuning
    IGNORES = ["example", "examples", "much", "is", "me", "who", "what",
               "when", "why", "how", "which", "whose", "common", "are", "at", "was"]
    SUBJECTS = ["nsubj", "nsubjpass"]
    OBJECTS = ["dobj", "pobj", "dobj"]

    def __init__(self, host=SPOTLIGHT_URL, nlp=None):
        self.nlp = nlp or get_nlp()
        self.parser = BasicQuestionParser()
        self.host = host

    def get_noun_chunks(self, doc):
        chunks =[ chunk.text for chunk in doc.noun_chunks if chunk.text not in self.IGNORES]
        for i, chunk in enumerate(chunks):
            words = chunk.split(" ")
            for idx, w in enumerate(words):
                if w in self.IGNORES:
                    words[idx] = ""
            chunks[i] = " ".join(words)
        return chunks

    def get_subject_object(self, doc):
        sub_toks = [str(tok) for tok in doc if (tok.dep_ in self.SUBJECTS) and str(tok) not in self.IGNORES]
        obj_toks = [str(tok) for tok in doc if (tok.dep_ in self.OBJECTS) and str(tok) not in self.IGNORES]
        #print("Subjects:", sub_toks)
        #print("Objects :", obj_toks)
        return sub_toks, obj_toks

    def get_root(self, doc):
        r = [str(tok) for tok in doc if (tok.dep_ == "ROOT")]
        if len(r):
            r = r[0]
        return r if r not in self.IGNORES else ""

    def get_main_verbs_of_sent(self, doc):
        """Return the main (non-auxiliary) verbs in a sentence."""
        return [tok for tok in doc
                if tok.pos == VERB and tok.dep_ not in {'aux', 'auxpass'}]

    def parse_question(self, text):
        text = normalize(text, True, False)
        subjects, parents, synonyms, url = self.spotlight_tag(text)

        # select center and target node using nlp parsing
        doc = self.nlp(text)

        target_node = ""
        subjects, objects = self.get_subject_object(doc)
        if len(subjects):
            center_node = subjects[0]
            if len(objects):
                target_node = objects[0]
            elif len(subjects) > 1:
                target_node = subjects[1]
        elif len(objects):
            center_node = objects[0]
            if len(objects) > 1:
                target_node = objects[1]
        else:
            center_node = self.get_root(doc)

        parse = self.regex_parse(text)
        # failsafe, use regex query
        if not center_node:
            if "Query1" in parse:
                center_node = parse["Query1"]
                target_node = parse["Query2"]
            else:
                center_node = parse["Query"]

        if not target_node:
            if "Query2" in parse:
                target_node = parse["Query2"]
            else:
                # extract noun chunks and pick last one
                chunks = self.get_noun_chunks(doc)
                chunks = [c for c in chunks if center_node not in c]
                if len(chunks):
                    target_node = chunks[-1]
                elif center_node != parse["Query"]:
                    target_node = parse["Query"].replace(center_node, "").replace("  ", " ")

        # rename user and self tags
        if center_node == "i":
            center_node = "user"
        elif center_node == "you":
            center_node = "self"
        if target_node == "i":
            target_node = "user"
        elif target_node == "you":
            target_node = "self"

        question = parse["QuestionWord"]
        root = self.get_root(doc)
        verbs = self.get_main_verbs_of_sent(doc)
        middle = [node for node in subjects if node != center_node and node != target_node]
        concepts = {"parents": parents, "synonyms": synonyms, "relevant": middle}
        data = {"source": center_node.strip(), "target": target_node.strip(), "concepts": concepts,
                "question_type": question, "question_root": root, "verbs": verbs}

        return data

    def regex_parse(self, text):
        parse = self.parser.parse(text)
        for k in ["Query", "Query1", "Query2"]:
            if not parse.get(k):
                continue
            words = parse[k].split(" ")
            for idx, w in enumerate(words):
                w = w.strip()
                if w in self.IGNORES:
                    words[idx] = ""
            parse[k] = " ".join(words)
        return parse

    def spotlight_tag(self, text):
        text = text.lower()
        subjects = {}
        parents = {}
        synonims = {}
        urls = {}
        try:
            annotations = spotlight.annotate(self.host, text)
            for annotation in annotations:

                score = annotation["similarityScore"]
                # entry we are talking about
                subject = annotation["surfaceForm"].lower()
                # index in text where it starts
                offset = annotation["offset"]
                # TODO tweak this value and make configuable
                if float(score) < 0.4:
                    continue
                subjects.setdefault(subject, offset)
                # categorie of this <- linked nodes <- parsing for dbpedia search
                if annotation["types"]:
                    p = []
                    types = annotation["types"].split(",")
                    for label in types:
                        label = label.replace("DBpedia:", "").replace("Schema:", "").replace("Http://xmlns.com/foaf/0.1/",
                                                                                           "").lower()
                        if label not in p and ":" not in label:
                            p.append(label)
                    parents.setdefault(subject, p)
                # dbpedia link
                urls[subject] = annotation["URI"]
                # print "link: " + url
                dbpedia_name = urls[subject].replace("http://dbpedia.org/resource/", "").replace("_", " ")
                if dbpedia_name.lower() not in subject:
                    synonims.setdefault(subject, dbpedia_name.lower())
        except:
            pass
        return subjects, parents, synonims, urls


def spot_concepts(text):
    parser = LILACSQuestionParser()
    subjects, parents, synonyms, urls = parser.spotlight_tag(text)

    concepts = {}
    for a in subjects:
        concepts[a] = {}
    for a in parents:
        b = synonyms[a]

        concepts[a] = {"instance of": b}
    for a in synonyms:
        b = synonyms[a]

        concepts[a] = {"synonym": b}
    for a in urls:
        b = urls[a]

        concepts[a] = {"link": b}

    return concepts


def test_qp():
    parser = LILACSQuestionParser()

    questions = ["dogs and cats in common",
                 "tell me about evil",
                 "how to kill animals ( a cow ) and make meat",
                 "what is a living being",
                 "why are humans living beings",
                 "give examples of animals",
                 "what is the speed of light",
                 "when were you born",
                 "where do you store your data",
                 "will you die",
                 "have you finished booting",
                 "should i program artificial stupidity",
                 "who made you",
                 "how long until sunset",
                 "how long ago was sunrise",
                 "how much is bitcoin worth",
                 "which city has more people",
                 "whose dog is this"]

    for text in questions:
        data = parser.parse_question(text)
        print("\nQuestion: " + text)
        print("start_node: " + str(data["source"]))
        print("target_node: " + str(data["target"]))
        print("question_type: " + str(data["question_type"]))
        print("question_root: " + str(data["question_root"]))
        print("question_verbs: " + str(data["verbs"]))
        print("parents: " + str(data["concepts"]["parents"]))
        print("relevant_nodes: " + str(data["concepts"]["relevant"]))
        print("synonyms: " + str(data["concepts"]["synonyms"]))


if __name__ == '__main__':
    test_qp()
