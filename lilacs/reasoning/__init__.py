from lilacs.reasoning.reading import machine_comprehension
from lilacs.reasoning.entailment import textual_entailment
from lilacs import nlp
from lilacs.parse import SentenceParser
from lilacs.spacy_extensions.lexicons import LEXICON
from jarbas_utils.parse import split_sentences
import numpy as np
import padaos
import math
import heapq


class LILACSWordAnalyzer(SentenceParser):
    # Lexicons Used
    # NRC Emotion Lexicon - http://www.saifmohammad.com/WebPages/lexicons.html
    # Bing Liu's Opinion Lexicon - http://www.cs.uic.edu/~liub/FBS/sentiment-analysis.html#lexicon
    # MPQA Subjectivity Lexicon - http://mpqa.cs.pitt.edu/lexicons/subj_lexicon/
    # Harvard General Inquirer - http://www.wjh.harvard.edu/~inquirer/spreadsheet_guide.htm
    # NRC Word-Colour Association Lexicon - http://www.saifmohammad.com/WebPages/lexicons.html

    @staticmethod
    def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
        """https://en.wikipedia.org/wiki/Cosine_similarity"""
        num = np.dot(v1, v2)
        d1 = np.dot(v1, v1)
        d2 = np.dot(v2, v2)

        if d1 > 0.0 and d2 > 0.0:
            return num / math.sqrt(d1 * d2)
        else:
            return 0.0

    # word2vec
    @staticmethod
    def get_word_vector(text):
        doc = nlp(text)
        return doc.vector

    @staticmethod
    def w2v_similarity_match(text1, text2):
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        return doc1.similarity(doc2)

    @staticmethod
    def get_sense_vector(text):
        doc = nlp(text)
        return doc._.s2v_vec

    @staticmethod
    def s2v_similarity_match(text1, text2):
        # inject pos_tag info, avoid 0 score
        if len(text1.split()) == 1:
            # king -> the king -> noun
            text1 = "the " + text1
        if len(text2.split()) == 1:
            text2 = "the " + text2
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        return doc1._.s2v_similarity_match(doc2)

    @staticmethod
    def related_concepts(text, n=3):
        doc = nlp(text)
        return doc._.s2v_related_concepts(n)

    @staticmethod
    def get_color(word):
        # http://www.saifmohammad.com/WebDocs/ACL2011-word-colour-associations-poster.pdf
        if word in LEXICON:
            return LEXICON[word]["color"]
        return None

    @staticmethod
    def get_emotion(word):
        if word in LEXICON:
            return LEXICON[word]["emotion"]
        return None

    @staticmethod
    def get_sentiment(word):
        if word in LEXICON:
            return LEXICON[word]["sentiment"]
        return None

    @staticmethod
    def get_subjectivity(word):
        if word in LEXICON:
            return LEXICON[word]["subjectivity"]
        return None

    @staticmethod
    def get_orientation(word):
        if word in LEXICON:
            return LEXICON[word]["orientation"]
        return None


