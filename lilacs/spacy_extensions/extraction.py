from textacy.spacier import utils as spacy_utils
import textacy.extract
from spacy.matcher import Matcher


def interesting_triples(doc, vocab, singularize=True):
    # Matcher class object
    matcher = Matcher(vocab)

    # define the pattern
    pattern = [{'DEP': 'ROOT'},
               {'DEP': 'prep', 'OP': "?"},
               {'DEP': 'agent', 'OP': "?"},
               {'POS': 'ADJ', 'OP': "?"}]

    matcher.add("triples", None, pattern)

    matches = matcher(doc)
    triples = []
    for k in range(len(matches)):
        span = doc[matches[k][1]:matches[k][2]]
        if singularize:
            rel = " ".join([tok._.lemma() for tok in span])
        else:
            rel = span.text

        root = span.root
        subj = spacy_utils.get_subjects_of_verb(root)
        obs = spacy_utils.get_objects_of_verb(root)
        if subj:
            subj = subj[0]
            for ob in obs:
                if ob and ob != subj:
                    triples.append((subj.text, rel, ob.text))
    return triples


def svo_triples(doc):
    return textacy.extract.subject_verb_object_triples(doc)


def extract_semi_structured_statements(doc, query=None):
    if query is None:
        triples = []
        for ent in textacy.extract.entities(doc, drop_determiners=True):
            for t in extract_semi_structured_statements(doc, ent.text):
                if t not in triples:
                    triples.append(t)
        return triples
    return textacy.extract.semistructured_statements(doc, query)
