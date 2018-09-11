
# LILACS ( Lilacs Is a Learning And Comprehension Subsystem )

you are a curious one, this is a toy project, dont expect to use it

there's lots of non sense and TODOS

nothing is ready

you cant use it if it is not ready

there are no docs

there is no purpose

im taking notes as i go, read on if you must


- [memory](lilacs/blog/0-LILACS-memory.md)
- [data](lilacs/blog/1-LILACS-data.md)
- [nervous system](lilacs/blog/2-LILACS-crawlers.md)
- [understanding](lilacs/blog/3-LILACS-understanding.md)
- [context](lilacs/blog/4-LILACS-context.md)
- [emotions](lilacs/blog/5-LILACS-emotions.md)
- [neurotransmitters](lilacs/blog/6-LILACS_feels.md)
- [reactions](lilacs/blog/7-LILACS-reactions.md)
- [references](lilacs/blog/8-LILACS-references.md)


# LILACS for analyzing emotions

detect emotions, politeness, sentiment and assign emojis

    
    TEST_SENTENCES = ['I love mom\'s cooking',
                      'I love how you never reply back..',
                      'I love cruising with my homies',
                      'I love messing with yo mind!!',
                      'I love you and now you\'re just gone..',
                      'Thank you for your help',
                      'This is shit',
                      'This is the shit']

    LILACS = LILACSEmotionalReactor()

    for text in TEST_SENTENCES:
        print("\n" + text)
        pprint(LILACS.sentiment_analysis(text))
        pprint(LILACS.emotion_analysis(text))
        pprint(LILACS.politeness_analysis(text))
        pprint(LILACS.emoji_reaction(text))

    # output
    """
       
    I love mom's cooking
    3.0
    ['Zeal', 'Love', 'Joy', 'Remorse']
    {'confidence': '91%',
     'isrequest': False,
     'label': 'neutral',
     'text': "I love mom's cooking"}
    [':stuck_out_tongue_closed_eyes:',
     ':heart_eyes:',
     ':heart:',
     ':blush:',
     ':yellow_heart:']
    
    I love how you never reply back..
    3.0
    ['Annoyance', 'boredom', 'Despair']
    {'confidence': '95%',
     'isrequest': False,
     'label': 'neutral',
     'text': 'I love how you never reply back..'}
    [':unamused:',
     ':expressionless:',
     ':angry:',
     ':neutral_face:',
     ':broken_heart:']
    
    I love cruising with my homies
    3.0
    ['Serenity', 'Optimism', 'Awe']
    {'confidence': '99%',
     'isrequest': False,
     'label': 'neutral',
     'text': 'I love cruising with my homies'}
    [':sunglasses:', ':ok_hand:', ':v:', ':relieved:', ':100:']
    
    I love messing with yo mind!!
    3.0
    ['Delight', 'Pride', 'Bemusement', 'Zeal', 'Disfavor']
    {'confidence': '98%',
     'isrequest': False,
     'label': 'neutral',
     'text': 'I love messing with yo mind!!'}
    [':stuck_out_tongue_winking_eye:',
     ':smiling_imp:',
     ':smirk:',
     ':wink:',
     ':speak_no_evil:']
    
    I love you and now you're just gone..
    3.0
    ['Despair', 'Disappointment', 'boredom', 'Sadness', 'Pessimism']
    {'confidence': '93%',
     'isrequest': False,
     'label': 'neutral',
     'text': "I love you and now you're just gone.."}
    [':broken_heart:', ':pensive:', ':disappointed:', ':sleepy:', ':cry:']
    
    Thank you for your help
    4.0
    ['Pride', 'Joy', 'Optimism', 'Delight']
    {'confidence': '83%',
     'isrequest': False,
     'label': 'polite',
     'text': 'Thank you for your help'}
    [':pray:', ':relaxed:', ':blush:', ':relieved:', ':+1:']
    
    This is shit
    -4.0
    ['Annoyance', 'Outrage', 'boredom', 'Cynicism']
    {'confidence': '81%',
     'isrequest': False,
     'label': 'impolite',
     'text': 'This is shit'}
    [':angry:', ':rage:', ':disappointed:', ':unamused:', ':triumph:']
    
    This is the shit
    -4.0
    ['Zeal', 'Delight', 'Optimism', 'Serenity', 'Bemusement']
    {'confidence': '80%',
     'isrequest': False,
     'label': 'impolite',
     'text': 'This is the shit'}
    [':headphones:', ':notes:', ':ok_hand:', ':sunglasses:', ':smirk:']

    """
    

