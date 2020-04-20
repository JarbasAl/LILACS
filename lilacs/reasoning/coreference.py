import requests
from lilacs.settings import ALLENNLP_URL
from lilacs import nlp
from lilacs.reasoning import LILACSWordAnalyzer


def allen_coreference(text):
    url = ALLENNLP_URL + "coreference-resolution"
    data = {"document": text}
    r = requests.post(url, json=data).json()
    tokens = r["document"]
    for cluster in r['clusters']:
        span = cluster[0]
        w = " ".join(tokens[span[0]:span[1] + 1]).strip()
        for span in cluster[1:]:
            tokens[span[0]] = w
            if span[0] > span[1]:
                tokens[span[0]: span[1] + 1] = ""

    # restore punctuation
    for idx, tok in enumerate(tokens):
        if idx == 0:
            continue
        if tok in [".", ",", ";", ":", "!", "?"]:
            tokens[idx-1] = tokens[idx-1] + tok
            tokens[idx] = ""
    text = " ".join([t for t in tokens if t])
    return text


def replace_coreferences(text):
    # TODO neuralcoref
    #doc = nlp(text)
    #     # TODO
    #     # https://github.com/huggingface/neuralcoref/issues/102
    #     # https://github.com/explosion/spaCy/issues/2852
    #return doc._.coref_resolve

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
    return allen_coreference(text)


