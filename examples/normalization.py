from lilacs.parse import SentenceParser

LILACS = SentenceParser()


s = "I love my dogs"
normalized = SentenceParser.normalize(s, make_singular=True)
"""
I love my dog
"""

normalized = SentenceParser.normalize(s, make_singular=True,
                                      remove_pronouns=True)
"""
I love dog
"""

s = "My sister has a dog. She loves him."
normalized = SentenceParser.normalize(s, solve_corefs=True)
"""
My sister has dog. She loves a dog.
"""
# MISSED
# She -> My sister


s = """
London is the capital and most populous city of England and the United Kingdom.
It was founded by the Romans,who named it Londinium.
"""
normalized = SentenceParser.normalize(s, solve_corefs=True,
                                      remove_articles=True)
"""
London is capital and most populous city of England and United Kingdom.
London was founded by Romans, who named London Londinium.
"""
# MISSED
# who -> the romans


normalized_chunks = SentenceParser.process_text(s)
"""
['london capital populous city england united kingdom', 
'found romans name londinium']
"""
