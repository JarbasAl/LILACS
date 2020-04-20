from lilacs import nlp

doc = nlp("london is the capital and most populous city")
print(doc._.semi_structured_statements)


print(doc._.vader_score)
print(doc._.afinn_score)
print(doc[0]._.vader_score)
print(doc[0]._.afinn_score)
print(doc[0:2]._.vader_score)
print(doc[0:2]._.afinn_score)

print(doc._.lexicon_colors)
print(doc._.is_passive)

tok = doc[1]
print(tok._.lexicon_color)
print(tok._.brown_tag)

doc = nlp("what's the weather like")
print(doc.text)
print(doc._.normalized)
print(doc._.normalize(True))
"""
what's the weather like
what is the weather like
what is weather like
"""

doc = nlp('I want to withdraw 5,000 euros')
print(doc._.enrich())
print(doc._.enrich(["economy"]))
"""
I (desire|want) to (draw_back|pull_away|move_back|withdraw|retire|pull_back|retreat|recede) 5,000 euros
I (need|want|require) to (draw|take_away|take_out|withdraw|remove|draw_off|take) 5,000 euros
"""

print(doc._.brown_tags)


doc = nlp('Mistakes were made.')
assert doc._.is_passive
doc = nlp('I made mistakes')
assert not doc._.is_passive
# NOTE Notable fail case.because the 'to be' verb is omitted.
#doc = nlp('guy shot by police')
#assert doc._.is_passive

doc = nlp("I am making dinner")
assert doc._.change_tense("past") == "I was making dinner"
assert doc._.change_tense("future") == "I will be making dinner"
assert doc._.change_tense("present") == "I am making dinner"