class CoreferSolver:
    CATEGORY = {
        'male': ['he', 'him', 'himself', 'his'],
        'female': ['she', 'her', 'herself', 'hers'],
        'first': ['i', 'me', 'my', 'mine', 'myself', 'we', 'us', 'our', 'ours',
                  'ourselves'],
        'neutral': ['it', 'itself', 'its'],
        'plural': ['they', 'them', 'themselves', 'their', 'theirs']
    }
    PRONOUN_TAG = ['PRP', 'PRP$', 'WP', 'WP$']
    NOUN_TAG = ['NN', 'NNP']
    PLURAL_NOUN_TAG = ['NNS', 'NNPS']
    SUBJ_TAG = ["nsubj", "dobj"]

    @staticmethod
    def _preprocess(doc):
        feature_dict = {}
        ents_dict = {}
        pronoun_dict = {}

        # --sentence-wise noun chunk features--
        counter = 0
        for s in doc.sents:

            # get noun chunks in each sentence
            chunk = list(s.noun_chunks)
            noun_feature = []

            # collect features for noun chunk
            for c in chunk:
                rt = c.root

                # find level of noun phrase root in tree
                level = 1
                predecessor = rt.head
                while predecessor.dep_ != "ROOT":
                    predecessor = predecessor.head
                    level += 1

                noun_feature.append((rt.text, rt.dep_, rt.tag_, level))

            feature_dict[counter] = noun_feature
            counter += 1

        # --gender of named entities--
        counter = 0
        for s in doc.sents:
            person_ents = []

            for e in s:
                if e.ent_type_ == "PERSON" and e.ent_iob_ == 'B':

                    # gender of first name only
                    gender = LILACSWordAnalyzer.predict_gender(str(e.text))

                    # find last name if present
                    rt = e.head
                    if rt.ent_type_ == "":
                        rt = e

                    person_ents.append((rt, gender))

            ents_dict[counter] = person_ents
            counter += 1

        # --assign category of pronouns--
        counter = 0
        for s in doc.sents:
            pronouns_present = []

            for w in s:

                # find level of pronoun in tree
                if w.tag_ in CoreferSolver.PRONOUN_TAG:
                    level = 1
                    predecessor = w.head

                    while predecessor.dep_ != "ROOT":
                        predecessor = predecessor.head
                        level += 1

                    for k, v in CoreferSolver.CATEGORY.items():
                        if w.text.lower() in v:
                            pronouns_present.append((w, k, level))

            pronoun_dict[counter] = pronouns_present
            counter += 1
        return ents_dict, pronoun_dict, feature_dict

    @staticmethod
    def _resolution(doc, ents_dict, pronoun_dict, feature_dict):

        mappings = []

        # check multiple nouns with same gender in a sentence
        # eg. Rohit Gupta telephoned Abhishek to tell him that he lost the laptop.
        def multiple_same_gender(cat, idx):
            if len(ents_dict[idx]) > 1:
                same = [item for item in ents_dict[idx] if item[1] == cat]
                if len(same) > 1:
                    return True

        # match gender of noun and pronoun
        # eg. I voted for Nader because he is clear about his values.
        def match_gender(_ents):
            noun = ''
            for (n, g) in _ents:
                if g == category:
                    for child in n.children:
                        if child.dep_ == "compound":
                            noun += child.text + ' '
                    noun += n.text
                    return False, noun
                else:
                    return True, noun

        # match same grammar relations
        # eg. Rohit Gupta telephoned Abhishek to tell him that he lost the laptop.
        def match_grammar(_ents):
            noun = ''
            for (n, g) in _ents:
                if n.dep_ == rel:
                    for child in n.children:
                        if child.dep_ == "compound":
                            noun += child.text + ' '
                    noun += n.text
                    mappings.append((pronoun, noun))

        def match_by_subject_level(subject):
            for sub in subject:
                for (noun, _, _, lev) in features:
                    if sub.text == noun and level > lev:
                        mappings.append((pronoun, noun))
                        break

        def third_person_pronouns(TAG):
            subject = [w for w in s if w.dep_ == "nsubj" and w.tag_ in TAG]

            # multiple possible mentions in same sentence
            if len(subject) > 1:
                match_by_subject_level(subject)

            # mention in same sentence
            elif len(subject) == 1 and subject[0] != pronoun:
                noun = subject[0].text
                mappings.append((pronoun, noun))

            # mention in previous sentence
            else:
                prev_sent = sents[counter - 1]
                prev_nouns = [w for w in prev_sent if
                              w.tag_ in TAG and w.dep_ in
                              CoreferSolver.SUBJ_TAG]
                if len(prev_nouns) > 1:
                    match_by_subject_level(prev_nouns)
                else:
                    noun = prev_nouns[0].text
                    mappings.append((pronoun, noun))

        # --begin resolution--
        counter = 0
        sents = [s for s in doc.sents]
        for s in sents:

            for i in range(0, len(pronoun_dict[counter])):
                (pronoun, category, level) = pronoun_dict[counter][i]
                rel = pronoun.dep_

                ents = ents_dict[counter]  # entities in current sentence
                features = feature_dict[
                    counter]  # features in current sentence

                # resolve first person pronouns
                if category == 'first':
                    mappings.append((pronoun, "<Author>"))

                # resolve gender pronouns
                elif category == LILACSWordAnalyzer.MALE or \
                        category == LILACSWordAnalyzer.FEMALE:

                    subject = pronoun
                    for w in s:
                        if w.tag_ in CoreferSolver.NOUN_TAG and w.dep_ == \
                                "nsubj":
                            subject = w
                            break

                    # pronouns with mention in same sentence
                    if ents and (pronoun.idx > ents[0][0].idx):

                        # match gender of noun and pronoun
                        if not multiple_same_gender(category, counter):
                            flag, noun = match_gender(ents)
                            if not flag:
                                mappings.append((pronoun, noun))

                        # match same grammar relations
                        else:
                            match_grammar(ents)

                    # gender pronouns where mention is not named-entity
                    elif pronoun.idx > subject.idx:
                        noun = subject.text
                        mappings.append((pronoun, noun))

                    # pronouns with mention in past sentence
                    else:
                        # go to closest past sentence with a noun mention
                        # eg. He is better than Rajeev.
                        prev_counter = counter - 1
                        prev_ents = ents_dict[prev_counter]
                        while not prev_ents and prev_counter != 0:
                            prev_counter -= 1
                            prev_ents = ents_dict[prev_counter]

                        # match gender of noun and pronoun
                        if not multiple_same_gender(category, counter):
                            is_not_match, noun = match_gender(prev_ents)
                            while is_not_match and prev_counter != 0:
                                prev_counter -= 1
                                prev_ents = ents_dict[prev_counter]
                                if prev_ents:
                                    is_not_match, noun = match_gender(
                                        prev_ents)
                            mappings.append((pronoun, noun))

                # resolve neutral pronouns
                elif category == 'neutral':
                    third_person_pronouns(CoreferSolver.NOUN_TAG)

                # resolve plural pronouns
                else:
                    third_person_pronouns(CoreferSolver.PLURAL_NOUN_TAG)

            counter += 1

        # --end resolution--
        return mappings

    @staticmethod
    def _build_output(doc, mappings):
        c = 0
        end = 0
        new_doc = ""

        for token in doc:
            if token == mappings[c][0]:
                new_doc += "<" + mappings[c][1] + "> "
                c += 1
                if c >= len(mappings):
                    end = token.i + 1
                    break
            else:
                new_doc += token.text + " "
        new_doc += doc[end:].text

        return new_doc

    @staticmethod
    def replace_coreferences(text):
        doc = nlp(text)
        ents_dict, pronoun_dict, feature_dict = CoreferSolver._preprocess(doc)
        mappings = CoreferSolver._resolution(doc, ents_dict,
                                             pronoun_dict, feature_dict)
        return CoreferSolver._build_output(doc, mappings)


if __name__ == "__main__":
    s = "My sister has a dog. She loves him."
    print(replace_coreferences(s))

    s = """London is the capital and most populous city of England and  the United Kingdom.
    Standing on the River Thames in the south east of the island of Great Britain,
    London has been a major settlement  for two millennia.  It was founded by the Romans,who named it Londinium.
    """
    print(replace_coreferences(s))