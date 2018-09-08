# LILACS - Knowledge

Bots are not limited like humans! they have the power of the interwebz and sql

What if we could populate our nodes and connections automatically?

Bootstraping nodes from other databases is something we can do, but realistically we don't want to store all that data

I decided to take at an hybrid approach and keep possibilities open, when possible we want to be able to query these databases, but we don't necessarily want to keep a copy of them

Let's look at some of the projects out there, if you are interested in this topic read [A Comparative Survey of DBpedia, Freebase, OpenCyc, Wikidata, and YAGO](http://www.semantic-web-journal.net/system/files/swj1141.pdf)

We can load most of those projects as ontologies and work with them directly using [owlready](https://owlready2.readthedocs.io/en/latest/)

# Cyc

Cyc is the world's longest-lived artificial intelligence project, attempting to assemble a comprehensive ontology and knowledge base that spans the basic concepts and "rules of thumb" about how the world works 

Think common sense knowledge but focusing more on things that rarely get written down or said, in contrast with facts one might find somewhere on the internet or retrieve via Google or Wikipedia
 
Cyc aims to enable AI applications to perform human-like reasoning and be less "brittle" when confronted with novel situations that were not preconceived.

Read [the cost of common sense](https://www.technologyreview.com/s/403757/cycorp-the-cost-of-common-sense/) if you are interested in learning more about this project

can we bootstrap lilacs with this [data](https://old.datahub.io/dataset/opencyc)?

opencyc was taken down, but the [wayback machine](https://web.archive.org/web/20161221222424/http://sw.opencyc.org/downloads/opencyc_owl_downloads_v4/opencyc-2012-05-10-readable.owl.gz) can help us, or some other [mirror](https://lod-cloud.net/dataset/opencyc)!

OpenCyc Ontology Size of dump and data set: ~1.6 million triples, ~150MB uncompressed

owlready also understands this file format!


# UMBEL

[UMBEL(http://umbel.org/)'s reference concepts form a coherent graph of relationships, organized into 31 mostly disjoint SuperTypes. Closely aligned concepts are clustered into hierarchically organized classes ("typologies") with further relatedness links.

![umb](http://umbel.org/imgs/umbel.graph.PNG  "umbel")

UMBEL has about 65,000 formal mappings to OpenCyc, DBpedia, PROTON, GeoNames, and schema.org, and provides linkages to more than 2 million Wikipedia entities (English version).

We can bootstrap from umbels [data](https://github.com/structureddynamics/umbel)


# DBPedia

DBpedia is a crowd-sourced community effort to extract structured content from the information created in various Wikimedia projects. This structured information resembles an open knowledge graph (OKG) which is available for everyone on the Web. A knowledge graph is a special kind of database which stores knowledge in a machine-readable form and provides a means for information to be collected, organised, shared, searched and utilised. Google uses a similar approach to create those knowledge cards during search. We hope that this work will make it easier for the huge amount of information in Wikimedia projects to be used in some new interesting ways. 

DBpedia data is served as Linked Data, which is revolutionizing the way applications interact with the Web. One can navigate this Web of facts with standard Web browsers, automated crawlers or pose complex queries with SQL-like query languages (e.g. SPARQL). Have you thought of asking the Web about all cities with low criminality, warm weather and open jobs? That's the kind of query we are talking about.


We can query DbPedia live

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
        
        
Or we can import its [ontology](https://wiki.dbpedia.org/downloads-2016-10) directly


# ConceptNet

[ConceptNet](http://conceptnet.io/) is a freely-available semantic network, designed to help computers understand the meanings of words that people use.

ConceptNet originated from the crowdsourcing project Open Mind Common Sense, which was launched in 1999 at the MIT Media Lab. It has since grown to include knowledge from other crowdsourced resources, expert-created resources, and games with a purpose.

We can query ConceptNet [live](https://github.com/commonsense/conceptnet5/wiki/API) or [host it](https://github.com/commonsense/conceptnet5)

     data = requests.get('http://api.conceptnet.io/c/en/' + subject).json()
     edges = data["edges"]


# WordNet

TODO

# Wikidata

TODO


# Mapping between each other

TODO

http://klon.wzks.uj.edu.pl/wiki-types/



# Unstructured Data Sources

The good old internet was made for humans, data is usually not structured in semantic networks

can LILACS get information out of other web resources?



# Wikipedia

TODO

# WikiHow

TODO


# Word Vectors

the hot new thing is word vectors, we can represent words in a vector space, its just that it needs 300+ dimensions instead of 2 or 3

What did fastText learn by reading Wikipedia? Let’s open the 2GB file and have a look:

    good -0.1242 -0.0674 -0.1430 -0.0005 -0.0345 ...
    day 0.0320 0.0381 -0.0299 -0.0745 -0.0624 ...
    three 0.0304 0.0070 -0.0708 0.0689 -0.0005 ...
    know -0.0370 -0.0138 0.0392 -0.0395 -0.1591 ...
    ...
    
Great, this format should be easy to work with. Each line contains one word, represented as a vector in 300-dimensional space. If this was in 2D, we could imagine it as follows:


![vecs](https://cdn-images-1.medium.com/max/800/1*mWQtzgXAFTsLg6NAjK6xDg.png  "wordvecs")

The only difference is that each word doesn’t have 2 coordinates, but 300.

First question: Which word is closest in the vector space to a given word?

How do we compute the distance between two word vectors a, b? 
You might say “Euclidean distance” but cosine similarity works much better for our use case. 
The idea is the absolute length of a vector doesn’t matter, what’s interesting is the angle between the two vectors.

From high school (or Wikipedia):

![cos formula](https://cdn-images-1.medium.com/max/800/1*Acs3Kbrrrb4d3fqMlGhMcQ.png  "fprmula")

Time to try it out:

    >>> print_related(words, 'spain')
    britain, england, france, europe, germany, spanish, italy
    >>> print_related(words, 'called')
    termed, dubbed, named, referred, nicknamed, titled, described
    >>> print_related(words, 'although')
    though, however, but, whereas, while, since, Nevertheless
    >>> print_related(words, 'arms')
    legs, arm, weapons, coat, coats, armaments, hands
    >>> print_related(words, 'roots')
    root, origins, stems, beginnings, rooted, grass, traditions

Let’s try something more difficult. Given two words like “Paris” and “France” with a semantic relationship between them (Paris is the capital of France), and a third word, “Rome”, can we infer “Italy”?

It turns out we can simply add and subtract vectors to do this! This is because the vectors for those words have a specific relationship in space:

![vec analogy](https://cdn-images-1.medium.com/max/800/1*EOVxNmHkrsPQ7Q44N0OiQg.png  "analogy")


Let’s ask some questions:

    >>> print_analogy('Paris', 'France', 'Rome', words)
    Paris-France is like Rome-Italy
    >>> print_analogy('man', 'king', 'woman', words)
    man-king is like woman-queen
    >>> print_analogy('walk', 'walked' , 'go', words)
    walk-walked is like go-went
    >>> print_analogy('quick', 'quickest' , 'far', words)
    quick-quickest is like far-furthest
    
It works! By reading Wikipedia, fastText learned something about capitals, genders, irregular verbs and adjectives


There are a lot of pre trained word vectors to choose from, training your own is out of scope for now, but here is what we can use in LILACS

- word2vec - https://code.google.com/archive/p/word2vec/
- word2vec models - https://github.com/3Top/word2vec-api
- Glove - https://github.com/stanfordnlp/GloVe
- elmo - https://allennlp.org/elmo
- sense2vec - https://github.com/explosion/sense2vec/releases
- fastText - https://github.com/facebookresearch/fastText/blob/master/pretrained-vectors.md


# Putting it all together

We can work with each of those individually as needed, LILACS provides an easy to way to interact with each of these sources

Further, LILACS loads information from these sources selectively into short term memory, it can then maybe be commited to our own long term ontologies

Tagging information automatically from these sources and commiting it too long term memory is covered in further blog posts

Here is how you can use lilacs lib

TODO

Getting raw data

    # online sources
    
    # get from dbpedia
    
    # get from source X
    
    # offline database / bootstrap
    
    
Getting data as concepts / connections

    # online sources
    
    # get concepts from X
    
    # get cons from X
    
    # offline database / bootstrap
    
    # get concepts from X
    
    # get cons from X