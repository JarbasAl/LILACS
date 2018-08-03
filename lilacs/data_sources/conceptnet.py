import requests


def extract_conceptnet_connections(subject):
    connections = get_conceptnet(subject)  # type : [nodes]
    new_cons = []
    for con_type in connections:
        cons = connections[con_type]
        for target in cons:
            new_cons.append((con_type, target, 50))

    return new_cons


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
    pof = []
    created = []
    defs = []
    syns = []
    nops = []

    obj = requests.get('http://api.conceptnet.io/c/en/' + subject).json()
    for edge in obj["edges"]:
        r, s, t = edge["@id"].split(",")
        if not s.startswith("/c/en/") or not t.startswith("/c/en/"):
            # ignore non english
            continue
        rel = edge["rel"]["label"]
        node = edge["end"]["label"]
        start = edge["start"]["label"]
        if start != node and start not in other:
            other.append(start)
        if rel == "IsA":
            node = node.replace(" a ", "").replace(" an ", "")
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
        elif rel == "PartOf":
            if node not in pof:
                pof.append(node)
        elif rel == "CreatedBy":
            if node not in created:
                created.append(node)
        elif rel == "DefinedAs":
            if node not in defs:
                defs.append(node)
        elif rel == "Synonym":
            if node not in syns:
                syns.append(node)
        elif rel == "NotHasProperty":
            if node not in nops:
                nops.append(node)
        usage = edge["surfaceText"]
        if usage is not None:
            examples.append(usage)

    return {"related": related,
            "instance of": parents,
            "capable of": capable,
            "used for": used,
            "desires": desires,
            "found at": location,
            "part of": pof,
            "created by": created,
            "label": defs,
            "synonym": syns,
            "incompatible": nops}

