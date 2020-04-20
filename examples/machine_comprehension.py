from lilacs.reasoning import textual_entailment
from lilacs.reasoning.reading import machine_comprehension, best_sentence, \
    bow_retrieve, tfidf_retrieve, generate_questions


passage = """London is the capital and most populous city of England and the United Kingdom.
   standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
   It was founded by the Romans, who named it Londinium. 
   London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. 
   Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""


# question generation
questions = generate_questions(passage)
"""
[{
    'question': 'What is London?', 
    'answers': [capital, city, Kingdom, settlement]
 },
 {
    'question': 'What does core retain?', 
    'answers': [boundaries]
 }]
"""

# question answering
for question in ["what is the capital of the uk",
                 "what is the area of london's core",
                 "who discovered london"]:
    answer = machine_comprehension(question, passage)
    """
    what is the capital of the uk
        London
        
    what is the area of london's core
        the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries
        
    who discovered london
        the Romans
    """

    # "dumb" baselines

    retrieve = best_sentence(question, passage)
    bow = bow_retrieve(question, passage)
    tfidf = tfidf_retrieve(question, passage)
    """
   what is the capital of the uk
       London is the capital and most populous city of England and the United Kingdom.
       London is the capital and most populous city of England and the United Kingdom.
       London is the capital and most populous city of England and the United Kingdom.
       
   what is the area of london's core
       standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
        London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries.
        London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries.
        
    who discovered london
        It was founded by the Romans, who named it Londinium.
        Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly.
        Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly.
   """


s = "The romans discovered london"

s2 = "The romans know about london"
entailment = textual_entailment(s, s2)
"""
{'entailment': 0.9251744151115417, 
'contradiction': 0.019063036888837814, 
'neutral': 0.055762507021427155}
"""

s3 = "The romans have never been to london"
entailment = textual_entailment(s, s3)
"""
{'entailment': 0.015860626474022865, 
'contradiction': 0.9449489116668701, 
'neutral': 0.039190422743558884}
"""

s4 = "The romans like wine"
entailment = textual_entailment(s, s4)
"""
{'entailment': 0.07881151139736176, 
'contradiction': 0.09066061675548553, 
'neutral': 0.8305278420448303}
"""

