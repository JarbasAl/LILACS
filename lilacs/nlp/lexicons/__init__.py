from os.path import dirname, join


def load_lexicon():
    bucket = {}

    lexicon_path = join(dirname(__file__), "word_emotion_lexicon.csv")
    with open(lexicon_path, "r") as f:
        lines = f.readlines()
        for l in lines[1:]:
            l = l.replace("\n", "")
            word, emotion, color, orientation, sentiment, subjectivity, source = l.split(",")
            bucket[word] = {"emotion": emotion,
                            "color": color,
                            "orientation": orientation,
                            "sentiment": sentiment,
                            "subjectivity": subjectivity,
                            "source": source}
    return bucket


LEXICON = load_lexicon()


if __name__ == "__main__":
    from pprint import pprint

    pprint(LEXICON)