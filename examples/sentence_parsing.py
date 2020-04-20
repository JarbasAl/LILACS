from lilacs.parse import SentenceParser

LILACS = SentenceParser()

# Chunking text
text = "turn on the light and turn it green"
big_text = """London is the capital and most populous city of England and 
the United Kingdom. Standing on the River Thames in the south east of the 
island of Great Britain, London has been a major settlement for 2 millennia. It was founded by the Romans, who named it Londinium."""


sentences = LILACS.split_sentences(big_text, solve_corefs=True)
"""
['London is the capital and most populous city of England and the United Kingdom.', 
'Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.', 
'London was founded by the Romans, who named London Londinium.']
"""
sentences = LILACS.chunk(big_text, solve_corefs=True)
"""
['London is the capital', 
'most populous city of England', 
'the United Kingdom.', 
'Standing on the River Thames in the south east of the island of Great Britain',
'London has been a major settlement for 2 millennia.', 
'London was founded by the Romans', 
'who named London Londinium.']
"""

commands = LILACS.chunk(text, solve_corefs=True)
"""
['turn on the light', 'turn the light green']
"""


# part of speech tagging

sentence = 'London is the capital'
dep_tags = LILACS.dependency_labels(sentence)
"""
[('London', 'nsubj'), ('is', 'ROOT'), ('the', 'det'), ('capital', 'attr')]
"""

universal_tags = LILACS.tag_sentence(sentence)
"""
[('London', 'PROPN'), ('is', 'AUX'), ('the', 'DET'), ('capital', 'NOUN')]
"""

pos_tags = LILACS.postag(sentence)
"""
[('London', 'NNP'), ('is', 'VBZ'), ('the', 'DT'), ('capital', 'NN')]
"""

# https://en.wikipedia.org/wiki/Brown_Corpus#Part-of-speech_tags_used
brown_tags = LILACS.brown_postag(sentence)
"""
[('London', 'NP-HL'), ('is', 'BEZ'), ('the', 'AT'), ('capital', 'NN')]
"""


# handling verbs
assert LILACS.is_passive('Mistakes were made.')
assert not LILACS.is_passive('I made mistakes.')
# NOTE Notable fail case. Fix me. I think it is because the 'to be' verb is omitted.
#assert LILACS.is_passive('guy shot by police')

assert LILACS.change_tense("I am making dinner",
                           "past") == "I was making dinner"
assert LILACS.change_tense("I am making dinner",
                           "future") == "I will be making dinner"
assert LILACS.change_tense("I am making dinner",
                           "present") == "I am making dinner"


# word metrics
n_words = LILACS.count_unique_words(big_text)
""" 38 """

bag = LILACS.bag_of_words(big_text)
"""
[('London', 2), ('capital', 1), ('populous', 1), ('city', 1), ('United', 1), 
('Kingdom', 1), ('stand', 1), ('River', 1), ('Thames', 1), ('south', 1), 
('east', 1), ('island', 1), ('Great', 1), ('Britain', 1), (...)"""


rank = LILACS.text_rank(big_text)
"""
[('major settlement', 0.04612352789123868), 
('populous city', 0.04092495866435582), 
('River Thames', 0.03982333027329801), 
('United Kingdom', 0.03941882384916587), 
('Great Britain', 0.03937889638376672)]
"""

rank = LILACS.ngram_rank(big_text)
"""
[('major settlement', 0.22021445349888044), 
('Great Britain', 0.14959586523832374)]
"""