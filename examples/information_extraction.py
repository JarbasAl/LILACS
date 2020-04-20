from lilacs.reasoning.extraction import LILACSextractor
from pprint import pprint as print

LILACS = LILACSextractor()


test_text = """London is the capital and most populous city of England and the United Kingdom.
          Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
          It was founded by the Romans, who named it Londinium. 
          London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. 
          Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""

facts = LILACS.extract_facts(test_text)
"""
[
 'Since at least the 19th century, "London" has also referred to the '
 'metropolis around this core, historically split between Middlesex, Essex, '
 'Surrey, Kent and Hertfordshire, which today largely makes up Greater London, '
 'a region governed by the Mayor of London and the London Assembly.',

 'London is the capital and most populous city of England and the United '
 'Kingdom.',

 'standing on the River Thames in the south east of the island of Great '
 'Britain, London has been a major settlement for 2 millennia.',

 "London's ancient core, the City of London, which covers an area of only 1.12 "
 'square miles (2.9 km2), largely retains its medieval boundaries.'
]
"""

facts = LILACS.extract_facts(test_text, "Romans")
"""
['It was founded by the Romans, who named it Londinium.']
"""

triples = LILACS.extract_semi_structured_statements(test_text)
"""
[('London', 'is', 'the capital and most populous city of England and the United Kingdom.'),
 ('London', 'has been', 'a major settlement for 2 millennia.')]
"""
print(triples)
exit()
triples = LILACS.extract_interesting_triples(test_text, singularize=True)
"""
[('London', 'be', 'capital'),
 ('London', 'be', 'populous'),
 ('London', 'be', 'city'),
 ('London', 'be', 'Kingdom'),
 ('London', 'be', 'settlement'),
 ('core', 'retain', 'boundaries')]
"""

entities = LILACS.extract(test_text)
# NOTE dbpedia is SLOW, disabled by default
# to include it in results bellow
# entities = LILACS.extract(big_text, dbpedia=True)
for ent in entities:
    print(ent + " " + str(entities[ent]["tags"]))
"""
"London ['Capital City', 'GPE', 'Noun']"
"City ['Noun']"
"England ['GPE', 'Noun']"
"River Thames ['LOC', 'Noun']"
"Greater London ['ORG', 'Noun']"
"United Kingdom ['GPE', 'Noun']"
"Great Britain ['GPE', 'Noun']"
"Romans ['NORP', 'Noun']"
"Londinium ['PERSON', 'Noun']"
"Middlesex ['GPE', 'Noun']"
"Essex ['GPE', 'Noun']"
"Surrey ['GPE', 'Noun']"
"Kent ['GPE', 'Noun']"
"Hertfordshire ['GPE', 'Noun']"
"Mayor ['Noun']"
"London Assembly ['ORG', 'Noun']"
"south east ['LOC']"
"City of London ['GPE']"
"only 1.12 square miles ['QUANTITY']"
"2 millennia ['DATE']"
"2.9 km2 ['Area:Square_kilometre', 'QUANTITY']"
"at least 19th century ['DATE']"
"today ['DATE']"
"2 ['Dimensionless_quantity']"
"1.12 square miles ['Area:Square_mile']"
"""

entities = LILACS.extract_named_entities(test_text)
"""
[{'confidence': 1,
  'data': {'explanation': 'Countries, cities, states',
           'facts': ['Since at least the 19th century, "London" has also '
                     'referred to the metropolis around this core, '
                     'historically split between Middlesex, Essex, Surrey, '
                     'Kent and Hertfordshire, which today largely makes up '
                     'Greater London, a region governed by the Mayor of London '
                     'and the London Assembly.',
                     'London is the capital and most populous city of England '
                     'and the United Kingdom.',
                     'Standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.']},
  'tags': ['GPE'],
  'value': 'London'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states',
           'facts': ['London is the capital and most populous city of England '
                     'and the United Kingdom.']},
  'tags': ['GPE'],
  'value': 'England'},
 {'confidence': 1,
  'data': {'explanation': 'Non-GPE locations, mountain ranges, bodies of water',
           'facts': ['Standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.']},
  'tags': ['LOC'],
  'value': 'River Thames'},
 {'confidence': 1,
  'data': {'explanation': 'Non-GPE locations, mountain ranges, bodies of water',
           'facts': ['Standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.']},
  'tags': ['LOC'],
  'value': 'south east'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states',
           'facts': ['London is the capital and most populous city of England '
                     'and the United Kingdom.']},
  'tags': ['GPE'],
  'value': 'City of London'},
 {'confidence': 1,
  'data': {'explanation': 'Measurements, as of weight or distance',
           'facts': ["London's ancient core, the City of London, which covers "
                     'an area of only 1.12 square miles (2.9 km2), largely '
                     'retains its medieval boundaries.']},
  'tags': ['QUANTITY'],
  'value': 'only 1.12 square miles'},
 {'confidence': 1,
  'data': {'explanation': 'Companies, agencies, institutions, etc.',
           'facts': ['Standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.']},
  'tags': ['ORG'],
  'value': 'Greater London'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'United Kingdom'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Great Britain'},
 {'confidence': 1,
  'data': {'explanation': 'Absolute or relative dates or periods', 'facts': []},
  'tags': ['DATE'],
  'value': '2 millennia'},
 {'confidence': 1,
  'data': {'explanation': 'Nationalities or religious or political groups', 'facts': []},
  'tags': ['NORP'],
  'value': 'Romans'},
 {'confidence': 1,
  'data': {'explanation': 'People, including fictional', 'facts': []},
  'tags': ['PERSON'],
  'value': 'Londinium'},
 {'confidence': 1,
  'data': {'explanation': 'Measurements, as of weight or distance', 'facts': []},
  'tags': ['QUANTITY'],
  'value': '2.9 km2'},
 {'confidence': 1,
  'data': {'explanation': 'Absolute or relative dates or periods', 'facts': []},
  'tags': ['DATE'],
  'value': 'at least 19th century'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Middlesex'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Essex'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Surrey'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Kent'},
 {'confidence': 1,
  'data': {'explanation': 'Countries, cities, states', 'facts': []},
  'tags': ['GPE'],
  'value': 'Hertfordshire'},
 {'confidence': 1,
  'data': {'explanation': 'Absolute or relative dates or periods', 'facts': []},
  'tags': ['DATE'],
  'value': 'today'},
 {'confidence': 1,
  'data': {'explanation': 'Companies, agencies, institutions, etc.',
           'facts': []},
  'tags': ['ORG'],
  'value': 'London Assembly'}]
