import requests
from bs4 import BeautifulSoup


def search_openie(arg1="", rel="", arg2="", thresh=3):
    url = 'http://openie.allenai.org/search/?arg1=%s&rel=%s&arg2=%s' % (
        arg1, rel, arg2,)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    div_el = soup.find("ul", {"class": "nav nav-tabs"})
    answers = div_el.find_all("li", {"class": "visible-phone"})
    result = []
    for a in answers:
        try:
            ans = a.find("span", {"class": "title-entity"}).text
            url = "http://openie.allenai.org/" + a.find("a")["href"]
            num = int(
                a.text.replace(ans, "").replace("(", "").replace(")", ""))
            bucket = {"answer": ans, "sources": parse_sources(url),
                      "num_sentences": num}
            if num < thresh:
                break
            result.append(bucket)
        except Exception as e:
            pass
    return result


def parse_sources(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    div_el = soup.find_all("a", {"class": "sent"})
    sauce = []
    for sent in div_el:
        try:
            url = sent["href"]
            sentence = sent.text.replace("\n", " ").split("(via ")[0]
            sentence = " ".join([w.strip() for w in sentence.split(" ") if
                                 w.strip()]).replace(" , ", ", ")
            if sentence and url:
                sauce.append({"url": url, "sentence": sentence})
        except Exception as e:
            pass
    return sauce


if __name__ == "__main__":
    from pprint import pprint

    pprint(search_openie("what", "kills", "bacteria"))
    pprint(search_openie("type:Country", "is located in", "Europe"))
