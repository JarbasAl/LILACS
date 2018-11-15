# LILACS - Reasoning

How can we process data in our knowledge base?

Let's talk a bit about Logic and see how we can apply it to our knowledge graph

There are several kinds of logic, you can waste hours [in](https://en.wikipedia.org/wiki/Description_logic) [wikipedia](https://en.wikipedia.org/wiki/History_of_logic) [reading](https://en.wikipedia.org/wiki/Propositional_calculus) [about](https://en.wikipedia.org/wiki/First-order_logic) [it](https://en.wikipedia.org/wiki/Higher-order_logic)

Logical connectives are found in natural languages. 

In English for example, some examples are "and" (conjunction), "or" (disjunction), "not” (negation) and "if" (but only when used to denote material conditional).

The following is an example of a very simple inference within the scope of propositional logic:

    Premise 1: If it's raining then it's cloudy.
    Premise 2: It's raining.
    Conclusion: It's cloudy.
    
Both premises and the conclusion are propositions. 

The premises are taken for granted and then with the application of modus ponens (an inference rule) the conclusion follows.

As propositional logic is not concerned with the structure of propositions beyond the point where they can't be decomposed anymore by logical connectives, this inference can be restated replacing those atomic statements with statement letters, which are interpreted as variables representing statements:

    Premise 1: {\displaystyle P\to Q} P\to Q
    Premise 2: {\displaystyle P} P
    Conclusion: {\displaystyle Q} Q
    
The same can be stated succinctly in the following way:

    {\displaystyle P\to Q,P\vdash Q} P\to Q,P\vdash Q

But this does not cover all kinds of logic, we also have:

- First-order logic (a.k.a. first-order predicate logic): First-order logic uses quantified variables over non-logical objects and allows the use of sentences that contain variables, so that rather than propositions such as Socrates is a man one can have expressions in the form "there exists X such that X is Socrates and X is a man" and there exists is a quantifier while X is a variable. This distinguishes it from propositional logic, which does not use quantifiers or relations.

- Modal logic: also offers a variety of inferences that cannot be captured in propositional calculus. For example, from "Necessarily p" we may infer that p. From p we may infer "It is possible that p". 

- Many-valued logics: are those allowing sentences to have values other than true and false. (For example, neither and both are standard "extra values"; "continuum logic" allows each sentence to have any of an infinite number of "degrees of truth" between true and false.) These logics often require calculational devices quite distinct from propositional calculus.

I will revisit this topic when talking about [teaching LILACS]()

For now lets see how we can use this logic to learn more from our knowledge base

# Semantic Reasoners

A semantic reasoner, reasoning engine, rules engine, or simply a reasoner, is a piece of software able to infer logical consequences from a set of asserted facts or axioms.
 
The inference rules are commonly specified by means of an ontology language, and often a description logic language. 

Many reasoners use [first-order predicate logic](https://en.wikipedia.org/wiki/First-order_predicate_logic) to perform reasoning; inference commonly proceeds by forward chaining and backward chaining.


**Ontology-based reasoning**

• Classification-based inference (e.g. RDF-S, OWL reasoning)

• The inference rules for RDF-S or OWL are fixed. Therefore: No need for rule engine -> procedural algorithm sufficient


![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/onto_reason.jpg?raw=true) 

We can use RDF to include rules in our ontology

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/rule_inverseOf.jpg?raw=true) 


Owlready makes our lifes easy, it uses the [HermiT](http://www.hermit-reasoner.com/) reasoner

    >>> from owlready2 import *
    
    >>> onto = get_ontology("http://test.org/onto.owl")
    
    >>> with onto:
    ...     class Drug(Thing):
    ...         def take(self): print("I took a drug")
    
    ...     class ActivePrinciple(Thing):
    ...         pass
    
    ...     class has_for_active_principle(Drug >> ActivePrinciple):
    ...         python_name = "active_principles"
    
    ...     class Placebo(Drug):
    ...         equivalent_to = [Drug & Not(has_for_active_principle.some(ActivePrinciple))]
    ...         def take(self): print("I took a placebo")
    
    ...     class SingleActivePrincipleDrug(Drug):
    ...         equivalent_to = [Drug & has_for_active_principle.exactly(1, ActivePrinciple)]
    ...         def take(self): print("I took a drug with a single active principle")
    
    ...     class DrugAssociation(Drug):
    ...         equivalent_to = [Drug & has_for_active_principle.min(2, ActivePrinciple)]
    ...         def take(self): print("I took a drug with %s active principles" % len(self.active_principles))
    
    >>> acetaminophen   = ActivePrinciple("acetaminophen")
    >>> amoxicillin     = ActivePrinciple("amoxicillin")
    >>> clavulanic_acid = ActivePrinciple("clavulanic_acid")
    
    >>> AllDifferent([acetaminophen, amoxicillin, clavulanic_acid])
    
    >>> drug1 = Drug(active_principles = [acetaminophen])
    >>> drug2 = Drug(active_principles = [amoxicillin, clavulanic_acid])
    >>> drug3 = Drug(active_principles = [])
    
    >>> close_world(Drug)

The reasoner is simply run by calling the sync_reasoner() global function:

    >>> sync_reasoner()

Owlready automatically gets the results of the reasoning from HermiT and reclassifies Individuals and Classes, 
i.e Owlready changes the Classes of Individuals and the superclasses of Classes.

    >>> print("drug2 new Classes:", drug2.__class__)
    drug2 new Classes: onto.DrugAssociation
    
    >>> drug1.take()
    I took a drug with a single active principle
    
    >>> drug2.take()
    I took a drug with 2 active principles
    
    >>> drug3.take()
    I took a placebo

In this example, drug1, drug2 and drug3 Classes have changed! The reasoner deduced that drug2 is an Association Drug, and that drug3 is a Placebo.

This step will be automatically performed by lilacs when committing something to long term memory to ensure consistency

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/kb_inconsistency.jpg?raw=true) 


We may want to perform some **Rule-based reasoning** on our own


![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/rules_reasoning.jpg?raw=true) 
    


**Forward Reasoning**

– Input: rules + data

– Output: extended data

– Starts with available facts

– Uses rules to derive new facts (which can be stored)

– Stops when there is nothing else to be derived


**Backward Reasoning**

– Input: rules + data + hypothesis (statement)

– Output: Statement is true / Statement is false

– Goes backwards from the hypothesis to the set of axioms (our data )

– If it can find the path to the original axioms, then the hypothesis is true (otherwise false)


[CWM]() is a Forward-chaining reasoner written in Python

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/cwmusage.jpg?raw=true) 

    TODO usage from lilacs
    
    
