import wptools
from lilacs.nodes.concept import ConceptDatabase

__author__ = 'jarbas'


def extract_wikidata_connections(subject, save=False, db=None):
    cons = get_wikidata(subject) # type : [nodes] || node
    if save:
        db = db or ConceptDatabase(debug=False)

    connections = []  # concept : [{type : con, strength: score}]
    skips = ["heart rate", "image", "topic's main category", "earliest date", "Commons gallery", "signature",
             "described by source", "on focus list of Wikimedia project", "Commons category", "topic's main template"]
    for con_type in cons:
        if con_type.endswith(")"):
            con_type = " ".join(con_type.split(" ")[:-1])
        targets = cons[con_type]
        if con_type in skips:
            continue
        if con_type == "use":
            con_type = "used for"
        elif con_type == "subclass of":
            con_type = "instance of"
        if isinstance(targets, list):
            for target in targets:
                if not target:
                    continue
                if "," in target:
                    t = target.split(",")
                    for target in t:
                        connections.append((con_type, target, 46))
                        if save:
                            db.add_connection(subject, target, con_type)
                else:
                    connections.append((con_type, target, 46))
                    if save:
                        db.add_connection(subject, target, con_type)
        elif targets:
            if "," in targets:
                t = targets.split(",")
                for target in t:
                    connections.append((con_type, target, 46))
                    if save:
                        db.add_connection(subject, target, con_type)
            else:
                connections.append((con_type, targets, 46))
                if save:
                    db.add_connection(subject, targets, con_type)
    return connections


def get_wikidata(subject):
    node_data = {}
    base = wptools.page(subject).get_parse().data["wikibase"]
    page = wptools.page(wikibase=base).get_wikidata().data

    # clean data (remove (PXXX) )
    data = page["wikidata"]

    def clean_dict(data=None):
        data = data or {}
        clean = {}
        for key in dict(data):
            if not key:
                continue
            val = data[key]
            if isinstance(val, list):
                for idx, v in enumerate(val):
                    if isinstance(v, str):
                        v = " ".join(v.split(" ")[:-1])
                        val[idx] = v
                    if isinstance(v, dict):
                        v = clean_dict(dict(v))
                        val[idx] = v
                    if isinstance(v, list):
                        for idx, v1 in enumerate(v):
                            v[idx] = " ".join(v1.split(" ")[:-1])
                        val[idx] = v
            elif isinstance(val, dict):
                val = clean_dict(dict(val))
            elif val.endswith(")"):
                val = " ".join(val.split(" ")[:-1])
            key = " ".join(key.split(" ")[:-1])
            if val and key:
                clean[key] = val
        return clean

    data = clean_dict(data)

    # parse for distant child of
    node_data["description"] = page["description"]
    # direct child of
    #node_data["instance of"] = page["what"]
    # data fields
    for k in data:
        node_data[k] = data[k]
    # related to
    node_data["url"] = page["wikidata_url"]
    #node_data["aliases"] = page["aliases"]
    return node_data

