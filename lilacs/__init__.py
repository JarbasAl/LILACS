import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from os.path import join
from lilacs.nlp import get_nlp, get_corefnlp
from lilacs.nlp.spotting import LILACSQuestionParser, BasicTeacher
from lilacs.nodes.concept import ConceptDatabase
from lilacs.nlp.parse import extract_facts, extract_entities, normalize
from lilacs.data_sources.dictionary import extract_dictionary_connections
from lilacs.data_sources.conceptnet import extract_conceptnet_connections
from lilacs.data_sources.dbpedia import DbpediaEnquirer
from lilacs.data_sources.reddit_hivemind import get_similar
from lilacs.data_sources.wikidata import extract_wikidata_connections
from lilacs.data_sources.wikipedia import extract_wikipedia_connections
from lilacs.settings import MODELS_DIR, SENSE2VEC_MODEL
#import sense2vec
import time


class LILACS(object):
    nlp = get_nlp()
    coref_nlp = None
    teacher = BasicTeacher()
    parser = LILACSQuestionParser()
    s2v = None

    def __init__(self, debug=False):
        self.db = ConceptDatabase(debug=debug)
        self.past_actions = []
        self.status = {}
        self.status_update("boot")

    def status_update(self, action, data=None):
        data = data or {}
        self.status["last_action_timestamp"] = time.time()
        self.status["last_action_data"] = data
        self.status["last_action"] = action
        self.past_actions.append(dict(self.status))

    # text parsing
    def normalize(self, text):
        return normalize(text, True, True, self.coref_nlp)

    def extract_named_entities(self, text):
        ents = extract_entities(text)
        self.status_update("NER", ents)
        return ents

    def extract_facts(self, subject, text):
        text = self.normalize(text)
        facts = extract_facts(subject, text, self.nlp)
        self.status_update("extract_facts", facts)
        return facts

    # data aquisition
    def get_related_entities(self, subject, sense="auto"):
        data = get_similar(subject, sense)
        cons = []
        for r in data.get("results"):
            cons.append((r["text"].strip(), (r["score"] * 100) - 30))
        self.status_update("sense2vec", cons)
        return cons

    def populate_node(self, subject):
        dbpedia = DbpediaEnquirer()
        cons = dbpedia.get_dbpedia_cons_for_dblink(subject)
        for c, t in cons:
            print((c, t, 55))
        ents = extract_conceptnet_connections(subject)
        for c in ents:
            print(c)
        ents = extract_wikidata_connections(subject)
        for c in ents:
            print(c)
        #ents = self.get_related_entities(subject)
        #for c in ents:
        #    c = ("related", c[0], c[1])
        #    print(c)


    # nodes
    def add_node(self, subject, description="", node_type="idea"):
        self.db.add_concept(subject, description, type=node_type)

    def add_connection(self, source_name, target_name, con_type="related"):
        return self.db.add_connection(source_name, target_name, con_type)

    @property
    def concepts(self):
        return self.db.get_concepts()

    @property
    def connections(self):
        return self.db.get_connections()

    @property
    def total_concepts(self):
        return self.db.total_concepts()

    @property
    def total_connections(self):
        return self.db.total_connections()


if __name__ == "__main__":
    l = LILACS()
    l.populate_node("elon musk")