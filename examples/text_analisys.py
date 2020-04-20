from lilacs.reasoning import LILACSTextAnalyzer, LILACSWordAnalyzer

LILACS = LILACSWordAnalyzer()

# word2vec
score = LILACS.w2v_similarity_match("cat", "dog")
# 0.8016854705531046

score = LILACS.w2v_similarity_match("wednesday", "january")
# 0.689202639742927

score = LILACS.w2v_similarity_match("car", "cat")
# 0.3190752856973872


# sense2vec
w1 = "king"
w2 = "queen"

sense_score = LILACS.s2v_similarity_match(w1, w2)
vec_score = LILACS.w2v_similarity_match(w1, w2)
# 0.8250584
# 0.7252610345406867


# Sentence level

s = "the king is dead, long live the king"

s2 = "the queen rules over the earth"

s3 = "play that song from queen"


sense_score = LILACS.s2v_similarity_match(s, s2)
vec_score = LILACS.w2v_similarity_match(s, s2)
# 0.8250584
# 0.8530856599658982

sense_score = LILACS.s2v_similarity_match(s2, s3)
vec_score = LILACS.w2v_similarity_match(s, s2)
# 0.3250367
# 0.8530856599658982

related = LILACS.related_concepts(s)
# [(('new king', 'NOUN'), 0.852),
# (('usurper', 'NOUN'), 0.8357),
# (('throne', 'NOUN'), 0.8272)]

related = LILACS.related_concepts(s2)
# [(('earth', 'NOUN'), 0.9023),
# (('Earth', 'LOC'), 0.886),
# (('earths', 'NOUN'), 0.8471),
# (('king', 'NOUN'), 0.8251),
# (('queen', 'VERB'), 0.8104),
# (('princess', 'NOUN'), 0.7896)]


related = LILACS.related_concepts(s3)
# [(('first song', 'NOUN'), 0.931),
# (('whole song', 'NOUN'), 0.9194),
# (('other song', 'NOUN'), 0.9191)]


# lexicon lookup get_XXX

                       # emotion  color  subjectivity  sentiment  orientation
TEST_WORDS = ['love',  # joy      pink   strong        positive   passive
              'shit',  # anger    brown                negative
              'pain',  # fear            strong        negative
              'hate',  # anger    black  strong        negative   passive
              "walk",  #                                          active
              "dog"    #          brown
              ]

for word in TEST_WORDS:
     emo = LILACS.get_emotion(word)
     color = LILACS.get_color(word)
     subj = LILACS.get_subjectivity(word)
     sent = LILACS.get_sentiment(word)
     ori = LILACS.get_orientation(word)


LILACS = LILACSTextAnalyzer() # NOTE: subclass of LILACSWordAnalyzer


# Readability
#   https://en.wikipedia.org/wiki/Readability

text = "I am some really difficult text to read because I use obnoxiously " \
     "large words."

"""The "Flesch–Kincaid Grade Level Formula" instead presents a score as a 
U.S. grade level"""
score = LILACSTextAnalyzer.grade_level(text)
# 8.412857142857145

"""
Score 	        School level 	    Notes
100.00–90.00 	5th grade 	        Very easy to read. Easily understood by an average 11-year-old student.
90.0–80.0 	    6th grade 	        Easy to read. Conversational English for consumers.
80.0–70.0 	    7th grade 	        Fairly easy to read.
70.0–60.0   	8th & 9th grade 	Plain English. Easily understood by 13- to 15-year-old students.
60.0–50.0   	10th to 12th grade 	Fairly difficult to read.
50.0–30.0   	College 	        Difficult to read.
30.0–0.0 	    College graduate 	Very difficult to read. Best understood by university graduates. 
"""
score = LILACSTextAnalyzer.reading_ease(text)
# 59.68214285714288 - 10th to 12th grade

