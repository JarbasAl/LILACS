from __future__ import print_function
from builtins import str
from builtins import object
import re
import spotlight
from lilacs.nodes.concept import ConceptDatabase
from lilacs.settings import SPOTLIGHT_URL


class EnglishQuestionParser(object):
    """
    Poor-man's english question parser. Not even close to conclusive, but
    appears to construct some decent w|a queries and responses.

    __author__ = 'seanfitz'

    """

    def __init__(self):
        self.regexes = [
            # re.compile(
            #    ".*(?P<QuestionWord>are) "
            #    "(?P<Query>.*)"),
            re.compile(
                ".*(?P<QuestionWord>who|what|when|where|why|which|whose) "
                "(?P<Query1>.*) (?P<QuestionVerb>is|are|was|were) "
                "(?P<Query2>.*)"),
            re.compile(
                ".*(?P<QuestionWord>are|is) "
                "(?P<Query1>.*) (?P<QuestionVerb>an|a|an example off|an instance off) "
                "(?P<Query2>.*)"),
            re.compile(
                "(?P<Query1>.*) (?P<QuestionVerb>and) "
                "(?P<Query2>.*) (?P<QuestionWord>in common)"),
            re.compile(
                ".*(?P<QuestionWord>talk|rant|think) "
                "(?P<QuestionVerb>\w+) (?P<Query>.*)"),
            re.compile(
                ".*(?P<QuestionWord>who|what|when|where|why|which|how|examples) "
                "(?P<QuestionVerb>\w+) (?P<Query>.*)")
        ]

    def _normalize(self, groupdict):
        if 'Query' in groupdict:
            return groupdict
        elif 'Query1' and 'Query2' in groupdict:
            return {
                'QuestionWord': groupdict.get('QuestionWord'),
                'QuestionVerb': groupdict.get('QuestionVerb'),
                'Query': ' '.join([groupdict.get('Query1'), groupdict.get(
                    'Query2')])
            }

    def parse(self, utterance):
        for regex in self.regexes:
            match = regex.match(utterance)
            if match:
                return self._normalize(match.groupdict())
        return None


class LILACSQuestionParser(object):
    def __init__(self, host = SPOTLIGHT_URL):
        self.parser = EnglishQuestionParser()
        self.host = host

    def process_entities(self, text):

        subjects, parents, synonims, url = self.tag_from_dbpedia(text)
        center = 666
        center_node = ""
        for node in subjects:
            if subjects[node] < center:
                center = subjects[node]
                center_node = node

        target = 666
        # TODO better select target mechanism
        target_node = ""
        for node in subjects:
            if subjects[node] < target and node != center_node:
                target = subjects[node]
                target_node = node

        parse = self.poor_parse(text)
        try:
            question = parse["QuestionWord"]
        except:
            question = "unknown"
        middle = [node for node in subjects if node != center_node and node != target_node]
        return center_node, target_node, parents, synonims, middle, question

    def poor_parse(self, text):
        return self.parser.parse(text)

    def tag_from_dbpedia(self, text):
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
                    for type in types:
                        type = type.replace("DBpedia:", "").replace("Schema:", "").replace("Http://xmlns.com/foaf/0.1/",
                                                                                           "").lower()
                        if type not in p:
                            p.append(type)
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


def extract_concepts(text, save=False, db=None):
    parser = LILACSQuestionParser()
    subjects, parents, synonyms, urls = parser.tag_from_dbpedia(text)
    if save:
        db = db or ConceptDatabase(debug=False)

    concepts = {}
    for a in subjects:
        if save:
            db.add_concept(a)
        concepts[a] = {}
    for a in parents:
        b = synonyms[a]
        if save:
            db.add_connection(a, b, "instance of")
        concepts[a] = {"instance of": b}
    for a in synonyms:
        b = synonyms[a]
        if save:
            db.add_connection(a, b, "synonym")
        concepts[a] = {"synonym": b}
    for a in urls:
        b = urls[a]
        if save:
            db.add_connection(a, b, "link")
            concepts[a] = {"link": b}

    return concepts


def test_qp():
    parser = LILACSQuestionParser()

    questions = ["how to kill animals ( a cow ) and make meat", "what is a living being",
                 "why are humans living beings", "give examples of animals"]

    for text in questions:
        center_node, target_node, parents, synonims, midle, question = parser.process_entities(text)
        print("\nQuestion: " + text)
        print("question_type: " + question)
        print("center_node: " + center_node)
        print("target_node: " + target_node)
        print("parents: " + str(parents))
        print("relevant_nodes: " + str(midle))
        print("synonims: " + str(synonims))


if __name__ == '__main__':
    text = "i love dogs"
    annotations = spotlight.annotate(SPOTLIGHT_URL, text)
    for annotation in annotations:
        print(annotation)