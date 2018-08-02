import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

from lilacs.nlp import get_nlp, get_corefnlp
from lilacs.nlp.spotting import LILACSQuestionParser
from lilacs.nodes.concept import ConceptDatabase
from lilacs.nlp.parse import extract_facts, extract_entities, normalize
from lilacs.data_sources.dictionary import extract_dictionary_connections
from lilacs.data_sources.conceptnet import extract_conceptnet_connections
#from lilacs.data_sources.dbpedia import extract_dbpedia_connections
from lilacs.data_sources.reddit_hivemind import extract_s2vec_connections, similar_entities
from lilacs.data_sources.wikidata import extract_wikidata_connections
from lilacs.data_sources.wikipedia import extract_wikipedia_connections


class LILACS(object):
    # TODO move here so it only loads once
    #nlp = get_nlp(True)
    #coref_nlp = get_corefnlp(True)

    def __init__(self, debug=False):
        self.parser = LILACSQuestionParser()
        self.db = ConceptDatabase(debug=debug)
        self.nlp = get_nlp(True)
        self.coref_nlp = get_corefnlp(True)

    # text parsing
    def normalize(self, text):
        return normalize(text, True, True, self.coref_nlp)

    def extract_named_entities(self, text):
        return extract_entities(text, self.nlp)

    def extract_facts(self, subject, text):
        text = self.normalize(text)
        return extract_facts(subject, text, self.nlp)

    # data aquisition
    def get_related_entities(self, subject, num=5):
        return similar_entities(subject, num, self.nlp)

    def populate_dictionary(self, subject):
        ents = extract_wikipedia_connections(subject, nlp=self.nlp)
        for c in ents:
            print(c)
        ents = extract_wikidata_connections(subject)
        for c in ents:
            print(c)
        ents = extract_s2vec_connections(subject, nlp=self.nlp)
        for c in ents:
            print(c)
        #ents = extract_dbpedia_connections(subject)
        for c in ents:
            print(c)
        ents = extract_dictionary_connections(subject)
        for c in ents:
            print(c)
        ents = extract_conceptnet_connections(subject)
        for c in ents:
            print(c)

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
    cons= l.concepts()
    for c in cons:
        print(c.name)