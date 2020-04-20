from nltk.corpus import wordnet as wn

try:

    def wordnet_test():
        synsets = wn.synsets("natural language processing")

except LookupError:
    import nltk

    def download_wordnet():
        nltk.download("wordnet")

    download_wordnet()


def get_definition(word, pos=wn.NOUN):
    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return synset.definition()


def get_examples(word, pos=wn.NOUN):
    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return synset.examples()


def get_lemmas(word, pos=wn.NOUN):
    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return [l.name().replace("_", " ") for l in synset.lemmas()]


def get_hypernyms(word, pos=wn.NOUN):

    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return [l.name().split(".")[0].replace("_", " ") for l in synset.hypernyms()]


def get_hyponyms(word, pos=wn.NOUN):

    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return [l.name().split(".")[0].replace("_", " ") for l in synset.hyponyms()]


def get_holonyms(word, pos=wn.NOUN):

    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return [l.name().split(".")[0].replace("_", " ") for l in synset.member_holonyms()]


def get_root_hypernyms(word, pos=wn.NOUN):

    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    return [l.name().split(".")[0].replace("_", " ") for l in synset.root_hypernyms()]


def common_hypernyms(word, word2, pos=wn.NOUN):
    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    synsets = wn.synsets(word2, pos=pos)
    if not len(synsets):
        return []
    synset2 = synsets[0]
    return [l.name().split(".")[0].replace("_", " ") for l in synset.lowest_common_hypernyms(synset2)]


def get_antonyms(word, pos=wn.NOUN):
    synsets = wn.synsets(word, pos=pos)
    if not len(synsets):
        return []
    synset = synsets[0]
    lemmas = synset.lemmas()
    if not len(lemmas):
        return []
    lemma = lemmas[0]
    antonyms = lemma.antonyms()
    return [l.name().split(".")[0].replace("_", " ") for l in antonyms]


def extract_wordnet_connections(word):
    cons = [] # type, target, strength
    for l in get_lemmas(word): # synonyms/rewordings of dog
        cons.append(("synonym", l, 70))
    for l in get_antonyms(word):#antonyms
        cons.append(("antonym", l, 70))
    for l in get_holonyms(word): # dog is part of
        cons.append(("part of", l, 55))
    for l in get_hyponyms(word): # are instances of dog
        cons.append(("sample of", l, 60))
    for l in get_hypernyms(word): # dog is instance of
        cons.append(("instance of", l, 70))
        cons.append(("label", l, 60))
    for l in get_root_hypernyms(word): # highest instance for dog
        cons.append(("instance of", l, 55))
    #for l in common_hypernyms(word): # common instances for dog and cat
    return cons