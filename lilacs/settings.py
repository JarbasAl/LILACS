from os.path import dirname, join

ROOT_DIR = dirname(__file__)
MODELS_DIR = join(ROOT_DIR, "models")
DATABASE_DIR = join(ROOT_DIR, "memory/database")
SPACY_MODEL = "en_core_web_sm" # "en_core_web_lg", "en_core_web_md" "xx_ent_wiki_sm"
SENSE2VEC_MODEL = "reddit_vectors-1.1.0"

#
SPOTLIGHT_URL = "https://api.dbpedia-spotlight.org/en/annotate"

# https://github.com/allenai/allennlp-demo  <- host your own
# demo server - http://demo.allennlp.org/predict/
ALLENNLP_URL = "http://207.154.234.38:8000/predict/"

HOST = "127.0.0.1"
PORT = 8181
ROUTE = "/lilacs"

DANDELION_API = "6ac8924185fe46f481a38f46d7c63aef"

# https://github.com/IBM/MAX-Scene-Classifier  <- host your own
SCENE_RECOGNITION_URL = "http://207.154.234.38:5000/model/predict"

# https://github.com/IBM/MAX-Object-Detector
OBJECT_DETECTOR_URL = "http://207.154.234.38:5001/model/predict"

# https://wiki.apache.org/tika/ImageCaption  <- host your own
# https://github.com/IBM/MAX-Image-Caption-Generator
IMAGE_CAPTION_URL = "http://207.154.234.38:5002/model/predict"

# https://github.com/IBM/MAX-Facial-Age-Estimator
FACE_AGE_URL = ""

# https://github.com/IBM/MAX-Inception-ResNet-v2
# https://github.com/IBM/MAX-ResNet-50
IMAGE_CLASSIFICATION_URL = ""

# https://github.com/IBM/MAX-Image-Colorizer
IMAGE_COLORIZATION_URL = ""

# https://github.com/IBM/MAX-Image-Segmenter
IMAGE_SEGMENTATION_URL = ""

# https://github.com/IBM/MAX-Audio-Classifier
SOUND_CLASSIFIER_URL = ""

