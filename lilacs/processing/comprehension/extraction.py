import requests


# use the source
# https://github.com/UKPLab/emnlp2017-relation-extraction
def relation_extraction(text):
    # DO NOT ABUSE, dev purposes only
    url = "http://semanticparsing.ukp.informatik.tu-darmstadt.de:5000/relation-extraction/parse/"
    relations = []
    try:
        data = requests.post(url, json={"inputtext": text}).json()
        data = data["relation_graph"]
        if data:
            tokens = data["tokens"]

            for edge in data["edgeSet"]:
                source = []
                target = []
                for i in edge["left"]:
                    source.append(tokens[i])
                for i in edge["right"]:
                    target.append(tokens[i])
                source = " ".join(source)
                target = " ".join(target)
                relation = edge["lexicalInput"]
                relations.append((source, relation, target))
    except:
        pass
    return relations

#from pprint import pprint
#t = "Star Wars VII is an American space opera epic film directed by  J. J. Abrams."
#pprint(relation_extraction(t))
# [('J. J. Abrams', 'notable work', 'Star Wars VII'),
#  ('J. J. Abrams', 'genre', 'space opera epic film'),
#  ('Star Wars VII', 'genre', 'space opera epic film')]



