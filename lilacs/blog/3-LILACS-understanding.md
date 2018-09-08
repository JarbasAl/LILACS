# LILACS Understanding

First things first, we have talked about memory, interwebz and crawlers, but the point of a bot is to answer questions!

How does it understand what is being asked ?


# normalize the text!

Text can be messy, let's clean things up using nlp techniques

TODO talk more about coref

- lowercase everything
- remove extra spaces
- expand contractions - can't => can not
- numbers into digits - "two" => 2
- singularize nouns - "dogs" => "dog"
- coreference resolution - "My sister has a dog. She loves him." => "My sister has a dog. My sister loves a dog."


        text = normalize(text)
        text = coreference_resolution(text)
        
        
# tag concepts

we have memory don't we? then lets tag concepts to decide what we are talking about!!

keeping in mind the power of the internet, as an optional step lets use [spotlight](), this will give us some concepts we can learn more about right away

connections from spotlight:
- tagged nodes
- instance of connections
- same as connections
- url connections


        concepts, parents, synonyms, urls = self.spotlight_tag(text)
        

then we can also perform Named Entity Recognition and tag a few more concepts

        concepts = NER(text)
        
TODO talk more about NER, samples from several sources


# classify and parse the question

we still have no idea what the question is about, lets look at the grammatical structure

Traditional grammar defines the object in a sentence as the entity that is acted upon by the subject. 

lets get those from the received text

        subjects, objects = get_subject_object(txt)
     
here we make a smart guess on which is the main node of the question, and the target node if any

        
        # did the sentence have subjects?
        if len(subjects):
            # the first one is probably the main one
            center_node = subjects[0]
            # did it have objects?
            if len(objects):
                # the first one is probably the main one
                target_node = objects[0]
            # no objects, maybe it had another subject
            elif len(subjects) > 1:
                target_node = subjects[1]
        elif len(objects):
            # object only, lets use the first one
            center_node = objects[0]
            # theres another, this is the target
            if len(objects) > 1:
                target_node = objects[1]
        else:
            # lets use the root verb of the sentence as the main concept
            center_node = self.get_root(doc)


Regex will let us know if there is 1 or 2 components in a question, lets use those to improve the tagged nodes

        parse = self.regex_parse(text)
        # failsafe, use regex query
        if not center_node:
            if "Query2" in parse:
                # we found our nodes
                center_node = parse["Query1"]
                target_node = parse["Query2"]
            else:
                # still missing target node
                center_node = parse["Query"]
                
        if not target_node:
            # found missing node in
            if "Query2" in parse:
                target_node = parse["Query2"]
                
If we are still missing a target node, lets pick all the nouns of the sentence, and use the last one!

            else:
                # extract noun chunks and pick last one
                chunks = self.get_noun_chunks(doc)
                chunks = [c for c in chunks if center_node not in c]
                if len(chunks):
                    target_node = chunks[-1]
                elif center_node != parse["Query"]:
                    target_node = parse["Query"].replace(center_node, "").replace("  ", " ")
                    
                    
Now that we have an idea of what the text is talking about and know what memory to access, what do we do with it?

Is the user asking a question or teaching me something? Or is it small talk? we assumed we were being asked something

This is just a pre tagging for decision making, actual answering will use other techniques, 

I decided to use [Padaos](), a dead simple regex intent parser! 

The reason for this choice is that i want it to miss cases it wasn't explicitly designed to handle


    from lilacs.nlp.spotting import LILACSQuestionParser
    
    parser = LILACSQuestionParser()

    questions = ["dogs and cats in common",
                 "tell me about evil",
                 "give examples of animals",
                 "what is the speed of light",
                 "when were you born",
                 "did you know that dogs are animals"]

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
        
Output

    Question: dogs and cats in common
    normalized: dog and cat in common
    start_node: dog
    target_node: cat
    question_type: common
    question_root: dog
    question_verbs: []
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: tell me about evil
    normalized: tell me about evil
    start_node: evil
    target_node: 
    question_type: what
    question_root: tell
    question_verbs: [tell]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: give examples of animals
    normalized: give example of animal
    start_node: animal
    target_node: 
    question_type: example
    question_root: give
    question_verbs: [give]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: what is the speed of light
    normalized: what is the speed of light
    start_node: speed
    target_node: light
    question_type: what of
    question_root: 
    question_verbs: [is]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    Question: when were you born
    normalized: when were you born
    start_node: self
    target_node: born
    question_type: when
    question_root: born
    question_verbs: [born]
    parents: {}
    relevant_nodes: ['you']
    synonyms: {}
  
    Question: did you know that dogs are animals
    normalized: teach dog is animal
    start_node: dog
    target_node: animal
    question_type: teach
    question_root: 
    question_verbs: [teach, is]
    parents: {}
    relevant_nodes: []
    synonyms: {}
    
    
# learning from text

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


# General Question Answering

All this was only a pre processing, it allows us to decide the next course of action

This all sounds like a "train the user" situation, we will end up talking very awkwardly to our bot or more often it will miss what we are saying

What can we do in this "last case scenario"? Which systems do we have in place for general question answering?

TODO wolfram alpha bla bla bla


# Multiple Choice Questions

There are 2 models we can use to solve multiple answer questions

- An entailment-based model that computes the entailment score for each (retrieved sentence, question+answer choice as an assertion) pair and scores each answer choice based on the highest-scoring sentence.
- A reading comprehension model (BiDAF) that converts the retrieved sentences into a paragraph per question. The model is used to predict the best answer span and each answer choice is scored based on the overlap with the predicted span.


Let's ask [Aristo](http://allenai.org/aristo/)

     question = """Which tool should a student use to compare the masses of two small rocks?
    (A) balance
    (B) hand lens
    (C) ruler
    (D) measuring cup
    """
    answer = ask_aristo(question)
    top20 = answer["top2"]
    print(answer["answer"])
    # A metric ruler and a balance will measure the size and mass of an object.
    

You can learn about the AI2 Reasoning Challenge (ARC) [here](http://data.allenai.org/arc/) and get the base models [here](https://github.com/allenai/ARC-Solvers)

The ARC dataset contains 7,787 genuine grade-school level, multiple-choice science questions, assembled to encourage research in advanced question-answering. 


# Mathematical Questions

If we tagged a question as a mathematical question

TODO

Let's ask [Euclid](https://allenai.org/euclid/)

       t = "If 30 percent of 48 percent of a number is 288, what is the number?"
       answer = ask_euclid(t)
       
       # ["2000"]



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
    

Can we extract relationships directly to improve our knowledge base?

The main goal of relation extraction is to determine a type of relation between two target entities that appear together in a text

a recent paper [Context-Aware Representations for Knowledge Base Relation Extraction](https://github.com/UKPLab/emnlp2017-relation-extraction) allows us to extract possible relations, [demo here](http://semanticparsing.ukp.informatik.tu-darmstadt.de:5000/relation-extraction/static/index.html)

        t = "Star Wars VII is an American space opera epic film directed by  J. J. Abrams."
        pprint(relation_extraction(t))
        
        # [('J. J. Abrams', 'notable work', 'Star Wars VII'),
        #  ('J. J. Abrams', 'genre', 'space opera epic film'),
        #  ('Star Wars VII', 'genre', 'space opera epic film')]

