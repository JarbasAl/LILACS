# Connections

Connections have a source node, a target node, and a type

most of the times the types can be directly used to answer questions, but often you will want to "crawl" connections with different strategies depending on the question asked


You can add new types at will for your own application



#  Types



***related***

this is the default connection type, it indicates an unknown type of relationship. 

Examples of this are connections extracted from *sense2vec
*

These are useful when we need to explore new nodes while ensuring we stay on topic


***fact***

the target node of this connection is always of the type "fact" and is usually a long string

Examples of this are connections extracted from semi structured text found in wikipedia summarys

These are good candidates for parsing the fact text for a new connection type


***instance of*** and ***sample of***

"dog" node should have "instance of" connection with "animal" node, these connections should always be 100% certain

*sample of *is the reverse, "planet" would have "mars" as *sample of* connection

This is one of the most useful connection types to answer factual questions

"are dogs animals?"
"give me examples of planets"
"what do cats and dogs have in common"




***example*** , ***meaning***, ***part of speech,*** ***synonym *** and ***antonym***

these are "dictionary" connections, *synonym* can be useful to select more nodes during crawling

*example* is a sentence with example usage of source node as a word, it is **NOT** the same as *sample of*



