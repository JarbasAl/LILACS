from lilacs.processing.nlp.word_vectors import WordTwoVec
from lilacs.processing.comprehension import textual_entailment
from os.path import join, dirname


class SolverBase(object):
    """
    interface for solvers. to implement one just inherit from this class and override
    `answer_question` and `solver_info`
    """
    def answer_question(self, question, choices):
        """answer the question"""
        raise NotImplementedError()

    def solver_info(self) -> str:
        """info about the solver"""
        raise NotImplementedError()


class WordVectorSimilaritySolver(SolverBase):
    """uses word2vec to score questions"""
    def __init__(self, model_file=None):
        # trained on aristo-mni-corpus
        # https://s3-us-west-2.amazonaws.com/aristo-public-data/aristo-mini-corpus-v1.txt.gz
        if model_file is None:
            model_file = join(dirname(dirname(dirname(__file__))), "models/word2answers")
        self.word_two_vec = WordTwoVec(model_file)

    def solver_info(self) -> str:
        return "word_vector_similarity"

    def answer_question(self, question, choices):
        return [self.word_two_vec.cosine_similarity(question, choice) for choice in choices]


class TextualEntailmentSolver(SolverBase):
    """uses textual entailment to score questions"""
    def solver_info(self) -> str:
        return "textual_entailment"

    def answer_question(self, question, choices):
        return [textual_entailment(question, choice) for choice in choices]


# TODO more solvers https://github.com/allenai/ARC-Solvers https://github.com/allenai/aristo-mini/
# An entailment-based model that computes the entailment score for each (retrieved sentence, question+answer choice as an assertion) pair and scores each answer choice based on the highest-scoring sentence.
# A reading comprehension model (BiDAF) that converts the retrieved sentences into a paragraph per question. The model is used to predict the best answer span and each answer choice is scored based on the overlap with the predicted span.