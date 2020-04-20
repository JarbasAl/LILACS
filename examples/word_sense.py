from lilacs.reasoning import LILACSWordAnalyzer


LILACS = LILACSWordAnalyzer()


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
