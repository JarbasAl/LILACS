# Propositional Logic

Let's consider different kinds of logic and how to handle them



if the question is tagged as a teaching it is passed to another intent parser

    self.container.add_intent('instance of', ['{source} (is|are|instance) {target}'])
    self.container.add_intent('sample of', ['{source} is (sample|example) {target}'])
    self.container.add_intent('incompatible', ['{source} (can not|is forbidden|is not allowed) {target}'])
    self.container.add_intent('synonym', ['{source} is (same|synonym) {target}'])
    self.container.add_intent('antonym', ['{source} is (opposite|antonym) {target}'])
    self.container.add_intent('part of', ['{source} is part {target}', '{target} is (composed|made) {source}'])
    self.container.add_intent('capable of', ['{source} (is capable|can) {target}'])
    self.container.add_intent('created by', ['{source} is created {target}'])
    self.container.add_intent('used for', ['{source} is used {target}'])
  
it can then be used to extract connections from text

    parser = BasicTeacher()

    questions = ["did you know that dogs are animals",
                 "did you know that fish is an example of animal",
                 "droids can not kill",
                 "you are forbidden to murder",
                 "you were created by humans",
                 "you are part of a revolution",
                 "robots are used to serve humanity",
                 "droids are the same as robots",
                 "murder is a crime", 
                 "everything is made of atoms"]

    for text in questions:
        data = parser.parse(text)
       
        
    """
    utterance: did you know that dogs are animals
    source: dog
    target: animal
    connection_type: instance of
    normalized_text: dog is animal
    
    utterance: did you know that fish is an example of animal
    source: fish
    target: animal
    connection_type: sample of
    normalized_text: fish is sample animal
    
    utterance: droids can not kill
    source: droid
    target: kill
    connection_type: incompatible
    normalized_text: droid can not kill
    
    utterance: you are forbidden to murder
    source: self
    target: murder
    connection_type: incompatible
    normalized_text: self is forbidden murder
    
    utterance: you were created by humans
    source: self
    target: human
    connection_type: created by
    normalized_text: self is created human
    
    utterance: you are part of a revolution
    source: self
    target: revolution
    connection_type: part of
    normalized_text: self is part revolution
    
    utterance: robots are used to serve humanity
    source: robot
    target: serve humanity
    connection_type: used for
    normalized_text: robot is used serve humanity
    
    utterance: droids are the same as robots
    source: droid
    target: robot
    connection_type: synonym
    normalized_text: droid is same robot
    
    utterance: murder is a crime
    source: murder
    target: crime
    connection_type: instance of
    normalized_text: murder is crime
    
    utterance: everything is made of atoms
    source: atom
    target: everything
    connection_type: part of
    normalized_text: everything is made atom

    """


# Extracting Knowledge

When we fail to understand we can do better than answer that we don't know, an assumption i'm going to make is that the user tried to teach us something 

Which kinds of questions can we ask back to the user?

Let's attempt to extract facts statements from text

There’s a python library called textacy that implements several common data extraction algorithms on top of spaCy. It’s a great starting point.

One of the algorithms it implements is called Semi-structured Statement Extraction. We can use it to search the parse tree for simple statements where the subject is one of our tagged nodes and the verb is a form of “be”.

    import spacy
    import textacy.extract
    
    # Load the large English NLP model
    nlp = spacy.load('en_core_web_lg')
    
    # The text we want to examine
    text = """London is the capital and most populous city of England and  the United Kingdom.  
    Standing on the River Thames in the south east of the island of Great Britain, 
    London has been a major settlement  for two millennia.  It was founded by the Romans, 
    who named it Londinium.
    """
    
    # Parse the document with spaCy
    doc = nlp(text)
    
    # Extract semi-structured statements
    statements = textacy.extract.semistructured_statements(doc, "London")
    
    # Print the results
    print("Here are the things I know about London:")
    
    for statement in statements:
        subject, verb, fact = statement
        print(f" - {fact}")
    
Here is what it spits out

    Here are the things I know about London:
     - the capital and most populous city of England and the United Kingdom.
    - a major settlement for two millennia.
    

# Extracting Relationships

Can we extract relationships directly from text to improve our knowledge base?

The main goal of relation extraction is to determine a type of relation between two target entities that appear together in a text

a recent paper [Context-Aware Representations for Knowledge Base Relation Extraction](https://github.com/UKPLab/emnlp2017-relation-extraction) allows us to extract possible relations, [demo here](http://semanticparsing.ukp.informatik.tu-darmstadt.de:5000/relation-extraction/static/index.html)

        t = "Star Wars VII is an American space opera epic film directed by  J. J. Abrams."
        pprint(relation_extraction(t))
        
        # [('J. J. Abrams', 'notable work', 'Star Wars VII'),
        #  ('J. J. Abrams', 'genre', 'space opera epic film'),
        #  ('Star Wars VII', 'genre', 'space opera epic film')]

