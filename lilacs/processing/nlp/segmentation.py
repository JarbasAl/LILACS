from syntok.tokenizer import Tokenizer
import syntok.segmenter as segmenter




def tokenize(document):
    tok = Tokenizer()
    return tok.tokenize(document)


def extract_paragraphs(document):
    return [paragraph for paragraph in segmenter.process(document)]


def extract_sentences(document):
    sentences = []
    for paragraph in segmenter.process(document):
        for sentence in paragraph:
            sentences.append(sentence)
    return sentences


def extract_formatted_sentences(document):
    sentences = []
    for paragraph in segmenter.process(document):
        for sentence in paragraph:
            sentences.append(" ".join([token.value for token in sentence]))
    return sentences

if __name__ == "__main__":
    document = """London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia.  It was founded by the Romans, who named it Londinium."""

    print(extract_sentences(document))
