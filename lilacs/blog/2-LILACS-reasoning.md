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
- Modal logic: also offers a variety of inferences that cannot be captured in propositional calculus. For example, from "Necessarily p" we may infer that p. From p we may infer "It is possible that p". The translation between modal logics and algebraic logics concerns classical and intuitionistic logics but with the introduction of a unary operator on Boolean or Heyting algebras, different from the Boolean operations, interpreting the possibility modality, and in the case of Heyting algebra a second operator interpreting necessity (for Boolean algebra this is redundant since necessity is the De Morgan dual of possibility). The first operator preserves 0 and disjunction while the second preserves 1 and conjunction.
- Many-valued logics: are those allowing sentences to have values other than true and false. (For example, neither and both are standard "extra values"; "continuum logic" allows each sentence to have any of an infinite number of "degrees of truth" between true and false.) These logics often require calculational devices quite distinct from propositional calculus. When the values form a Boolean algebra (which may have more than two or even infinitely many values), many-valued logic reduces to classical logic; many-valued logics are therefore only of independent interest when the values form an algebra that is not Boolean.

I will revisit this topic when talking about [teaching LILACS]()

For now lets see how we can use this logic to learn more from our knowledge base

# Semantic Reasoners

A semantic reasoner, reasoning engine, rules engine, or simply a reasoner, is a piece of software able to infer logical consequences from a set of asserted facts or axioms.
 
The notion of a semantic reasoner generalizes that of an inference engine, by providing a richer set of mechanisms to work with. 

The inference rules are commonly specified by means of an ontology language, and often a description logic language. 

Many reasoners use [first-order predicate logic](https://en.wikipedia.org/wiki/First-order_predicate_logic) to perform reasoning; inference commonly proceeds by forward chaining and backward chaining.

Forward chaining (or forward reasoning) is one of the two main methods of reasoning when using an inference engine and can be described logically as repeated application of modus ponens. Forward chaining is a popular implementation strategy for expert systems, business and production rule systems. The opposite of forward chaining is backward chaining.

Forward chaining starts with the available data and uses inference rules to extract more data (from an end user, for example) until a goal is reached. An inference engine using forward chaining searches the inference rules until it finds one where the antecedent (If clause) is known to be true. When such a rule is found, the engine can conclude, or infer, the consequent (Then clause), resulting in the addition of new information to its data.[1]

Inference engines will iterate through this process until a goal is reached.


![reasoner](https://upload.wikimedia.org/wikipedia/commons/a/a3/Backward_Chaining_Frog_Color_Example.png  "bkwardreasoner")

Owlready makes our lifes easier, it uses the [HermiT]() reasoner

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

Other option we have to perform reasoning is the EYE reasoner



# Crawlers - Navigating the Short Term memory graph

With so much data available, we need to have some strategies to maintain it and access the relevant connections, only then can we apply logic to it

LILACS will behave like a spotlight, it will start from tagged concepts and load every connection up to N layers

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

