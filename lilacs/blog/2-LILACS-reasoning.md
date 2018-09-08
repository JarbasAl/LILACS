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


![](/home/user/PycharmProjects/LILACS_github/lilacs/blog/onto_reason.jpg) 

We can use RDF to include rules in our ontology

![](/home/user/PycharmProjects/LILACS_github/lilacs/blog/rule_inverseOf.jpg) 


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

![](/home/user/PycharmProjects/LILACS_github/lilacs/blog/kb_inconsistency.jpg) 


We may want to perform some **Rule-based reasoning** on our own

• General rule-based inference (semantic rules)

![](/home/user/PycharmProjects/LILACS_github/lilacs/blog/rules_reasoning.jpg) 
    
• Further classification: forward-chaining and backward- chaining


**Forward Reasoning**

– Input: rules + data
– Output: extended data
– Starts with available facts
– Uses rules to derive new facts (which can be stored)
– Stops when there is nothing else to be derived

[CWM]() is a Forward-chaining reasoner written in Python

![](/home/user/PycharmProjects/LILACS_github/lilacs/blog/cwm usage.jpg) 

TODO usage from lilacs


**Backward Reasoning**

– Input: rules + data + hypothesis (statement)
– Output: Statement is true / Statement is false
– Goes backwards from the hypothesis to the set of axioms (our data )
– If it can find the path to the original axioms, then the hypothesis is true (otherwise false)


Euler/EYE – a backward-forward-backward chaining reasoner design enhanced with Euler path detection

Input: rules + data + hypothesis

Output: Chain of rules that lead to the hypothesis (if the hypothesis is true)

[learn to use EYE](http://n3.restdesc.org/), you can host your own [EYE server](https://github.com/RubenVerborgh/EyeServer)



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



# Answering What

TODO sample crawling for common types of questions

