# self hosted - https://github.com/dbpedia/lookup

import requests


def dbpedia_keyword_api(concept):
    url = "http://lookup.dbpedia.org/api/search/KeywordSearch?QueryClass=place&QueryString=" + concept
    r = requests.get(url, headers={"Accept": "application/json"})
    data = r.json()
    return data["results"]


def dbpedia_prefix_api(concept):
    url = "http://lookup.dbpedia.org/api/search/PrefixSearch?QueryClass=&MaxHits=5&QueryString=" + concept
    r = requests.get(url, headers={"Accept": "application/json"})
    data = r.json()
    return data["results"]



