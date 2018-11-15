# LILACS - Memory

For a bot to understand you, it needs to have some kind of memory

Information needs to be expressed in a format that makes their semantics machine-readable or interpretable, in other words explicit and unified, independent of natural languages. 
Explicit means having least hidden assumptions or ambiguity. 
Unified means bearing one or more standards of terminology, reaching a certain level of consensus of the semantics of domain knowledge, expressed in formal vocabularies or ontologies.

Basic elements of the Semantic Web technology are 3 languages with increasing expressiveness: 

- Resource Description Framework (RDF)
- RDF Schema (RDFS)
- Web Ontology Language (OWL). 
    
They are based on logic and math (first order predicate logic, model theory and set theory).

So lets do the same for LILACS, that's also almost like humans do, we store some abstract concept and connect it to other concepts

The connections and concepts can be anything

# Idea and Concept of RDF / SPARQL

SPARQL is a query language for RDF databases. In contrast to relational databases like SQL, items are not part of any tables. Instead, items are linked with each other like a graph or network:

Example how to visualize an RDF database

![rdf](https://cdn-images-1.medium.com/max/800/1*-HH5qvBUoLyxcx9QCJdiSA.png  "rdf")


To describe these relations, we can use a triple:

    A triple is a statement containing a subject predicate and object.

Examples:

- Germany (subject) has the capital (predicate) Berlin (object).
- Berlin (subject) has the coordinates (predicate) 3.5million (object).
- The European Union (subject) has the member (predicate) Germany (object).
- Germany (subject) is a member of (predicate) the European Union (object).

You can come up with various statements to describe the graph above. And that is a huge benefit of SPARQL. You are not limited to a certain structure of relational databases and new information can be easily added.

If you want to dive deeper into the concept of SPARQL, I recommend [this Youtube video]() (11min)


# Long term memory

We will be working with ontologies, lets use the owlready [python package](https://owlready2.readthedocs.io/en/latest/) to make our lives easier

Owlready2 currently reads the following file format: RDF/XML, OWL/XML, NTriples. The file format is automatically detected.

Long term memory for LILACS is a permanent database of facts known to be correct, every concept and connection stored here must be verified

What is an ontology?

If you are processing text, "Jarbas" is a "Noun" and also a "Word"

But if you are talking about persons "Jarbas" is a "Person"

Some words have different properties depending on context, LILACS works with a default "world", if needed you can load different ones depending on the task, each world is a different ontology

you may work with a grammar ontology, or with the foaf ontology

ontologies are useful because they encode properties and relationships, they can even include rules as explored in [the reasoning blog post]()

An ontology does not define what the data is, but it defines what it can be, it tells you have attributes and relationships of things

If you want to learn more about ontologies i recommend this excellent [youtube video](https://www.youtube.com/watch?v=bxVqppNWSyE) (19 mins)


How do we use an ontology?

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
    

# Default Ontologies

Think of this as specialized kinds of concepts with pre defined properties and allowed relationships

Visualize the FOAF ontology at [WebVOWL](http://www.visualdataweb.de/webvowl/)

LILACS includes the following ontologies by default:

[FOAF](http://www.foaf-project.org/) 

Friend of a Friend, this ontology is used to describe people and social relationship on the Web. 
It is mostly focused on people's existence in the virtual world, with many properties related to online activity or identity
Nothing about family relations, physical address... It provides similar information on organisations or groups with a similar focus on their existence on the Web (work place webpage, etc). 
It is particularly well suited for describing people on Web-based Social platforms (facebook, twitter, blogspot, ...).

![foaf](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/foaf.jpg?raw=true "foaf")


[Event ontology](http://motools.sourceforge.net/event/event.html#event)

This ontology deals with the notion of reified events. It defines one main Event concept. An event may have a location, a time, active agents, factors and products, as depicted below.

![event](http://motools.sourceforge.net/event/event.png "events")

[Timeline ontology](http://motools.sourceforge.net/timeline/timeline.html)

This ontology deals with the notion of reified events. It defines one main Event concept. An event may have a location, a time, active agents, factors and products, as depicted below.

![time](http://motools.sourceforge.net/timeline/timeline.png "time")

[Expression of Core FRBR Concepts](http://vocab.org/frbr/core.html)

This vocabulary is an expression in RDF of the concepts and relations described in the IFLA report on the Functional Requirements for Bibliographic Records (FRBR). [en]
It includes RDF classes for the group 1, 2 and 3 entities described by the FRBR report and properties corresponding to the core relationships between those entities.

![coree](https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/FRBR-Group-1-entities-and-basic-relations.svg/220px-FRBR-Group-1-entities-and-basic-relations.svg.png
 "tcoe")



[SIOC](http://rdfs.org/sioc/spec/) 

Socially Interconnected Online Communities,  this ontology is used to describe online communities such as forums, blogs, mailing lists, wikis. It complements FOAF by stressing on the description of the products of those communities (posts, replies, threads, etc).

![sio](http://rdfs.org/sioc/spec/img/main_classes_properties.png "sioc")


[Music](http://musicontology.com/)

this ontology is used to describe information related to the music industry. It does not provide any means to describe in detail the music itself (notes, instruments, rythms, etc) but focus more on releases, live events, albums, artists, tracks that characterise most of the business-related information about music that can be found on the Web.


[Good relations](http://purl.org/goodrelations/) 

The goal of GoodRelations is to define a data structure for e-commerce that is industry-neutral, valid across the different stages of the value chain and syntax-neutral

This is achieved by using just four entities for representing e-commerce scenarios:

- An agent (e.g. a person or an organization),
- An object (e.g. a camcorder, a house, a car,...) or service (e.g. a haircut),
- A promise (offer) to transfer some rights (ownership, temporary usage, a certain license, ...) on the object or to provide the service for a certain compensation (e.g. an amount of money), made by the agent and related to the object or service, and
- A location from which this offer is available (e.g. a store, a bus stop, a gas station,...).
   

# Short term memory

All pieces of data that come to LILACS, (i e, user speech) will be pre processed

some of that data may not be present in our long term memory but we still need to tag it and work with it

we don't even know what ontology we should use most of the time

we will be using sql alchemy and maintain a sql database of runtime concepts!

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


While i call this short term memory it more like unprocessed memory, while not meant to be permanent it can still be stored and retrieved later

Fun experiment, save daily snapshots of this db and start fresh, you have the daily log of concepts lilacs explored, make visualization and tweet


# Short vs Long term

for LILACS truth is a connection that is part of the long term memory, there is no questioning this connection when deducing facts

Discovery is a process of navigating short term memory, Truths must be approved by user before being committed to long term memory

|     Memory    | Short Term |   Long Term  | 
|:-------------:|:----------:|:------------:|
| Database      |      SQL	 |      RDF     |
| Speed	        |      Fast  |	    Slow    |
| Consistency   |      ?     |	    Yes     |
| Accuracy	    |      ?	 |      Yes     |
| User Friendly |      Yes	 |      No      |
| Automatic Reasoning| No    |	    Yes     |
| Permanent	    |      No	 |      Yes     |
| Memory Usage  |	   small |	    high    |
| Python backend|	   SQL Alchemy|	OWLready|


How do we discover and define a truth? 

if it comes from a trusted source we accept it! A trusted source can be user input, or mirroring dbpedia connections

Further blog posts will explore how to generate possible truths in short term memory and ask the user about it before committing to long term memory

We can check for inconsistencies with our [reasoning engine]() and not allow additions to our world ontology until these are solved

In case of inconsistent ontology, an OwlReadyInconsistentOntologyError is raised.

Inconsistent classes may occur without making the entire ontology inconsistent, as long as these classes have no individuals. Inconsistent classes are inferred as equivalent to Nothing. They can be obtained as follows:

    list(default_world.inconsistent_classes())

In addition, the consistency of a given class can be tested by checking for Nothing in its equivalent classes, as follows:

    if Nothing in Drug.equivalent_to:
          print("Drug is inconsistent!")
          
          