"""


# Bellow are simple_NER wrappers

entities = LILACS.extract_dbpedia(test_text, strict=False)
# strict=False ignores exception when spotlight is down
"""
[{'confidence': 0.9986392327537942,
  'data': {'facts': ['Since at least the 19th century, "London" has also '
                     'referred to the metropolis around this core, '
                     'historically split between Middlesex, Essex, Surrey, '
                     'Kent and Hertfordshire, which today largely makes up '
                     'Greater London, a region governed by the Mayor of London '
                     'and the London Assembly.',
                     'London is the capital and most populous city of England '
                     'and the United Kingdom.',
                     'standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'uri': 'http://dbpedia.org/resource/London'},
  'tags': ['Wikidata:Q486972',
           'Schema:Place',
           'DBpedia:Settlement',
           'DBpedia:PopulatedPlace',
           'DBpedia:Place',
           'DBpedia:Location'],
  'value': 'London'},
 {'confidence': 0.9987980803946171,
  'data': {'facts': [],
           'uri': 'http://dbpedia.org/resource/United_Kingdom'},
  'tags': ['Wikidata:Q6256',
           'Schema:Place',
           'Schema:Country',
           'DBpedia:PopulatedPlace',
           'DBpedia:Place',
           'DBpedia:Location',
           'DBpedia:Country'],
  'value': 'United Kingdom'},
 {'confidence': 0.9999999999907914,
  'data': {'facts': ['standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'uri': 'http://dbpedia.org/resource/River_Thames'},
  'tags': ['Wikidata:Q47521',
           'Wikidata:Q4022',
           'Schema:RiverBodyOfWater',
           'Schema:Place',
           'Schema:BodyOfWater',
           'DBpedia:Stream',
           'DBpedia:River',
           'DBpedia:Place',
           'DBpedia:NaturalPlace',
           'DBpedia:Location',
           'DBpedia:BodyOfWater'],
  'value': 'River Thames'},
  
(....)

 {'confidence': 0.9999981762260153,
  'data': {'facts': ['standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'uri': 'http://dbpedia.org/resource/Greater_London'},
  'tags': ['Wikidata:Q3455524',
           'Schema:Place',
           'Schema:AdministrativeArea',
           'DBpedia:Region',
           'DBpedia:PopulatedPlace',
           'DBpedia:Place',
           'DBpedia:Location',
           'DBpedia:AdministrativeRegion'],
  'value': 'Greater London'},
 {'confidence': 0.9999996204112885,
  'data': {'facts': [],
           'uri': 'http://dbpedia.org/resource/London_Assembly'},
  'tags': ['Wikidata:Q43229',
           'Wikidata:Q24229398',
           'Wikidata:Q11204',
           'DUL:SocialPerson',
           'DUL:Agent',
           'Schema:Organization',
           'DBpedia:Organisation',
           'DBpedia:Legislature',
           'DBpedia:Agent'],
  'value': 'London Assembly'}
]
"""

entities = LILACS.extract_keywords(test_text)  # Rake Keywords
"""
[{'confidence': 1,
  'data': {'facts': [], 'keyword_score': 9.0},
  'tags': ['keyword'],
  'value': 'today largely makes'},
 {'confidence': 1,
  'data': {'facts': ['London is the capital and most populous city of England '
                     'and the United Kingdom.'],
           'keyword_score': 4.0},
  'tags': ['keyword'],
  'value': 'populous city'},
 {'confidence': 1,
  'data': {'facts': [], 'keyword_score': 4.0},
  'tags': ['keyword'],
  'value': 'united kingdom'},
 {'confidence': 1,
  'data': {'facts': ['standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'keyword_score': 4.0},
  'tags': ['keyword'],
  'value': 'river thames'},
 {'confidence': 1,
  'data': {'facts': ['standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'keyword_score': 4.0},
  'tags': ['keyword'],
  'value': 'south east'},
 (...)
"""

entities = LILACS.extract_location(test_text)  # wordlist, country names and  capital cities only
"""
[{'confidence': 0.9,
  'data': {'country_code': 'GB',
           'country_name': 'United Kingdom',
           'facts': ['Since at least the 19th century, "London" has also '
                     'referred to the metropolis around this core, '
                     'historically split between Middlesex, Essex, Surrey, '
                     'Kent and Hertfordshire, which today largely makes up '
                     'Greater London, a region governed by the Mayor of London '
                     'and the London Assembly.',
                     'London is the capital and most populous city of England '
                     'and the United Kingdom.',
                     'standing on the River Thames in the south east of the '
                     'island of Great Britain, London has been a major '
                     'settlement for 2 millennia.'],
           'hemisphere': 'north',
           'name': 'London'},
  'tags': ['Capital City'],
  'value': 'London'}]
"""

entities = LILACS.extract_units(test_text)
"""
TODO BUG in quantulum 3
"""
