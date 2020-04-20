import spacy
from requests.exceptions import HTTPError
from jarbas_utils.log import LOG
from jarbas_utils.parse import extract_sentences, split_sentences
from jarbas_utils.json_helper import merge_dict
from simple_NER.annotators.names import NamesNER
from simple_NER.annotators.locations import LocationNER
from simple_NER.annotators.units import UnitsNER
from simple_NER.annotators.keyword_ner import KeywordNER
from simple_NER.annotators.remote.dbpedia import SpotlightNER
from simple_NER import Entity

from lilacs import nlp
from lilacs.settings import SPOTLIGHT_URL
from lilacs.parse import SentenceParser
from lilacs.exceptions import SpotlightDown
from lilacs.spacy_extensions.extraction import interesting_triples


class LILACSextractor:
    @staticmethod
    def extract_svo_triples(text):
        if not text:
            return []
        t = []

        for sent in split_sentences(text):
            doc = nlp(sent)
            # Extract svo triples
            triples = doc._.svo_triples
            for tr in triples:
                # filter circularity
                if str(tr[0]) != str(tr[2]):
                    trip = (str(tr[0]), str(tr[1]), str(tr[2]))
                    if trip not in t:
                        t.append(trip)
        return t

    @staticmethod
    def extract_interesting_triples(text, solve_corefs=False, singularize=False):
        triples = []
        if solve_corefs:
            text = SentenceParser.replace_coreferences(text)
        for sent in split_sentences(text):
            doc = nlp(sent)
            triples += interesting_triples(doc, nlp.vocab, singularize)
        return triples

    @staticmethod
    def extract_semi_structured_statements(text, query=None):
        doc = nlp(text)
        triples = []
        for t in doc._.extract_semi_structured_statements(query):
            triples += [(str(t[0]).strip(), str(t[1]).strip(),
                         str(t[2]).strip())]
        return triples

    @staticmethod
    def extract_facts(text, query=None):
        facts = []
        if query is None:
            for ent in LILACSextractor.extract_named_entities(text):
                _facts = ent["data"]["facts"]
                for f in _facts:
                    if f not in facts:
                        facts.append(f)
        else:
            for f, _ in extract_sentences(query, text):
                if f not in facts:
                    facts.append(f)
        return facts

    @staticmethod
    def extract_named_entities(text):
        """
        PERSON 	    People, including fictional.
        NORP 	    Nationalities or religious or political groups.
        FAC 	    Buildings, airports, highways, bridges, etc.
        ORG 	    Companies, agencies, institutions, etc.
        GPE 	    Countries, cities, states.
        LOC 	    Non-GPE locations, mountain ranges, bodies of water.
        PRODUCT 	Objects, vehicles, foods, etc. (Not services.)
        EVENT 	    Named hurricanes, battles, wars, sports events, etc.
        WORK_OF_ART 	Titles of books, songs, etc.
        LAW 	    Named documents made into laws.
        LANGUAGE 	Any named language.
        DATE 	    Absolute or relative dates or periods.
        TIME 	    Times smaller than a day.
        PERCENT 	Percentage, including "%".
        MONEY 	    Monetary values, including unit.
        QUANTITY 	Measurements, as of weight or distance.
        ORDINAL 	"first", "second", etc.
        CARDINAL 	Numerals that do not fall under another type.
        """
        entities = []
        # Process the text
        doc = nlp(text)

        # Iterate over the predicted entities
        for ent in doc.ents:
            explanation = spacy.explain(ent.label_)
            ent_text = SentenceParser.normalize(ent.text,
                                                remove_pronouns=True,
                                                remove_articles=True)
            ent = Entity(ent_text, ent.label_, text)
            facts = [f[0] for f in extract_sentences(ent.value, text)
                     if f[1] > 0.3]
            ent.data["facts"] = facts
            ent.data["explanation"] = explanation
            ent = ent.as_json()
            ent["tags"] = [ent.pop("entity_type")]
            ent.pop("spans")
            ent.pop("rules")
            ent.pop("source_text")
            if ent not in entities:
                entities.append(ent)

        entities.sort(key=lambda k: len(k["data"]["facts"]), reverse=True)
        return entities

    # simple_NER wrappers
    @staticmethod
    def extract_nouns(text):
        entities = []
        for sent in split_sentences(text):
            for ent in NamesNER().extract_entities(sent):
                facts = [f[0] for f in extract_sentences(ent.value, text)
                         if f[1] > 0.3]
                ent.data["facts"] = facts
                if ent.spans[0][0] != 0:
                    ent = ent.as_json()
                    ent["tags"] = [ent.pop("entity_type")]
                    ent.pop("spans")
                    ent.pop("source_text")
                    ent.pop("rules")
                    if ent not in entities:
                        entities.append(ent)
        entities.sort(key=lambda k: len(k["data"]["facts"]), reverse=True)
        return entities

    @staticmethod
    def extract_keywords(text):
        entities = []
        for sent in split_sentences(text):
            for ent in KeywordNER().extract_entities(sent):
                facts = [f[0] for f in extract_sentences(ent.value, text)
                         if f[1] > 0.3]
                ent.data["facts"] = facts
                ent = ent.as_json()
                ent["tags"] = [ent.pop("entity_type")]
                ent["data"]["keyword_score"] = ent["data"].pop("score")
                ent.pop("spans")
                ent.pop("source_text")
                ent.pop("rules")
                if ent not in entities:
                    entities.append(ent)
        entities.sort(key=lambda k: k["data"]["keyword_score"], reverse=True)
        return entities

    @staticmethod
    def extract_location(text):
        entities = []
        for ent in LocationNER().extract_entities(text):
            facts = [f[0] for f in extract_sentences(ent.value, text)
                     if f[1] > 0.3]
            ent.data["facts"] = facts
            ent = ent.as_json()
            ent["tags"] = [ent.pop("entity_type")]
            ent.pop("spans")
            ent.pop("rules")
            ent.pop("source_text")
            if ent not in entities:
                entities.append(ent)
        entities.sort(key=lambda k: len(k["data"]["facts"]), reverse=True)
        return entities

    @staticmethod
    def extract_units(text):
        entities = []
        for sent in split_sentences(text):
            for ent in UnitsNER().extract_entities(sent):
                facts = [f[0] for f in extract_sentences(ent.value, text)
                         if f[1] > 0.3]
                ent.data["facts"] = facts
                ent = ent.as_json()
                ent["tags"] = [ent.pop("entity_type")]
                ent.pop("spans")
                ent.pop("rules")
                ent.pop("source_text")
                if ent not in entities:
                    entities.append(ent)

        return entities

    @staticmethod
    def extract_dbpedia(text, strict=True):
        entities = []
        for sent in split_sentences(text):
            try:
                for ent in SpotlightNER(host=SPOTLIGHT_URL).extract_entities(sent):
                    facts = [f[0] for f in extract_sentences(ent.value, text)
                             if f[1] > 0.3]
                    ent.data["facts"] = facts
                    ent = ent.as_json()
                    ent["tags"] = ent["data"].pop("types")
                    ent["data"].pop('offset')
                    ent["data"].pop('support')
                    ent["data"].pop('percentageOfSecondRank')
                    ent["data"].pop('similarityScore')
                    ent.pop("spans")
                    ent.pop("entity_type")
                    ent.pop("rules")
                    ent.pop("source_text")
                    if ent not in entities:
                        entities.append(ent)
            except HTTPError:
                LOG.error("Spotlight api seems to be down again!")
                if strict:
                    raise SpotlightDown
                break
        return entities

    @staticmethod
    def extract(text, dbpedia=False):
        entities = {}
        for ent in LILACSextractor.extract_nouns(text):
            name = ent["value"]
            if name not in entities:
                entities[name] = ent
            ent["data"] = merge_dict(entities[name]["data"], ent["data"])
            ent["tags"] += [t for t in entities[name]["tags"] if
                            t not in ent["tags"]]
            entities[name] = ent
        for ent in LILACSextractor.extract_named_entities(text):
            name = ent["value"]
            if name not in entities:
                entities[name] = ent
            ent["data"] = merge_dict(entities[name]["data"], ent["data"])
            ent["tags"] += [t for t in entities[name]["tags"] if
                            t not in ent["tags"]]
            entities[name] = ent
        for ent in LILACSextractor.extract_location(text):
            name = ent["value"]
            if name not in entities:
                entities[name] = ent
            ent["data"] = merge_dict(entities[name]["data"], ent["data"])
            ent["tags"] += [t for t in entities[name]["tags"] if
                            t not in ent["tags"]]
            entities[name] = ent
        for ent in LILACSextractor.extract_units(text):
            name = ent["value"]
            if name not in entities:
                entities[name] = ent
            ent["data"] = merge_dict(entities[name]["data"], ent["data"])
            ent["tags"] += [t for t in entities[name]["tags"] if
                            t not in ent["tags"]]
            entities[name] = ent
        if dbpedia:
            for ent in LILACSextractor.extract_dbpedia(text, strict=False):
                name = ent["value"]
                if name not in entities:
                    entities[name] = ent
                ent["data"] = merge_dict(entities[name]["data"], ent["data"])
                ent["tags"] += [t for t in entities[name]["tags"] if
                                t not in ent["tags"]]
                entities[name] = ent
        return entities

    #### wip zone #######
    @staticmethod
    def extract_date(text):
        raise NotImplementedError

    @staticmethod
    def extract_date_range(text):
        raise NotImplementedError

    @staticmethod
    def extract_relations(text):
        raise NotImplementedError

