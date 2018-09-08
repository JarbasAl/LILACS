import requests


def similar_sense2vec_demo(text, sense="auto"):
    data = {"word": text, "sense": sense}
    r = requests.post("https://api.explosion.ai/sense2vec/find", data)
    return r.json()


def similar_sense2vec(text, nlp, num=5):
    doc = nlp(str(text))
    ents = []
    for token in doc:
        similar = [(s[0][0], s[1]) for s in token._.s2v_most_similar(num)]
        ents.extend([{"strength": int(s[1] * 100), "concept": str(s[0])} for s in similar if s[0] != text])
    return ents


# WIP - scrapping failing

# DO NOT ABUSE, de purposes only
# run from source https://github.com/fginter/w2v_demo

def similar_turkunlp_demo(text, n=10, model="Finnish+4B+wordforms+skipgram"):
    models = ["Suomi24 wordforms skipgram",
              "Finnish 4B wordforms skipgram",
              "Suomi24 lemmas skipgram",
              "English GoogleNews Negative300"]
    model = model.replace(" ", "+")
    text = text.replace(" ", "+")
    url = "http://bionlp-www.utu.fi/wv_demo/nearest"
    data = {
        "form[0][name]": "word",
        "form[0][value]": text,
        "form[1][name]": "topn",
        "form[1][value]": n,
        "model_name": model
    }
    headers = {"Host": "bionlp-www.utu.fi",
        "Connection": "keep-alive",
        "Content-Length": "148",
        "Origin": "http://bionlp-www.utu.fi",
        "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "DNT": "1",
        "Referer": "http://bionlp-www.utu.fi/wv_demo/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en-US,en;q=0.9"}
    r = requests.post(url, data=data)
    print(r.text)

similar_turkunlp_demo("dog")
