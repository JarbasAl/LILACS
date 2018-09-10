from lilacs.processing.comprehension.extraction import relation_extraction
from lilacs.processing.comprehension import replace_coreferences
from lilacs.processing.nlp.parse import normalize
from lilacs.processing.comprehension import constituency_parse_demo, textual_entailment_demo, comprehension_demo
from lilacs.settings import SPACY_MODEL
import textacy


class LILACSTextAnalyzer(object):
    def __init__(self, bus=None):
        self.bus = bus

    def normalize(self, text, remove_articles=False):
        return normalize(text, remove_articles=remove_articles)

    def coreference_resolution(self, text):
        return replace_coreferences(text)

    def possible_relations(self, sentences):
        if isinstance(sentences, str):
            sentences = [sentences]
        relations = []
        for s in sentences:
            for r in relation_extraction(s):
                if r[1] == "ALL_ZERO":
                    r = (r[0], "?", r[2])
                    continue
                relations.append(r)
        return relations

    def extract_nouns(self, text):
        # normalize
        text = self.normalize(text, remove_articles=False)
        doc = textacy.doc.Doc(text, lang=SPACY_MODEL)
        # Extract svo triples
        nouns = textacy.extract.noun_chunks(doc)
        return list(nouns)

    def extract_facts(self, subject, text):
        # normalize
        subject = subject.lower()
        text = self.normalize(text, remove_articles=False)
        doc = textacy.doc.Doc(text, lang=SPACY_MODEL)
        # Extract semi-structured statements
        statements = textacy.extract.semistructured_statements(doc, subject)
        facts = []
        for s in statements:
            fact = str(s[2]).strip().replace(" .", "")
            if fact not in facts:
                facts.append(fact)
        return facts

    def extract_triples(self, text):
        # normalize
        if not text:
            return []
        text = self.coreference_resolution(text)
        doc = textacy.doc.Doc(text, lang=SPACY_MODEL)
        # Extract svo triples
        triples = textacy.extract.subject_verb_object_triples(doc)
        t = []
        for tr in triples:
            trip = (str(tr[0]), str(tr[1]), str(tr[2]))
            if trip not in t:
                t.append(trip)
        return t

    def interesting_triples(self, text):
        interest = ["is", "has", "can"]
        discard = ["who", "they", "it", "she", "he", "them", "we", "there", "which", "is"]
        # Extract svo triples
        triples = [t for t in self.extract_triples(text) if t[1] in interest and t[2] not in discard and t[0] not in discard and t[0] != t[2]]
        return triples

    def answer_question(self, question, passage):
        #passage = self.normalize(passage)
        #question = self.normalize(question)
        return comprehension_demo(question, passage).lower()

    def validity_of_hypothesys(self, premise, hypothesys):
        return textual_entailment_demo(premise, hypothesys)

    def constituency_parse(self, text):
        return constituency_parse_demo(text)


if __name__ == "__main__":
    from pprint import pprint
    test_text = """London is the capital and most populous city of England and the United Kingdom.
    Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia.
    It was founded by the Romans, who named it Londinium. London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""
    LILACS = LILACSTextAnalyzer()
    #assert LILACS.coreference_resolution("My sister has a dog. She loves him.") == 'My sister has a dog. my sister loves a dog.'
    #pprint(LILACS.normalize(test_text))
    #pprint(LILACS.possible_relations(test_text.split(".")))
    """
    [('London', 'country', 'United Kingdom'),
     ('London', 'instance of', 'capital'),
     ('London', 'instance of', 'populous city'),
     ('England', 'instance of', 'capital'),
     ('England', 'instance of', 'populous city')]
    """
    #pprint(LILACS.extract_facts("London", test_text))
    """
    ['the capital and most populous city of england and the united kingdom',
    'a major settlement for 2 millennium']
    """
    #pprint(LILACS.extract_triples(test_text))
    pprint(LILACS.interesting_triples(test_text))
    """
    [('london', 'is', 'capital'),
     ('london', 'is', 'city'),
     ('london', 'is', 'kingdom')]
    """
    #pprint(LILACS.extract_nouns(test_text))

    question = "what is the capital of england"
    #assert LILACS.answer_question(question, test_text) == "london"
    question = "what is the most populous city of england"
    #assert LILACS.answer_question(question, test_text) == "london"
    question = "who founded london"
    #assert LILACS.answer_question(question, test_text) == "the romans"

    premise = "London is the capital and most populous city of England and the United Kingdom"
    hypothesys = "Humans live in London"
    #pprint(LILACS.validity_of_hypothesys(premise, hypothesys))
    """
    {'contradiction': 0.009316228330135345,
     'entailment': 0.936576783657074,
     'neutral': 0.05410700663924217}
    """

    premise = "Romans named London Londinium"
    hypothesys = "Romans never went to London"
    #pprint(LILACS.validity_of_hypothesys(premise, hypothesys))
    """
    {'contradiction': 0.9378615617752075,
     'entailment': 0.007486931513994932,
     'neutral': 0.054651517421007156}
    """
