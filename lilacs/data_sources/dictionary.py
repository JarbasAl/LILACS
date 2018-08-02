from lilacs.nodes.concept import ConceptDatabase
from vocabulary.vocabulary import Vocabulary as vb


def extract_dictionary_connections(subject, save=False, db=None):

    cons = get_dictionary(subject) # type : [nodes]
    if save:
        db = db or ConceptDatabase(debug=False)
    concepts = []

    for con_type in cons:
        connections = cons[con_type]
        try:
            for target in connections:
                if con_type == "part of speech":
                    descript = target[1]
                    target = target[0]
                if save:
                    db.add_connection(subject, target, con_type)
                    if con_type == "part of speech":
                        c = db.get_concept_by_name(target)
                        if c:
                            c[0].description = descript
                concepts.append({con_type: target, "strength": 60})
        except:
            pass

    return concepts


def get_dictionary(subject):
    cons = {"meaning": [], "synonym": [], "antonym": [], "example": [], "part of speech": []}
    cons["meaning"] = [e.replace("<i>", "").replace("</i>", "").replace("[i]", "") .replace("[/i]", "") for e in vb.meaning(subject, format="list")]
    cons["synonym"] = vb.synonym(subject, format="list")
    cons["antonym"] = vb.antonym(subject, format="list")
    cons["part of speech"] = vb.part_of_speech(subject, format="list")
    cons["example"] = [e.replace("[", "").replace("]", "") for e in vb.usage_example(subject, format="list")]
    return cons

extract_dictionary_connections("dog")