# LILACS for analyzing text

ask LILACS things about text

    test_text = """London is the capital and most populous city of England and the United Kingdom.
    Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for two millennia.
    It was founded by the Romans, who named it Londinium. London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""
    
    LILACS = LILACSTextAnalyzer()
    
    assert LILACS.coreference_resolution("My sister has a dog. She loves him.") == 'My sister has a dog. My sister loves a dog.'
    pprint(LILACS.possible_relations(test_text.split(".")))
    
    """
    [('London', 'country', 'United Kingdom'),
     ('London', 'instance of', 'capital'),
     ('London', 'instance of', 'populous city'),
     ('England', 'instance of', 'capital'),
     ('England', 'instance of', 'populous city')]
    """
    
    pprint(LILACS.extract_facts("London", test_text))
    """
    ['the capital and most populous city of england and the united kingdom',
    'a major settlement for 2 millennium']
    """
    #pprint(LILACS.extract_triples(test_text))
    pprint(LILACS.interesting_triples(test_text))
    """
    [('london', 'is', 'capital'),
     ('london', 'is', 'city'),
     ('london', 'is', 'kingdom')]
    """
    #pprint(LILACS.extract_nouns(test_text))

    question = "what is the capital of england"
    assert LILACS.answer_question(question, test_text) == "london"
    question = "what is the most populous city of england"
    assert LILACS.answer_question(question, test_text) == "london"
    question = "who founded london"
    assert LILACS.answer_question(question, test_text) == "the romans"

    premise = "London is the capital and most populous city of England and the United Kingdom"
    hypothesys = "Humans live in London"
    pprint(LILACS.validity_of_hypothesys(premise, hypothesys))
    """
    {'contradiction': 0.009316228330135345,
     'entailment': 0.936576783657074,
     'neutral': 0.05410700663924217}
    """

    premise = "Romans named London Londinium"
    hypothesys = "Romans never went to London"
    pprint(LILACS.validity_of_hypothesys(premise, hypothesys))
    """
    {'contradiction': 0.9378615617752075,
     'entailment': 0.007486931513994932,
     'neutral': 0.054651517421007156}
    """
    

# LILACS for extracting data from text

Extract entities and external data about them from text


        LILACS = LILACSextractor()
    
        test_text = """London is the capital and most populous city of England and the United Kingdom.
        Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
        It was founded by the Romans, who named it Londinium. London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""
    
    
        entities = LILACS.extract_entities(test_text)
        pprint(entities)
        
        # output
        # [('London', 'gpe'),
        #  ('England', 'gpe'),
        #  ('the United Kingdom', 'gpe'),
        #  ('the River Thames', 'fac'),
        #  ('Great Britain', 'gpe'),
        #  ('London', 'gpe'),
        #  ('two millennia', 'date'),
        #  ('Romans', 'norp'),
        #  ('Romans', 'norp'),
        #  ('Londinium', 'gpe'),
        #  ('London', 'gpe'),
        #  ('the City of London', 'gpe'),
        #  ('only 1.12 square miles', 'quantity'),
        #  ('2.9 km2', 'quantity'),
        #  ('at least the 19th century', 'date'),
        #  ('London', 'gpe'),
        #  ('Middlesex', 'gpe'),
        #  ('Essex', 'gpe'),
        #  ('Surrey', 'gpe'),
        #  ('Kent', 'gpe'),
        #  ('Hertfordshire', 'gpe'),
        #  ('today', 'date'),
        #  ('Greater London', 'loc'),
        #  ('London', 'gpe'),
        #  ('the London Assembly', 'org')]
    
        locations = LILACSextractor.extract_location(test_text)
        pprint(locations)
        
        # output
        # [{'accuracy': 0.975489576540198,
        #   'address': 'London, Greater London, England, SW1A 2DU, UK',
        #   'bbox': {'northeast': [51.6673219, 0.0323526],
        #            'southwest': [51.3473219, -0.2876474]},
        #   'city': 'London',
        #   'confidence': 1,
        #   'country': 'UK',
        #   'country_code': 'gb',
        #   'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
        #   'importance': 0.975489576540198,
        #   'lat': 51.5073219,
        #   'lng': -0.1276474,
        #   'ok': True,
        #   'osm_id': '107775',
        #   'osm_type': 'node',
        #   'place_id': '100145',
        #   'place_rank': '15',
        #   'postal': 'SW1A 2DU',
        #   'quality': 'city',
        #   'raw': {'address': {'city': 'London',
        #                       'country': 'UK',
        #                       'country_code': 'gb',
        #                       'postcode': 'SW1A 2DU',
        #                       'state': 'England',
        #                       'state_district': 'Greater London'},
        #           'boundingbox': ['51.3473219',
        #                           '51.6673219',
        #                           '-0.2876474',
        #                           '0.0323526'],
        #           'category': 'place',
        #           'display_name': 'London, Greater London, England, SW1A 2DU, UK',
        #           'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
        #           'importance': 0.975489576540198,
        #           'lat': '51.5073219',
        #           'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
        #                      'https://osm.org/copyright',
        #           'lon': '-0.1276474',
        #           'osm_id': '107775',
        #           'osm_type': 'node',
        #           'place_id': '100145',
        #           'place_rank': '15',
        #           'type': 'city'},
        #   'region': 'England',
        #   'state': 'England',
        #   'status': 'OK',
        #   'type': 'city'},
       
        #   ...
    
        #   }]
        
        annotations = LILACS.annotate(test_text)
        pprint(annotations)
        
        # output
        """
                
                [{'URI': 'http://dbpedia.org/resource/Greater_London',
                  'offset': 0,
                  'percentageOfSecondRank': 2.0763189316436016e-05,
                  'similarityScore': 0.9999778324259112,
                  'support': 4571,
                  'surfaceForm': 'London',
                  'types': 'Wikidata:Q3455524,Schema:Place,Schema:AdministrativeArea,DBpedia:Region,DBpedia:PopulatedPlace,DBpedia:Place,DBpedia:Location,DBpedia:AdministrativeRegion'},
                 {'URI': 'http://dbpedia.org/resource/Capital_city',
                  'offset': 14,
                  'percentageOfSecondRank': 2.143566429464659e-07,
                  'similarityScore': 0.9999995979453287,
                  'support': 8100,
                  'surfaceForm': 'capital',
                  'types': ''},
                
                 ...
                
                
                 {'URI': 'http://dbpedia.org/resource/Mayor',
                  'offset': 658,
                  'percentageOfSecondRank': 0.00023661355713781133,
                  'similarityScore': 0.999708913147703,
                  'support': 19123,
                  'surfaceForm': 'Mayor',
                  'types': ''},
                  {'URI': 'http://dbpedia.org/resource/London_Assembly',
                  'offset': 682,
                  'percentageOfSecondRank': 7.363265257106634e-09,
                  'similarityScore': 0.9999999926367309,
                  'support': 775,
                  'surfaceForm': 'London Assembly',
                  'types': 'Wikidata:Q43229,Wikidata:Q24229398,Wikidata:Q11204,DUL:SocialPerson,DUL:Agent,Schema:Organization,DBpedia:Organisation,DBpedia:Legislature,DBpedia:Agent'}]
                    """