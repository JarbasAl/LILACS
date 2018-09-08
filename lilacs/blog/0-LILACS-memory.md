# LILACS - Memory

For a bot to understand you, it needs to have some kind of memory

Projects like [DbPedia]() and [Concept Net]() store data in semantic networks

So lets do the same for LILACS, that's also almost like humans do, we store some abstract concept and connect it to other concepts

The connections and concepts can be anything

# Long term memory

We will be working with ontologies, lets use the owlready [python package](https://owlready2.readthedocs.io/en/latest/) to make our lives easier

Long term memory for LILACS is a permanent database of facts known to be correct, every concept and connection stored here must be verified

Some words have different meanings depending on context, we can load different "worlds" depending on the task, each world is a different ontology

This will be explored further in the [next blog post]()

What is an ontology?

    TODO
    
What can we do with it?

    # Load an ontology from a local repository, or from Internet:

    from owlready2 import *
    onto = get_ontology("http://www.lesfleursdunormal.fr/static/_downloads/pizza_onto.owl")
    onto.load()
    # Create new classes in the ontology, possibly mixing OWL constructs and Python methods:
    
    class NonVegetarianPizza(onto.Pizza):
      equivalent_to = [
        onto.Pizza
      & ( onto.has_topping.some(onto.MeatTopping)
        | onto.has_topping.some(onto.FishTopping)
        ) ]
       def eat(self): print("Beurk! I'm vegetarian!")
    
    # Access the classes of the ontology, and create new instances / individuals:
    
    test_pizza = onto.Pizza("test_pizza_owl_identifier")
    test_pizza.has_topping = [ onto.CheeseTopping(),
                               onto.TomatoTopping() ]
    
    # In Owlready2, almost any lists can be modified in place, for example by appending/removing items from lists. Owlready2 automatically updates the RDF quadstore.
    
    test_pizza.has_topping.append(onto.MeatTopping())
    
    
# Short term memory

All pieces of data that come to LILACS, (i e, user speech) will be pre processed, some of that data may not be present in our long term memory but we still need to tag it and work with it

we don't want to add unverified data to our ontology, we will be using sql alchemy and maintain a sql database of runtime concepts!

At the same time we will load concepts from our long term memory as needed and process everything together

    from lilacs.nodes.concept import ConceptDatabase
    
    db = ConceptDatabase()

    def add_node(db, subject, description="", node_type="idea"):
        db.add_concept(subject, description, type=node_type)

    def add_connection(db, source_name, target_name, con_type="related"):
        return db.add_connection(source_name, target_name, con_type)

    def concepts(db):
        return db.get_concepts()

    def connections(db):
        return db.get_connections()

    def total_concepts(db):
        return db.total_concepts()

    def total_connections(db):
        return db.total_connections()

Fun experiment, save daily snapshots of this db and start fresh, you have the daily log of concepts lilacs explored, make visualization and tweet



# Defining Truth

for LILACS truth is a connection that is part of the long term memory, there is no questioning this connection when deducing facts

Discovery is a process of navigating short term memory, Truths must be aproved by user before being commited to long term memory

How do we discover and define a truth? if it comes from a trusted source we accept it!

We can check for inconsistencies with our reasoning engine and not allow additions until these are solved

In case of inconsistent ontology, an OwlReadyInconsistentOntologyError is raised.

Inconcistent classes may occur without making the entire ontology inconsistent, as long as these classes have no individuals. Inconsistent classes are inferred as equivalent to Nothing. They can be obtained as follows:

    list(default_world.inconsistent_classes())

In addition, the consistency of a given class can be tested by checking for Nothing in its equivalent classes, as follows:

    if Nothing in Drug.equivalent_to:
          print("Drug is inconsistent!")
          