class LILACSTextAnalyzer(LILACSWordAnalyzer):
    @staticmethod
    def enrich_sentence(text, domains=None):
        """ tokens in common between texts """
        doc = nlp(text)
        return doc._.enrich(domains)

    @staticmethod
    def get_overlaps(text1, text2):
        """ tokens in common between texts """
        doc1 = nlp(text1)
        doc2 = nlp(text2)
        return doc1._.overlap(doc2)

    @staticmethod
    def summarize(text):
        # Tokenizing the sentence into sentences
        sentences = split_sentences(text)

        # Adding all stopwords to a list
        stop_words = nlp.Defaults.stop_words

        # Histogram
        word2Count = {}
        for word in SentenceParser.tokenize(text, stop_words):
            if word not in word2Count.keys():
                word2Count[word] = 1
            else:
                word2Count[word] += 1

        # Weighted Histogram
        for key in word2Count.keys():
            word2Count[key] = word2Count[key] / max(word2Count.values())

        sent_Score = {}
        for sentence in sentences:
            for word in SentenceParser.tokenize(sentence.lower()):
                if word in word2Count.keys():
                    if len(sentence.split(
                            " ")) < 15:  # We only want smaller length sentences
                        if sentence not in sent_Score.keys():
                            sent_Score[sentence] = word2Count[word]
                        else:
                            sent_Score[sentence] += word2Count[word]

        # Summary
        return heapq.nlargest(15, sent_Score, sent_Score.get)

    # Readability
    #   https://en.wikipedia.org/wiki/Readability
    @staticmethod
    def grade_level(text):
        """
        These readability tests are used extensively in the field of education.
        The "Flesch–Kincaid Grade Level Formula" instead presents
        a score as a U.S. grade level, making it easier for teachers, parents,
        librarians, and others to judge the readability level of various
        books and texts. It can also mean the number of years of education
        generally required to understand this text, relevant when
        the formula results in a number greater than 10.

        The result is a number that corresponds with a U.S. grade level.
        The sentence, "The Australian platypus is seemingly a hybrid of a
        mammal and reptilian creature" is an 11.3 as it has 24 syllables
        and 13 words. The different weighting factors for words per sentence
        and syllables per word in each scoring system mean that the two
        schemes are not directly comparable and cannot be converted.
        The grade level formula emphasises sentence length over word length.
        By creating one-word strings with hundreds of random characters,
        grade levels may be attained that are hundreds of times larger
        than high school completion in the United States.
        Due to the formula's construction,
        the score does not have an upper bound.

        The lowest grade level score in theory is −3.40, but there are few
        real passages in which every sentence consists of a single
        one-syllable word. Green Eggs and Ham by Dr. Seuss comes close,
        averaging 5.7 words per sentence and 1.02 syllables per word,
        with a grade level of −1.3. (Most of the 50 used words are
        monosyllabic; "anywhere", which occurs eight times,
        is the only exception.)
        """
        doc = nlp(text)
        return doc._.flesch_kincaid_grade_level

    @staticmethod
    def reading_ease(text):
        """
        n the Flesch reading-ease test, higher scores indicate material that
        is easier to read; lower numbers mark passages that are more
        difficult to read. The formula for the Flesch reading-ease
        score (FRES) test is

            206.835 − 1.015 ( total words total sentences ) − 84.6 ( total syllables total words ) {\displaystyle 206.835-1.015\left({\frac {\text{total words}}{\text{total sentences}}}\right)-84.6\left({\frac {\text{total syllables}}{\text{total words}}}\right)} {\displaystyle 206.835-1.015\left({\frac {\text{total words}}{\text{total sentences}}}\right)-84.6\left({\frac {\text{total syllables}}{\text{total words}}}\right)}[7]

        Score 	        School level 	    Notes
        100.00–90.00 	5th grade 	        Very easy to read. Easily understood by an average 11-year-old student.
        90.0–80.0 	    6th grade 	        Easy to read. Conversational English for consumers.
        80.0–70.0 	    7th grade 	        Fairly easy to read.
        70.0–60.0   	8th & 9th grade 	Plain English. Easily understood by 13- to 15-year-old students.
        60.0–50.0   	10th to 12th grade 	Fairly difficult to read.
        50.0–30.0   	College 	        Difficult to read.
        30.0–0.0 	    College graduate 	Very difficult to read. Best understood by university graduates.
        """
        doc = nlp(text)
        return doc._.flesch_kincaid_reading_ease

    @staticmethod
    def dale_chall(text):
        """
        Edgar Dale, a professor of education at Ohio State University, was one of the first critics of Thorndike’s vocabulary-frequency lists. He claimed that they did not distinguish between the different meanings that many words have. He created two new lists of his own. One, his “short list” of 769 easy words, was used by Irving Lorge in his formula. The other was his “long list” of 3,000 easy words, which were understood by 80% of fourth-grade students. However, one has to extend the word lists by regular plurals of nouns, regular forms of the past tense of verbs, progressive forms of verbs etc. In 1948, he incorporated this list into a formula he developed with Jeanne S. Chall, who later founded the Harvard Reading Laboratory.

        To apply the formula:

            Select several 100-word samples throughout the text.
            Compute the average sentence length in words (divide the number of words by the number of sentences).
            Compute the percentage of words NOT on the Dale–Chall word list of 3,000 easy words.
            Compute this equation from 1948:

                Raw score = 0.1579*(PDW) + 0.0496*(ASL) if the percentage of PDW is less than 5 %, otherwise compute
                Raw score = 0.1579*(PDW) + 0.0496*(ASL) + 3.6365

        Where:

            Raw score = uncorrected reading grade of a student who can answer one-half of the test questions on a passage.
            PDW = Percentage of difficult words not on the Dale–Chall word list.
            ASL = Average sentence length

        Finally, to compensate for the “grade-equivalent curve,” apply the following chart for the Final Score:

        Raw score	Final score
        4.9 and below	Grade 4 and below
        5.0–5.9	Grades 5–6
        6.0–6.9	Grades 7–8
        7.0–7.9	Grades 9–10
        8.0–8.9	Grades 11–12
        9.0–9.9	Grades 13–15 (college)
        10 and above	Grades 16 and above.

        :param text:
        :return:
        """
        doc = nlp(text)
        return doc._.dale_chall

    @staticmethod
    def smog(text):
        """
        Harry McLaughlin determined that word length and sentence length
        should be multiplied rather than added as in other formulas.
        In 1969, he published his SMOG (Simple Measure of Gobbledygook) formula

        SMOG grading = 3 + √polysyllable count.

        Where: polysyllable count = number of words of more than two syllables
        in a sample of 30 sentences.

        The SMOG formula correlates 0.88 with comprehension as measured by reading tests.
        It is often recommended for use in healthcare.
        """
        doc = nlp(text)
        return doc._.smog

    @staticmethod
    def readability_index(text):
        doc = nlp(text)
        return doc._.automated_readability_index

    @staticmethod
    def forcast(text):
        """
        In 1973, a study commissioned by the US military of the reading
        skills required for different military jobs produced the FORCAST
        formula. Unlike most other formulas, it uses only a vocabulary
        element, making it useful for texts without complete sentences.
        The formula satisfied requirements that it would be:

            Based on Army-job reading materials.
            Suitable for the young adult-male recruits.
            Easy enough for Army clerical personnel to use without special training or equipment.

        The formula is:

            Grade level = 20 − (N / 10)

            Where N = number of single-syllable words in a 150-word sample.

        The FORCAST formula correlates 0.66 with comprehension as measured by reading tests.

                """
        doc = nlp(text)
        return doc._.forcast


