# Learning

When we fail to understand we can do better than answer that we don't know, an assumption i'm going to make is that the user tried to teach us something 

Which kinds of questions can we ask back to the user?

This is a very simple approach, let's explore what kinds of learning we can do so we can design an user interface for them

# Extracting Knowledge

Let's attempt to extract facts statements from text

    test_text = """London is the capital and most populous city of England and the United Kingdom. Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium. London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""
    
    LILACS = LILACSTextAnalyzer()
     
There’s a python library called textacy that implements several common data extraction algorithms on top of spaCy. It’s a great starting point.

One of the algorithms it implements is called Semi-structured Statement Extraction. We can use it to search the parse tree for simple statements where the subject is one of our tagged nodes and the verb is a form of “be”.


    LILACS.extract_facts("London", test_text)
    
    # output
    [('London', 'is'. 'the capital and most populous city of england and the united kingdom'),
    ('London', 'is', 'a major settlement for 2 millennium')]

Facts are extracted when the verb "is" is used

Another thing we can do is use coreference resolution and assume the linked entities are related, this way we do not need to care about the subject

    LILACS.coreference_triples(test_text)
    
    # output
    [('London', 'is', 'the capital'),
     ('the capital', 'is', 'most populous city of England and the United Kingdom'),
     ('London', 'is', 'the City of London'),
     ('London', 'is', 'a region governed by the Mayor of London and the London Assembly')]


# Extracting triples from text

Textacy provides an out of the box way to extract triples from text


    LILACS.extract_triples("London", test_text)
    
    # output
    [('london', 'is', 'capital'),
     ('london', 'is', 'city'),
     ('london', 'is', 'kingdom'),
     ('london', 'has been', 'settlement'),
     ('who', 'named', 'it'),
     ('who', 'named', 'londinium'),
     ('which', 'covers', 'area'),
     ('core', 'retains', 'boundary'),
     ('which', 'makes', 'london'),
     ('which', 'makes', 'region')]

We can automatically filter some interesting ones if we select "is" and "has" triples

    LILACS.interesting_triples(test_text)    
    
    # output

    [('london', 'is', 'capital'),
     ('london', 'is', 'city'),
     ('london', 'is', 'kingdom')]



# Extracting Relationships

Can we extract relationships directly from text to improve our knowledge base?

The main goal of relation extraction is to determine a type of relation between two target entities that appear together in a text

a recent paper [Context-Aware Representations for Knowledge Base Relation Extraction](https://github.com/UKPLab/emnlp2017-relation-extraction) allows us to extract possible relations, [demo here](http://semanticparsing.ukp.informatik.tu-darmstadt.de:5000/relation-extraction/static/index.html)

        # takes a list of sentences
        sentences = test_text.split(".")
        LILACS.possible_relations(sentences)
        
        # output
        [('London', 'country', 'United Kingdom'),
         ('London', 'instance of', 'capital'),
         ('London', 'instance of', 'populous city'),
         ('England', 'instance of', 'capital'),
         ('England', 'instance of', 'populous city'),
         ('River Thames', 'country', 'Great Britain'),
         ('Great Britain', 'instance of', 'island'),
         ('Romans', 'subclass of', 'Londinium'),
         ('London', 'instance of', 'City'),
         ('London', 'instance of', 'area'),
         ('London', 'instance of', 'City'),
         ('km2', 'subclass of', 'boundaries'),
         ('Kent', 'capital', 'London'),
         ('Kent', 'shares border with', 'Middlesex'),
         ('Kent', 'shares border with', 'Essex'),
         ('Kent', 'shares border with', 'Surrey')]

# Machine Comprehension

Machine Comprehension (MC) answers natural language questions by selecting an answer span within an evidence text. 

The AllenNLP toolkit provides a reimplementation of BiDAF (Seo et al, 2017), or Bi-Directional Attention Flow, a widely used MC baseline that achieved state-of-the-art accuracies on the SQuAD dataset (Wikipedia sentences) in early 2017.

Passage

    "Saturn is the sixth planet from the Sun and the second-largest in the Solar System, after Jupiter. It is a gas giant with an average radius about nine times that of Earth. Although it has only one-eighth the average density of Earth, with its larger volume Saturn is just over 95 times more massive. Saturn is named after the Roman god of agriculture; its astronomical symbol represents the god's sickle."

Question

    "What does Saturn’s astronomical symbol represent?"
    
Answer

    the god's sickle

# Textual Entailment

Textual Entailment (TE) takes a pair of sentences and predicts whether the facts in the first necessarily imply the facts in the second one. 

The AllenNLP toolkit provides a reimplementation of the decomposable attention model (Parikh et al, 2017) , which was state of the art for the SNLI benchmark (short sentences about visual scenes) in 2016. Rather than pre-trained Glove vectors, this model uses ELMo embeddings, which are completely character based and improve performance by 2%

Premise

    "An interplanetary spacecraft is in orbit around a gas giant's icy moon."

Hypothesis

    "The spacecraft has the ability to travel between planets."

Summary

    It is likely that the premise entails the hypothesis.
    
    Judgement	Probability
    Entailment	89.4%
    Contradiction	0.8%
    Neutral	9.8%
    
    

# Semantic Role Labeling

Semantic Role Labeling (SRL) recovers the latent predicate argument structure of a sentence, providing representations that answer basic questions about sentence meaning, including “who” did “what” to “whom,” etc. 

The AllenNLP toolkit provides a reimplementation of a deep BiLSTM model (He et al, 2017), which is currently state of the art for PropBank SRL (Newswire sentences).

We can use this to extract arguments and verbs connecting them

Sentence

    The keys, which were needed to access the building, were locked in the car.
    
Output

    were: The keys , which [V: were] needed to access the building , were locked in the car .
    needed: [ARG1: The keys] , [R-ARG1: which] were [V: needed] [ARGM-PRP: to access the building] , were locked in the car .
    access: The keys , which were needed to [V: access] [ARG1: the building] , were locked in the car .
    were: The keys , which were needed to access the building , [V: were] locked in the car .
    locked: [ARG1: The keys , which were needed to access the building ,] were [V: locked] [ARGM-LOC: in the car] .
    
    # LILACS filters down to
    
    # {
    #   'locked': ['the car', 'keys , which were needed to access the building'],
    #   'needed': ['access the building', 'keys']
    # }


# Learning Crawlers

We can make a crawler that proposes new triples by reading wikipedia summarys

    ** current node: text
    ** triple: ('Literature', 'is' ,'text')
    ** triple: ('literature', 'is', 'art')
    ** triple: ('classification', 'is', 'poetry')
    ** triple: ('classification', 'is', 'prose')
    ** triple: ('classification', 'is', 'fiction')
    
Or one that proposes new relationships directly

    ** current judaism
    ** triple: ('Tanakh', 'instance of', 'religion')
    ** triple: ('Tanakh', 'part of', 'Hebrew Bible')
    ** triple: ('Judaism', 'instance of', 'religion')
    ** triple: ('Judaism', 'part of', 'Hebrew Bible')