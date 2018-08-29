from lilacs.nlp import get_nlp, get_corefnlp
from lilacs.processing.crawlers import BaseCrawler


class NLPCrawler(BaseCrawler):
    nlp = None
    coref_nlp = None

    def __init__(self, db=None, max_crawl=200, threaded=True, debug=False, nlp=None, coref_nlp=None):
        BaseCrawler.__init__(self, db, max_crawl, threaded, debug)
        self.nlp = nlp or get_nlp()
        self.coref_nlp = coref_nlp or get_corefnlp()
