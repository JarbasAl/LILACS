
import requests


def extract_facts(subject, text, nlp=None, coref_nlp=None, norm=True):
    from lilacs.processing.nlp import get_nlp
    from lilacs.processing.nlp.parse import normalize
    import textacy.extract
    facts = []
    nlp = nlp or get_nlp()
    # Parse the document with spaCy
    if norm:
        text = normalize(text, remove_articles=False, coref_nlp=coref_nlp)
    doc = nlp(text)
    # Extract semi-structured statements
    statements = textacy.extract.semistructured_statements(doc, subject)
    for statement in statements:
        subject, verb, fact = statement
        facts.append(fact)
    return facts


def replace_coreferences(text, nlp=None):
    # "My sister has a dog. She loves him." -> "My sister has a dog. My sister loves a dog."

    # """
    # London is the capital and most populous city of England and  the United Kingdom.
    # Standing on the River Thames in the south east of the island of Great Britain,
    # London has been a major settlement  for two millennia.  It was founded by the Romans,
    # who named it Londinium.
    # """ -> """
    # London is the capital and most populous city of England and  the United Kingdom.
    # Standing on the River Thames in the south east of the island of Great Britain,
    # London has been a major settlement  for two millennia.  London was founded by the Romans,
    # who named London Londinium.
    # """
    if nlp:
        doc = nlp(text)
        text = doc._.coref_resolved
    else:
        try:
            params = {"text": text}
            text = requests.get("https://coref.huggingface.co/coref", params=params).json()["corefResText"]
        except Exception as e:
            print(e)
    return text


def neuralcoref_demo(text):
    try:
        params = {"text": text}
        text = requests.get("https://coref.huggingface.co/coref", params=params).json()["corefResText"]
    except Exception as e:
        print(e)
    return text


def textual_entailment_demo(premise, hypothesis):
    # use the source: https://github.com/allenai/scitail
    """
    Textual Entailment (TE) takes a pair of sentences and predicts whether the facts in the first necessarily imply the facts in the second one.
    The AllenNLP toolkit provides the following TE visualization, which can be run for any TE model you develop.
    This page demonstrates a reimplementation of the decomposable attention model (Parikh et al, 2017) ,
    which was state of the art for the SNLI benchmark (short sentences about visual scenes) in 2016.
    Rather than pre-trained Glove vectors, this model uses ELMo embeddings,
    which are completely character based and improve performance by 2%

    :param premise:
    :param hypotheses:
    :return:
    """
    url = "http://demo.allennlp.org/predict/textual-entailment"
    data = {"premise": premise,
            "hypothesis": hypothesis}
    r = requests.post(url, json=data).json()
    probs = r["label_probs"]
    return {"entailment": probs[0], "contradiction": probs[1], "neutral": probs[2]}

p = "If you help the needy, God will reward you."
h = "Giving money to the poor has good consequences."
#print(textual_entailment_demo(p, h))
# {'contradiction': 0.04034089669585228, 'neutral': 0.1409262865781784, 'entailment': 0.8187329173088074}


def comprehension_demo(question, passage):
    # DO NOT ABUSE, dev purposes only
    # curl 'http://demo.allennlp.org/predict/machine-comprehension' -H 'Origin: http://demo.allennlp.org' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.9' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Referer: http://demo.allennlp.org/machine-comprehension/MzIzOTM2' -H 'Connection: keep-alive' -H 'DNT: 1' --data-binary '{"passage":"Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. These technologies are used to develop machines that can substitute for humans. Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive. Robots can take on any form but some are made to resemble humans in appearance. This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people. Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do.","question":"What do robots that resemble humans attempt to do?"}' --compressed
    """
    Machine Comprehension (MC) answers natural language questions by selecting an answer span within an evidence text.
    The AllenNLP toolkit provides the following MC visualization, which can be used for any MC model in AllenNLP.
    This page demonstrates a reimplementation of BiDAF (Seo et al, 2017), or Bi-Directional Attention Flow,
    a widely used MC baseline that achieved state-of-the-art accuracies on the SQuAD dataset (Wikipedia sentences) in early 2017.

    :param question:
    :param passage:
    :return:
    """
    url = "http://demo.allennlp.org/predict/machine-comprehension"
    data = {"passage": passage, "question": question}
    r = requests.post(url, json=data).json()
    return r["best_span_str"]


p = "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. These technologies are used to develop machines that can substitute for humans. Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive. Robots can take on any form but some are made to resemble humans in appearance. This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people. Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do."
q = "What do robots that resemble humans attempt to do?"
#print(comprehension_demo(q, p))
# replicate walking, lifting, speech, cognition

from pprint import pprint
def semantic_role_labeling_demo(sentence):
    # DO NOT ABUSE, dev purposes only
    """
    Semantic Role Labeling (SRL) recovers the latent predicate argument structure of a sentence,
    providing representations that answer basic questions about sentence meaning,
    including “who” did “what” to “whom,” etc.
    The AllenNLP toolkit provides the following SRL visualization, which can be used for any SRL model in AllenNLP.
    This page demonstrates a reimplementation of a deep BiLSTM model (He et al, 2017),
    which is currently state of the art for PropBank SRL (Newswire sentences).
    :param sentence:
    :return:
    """
    url = "http://demo.allennlp.org/predict/semantic-role-labeling"
    data = {"sentence": sentence}
    r = requests.post(url, json=data).json()
    roles = {}
    words = r["words"]
    verbs = r["verbs"]
    pprint(r)
    for v in verbs:
        arg0 = []
        arg1 = []
        verb = v["verb"]
        tags = v["tags"]
        for idx, t in enumerate(tags):
            if "I-ARGM" in t:
                arg0.append(words[idx])
            elif "I-ARG1" in t:
                arg1.append(words[idx])
        if not len(arg0):
            continue
        arg0 = " ".join(arg0)
        arg1 = " ".join(arg1)
        roles[verb] = [arg0, arg1]
    return roles

t = "The keys, which were needed to access the building, were locked in the car."

pprint(semantic_role_labeling_demo(t))
 #{'decided': ['voters', 'that if the stadium was such a good idea someone would build it himself'], 'build': ['someone', 'it'], 'rejected': ['voters', 'it']}


def constituency_parse_demo(sentence):
    # DO NOT ABUSE, dev purposes only
    """
    A constituency parse tree breaks a text into sub-phrases, or constituents. Non-terminals in the tree are types of phrases, the terminals are the words in the sentence. This demo is an implementation of a minimal neural model for constituency parsing based on an independent scoring of labels and spans described in Extending a Parser to Distant Domains Using a Few Dozen Partially Annotated Examples (Joshi et al, 2018). This model uses ELMo embeddings, which are completely character based and improves single model performance from 92.6 F1 to 94.11 F1 on the Penn Treebank, a 20% relative error reduction.
    :param sentence:
    :return:
    """
    url = "http://demo.allennlp.org/predict/constituency-parsing"
    data = {"sentence": sentence}
    r = requests.post(url, json=data).json()
    r.pop('class_probabilities')
    r.pop('spans')
    r.pop("slug")
    r.pop("num_spans")
    return r

t = "James went to the corner shop to buy some eggs, milk and bread for breakfast."

#from pprint import pprint
#pprint(constituency_parse_demo(t))

# TODO parse response
def allennlp_coref_demo(text):
    try:
        url = "http://demo.allennlp.org/predict/coreference-resolution"
        data = {"document": text}
        r = requests.post(url, json=data).json()
        print(r.text)
    except Exception as e:
        print(e)
    return text