# LILACS Question Parser

formats questions in a way that lilacs can answer them


# Usage

    from lilacs.nlp.spotting import LILACSQuestionParser
    
    parser = LILACSQuestionParser()

    questions = ["dogs and cats in common",
                 "tell me about evil",
                 "how to kill animals ( a cow ) and make meat",
                 "what is a living being",
                 "why are humans living beings",
                 "give examples of animals",
                 "what is the speed of light",
                 "when were you born",
                 "where do you store your data",
                 "will you die",
                 "have you finished booting",
                 "should i program artificial stupidity",
                 "who made you",
                 "how long until sunset",
                 "how long ago was sunrise",
                 "how much is bitcoin worth",
                 "which city has more people",
                 "whose dog is this"]

    for text in questions:
        data = parser.parse_question(text)
        print("\nQuestion: " + text)
        print("start_node: " + str(data["source"]))
        print("target_node: " + str(data["target"]))
        print("question_type: " + str(data["question_type"]))
        print("question_root: " + str(data["question_root"]))
        print("question_verbs: " + str(data["verbs"]))
        print("parents: " + str(data["concepts"]["parents"]))
        print("relevant_nodes: " + str(data["concepts"]["relevant"]))
        print("synonyms: " + str(data["concepts"]["synonyms"]))
        
# Output

    Question: dogs and cats in common
    start_node: dog
    target_node: cat
    question_type: common
    question_root: dog
    question_verbs: []
    parents: {}
    relevant_nodes: []
    synonyms: {'common': 'common land'}
    
    Question: tell me about evil
    start_node: evil
    target_node: 
    question_type: what
    question_root: tell
    question_verbs: [tell]
    parents: {}
    relevant_nodes: []
    synonyms: {'evil': 'good and evil'}
    
    Question: how to kill animals ( a cow ) and make meat
    start_node: animal
    target_node: meat
    question_type: how to
    question_root: kill
    question_verbs: [kill, make]
    parents: {}
    relevant_nodes: []
    synonyms: {'kill': 'murder', 'cow': 'cattle'}
    
    Question: what is a living being
    start_node: a living being
    target_node: 
    question_type: what
    question_root: 
    question_verbs: [is, living]
    parents: {}
    relevant_nodes: []
    synonyms: {'living': 'life'}
    
    Question: why are humans living beings
    start_node: living
    target_node: human being
    question_type: why
    question_root: living
    question_verbs: [living]
    parents: {}
    relevant_nodes: []
    synonyms: {'living': 'life'}
    
    Question: give examples of animals
    start_node: animal
    target_node: 
    question_type: example
    question_root: give
    question_verbs: [give]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: what is the speed of light
    start_node: speed
    target_node: light
    question_type: what of
    question_root: 
    question_verbs: [is]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: when were you born
    start_node: self
    target_node: born
    question_type: when
    question_root: born
    question_verbs: [born]
    parents: {'born': ['disease']}
    relevant_nodes: ['you']
    synonyms: {'born': 'childbirth'}
    
    Question: where do you store your data
    start_node: self
    target_node: data
    question_type: where
    question_root: store
    question_verbs: [store]
    parents: {}
    relevant_nodes: ['you']
    synonyms: {}
    
    Question: will you die
    start_node: self
    target_node: die
    question_type: will you
    question_root: die
    question_verbs: [die]
    parents: {}
    relevant_nodes: ['you']
    synonyms: {'die': 'dice'}
    
    Question: have you finished booting
    start_node: self
    target_node: finished booting
    question_type: have you
    question_root: finished
    question_verbs: [finished, booting]
    parents: {}
    relevant_nodes: ['you']
    synonyms: {}
    
    Question: should i program artificial stupidity
    start_node: user
    target_node: stupidity
    question_type: should
    question_root: program
    question_verbs: [program]
    parents: {}
    relevant_nodes: ['i']
    synonyms: {'program': 'computer program'}
    
    Question: who made you
    start_node: self
    target_node: made
    question_type: who
    question_root: made
    question_verbs: [made]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: how long until sunset
    start_node: sunset
    target_node: until
    question_type: how long
    question_root: long
    question_verbs: []
    parents: {}
    relevant_nodes: []
    synonyms: {'long': 'vowel length'}
    
    Question: how long ago was sunrise
    start_node: sunrise
    target_node: ago
    question_type: how long
    question_root: 
    question_verbs: [was]
    parents: {}
    relevant_nodes: []
    synonyms: {'long': 'vowel length'}
    
    Question: how much is bitcoin worth
    start_node: bitcoin
    target_node: worth
    question_type: how much
    question_root: bitcoin
    question_verbs: []
    parents: {'bitcoin': ['currency']}
    relevant_nodes: []
    synonyms: {}
    
    Question: which city has more people
    start_node: city
    target_node: person
    question_type: which
    question_root: has
    question_verbs: [has]
    parents: {}
    relevant_nodes: []
    synonyms: {'person': 'grammatical person'}
    
    Question: whose dog is this
    start_node: dog
    target_node: this
    question_type: whose
    question_root: 
    question_verbs: [is]
    parents: {}
    relevant_nodes: []
    synonyms: {}
