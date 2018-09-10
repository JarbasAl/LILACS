import requests


def ask_wdaqua(text):
    url = "https://wdaqua-core1.univ-st-etienne.fr/gerbil"
    data = {"query": text}
    r = requests.post(url, data=data)
    data = r.json()
    # TODO send sparql query


# https://github.com/allenai/ARC-Solvers
def IKE():
    # https://github.com/allenai/ikev
    pass


# DO NOT ABUSE
def ask_euclid(text):
    url = "http://euclid.allenai.org/api/solve?query=" + text
    return requests.get(url).text


# DO NOT ABUSE
# use the source https://github.com/allenai/aristo-mini
def ask_aristo(text, raw=False):
    url = "http://aristo-demo.allenai.org/api/ask?text=" + text
    data = requests.get(url).json()
    if raw:
        return data
    answers = data["response"]["success"]["answers"]

    response = {}
    for a in answers:
        # 'confidence', 'analyses', 'selection', 'selected'
        if a["selected"]:
            response["answer"] = a["selection"]["directAnswer"]["answer"]
            response["confidence"] = a["confidence"]
            data = a["analyses"][0]["analysis"]["analyses"][0]
            response["expectedAnswerType"] = data['expectedAnswerType']
            response['questionSentence'] = data['questionSentence']
            response['questionType'] = data['questionType']
            response['questionTheme'] = data['questionTheme']
            response['questionSetup'] = data['questionSetup']
            response["dataSource"] = data["sourceFriendlyName"]
            response["top20"] = data['top20ThisCluster']
    return response


def EYE_rest(data, rules="", query="{ ?a ?b ?c. } => { ?a ?b ?c. }.", server_url="http://eye.restdesc.org/"):
    if rules:
        data = data + "\n" + rules
    r = requests.post(server_url, json={"data": data, "query": query}).text
    return r


from lilacs.memory.data_sources import LILACSKnowledge


class LILACSReasoner(object):
    def __init__(self, bus=None):
        self.bus = bus
        self.knowledge = LILACSKnowledge(self.bus)

    def what(self, node):
        pass

    def EYE(self, data, rules="", query="{ ?a ?b ?c. } => { ?a ?b ?c. }."):
        return EYE_rest(data, rules, query)

    def aristo(self, query):
        return ask_aristo(query)

    def euclid(self, query):
        return ask_euclid(query)


if __name__ == "__main__":

    LILACS = LILACSReasoner()
    t = "If 30 percent of 48 percent of a number is 288, what is the number?"
    print(LILACS.euclid(t))


    t = """Which tool should a student use to compare the masses of two small rocks?
    (A) balance
    (B) hand lens
    (C) ruler
    (D) measuring cup
    """
    print(LILACS.aristo(t))

    data = """@prefix ppl: <http://example.org/people#>.
    @prefix foaf: <http://xmlns.com/foaf/0.1/>.

    ppl:Cindy foaf:knows ppl:John.
    ppl:Cindy foaf:knows ppl:Eliza.
    ppl:Cindy foaf:knows ppl:Kate.
    ppl:Eliza foaf:knows ppl:John.
    ppl:Peter foaf:knows ppl:John."""

    rules = """@prefix foaf: <http://xmlns.com/foaf/0.1/>.

    {
        ?personA foaf:knows ?personB.
    }
    =>
    {
        ?personB foaf:knows ?personA.
    }."""

    print(LILACS.EYE(data, rules))
