from __future__ import print_function
import wptools
from lilacs.nodes.concept import ConceptDatabase
from lilacs.nlp.parse import extract_facts

__author__ = 'jarbas'


def extract_wikipedia_connections(subject, save=False, db=None, nlp=None):
    data = get_wikipedia(subject)
    subject = data["name"]
    if save:
        db = db or ConceptDatabase(debug=False)

    connections = [] # concept : [{type : con, strength: score}]
    if save:
        db.add_concept(subject)
        c = db.get_concept_by_name(subject)[0]
        c.description = data["description"]

    for link in data["link"]:
        connections.append({"link": link, "con_strength": 80})
        if save:
            db.add_connection(subject, link, "link")

    facts = extract_facts(subject, data["summary"], nlp=nlp)
    for f in facts:
        connections.append({"fact": f, "con_strength": 90})
        if save:
            db.add_connection(subject, f, "fact")

    return connections


def get_wikipedia(subject):
    node_data = {}
    try:
        page = wptools.page(subject, silent=True, verbose=False).get_query().data
        #node_data["image"] = page["image"]["url"]
        node_data["name"] = page["label"]

        node_data["link"] = [page["url"]]
        #node_data["link"] += page["links"]
        node_data["description"] = page["description"]
        node_data["summary"] = page["extext"]
    except LookupError:
        print("could not find wikipedia data for ", subject)
    return node_data
