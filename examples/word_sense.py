from lilacs.reasoning import LILACSWordAnalyzer

from lilacs.reasoning.disambiguation import LILACSDisambiguation


LILACS = LILACSWordAnalyzer()


# disambiguation

bank_sents = ['I went to the bank to deposit my money',
              'The river bank was full of dead fishes']

plant_sents = ['The workers at the industrial plant were overworked',
               'The plants are no longer bearing flowers',
               'my plant is dying but still alive']

for sent in bank_sents:
    print(sent)
    candidates = LILACSDisambiguation.disambiguate(sent, "bank",
                                                   multiple=True)
    for c, score in candidates[:3]:
        print(score, c.definition())
    """
    I went to the bank to deposit my money
    0.6 a financial institution that accepts deposits and channels the money into lending activities
    0.2 sloping land (especially the slope beside a body of water)
    0.2 the funds held by a gambling house or the dealer in some gambling games
    
    The river bank was full of dead fishes 
    0.6 sloping land (especially the slope beside a body of water)
    0.30000000000000004 an arrangement of similar objects in a row or in tiers
    0.2 a financial institution that accepts deposits and channels the money into lending activities
    """

for sent in plant_sents:
    print(sent)
    candidates = LILACSDisambiguation.disambiguate(sent, "plant",
                                                   multiple=True)
    for c, score in candidates[:3]:
        print(score, c.definition())

    """
    The workers at the industrial plant were overworked
    0.6 buildings for carrying on industrial labor
    0.5 (botany) a living organism lacking the power of locomotion
    0.1 an actor situated in the audience whose acting is rehearsed but seems spontaneous to the audience
    
    The plants are no longer bearing flowers
    0.6 (botany) a living organism lacking the power of locomotion
    0.30000000000000004 something planted secretly for discovery by another
    0.2 buildings for carrying on industrial labor
    
    my plant is dying but still alive
    0.6 buildings for carrying on industrial labor
    0.30000000000000004 (botany) a living organism lacking the power of locomotion
    0.2 an actor situated in the audience whose acting is rehearsed but seems spontaneous to the audience
    """


# Word level
w1 = "king"
w2 = "queen"

sense_score = LILACS.s2v_similarity_match(w1, w2)
vec_score = LILACS.w2v_similarity_match(w1, w2)
# 0.8250584 0.7252610345406867


# Sentence level

s = "the king is dead, long live the king"

s2 = "the queen rules over the earth"

s3 = "play that song from queen"


sense_score = LILACS.s2v_similarity_match(s, s2)
vec_score = LILACS.w2v_similarity_match(s, s2)
# 0.8250584 0.8530856599658982

sense_score = LILACS.s2v_similarity_match(s2, s3)
vec_score = LILACS.w2v_similarity_match(s, s2)
# 0.3250367 0.8530856599658982

print(LILACS.related_concepts(s))
# [(('new king', 'NOUN'), 0.852),
# (('usurper', 'NOUN'), 0.8357),
# (('throne', 'NOUN'), 0.8272)]

print(LILACS.related_concepts(s2))
# [(('earth', 'NOUN'), 0.9023),
# (('Earth', 'LOC'), 0.886),
# (('earths', 'NOUN'), 0.8471),
# (('king', 'NOUN'), 0.8251),
# (('queen', 'VERB'), 0.8104),
# (('princess', 'NOUN'), 0.7896)]


print(LILACS.related_concepts(s3))
# [(('first song', 'NOUN'), 0.931),
# (('whole song', 'NOUN'), 0.9194),
# (('other song', 'NOUN'), 0.9191)]
