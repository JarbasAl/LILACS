
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

Extract numbers and dates from text

    # NOTE 1 number per sentence only
    assert LILACS.extract_number("it's over nine thousand") == 9000


    now = datetime.datetime.now()
    print(now)
    pprint(LILACS.extract_date("tomorrow i will finish LILACS", now))
    
    # output
    # 2018-09-11 01:55:07.639843
    # [datetime.datetime(2018, 9, 12, 0, 0), 'i will finish lilacs']

    assert LILACS.extract_date_range("From March 5 until April 7 1988") == [[datetime.datetime(1988, 3, 5, 0, 0), datetime.datetime(1988, 4, 8, 0, 0)]]


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
                    
# LILACS for thinking

answer questions with LILACS


    LILACS = LILACSReasoner()

    subject = "Elon Musk"
    question = "where was Elon Musk born"
    print(LILACSReasoner.answer_wikipedia(question, subject))
    # Pretoria, South Africa

    p = "Robotics is an interdisciplinary branch of engineering and science that includes mechanical engineering, electrical engineering, computer science, and others. Robotics deals with the design, construction, operation, and use of robots, as well as computer systems for their control, sensory feedback, and information processing. These technologies are used to develop machines that can substitute for humans. Robots can be used in any situation and for any purpose, but today many are used in dangerous environments (including bomb detection and de-activation), manufacturing processes, or where humans cannot survive. Robots can take on any form but some are made to resemble humans in appearance. This is said to help in the acceptance of a robot in certain replicative behaviors usually performed by people. Such robots attempt to replicate walking, lifting, speech, cognition, and basically anything a human can do."
    q = "What do robots that resemble humans attempt to do?"
    print(LILACS.answer_corpus(q, p))
    # replicate walking, lifting, speech, cognition

    t = "Which tool should a student use to compare the masses of two small rocks?"
    c = ["balance", "hand lens", "ruler", "measuring cup"]
    print(LILACS.answer_choice(t, c))
    # balance
    
    print(LILACS.is_math_question(t))
    # False

    t = "If 30 percent of 48 percent of a number is 288, what is the number?"
    print(LILACS.is_math_question(t))
    # True
    
    print(LILACS.answer(t))
    # 2000

    t = """Which tool should a student use to compare the masses of two small rocks?
    (A) balance
    (B) hand lens
    (C) ruler
    (D) measuring cup
    """
    print(LILACS.answer(t))
    # A metric ruler and a balance will measure the size and mass of an object.

    
Reasoning with LILACS


    data = """@prefix ppl: <http://example.org/people#>.
    @prefix foaf: <http://xmlns.com/foaf/0.1/>.

    ppl:Cindy foaf:knows ppl:John.
    ppl:Cindy foaf:knows ppl:Eliza.
    ppl:Cindy foaf:knows ppl:Kate.
    ppl:Eliza foaf:knows ppl:John.
    ppl:Peter foaf:knows ppl:John."""

    rules = """@prefix foaf: <http://xmlns.com/foaf/0.1/>.

    {
        ?personA foaf:knows ?personB.
    }
    =>
    {
        ?personB foaf:knows ?personA.
    }."""

    # print(LILACS.EYE(data, rules))
    # PREFIX ppl: <http://example.org/people#>
    # PREFIX foaf: <http://xmlns.com/foaf/0.1/>
    #
    # ppl:Cindy foaf:knows ppl:John.
    # ppl:Cindy foaf:knows ppl:Eliza.
    # ppl:Cindy foaf:knows ppl:Kate.
    # ppl:Eliza foaf:knows ppl:John.
    # ppl:Peter foaf:knows ppl:John.
    # ppl:John foaf:knows ppl:Cindy.
    # ppl:Eliza foaf:knows ppl:Cindy.
    # ppl:Kate foaf:knows ppl:Cindy.
    # ppl:John foaf:knows ppl:Eliza.
    # ppl:John foaf:knows ppl:Peter.

# LILACS for image analysis

Perception includes vision!

    LILACS = LILACSVisualReasoner()

    picture = "sasha.jpg"

    question = "how many humans?"
    data = LILACS.answer_question(question, picture)
    result = data["answer"]
    print(result)
    # 1

    question = "is the person male or female?"
    data = LILACS.answer_question(question, picture)
    result = data["answer"]
    print(result)
    # female

    data = LILACS.label_image(picture)
    result = data["predictions"][0]
    print(result)
    # {'label_id': 'n03770439', 'label': 'miniskirt', 'probability': 0.2659367024898529}

    data = LILACS.caption_image(picture)
    result = data["predictions"][0]
    print(result)
    # {'caption': 'a woman in a white shirt and a red tie', 'index': '0', 'probability': 2.5158757668475684e-05}

    data = LILACS.recognize_objects(picture)
    result = data["predictions"][0]
    print(result)
    # {'detection_box': [0.028039246797561646, 0.16406074166297913, 1.0, 0.993462085723877], 'label': 'person', 'label_id': '1', 'probability': 0.9459671974182129}

    data = LILACS.recognize_scene(picture)
    result = data["predictions"][0]
    print(result)
    # {'label': 'beauty_salon', 'label_id': '50', 'probability': 0.5930100679397583}

    data = LILACS.image_segmentation(picture)
    result = data
    print(result)
    # {'seg_map': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ...   15, 15, 15, 15, 0]], 'label_map': ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'], 'annotated_image': '/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg.seg.jpg', 'image_size': [513, 513], 'status': 'ok', 'labels': ['person']}

    colorized_pic_path = LILACS.colorize_image(picture)
    print(colorized_pic_path)
    # /home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_colorize.png
    
    
Vision includes Faces

    LILACS = LILACSFace()

    picture = "sasha.jpg"

    data = LILACS.face_analysis(picture)
    print(data)
    # {'width': 2932, 'height': 2932, 
    #  'faces': [{'box': {'top': 724, 'width': 959, 'height': 959, 'left': 1043}, 
    #  'gender': 'Female', 
    #  'eyes': {'right': {'status': 'open', 'score': 0.3153488961123401}, 'left': {'status': 'open', 'score': 0.30432877233646144}}, 
    #  'age': 20, 
    #  'skin': {'color': '#9f8c86', 'white': 0.7}}], 
    #  '#faces': 1}

    data = LILACS.face_emotion(picture)
    print(data)
    # {'width': 2932, 'height': 2932, 
    #   'faces': [{'box': {'top': 724, 'width': 959, 'height': 959, 'left': 1043}, 
    #   'emotions': [{'angry': 0.547586977481842}, {'disgust': 0.03107559122145176}, {'fear': 0.07608325034379959}, {'happy': 0.049507103860378265}, {'neutral': 0.058710116893053055}, {'sad': 0.1907171905040741}, {'surprise': 0.04631979763507843}], 'smile': True}], 
    #   '#faces': 1}
    
    data = LILACS.face_age(picture)
    print(data)
    # [{'age_estimation': 23, 'face_box': [360, 165, 291, 406]}]

    files = LILACS.animate_eyes(picture)
    print(files)
    # ['/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_roll.mp4', '/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_scroll.mp4', '/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_cross.mp4', '/home/user/PycharmProjects/LILACS_github/lilacs/processing/vision/sasha.jpg_shift.mp4']