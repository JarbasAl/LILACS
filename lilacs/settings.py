from os.path import dirname, join

ROOT_DIR = dirname(__file__)
MODELS_DIR = join(ROOT_DIR, "models")
DATABASE_DIR = join(ROOT_DIR, "memory/database")
SPACY_MODEL = "en_core_web_sm" # "en_core_web_lg", "en_core_web_md" "xx_ent_wiki_sm"
SENSE2VEC_MODEL = "reddit_vectors-1.1.0"
SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"

HOST = "127.0.0.1"
PORT = 8181
ROUTE = "/lilacs"

DANDELION_API = "6ac8924185fe46f481a38f46d7c63aef"
