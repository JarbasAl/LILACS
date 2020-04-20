from lilacs.reasoning import textual_entailment
from lilacs.reasoning.disambiguation import LILACSDisambiguation


# disambiguation

bank_sents = ['I went to the bank to deposit my money',
              'The river bank was full of dead fishes']

plant_sents = ['The workers at the industrial plant were overworked',
               'The plants are no longer bearing flowers',
               'my plant is dying but still alive']

for sent in bank_sents:
    print(sent, "\n")
    candidates = LILACSDisambiguation.disambiguate(sent, "bank",
                                                   multiple=True)
    for c, score in candidates:
        if score:
            print(score, c.definition())
    print("\n######\n")

for sent in plant_sents:
    print(sent, "\n")
    candidates = LILACSDisambiguation.disambiguate(sent, "plant",
                                                   multiple=True)
    for c, score in candidates:
        if score:
            print(score, c.definition())
    print("\n######\n")


# question answering

s = "The romans discovered london"

s2 = "The romans know about london"
print(textual_entailment(s, s2))
"""
{'entailment': 0.9251744151115417, 
'contradiction': 0.019063036888837814, 
'neutral': 0.055762507021427155}
"""

s3 = "The romans have never been to london"
print(textual_entailment(s, s3))
"""
{'entailment': 0.015860626474022865, 
'contradiction': 0.9449489116668701, 
'neutral': 0.039190422743558884}
"""

s4 = "The romans like wine"
print(textual_entailment(s, s4))
"""
{'entailment': 0.07881151139736176, 
'contradiction': 0.09066061675548553, 
'neutral': 0.8305278420448303}
"""