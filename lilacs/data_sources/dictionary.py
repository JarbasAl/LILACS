from vocabulary.vocabulary import Vocabulary as vb


def extract_dictionary_connections(subject):

    cons = get_dictionary(subject) # type : [nodes]
    concepts = []
    for con_type in cons:
        connections = cons[con_type]
        try:
            for target in connections:
                if con_type == "part of speech":
                    continue
                concepts.append((con_type, target, 60))
        except:
            pass

    return concepts


def get_dictionary(subject):
    cons = {"meaning": [], "synonym": [], "antonym": [], "example": [], "part of speech": []}
    meanings = vb.meaning(subject, format="list")
    if meanings:
        cons["meaning"] = [e.replace("<i>", "").replace("</i>", "").replace("[i]", "") .replace("[/i]", "") for e in meanings]
    synonyms = vb.synonym(subject, format="list")
    if synonyms:
        cons["synonym"] = synonyms
    antonyms = vb.antonym(subject, format="list")
    if antonyms:
        cons["antonym"] = antonyms
    ps = vb.part_of_speech(subject, format="list")
    if ps:
        cons["part of speech"] = ps
    examples = vb.usage_example(subject, format="list")
    if examples:
        cons["example"] = [e.replace("[", "").replace("]", "") for e in examples]
    return cons

