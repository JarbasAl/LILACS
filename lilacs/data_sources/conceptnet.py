import requests
from lilacs.nodes.concept import ConceptDatabase


def extract_conceptnet_connections(subject, save=False, db=None):
    cons = get_conceptnet(subject) # type : [nodes]
    if save:
        db = db or ConceptDatabase(debug=False)

    connections = []

    for a in cons:
        b = cons[a]
        for c in b:
            if save:
                db.add_connection(subject, c , a)
            connections.append({a: c, "con_strength": 50})

    return connections


def get_conceptnet(subject):
    # get knowledge about
    parents = []
    capable = []
    has = []
    desires = []
    used = []
    related = []
    examples = []
    location = []
    other = []

    obj = requests.get('http://api.conceptnet.io/c/en/' + subject).json()
    for edge in obj["edges"]:
        rel = edge["rel"]["label"]
        node = edge["end"]["label"]
        start = edge["start"]["label"]
        if start != node and start not in other:
            other.append(start)
        if rel == "IsA":
            node = node.replace("a ", "").replace("an ", "")
            if node not in parents:
                parents.append(node)
        elif rel == "CapableOf":
            if node not in capable:
                capable.append(node)
        elif rel == "HasA":
            if node not in has:
                has.append(node)
        elif rel == "Desires":
            if node not in desires:
                desires.append(node)
        elif rel == "UsedFor":
            if node not in used:
                used.append(node)
        elif rel == "RelatedTo":
            if node not in related:
                related.append(node)
        elif rel == "AtLocation":
            if node not in location:
                location.append(node)
        usage = edge["surfaceText"]
        if usage is not None:
            examples.append(usage)

    return {"related": other,
            "instance of": parents,
            "capable of": capable,
            "used for": used}


