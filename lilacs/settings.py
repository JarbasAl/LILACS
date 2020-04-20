from os.path import dirname, join

ROOT_DIR = dirname(__file__)
MODELS_DIR = join(ROOT_DIR, "models")
DATABASE_DIR = join(ROOT_DIR, "memory", "database")
LEXICONS_DIR = join(ROOT_DIR, "spacy_extensions", "lexicons")


# https://github.com/allenai/allennlp-demo  <- host your own
# demo server - http://demo.allennlp.org/predict/
ALLENNLP_URL = "http://demo.allennlp.org/predict/"

# host your own ->
# demo server - 'http://api.dbpedia-spotlight.org/en/annotate'
SPOTLIGHT_URL = 'http://api.dbpedia-spotlight.org/en/annotate'


# LILACS reactor websocket
HOST = "127.0.0.1"
PORT = 8181
ROUTE = "/lilacs"