class BasicTeacher:
    """
    Poor-man's english connection extractor. Not even close to complete
    """
    container = padaos.IntentContainer()

    container.add_intent('instance of', [
        '{source} (is|are|instance) {target}'])
    container.add_intent('sample of', [
        '{source} is (sample|example) {target}'])
    container.add_intent('incompatible', [
        '{source} (can not|is forbidden|is not allowed) {target}'])
    container.add_intent('synonym', [
        '{source} is (same|synonym) {target}'])
    container.add_intent('antonym', [
        '{source} is (opposite|antonym) {target}'])
    container.add_intent('part of', [
        '{source} is part {target}',
        '{target} is (composed|made) {source}'])
    container.add_intent('capable of', [
        '{source} (is capable|can) {target}'])
    container.add_intent('created by', [
        '{source} is created {target}'])
    container.add_intent('used for', [
        '{source} is used {target}'])

    @staticmethod
    def normalize(text):
        text = SentenceParser.normalize(text, make_singular=True,
                                        remove_articles=True)
        # lets be aggressive to improve parsing
        text = text.lower().replace("did you know that", "")
        text = text.replace("example", "sample of")
        words = text.split(" ")
        removes = ["a", "an", "of", "that", "this", "to", "with", "as", "by",
                   "for"]
        replaces = {"be": "is", "are": "is", "you": "self", "was": "is",
                    "i": "user", "were": "is"}
        for idx, word in enumerate(words):
            if word in removes:
                words[idx] = ""
            if word in replaces:
                words[idx] = replaces[word]

        return " ".join([w for w in words if w])

    @staticmethod
    def parse(utterance):
        utterance = BasicTeacher.normalize(utterance)
        match = BasicTeacher.container.calc_intent(utterance)

        data = match["entities"]
        data["normalized_text"] = utterance
        data["connection_type"] = match["name"]
        return data
