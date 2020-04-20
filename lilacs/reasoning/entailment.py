import requests
from lilacs.settings import ALLENNLP_URL


def textual_entailment(premise, hypothesis):
    # TODO use the source: https://github.com/allenai/scitail
    return textual_entailment_allen_elmo_snli(premise, hypothesis)


def textual_entailment_allen_elmo_snli(premise, hypothesis):
    url = ALLENNLP_URL + "elmo-snli"
    data = {"premise": premise,
            "hypothesis": hypothesis}
    r = requests.post(url, json=data).json()
    probs = r["label_probs"]
    return {"entailment": probs[0], "contradiction": probs[1],
            "neutral": probs[2]}


def textual_entailment_allen_roberta_snli(premise, hypothesis):
    url = ALLENNLP_URL + "roberta-snli"
    data = {"premise": premise,
            "hypothesis": hypothesis}
    r = requests.post(url, json=data).json()
    probs = r["probs"]
    return {"entailment": probs[0], "contradiction": probs[1],
            "neutral": probs[2]}


def textual_entailment_allen_roberta_mnli(premise, hypothesis):
    url = ALLENNLP_URL + "roberta-mnli"
    data = {"premise": premise,
            "hypothesis": hypothesis}
    r = requests.post(url, json=data).json()
    probs = r["probs"]
    return {"entailment": probs[0], "contradiction": probs[1],
            "neutral": probs[2]}



if __name__ == "__main__":
    s = "The romans discovered london"
    s2 = "The romans know about london"
    s3 = "The romans have never been to london"
    s4 = "The romans like wine"
    print(textual_entailment_allen_elmo_snli(s, s2))
    """
    {'entailment': 0.9251744151115417, 
    'contradiction': 0.019063036888837814, 
    'neutral': 0.055762507021427155}
    """
    print(textual_entailment_allen_roberta_snli(s, s3))
    """
    {'entailment': 0.002643301384523511,
     'contradiction': 0.5707087516784668, 
     'neutral': 0.4266479015350342}
    """
    print(textual_entailment_allen_roberta_mnli(s, s4))
    """
    {'entailment': 0.004460913594812155, 
    'contradiction': 0.3219139873981476, 
    'neutral': 0.673625111579895}
    """