from lilacs.processing.nlp.segmentation import extract_formatted_sentences, extract_sentences
from lilacs.processing.comprehension import replace_coreferences
from pprint import pprint

MIDSENTENCE_MARKERS = ["and", ",", ";", "."]


def extract_candidates(sentence):
    sentence = replace_coreferences(sentence)
    sentences = extract_sentences(sentence)
    candidates = []
    for sentence in sentences:
        candidates.append("")
        for tok in sentence:
            if tok.value not in MIDSENTENCE_MARKERS:
                candidates[-1] += tok.value + " "
                continue
            candidates.append("")
    return [c.strip() for c in candidates if c.strip()]


def extract_orders(sentence):
    sentences = extract_formatted_sentences(sentence)
    return sentences


if __name__ == "__main__":
    # sentence segmentation
    sentence = "Tell me a joke. Turn on the light"
    orders = extract_candidates(sentence)
    pprint(orders)

    # split on comma
    sentence = "Tell me a joke, Turn on the light"
    orders = extract_candidates(sentence)
    pprint(orders)

    # split on "and"
    sentence = "Tell me a joke and turn on the light"
    orders = extract_candidates(sentence)
    pprint(orders)

    # coreference resolution on extracted pieces
    sentence = "Turn on the light and change it to blue"
    orders = extract_candidates(sentence)
    pprint(orders)
