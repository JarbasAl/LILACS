import unittest
import spacy
from lilacs.processing.comprehension.reasoning import LILACSReasoner, \
    LILACSMultipleChoiceReasoner


class TestReasoner(unittest.TestCase):

    def test_comprehension(self):
        corpus = "Robotics is an interdisciplinary branch of engineering and " \
                 "science that includes mechanical engineering, electrical " \
                 "engineering, computer science, and others. Robotics deals " \
                 "with the design, construction, operation, and use of robots, " \
                 "as well as computer systems for their control, sensory " \
                 "feedback, and information processing. These technologies " \
                 "are used to develop machines that can substitute for humans. " \
                 "Robots can be used in any situation and for any purpose, " \
                 "but today many are used in dangerous environments " \
                 "(including bomb detection and de-activation), " \
                 "manufacturing processes, or where humans cannot survive. " \
                 "Robots can take on any form but some are made to resemble " \
                 "humans in appearance. This is said to help in the " \
                 "acceptance of a robot in certain replicative behaviors " \
                 "usually performed by people. Such robots attempt to " \
                 "replicate walking, lifting, speech, cognition, and " \
                 "basically anything a human can do."
        question = "What do robots that resemble humans attempt to do?"
        self.assertEqual(LILACSReasoner.answer_corpus(question, corpus),
                         "replicate walking, lifting, speech, cognition")

    def test_web(self):
        # NOTE internet sources may update info and break tests

        # multiple paragraphs
        subject = "Elon Musk"
        question = "where was Elon Musk born"

        self.assertEqual(LILACSReasoner.answer_wikipedia(question, subject),
                         "Pretoria, Transvaal, South Africa")

        # multiple documents
        ans = LILACSReasoner.answer_web(
            "What has the strongest magnet field in the Universe?")
        self.assertEqual(ans["short_answers"][0], "pulsar")
        self.assertEqual(ans["answers"][0],
                         'Astrophysicists at the California Institute of Technology, using '
                         'the Palomar 200-inch telescope, have uncovered evidence that a '
                         'special type of pulsar has the strongest magnetic field in the '
                         'universe')
        for a in ans["sources"]:
            self.assertTrue(a.startswith("http"))

    def test_multiple_choice(self):
        LILACS = LILACSMultipleChoiceReasoner()
        question = "Which tool should a student use to compare the masses of two small rocks?"
        c = ["balance", "hand lens", "ruler", "measuring cup"]
        self.assertEqual(c[LILACS.answer(question, c)], "balance")
        self.assertEqual(LILACS.textual_entailment(question, c), 0)
        self.assertEqual(LILACS.vector_similarity(question, c), 0)

    def test_math(self):
        question = "If 30 percent of 48 percent of a number is 288, what is the number?"
        self.assertEqual(LILACSReasoner.is_math_question(question), True)
        self.assertEqual(LILACSReasoner.euclid(question), "2000")
        question = "Which tool should a student use to compare the masses of two small rocks?"
        self.assertEqual(LILACSReasoner.is_math_question(question), False)

    def test_science(self):
        question = """what is the speed of light"""
        self.assertEqual(LILACSReasoner.aristo(question)["answer"], 'Sound travels at 340 metres per second at sea level.  Light travels 300 million metres per second at sea level.')

        # multiple choice
        question = """Which tool should a student use to compare the masses of two small rocks?
               (A) balance
               (B) hand lens
               (C) ruler
               (D) measuring cup
               """
        self.assertEqual(LILACSReasoner.aristo(question)["answer"],
                         'A metric ruler and a balance will measure the size and mass of an object.')

    def test_analogy(self):
        parser = spacy.load('en_core_web_md')
        # gender
        self.assertEqual(LILACSReasoner.analogy("man", "king", "woman",
                                                parser)[0], "queen")
        # Fail case, capitals
        self.assertEqual(LILACSReasoner.analogy('Paris', 'France', 'Rome',
                                                parser),
                         ['pompei', 'fiumicino', 'civitavecchia'])
        # verb tenses
        self.assertEqual(LILACSReasoner.analogy('walk', 'walked', 'go',
                                                parser),
                         ['went', 'walked', 'trotted'])

        # fail case
        self.assertEqual(LILACSReasoner.analogy('quick', 'quickest', 'smart',
                                                parser),
                         ['sleekest', 'sneakiest', 'best-connected'])


if __name__ == "__main__":
    unittest.main()
