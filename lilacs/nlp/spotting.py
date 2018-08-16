import spotlight
from lilacs.settings import SPOTLIGHT_URL
from padaos import IntentContainer
from lilacs.nlp import get_nlp
from lilacs.nlp.parse import normalize
from spacy.parts_of_speech import VERB


class BasicTeacher(object):
    """
    Poor-man's english connection extractor. Not even close to complete

    """
    nlp = None
    coref = None

    def __init__(self, nlp=None, coref=None, use_nlp=False):
        if use_nlp:
            self.nlp = nlp or self.nlp or get_nlp()
            self.coref = coref or self.coref

        self.container = IntentContainer()
        self.register_utterances()

    def register_utterances(self):
        self.container.add_intent('instance of', ['{source} (is|are|instance) {target}'])
        self.container.add_intent('sample of', ['{source} is (sample|example) {target}'])
        self.container.add_intent('incompatible', ['{source} (can not|is forbidden|is not allowed) {target}'])
        self.container.add_intent('synonym', ['{source} is (same|synonym) {target}'])
        self.container.add_intent('antonym', ['{source} is (opposite|antonym) {target}'])
        self.container.add_intent('part of', ['{source} is part {target}', '{target} is (composed|made) {source}'])
        self.container.add_intent('capable of', ['{source} (is capable|can) {target}'])
        self.container.add_intent('created by', ['{source} is created {target}'])
        self.container.add_intent('used for', ['{source} is used {target}'])

    def normalize(self, text):
        text = normalize(text, True, True, nlp=self.nlp, coref_nlp=self.coref)
        # lets be aggressive to improve parsing
        text = text.lower().replace("did you know that", "")
        text = text.replace("example", "sample of")
        words = text.split(" ")
        removes = ["a", "an", "of", "that", "this", "to", "with", "as", "by", "for"]
        replaces = {"be": "is", "are": "is", "you": "self", "was": "is", "i": "user", "were": "is"}
        for idx, word in enumerate(words):
            if word in removes:
                words[idx] = ""
            if word in replaces:
                words[idx] = replaces[word]

        return " ".join([w for w in words if w])

    def parse(self, utterance):
        utterance = self.normalize(utterance)
        match = self.container.calc_intent(utterance)

        data = match["entities"]
        data["normalized_text"] = utterance
        data["connection_type"] = match["name"]
        return data


class BasicQuestionParser(BasicTeacher):
    """
    Poor-man's english question parser. Not even close to conclusive, but
    appears to construct some decent w|a queries and responses.

    """
    def register_utterances(self):
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
        self.container.add_intent('teach', ['teach {query}'])

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


class LILACSQuestionParser(BasicQuestionParser):
    # these are mostly hand picked by trial and error, may need tuning
    IGNORES = ["example", "examples", "much", "is", "me", "who", "what",
               "when", "why", "how", "which", "whose", "common", "are", "at", "was"]
    SUBJECTS = ["nsubj", "nsubjpass"]
    OBJECTS = ["dobj", "pobj", "dobj"]
    HOST = SPOTLIGHT_URL

    def __init__(self, use_spotlight=False, nlp=None, coref=None):
        BasicQuestionParser.__init__(self, nlp, coref, True)
        self.use_spotlight = use_spotlight

    def get_noun_chunks(self, doc):
        chunks = [chunk.text for chunk in doc.noun_chunks if chunk.text not in self.IGNORES]
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
        # print("Subjects:", sub_toks)
        # print("Objects :", obj_toks)
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

    def normalize(self, text):
        text = normalize(text, False, False, nlp=self.nlp, coref_nlp=self.coref)
        # lets be aggressive to improve parsing
        text = text.lower().replace("did you know that", "teach")
        words = text.split(" ")
        removes = []
        replaces = {}
        for idx, word in enumerate(words):
            if word in removes:
                words[idx] = ""
            if word in replaces:
                words[idx] = replaces[word]

        return " ".join(words)

    def parse_question(self, text):
        text = self.normalize(text)
        # print(text)
        if self.use_spotlight:
            subjects, parents, synonyms, url = self.spotlight_tag(text)
        else:
            parents = {}
            synonyms = {}

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
                "question_type": question, "question_root": root, "verbs": verbs, "normalized_text": text}

        return data

    def regex_parse(self, text):
        parse = self.parse(text)
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

    @staticmethod
    def spotlight_tag(text):
        text = text.lower()
        subjects = {}
        parents = {}
        synonims = {}
        urls = {}
        try:
            annotations = spotlight.annotate(LILACSQuestionParser.HOST, text)
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
                        label = label.replace("DBpedia:", "").replace("Schema:", "").replace(
                            "Http://xmlns.com/foaf/0.1/",
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
        except Exception as e:
            print(e)
        return subjects, parents, synonims, urls


def spot_concepts(text):
    subjects, parents, synonyms, urls = LILACSQuestionParser.spotlight_tag(text)

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
                 "whose dog is this",
                 "did you know that dogs are animals"]

    for text in questions:
        data = parser.parse_question(text)
        print("\nQuestion: " + text)
        print("normalized: " + str(data["normalized_text"]))
        print("start_node: " + str(data["source"]))
        print("target_node: " + str(data["target"]))
        print("question_type: " + str(data["question_type"]))
        print("question_root: " + str(data["question_root"]))
        print("question_verbs: " + str(data["verbs"]))
        print("parents: " + str(data["concepts"]["parents"]))
        print("relevant_nodes: " + str(data["concepts"]["relevant"]))
        print("synonyms: " + str(data["concepts"]["synonyms"]))


def test_teacher():
    parser = BasicTeacher()

    questions = ["did you know that dogs are animals",
                 "did you know that fish is an example of animal",
                 "droids can not kill",
                 "you are forbidden to murder",
                 "you were created by humans",
                 "you are part of a revolution",
                 "robots are used to serve humanity",
                 "droids are the same as robots",
                 "murder is a crime",
                 "everything is made of atoms"]

    for text in questions:
        data = parser.parse(text)
        print("\nutterance: " + text)
        print("source:", data.get("source"))
        print("target:", data.get("target"))
        print("connection_type:", data.get("connection_type"))
        print("normalized_text:", data.get("normalized_text"))


if __name__ == '__main__':
    test_teacher()
    test_qp()