Euler/EYE – a Semibackward chaining reasoner design enhanced with Euler path detection

Semibackward chaining is backward chaining for rules using <= in N3 and forward chaining for rules using => in N3.

[learn to use EYE](http://n3.restdesc.org/), you can host your own [EYE server](https://github.com/RubenVerborgh/EyeServer)

EYE REST api can easily used from lilacs

    from lilacs.processing.comprehension.reasoning import EYE_rest
    
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
    
    
    result = EYE_rest(data, rules)
    print(result)
    
    # output
    
    # 'PREFIX ppl: <http://example.org/people#>\n'
    # 'PREFIX foaf: <http://xmlns.com/foaf/0.1/>\n'
    # '\n'
    # 'ppl:Cindy foaf:knows ppl:John.\n'
    # 'ppl:Cindy foaf:knows ppl:Eliza.\n'
    # 'ppl:Cindy foaf:knows ppl:Kate.\n'
    # 'ppl:Eliza foaf:knows ppl:John.\n'
    # 'ppl:Peter foaf:knows ppl:John.\n'
    # 'ppl:John foaf:knows ppl:Cindy.\n'
    # 'ppl:Eliza foaf:knows ppl:Cindy.\n'
    # 'ppl:Kate foaf:knows ppl:Cindy.\n'
    # 'ppl:John foaf:knows ppl:Eliza.\n'
    # 'ppl:John foaf:knows ppl:Peter.\n'


# Crawlers - Navigating the Short Term memory graph

With so much data available, we need to have some strategies to maintain it and access the relevant connections, only then can we apply logic to it

For this task i created the concept of Crawler, think of it as a spider going trough your knowledge web, but this spider can execute code as it goes!

LILACS will behave like a spotlight, it will start from tagged concepts and load every connection up to N layers, as you crawl around you load more connections

Tagging concepts is explained in the [next blog post]()

    TODO loading up a crawler code

# Build your own crawler

to make a crawler override the base class, main methods that you need to implement are choose_next_node and execute_action


        from lilacs.crawlers import BaseCrawler
        
        import random


        class URLCrawler(BaseCrawler):
        
            def select_connections(self):
                # select relevant connections from current node
                # these are passed to execute_action and choose_next_node
                return self.current_node.out_connections
        
            def choose_next_node(self, connections):
                # NOTE this crawler ignores the selected connections because it does not use them
                
                # pick a random next node
                nodes = [n for n in self.db.get_concepts() if n.name not in self.crawl_list and not n.name.startswith("http")]
                if not len(nodes):
                    return None
                next_node = random.choice(nodes)
                return next_node
        
            def execute_action(self, connections):
                # NOTE this crawler ignores the selected connections because it does not use them
                
                # execute an action in current node
                new_cons = []
                
                # search urls about current node
                urls = self.dbpedia.get_external_urls_for_dblink(self.current_node.name)
                for con in urls:
                    url = con[1]
                    if not self.con_exists("link", self.current_node.name, url):
                        c = self.db.add_connection(self.current_node.name, url, "link")
                        if c is not None:
                            new_cons.append(c)
                            
                # return newly created connections
                return new_cons
                
            def on_dead_end(self):
                # crawling reached a node with no connections
                # in here you may want to re-start crawling from other node
                # NOTE in this crawler nodes are chosen randomly and this will only happen after all nodes were visited
                self.stop_crawling()
                
            def default_node(self, start_node=None):
                # you can return a default node to start crawling from
                nodes = self.db.get_concepts()
                start_node = random.choice(nodes)
                return start_node
                

# Useful crawlers

Lets have a bunch of sample crawlers each with some strategy to perform a certain action on short memory nodes

- url finder -> search dbpedia, extract and create "link" concepts/connections
- fact finder -> search wikipedia, extracts semi structured facts from text, create "fact" concepts/connections
- label finder -> search dbpedia, extract and create "label" concepts/connections
- maintenace -> removes malformed connections, references to self, and removes some invalid connections (you can not be labeled "drug" and "person" at same time)
- connection finder -> search conceptnet/wordnet/dictionary

TODO

- long term memory candidate seeker - marks connections to be commited to long term memory
- long term memory reader - loads long term memory concepts into short memory



# Natural Language to logic

We expect to handle natural language statements, that is far away from the language we need to use with reasoners

in the [next blog post]() i will talk about question parsing, lets just consider that we extracted some data from natural language

    start_node: X
    target_node: Y
    question_type: T
    question_verbs: []
    relevant_nodes: []
 
this is pretty much a triple we can work with

let's see how we can answer certain kinds of questions using crawlers and reasoning

# question_type: what
    
What is X, tell me about X, we don't need anything fancy, let's check wikipedia

    Input:what is dog

    2017-04-21 18:13:47,752 - CLIClient - INFO - Speak: The domestic dog (Canis lupus familiaris or Canis familiaris) is a domesticated canid which has been selectively bred for millennia for various behaviors, sensory capabilities, and physical attributes. Although initially thought to have originated as a manmade variant of an extant canid species (variously supposed as being the dhole, golden jackal, or gray wolf), extensive genetic studies undertaken during the 2010s indicate that dogs diverged from an extinct wolf-like canid in Eurasia 40,000 years ago. Being the oldest domesticated animal, their long association with people has allowed dogs to be uniquely attuned to human behavior, as well as thrive on a starch-rich diet which would be inadequate for other canid species. Dogs perform many roles for people, such as hunting, herding, pulling loads, protection, assisting police and military, companionship and, more recently, aiding handicapped individuals. This impact on human society has given them the nickname "man's best friend" in the Western world. In China and South Vietnam dogs .

    
TODO code


# question_type: talk

Talk about X

i wanted to make a crawler that would give me random info, i made one that told me the wikipedia summary of some subject and of something connected to it


        Input: talk about evil
        2017-04-21 20:57:34,081 - CLIClient - INFO - Speak: Evil, in a general context, is the absence or opposite of that which is described as being good. Often, evil is used to denote profound immorality. In certain religious contexts, evil has been described as a supernatural force. Definitions of evil vary, as does the analysis of its motives. However, elements that are commonly associated with evil involve unbalanced behavior involving expediency, selfishness, ignorance, or neglect. In cultures with an Abrahamic religious influence, evil is usually perceived as the dualistic antagonistic opposite of good, in which good should prevail and evil should be defeated. In cultures with Buddhist spiritual influence, both good and evil are perceived as part of an antagonistic duality that itself must be overcome through achieving Śūnyatā meaning emptiness in the sense of recognition of good and evil being two opposing principles but not a reality, emptying the duality of them, and achieving a oneness. The philosophical question of whether morality is absolute, relative, or illusory leads to questions about the nature of evil, with views falling into one of four opposed camps: moral absolutism, amoralism, moral relativism, and moral universalism. While the term is applied to events and conditions without agency, the forms of evil addressed in this article presume an evildoer or doers.
        2017-04-21 20:57:34,616 - CLIClient - INFO - Speak: The devil (from Greek: διάβολος or diábolos = slanderer or accuser) is believed in many religions, myths and cultures to be a supernatural entity that is the personification of evil and the archenemy of God and humankind. The nature of the role varies greatly, ranging from being an effective opposite force to the creator god, locked in an eons long struggle for human souls on what may seem even terms (to the point of dualistic ditheism/bitheism), to being a comical figure of fun or an abstract aspect of the individual human condition. While mainstream Judaism contains no overt concept of a devil, Christianity and Islam have variously regarded the devil as a rebellious fallen angel or jinn that tempts humans to sin, if not committing evil deeds himself. In these religions – particularly during periods of division or external threat – the devil has assumed more of a dualistic status commonly associated with heretics, infidels, and other unbelievers. As such, the devil is seen as an allegory that represents a crisis of faith, individualism, free will, wisdom and enlightenment. In mainstream Islam and Christianity, God and the devil are usually portrayed as fighting over the souls of humans. The devil commands a force of evil spirits, commonly known as demons. The Hebrew Bible (or Old Testament) describes the Adversary (ha-satan) as an angel who instigates tests upon humankind. Many other religions have a trickster or tempter figure that is similar to the devil. Modern conceptions of the devil include the concept that he symbolizes humans' own lower nature or sinfulness.

        Input: talk about alien life
        2017-04-21 23:10:53,767 - CLIClient - INFO - Speak: Extraterrestrial life is life that does not originate from Earth. It is also called alien life, or, if it is a sentient and/or relatively complex individual, an "extraterrestrial" or "alien" (or, to avoid confusion with the legal sense of "alien", a "space alien"). These as-yet-hypothetical life forms range from simple bacteria-like organisms to beings with civilizations far more advanced than humanity. Although many scientists expect extraterrestrial life to exist, there is no unambiguous evidence for its existence so far. The science of extraterrestrial life is known as exobiology. The science of astrobiology also considers life on Earth as well, and in the broader astronomical context. Meteorites that have fallen to Earth have sometimes been examined for signs of microscopic extraterrestrial life. In 2015, "remains of biotic life" were found in 4.1 billion-year-old rocks in Western Australia, when the young Earth was about 400 million years old. According to one of the researchers, "If life arose relatively quickly on Earth ... then it could be common in the universe." Since the mid-20th century, there has been an ongoing search for signs of extraterrestrial intelligence, from radios used to detect possible extraterrestrial signals, to telescopes used to search for potentially habitable extrasolar planets. It has also played a major role in works of science fiction. Over the years, science fiction works, especially Hollywood's involvement, has increased the public's interest in the possibility of extraterrestrial life. Some encourage aggressive methods to try to get in contact with life in outer space, whereas others argue that it might be dangerous to actively call attention to Earth.
        2017-04-21 23:10:54,345 - CLIClient - INFO - Speak: Space exploration is the ongoing discovery and exploration of celestial structures in outer space by means of continuously evolving and growing space technology. While the study of space is carried out mainly by astronomers with telescopes, the physical exploration of space is conducted both by unmanned robotic probes and human spaceflight. While the observation of objects in space, known as astronomy, predates reliable recorded history, it was the development of large and relatively efficient rockets during the early 20th century that allowed physical space exploration to become a reality. Common rationales for exploring space include advancing scientific research, national prestige, uniting different nations, ensuring the future survival of humanity, and developing military and strategic advantages against other countries. Space exploration has often been used as a proxy competition for geopolitical rivalries such as the Cold War. The early era of space exploration was driven by a "Space Race" between the Soviet Union and the United States. The launch of the first human-made object to orbit Earth, the Soviet Union's Sputnik 1, on 4 October 1957, and the first Moon landing by the American Apollo 11 mission on 20 July 1969 are often taken as landmarks for this initial period. The Soviet space program achieved many of the first milestones, including the first living being in orbit in 1957, the first human spaceflight (Yuri Gagarin aboard Vostok 1) in 1961, the first spacewalk (by Aleksei Leonov) on 18 March 1965, the first automatic landing on another celestial body in 1966, and the launch of the first space station (Salyut 1) in 1971. After the first 20 years of exploration, focus shifted from one-off flights to renewable hardware, such as the Space Shuttle program, and from competition to cooperation as with the International Space Station (ISS). With the substantial completion of the ISS following STS-133 in March 2011, plans for space exploration by the USA remain in flux. Constellation, a Bush Administration program for a return to the Moon by 2020 was judged inadequately funded and unrealistic by an expert review panel reporting in 2009. The Obama Administration proposed a revision of Constellation in 2010 to focus on the development of the capability for crewed missions beyond low Earth orbit (LEO), envisioning extending the operation of the ISS beyond 2020, transferring the development of launch vehicles for human crews from NASA to the private sector, and developing technology to enable missions to beyond LEO, such as Earth–Moon L1, the Moon, Earth–Sun L2, near-Earth asteroids, and Phobos or Mars orbit. In the 2000s, the People's Republic of China initiated a successful manned spaceflight program, while the European Union, Japan, and India have also planned future manned space missions. China, Russia, Japan, and India have advocated manned missions to the Moon during the 21st century, while the European Union has advocated manned missions to both the Moon and Mars during the 20/21st century. From the 1990s onwards, private interests began promoting space tourism and then private space exploration of the Moon (see Google Lunar X Prize).
 
 TODO code
    
# question_type: think

Thinking about X

this is just like talk, but no limit on the concept number, it stops when you tell it to

        Input: think about evil
        2017-04-21 23:30:15,548 - CLIClient - INFO - Speak: Evil, in a general context, is the absence or opposite of that which is described as being good. Often, evil is used to denote profound immorality. In certain religious contexts, evil has been described as a supernatural force. Definitions of evil vary, as does the analysis of its motives. However, elements that are commonly associated with evil involve unbalanced behavior involving expediency, selfishness, ignorance, or neglect. In cultures with an Abrahamic religious influence, evil is usually perceived as the dualistic antagonistic opposite of good, in which good should prevail and evil should be defeated. In cultures with Buddhist spiritual influence, both good and evil are perceived as part of an antagonistic duality that itself must be overcome through achieving Śūnyatā meaning emptiness in the sense of recognition of good and evil being two opposing principles but not a reality, emptying the duality of them, and achieving a oneness. The philosophical question of whether morality is absolute, relative, or illusory leads to questions about the nature of evil, with views falling into one of four opposed camps: moral absolutism, amoralism, moral relativism, and moral universalism. While the term is applied to events and conditions without agency, the forms of evil addressed in this article presume an evildoer or doers.
        2017-04-21 23:30:15,554 - CLIClient - INFO - Speak: Satan (Hebrew: שָּׂטָן satan, meaning "adversary"; Arabic: شيطان shaitan, meaning; "astray", "distant", or sometimes "devil") is a figure appearing in the texts of the Abrahamic religions who brings evil and temptation, and is known as the deceiver who leads humanity astray. Some religious groups teach that he originated as an angel who fell out of favor with God, seducing humanity into the ways of sin, and who has power in the fallen world. In the Hebrew Bible and the New Testament, Satan is primarily an accuser and adversary, a decidedly malevolent entity, also called the devil, who possesses demonic qualities. In Theistic Satanism, Satan is considered a positive force and deity who is either worshipped or revered. In LaVeyan Satanism, Satan is regarded as holding virtuous characteristics.
        2017-04-21 23:30:16,092 - CLIClient - INFO - Speak: Deities depicted with horns or antlers are found in many different religions across the world.
        2017-04-21 23:30:16,616 - CLIClient - INFO - Speak: Azazel [ə-ˈzā-zəl], also spelled Azazael (Hebrew: עֲזָאזֵל, Azazel; Arabic: عزازيل , Azāzīl) appears in the Bible in association with the scapegoat rite. In some traditions of Judaism and Christianity, it is the name for a fallen angel. In Rabbinic Judaism it is not a name of an entity but rather means literally "for the complete removal", i.e., designating the goat to be cast out into the wilderness as opposed to the goat sacrificed "for YHWH".
 
 TODO code       
  
# question_type: example

Giving examples of X

we could use a crawler here, but we can just query our knowledge base


    Input: examples of planet
    2017-04-21 18:45:24,097 - CLIClient - INFO - Speak: neptune is an example of planet
    2017-04-21 18:45:24,098 - CLIClient - INFO - Speak: saturn is an example of planet
    2017-04-21 18:45:24,103 - CLIClient - INFO - Speak: venus is an example of planet
    2017-04-21 18:45:24,107 - CLIClient - INFO - Speak: earth is an example of planet
    2017-04-21 18:45:24,110 - CLIClient - INFO - Speak: mars is an example of planet
    2017-04-21 18:45:24,112 - CLIClient - INFO - Speak: uranus is an example of planet
    2017-04-21 18:45:24,114 - CLIClient - INFO - Speak: jupiter is an example of planet
    
    
    
TODO code
    

# question_type: describe
    
this is what "what" would probably look like if we didnt go for wikipedia

    Input: describe cow
    Speak: cow is animal
    Speak: cow is living being
    
TODO code

# question_type: is a

is X a Y

    Input: are frogs also animals
    Speak: answer to is frog a animal is True
    
TODO code

# question_type: same as

is X same as Y

    Input: are dogs same as animals
    Speak: answer to is dog equal to animals is False
    
TODO code

# question_type: common

What do node X and Y have in common?

There are many ways to do this, we can have 2 crawlers following the "is instance of" connections from both concepts and compare the crawl_list
    
    Input: what do frogs and humans have in common
    Speak: frog are animal like human
    Speak: frog are living being like human
    
TODO code
  
Or we can use our knowledge base directly
    
TODO code


# question_type: what of
     
In this case X is a connection of Y, instead of X being connected to Y

What is the X of Y

    ...  TODO output
    
TODO code


# question_type: path to

    Input: Why are frogs living beings
    Speak: answer to is frog a living being is True
    Speak: frog is animal
    Speak: animal is living being

TODO code

# question_type: when

    ...  TODO output
    
TODO code

# question_type: how


in here i cheated a bit and skipped our knowledge base, how to questions are hard to answer, but we can use [wikihow](https://github.com/JarbasAI/PyWikiHow)!


    Input: how to boil an egg
    
    How to Hardboil Eggs in a Microwave
    step 0 : Place your eggs in a microwave safe bowl.
    http://pad1.whstatic.com/images/thumb/b/b2/Hardboil-Eggs-in-a-Microwave-Step-1-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-1-Version-3.jpg
    step 1 : Add water to the bowl.
    http://pad2.whstatic.com/images/thumb/a/a5/Hardboil-Eggs-in-a-Microwave-Step-2-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-2-Version-3.jpg
    step 2 : Pour one tablespoon of salt into the bowl.
    http://pad1.whstatic.com/images/thumb/5/53/Hardboil-Eggs-in-a-Microwave-Step-3-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-3-Version-3.jpg
    step 3 : Cook the eggs for up to 12 minutes.
    http://pad3.whstatic.com/images/thumb/9/9b/Hardboil-Eggs-in-a-Microwave-Step-4-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-4-Version-3.jpg
    step 4 : Let the eggs cool down before you touch them.
    http://pad2.whstatic.com/images/thumb/1/10/Hardboil-Eggs-in-a-Microwave-Step-5-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-5-Version-3.jpg
    step 5 : Enjoy your hard-boiled eggs.
    http://pad1.whstatic.com/images/thumb/8/80/Hardboil-Eggs-in-a-Microwave-Step-6-Version-3.jpg/aid238320-v4-728px-Hardboil-Eggs-in-a-Microwave-Step-6-Version-3.jpg


TODO code

    
# question_type: teach
    
this question type is to indicate a teaching command, the BasicTeacher parser will be used

if the question is tagged as a teaching it is normalized and passed to basic teaching intent parser

    self.container.add_intent('instance of', ['{source} (is|are|instance) {target}'])
    self.container.add_intent('sample of', ['{source} is (sample|example) {target}'])
    self.container.add_intent('incompatible', ['{source} (can not|is forbidden|is not allowed) {target}'])
    self.container.add_intent('synonym', ['{source} is (same|synonym) {target}'])
    self.container.add_intent('antonym', ['{source} is (opposite|antonym) {target}'])
    self.container.add_intent('part of', ['{source} is part {target}', '{target} is (composed|made) {source}'])
    self.container.add_intent('capable of', ['{source} (is capable|can) {target}'])
    self.container.add_intent('created by', ['{source} is created {target}'])
    self.container.add_intent('used for', ['{source} is used {target}'])
  
it is then used to extract connections from text

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
       
        
here are a few examples of connections we can extract

    utterance: did you know that dogs are animals
    source: dog
    target: animal
    connection_type: instance of
    normalized_text: dog is animal
    
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