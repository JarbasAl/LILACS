from os.path import dirname, join
from lilacs.settings import MODELS_DIR
from lilacs.spacy_extensions import load_extensions
from lingua_franca.lang import set_active_lang

# SpaCy setup
# python -m spacy download en_core_web_lg
import spacy
import lemminflect
from spacy_readability import Readability
from negspacy.negation import Negex
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from sense2vec import Sense2VecComponent

nlp = spacy.load("en_core_web_lg")
set_active_lang(nlp.lang)
negex = Negex(nlp)
nlp.add_pipe(negex, last=True)
nlp.add_pipe(Readability())
nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')


SENSE2VEC_MODEL = join(MODELS_DIR, "s2v_reddit_2015_md/s2v_old")
s2v = Sense2VecComponent(nlp.vocab).from_disk(SENSE2VEC_MODEL)
nlp.add_pipe(s2v)


load_extensions(nlp)

# TODO load NeuralCoref and add it to the pipe of SpaCy's model
#import neuralcoref
#neuralcoref.add_to_pipe(nlp)
