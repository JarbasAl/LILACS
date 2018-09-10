import requests


def polyglot_NER_demo(text):
    # DO NOT ABUSE THIS, dev purposes only
    data = {"text": text.replace(" ", "+"),
            "langs": "en",
            "tokenization": "tokenization",
            "min_O": 0.00
            }
    url = "https://entityextractor.appspot.com/ner"
    r = requests.post(url, data=data)

    t = r.text.replace("<br>", "")
    NER = []
    # parse colors
    candidates = [c for c in t.split("</font>") if not c.startswith('<font color="black">')]
    for c in candidates:
        if not c:
            continue
        color, name = c.split(">")
        color = color.replace('<font color="', "").replace('"', "")
        name = name.strip()
        if color == "red":
            NER.append((name, "person"))
        elif color == "green":
            NER.append((name, "organization"))
        elif color == "blue":
            NER.append((name, "location"))
    return NER


def polyglot_NER(blob):
    from polyglot.text import Text

    text = Text(blob)
    ENTS = []
    for sent in text.sentences:
        for entity in sent.entities:
            ENTS.append((entity[0], entity.tag))
            print(entity.tag, entity)

    return ENTS


def spacy_NER(text, nlp):
    from lilacs.sentience.emotions.emotions import EMOTION_NAMES
    from lilacs.processing.nlp.parse import normalize

    ents = []
    text = normalize(text, nlp=nlp)
    doc = nlp(text)
    for entity in doc.ents:
        ents.append((entity.text, entity.label_))

    # recognize emotions
    words = text.lower().split(" ")
    for emotion in EMOTION_NAMES:
        if emotion in words:
            ents.append((emotion, "emotion"))
    return ents


def spacy_NER_demo(text):
    ents = []
    try:
        data = {"model": "en_core_web_lg", "text": text}
        r = requests.post("https://api.explosion.ai/displacy/ent", data)
        r = r.json()
        for e in r:
            txt = text[e["start"]:e["end"]]
            ents.append((txt, e["label"].lower()))
    except Exception as e:
        print(e)
    return ents


def FOX_NER(text):
    # use the source https://github.com/dice-group/fox
    # http://fox-demo.aksw.org/#!/home
    from foxpy.fox import Fox
    from foxpy.utils import extractNifPhrases
    f = Fox()
    json_ld = f.recognizeText(text)
    nif_phrases = extractNifPhrases(json_ld)
    if len(nif_phrases) < 1:
        return text

    nif_phrases = sorted(nif_phrases, key=lambda t: t["endIndex"], reverse=True)
    ents = []
    for n in nif_phrases:
        name = n["anchorOf"]
        tag = n["taClassRef"][1].split(":")[1].lower()
        ents.append((name, tag))
    return ents


def allennlp_NER_demo(text):
    try:
        url = "http://demo.allennlp.org/predict/named-entity-recognition"
        data = {"sentence": text}
        r = requests.post(url, json=data).json()
        words = r["words"]
        tags = r["tags"]
        ents = []
        for idx, tag in enumerate(tags):
            if tag != "O":
                ents.append((words[idx], tag))
        return ents
    except Exception as e:
        print(e)
    return text

