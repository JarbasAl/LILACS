# LILACS - nervous system

Where do the internal signals flow? in a messagebus!

different parts of LILACS talk to each other via websocker

# message list

TODO

# Crawlers

With so much data available, we need to have some strategies to maintain it and access the relevant one 

Lets have a bunch of crawlers each with some strategy to perform a certain action


- url finder -> search dbpedia, extract and create "link" concepts/connections
- fact finder -> search wikipedia, extracts semi structured facts from text, create "fact" concepts/connections
- label finder -> search dbpedia, extract and create "label" concepts/connections
- maintenace -> removes malformed connections, references to self, and removes some invalid connections (you can not be labeled "drug" and "person" at same time)
- connection finder -> search conceptnet/wordnet/dictionary

# making a crawler


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
                
# running a crawler

    c = URLCrawler(threaded=False)
    c.start_crawling()  # or you can pass a start node in the args
    print(c.crawl_list)
    print(c.total_steps)
    

# output
    
    ** current elon musk
    ** new cons [23: 24->25, 24: 24->26, 25: 24->27, 26: 24->28, 27: 24->29, 28: 24->30, 29: 24->31, 30: 24->32, 31: 24->33, 32: 24->34, 33: 24->35, 34: 24->36, 35: 24->37, 36: 24->38, 37: 24->39, 38: 24->40, 39: 24->41, 40: 24->42, 41: 24->43]
    ** next demons in christianity
    ** current demons in christianity
    ** new cons []
    ** next a symbol of virtuous characteristics and liberty
    ** current a symbol of virtuous characteristics and liberty
    ** new cons []
    ** next belief
    ** current belief
    ** new cons [42: 8->44, 43: 8->45, 44: 8->46]
    ** next person
    ** current person
    ** new cons [45: 3->47, 46: 3->48]
    ** next satan
    ** current satan
    ** new cons [47: 1->49, 48: 1->50, 49: 1->51, 50: 1->52, 51: 1->53, 52: 1->54, 53: 1->55, 54: 1->56, 55: 1->57, 56: 1->58, 57: 1->59, 58: 1->60, 59: 1->61, 60: 1->62, 61: 1->63, 62: 1->64, 63: 1->65, 64: 1->66, 65: 1->67]
    ** next demons
    ** current demons
    ** new cons []
    ** next cognition
    ** current cognition
    ** new cons [66: 9->68, 67: 9->69, 68: 9->70, 69: 9->71, 70: 9->72, 71: 9->73, 72: 9->74, 73: 9->75]
    ** next evil spirit
    
    (...)
    
    ** dead end!
    ['elon musk', 'demons in christianity', 'a symbol of virtuous characteristics and liberty', 'belief', 'person', 'satan', 'demons', 'an important aspect of mundane life, according to eric schwitzgebel in the _stanford encyclopedia of philosophy', 'cognition', 'evil spirit', 'devil', 'angels', 'angel', 'psychological feature', 'Figure', 'fallen angels', 'an entity in the abrahamic religions that seduces humans into sin', 'abstraction', 'individual angels', 'spiritual being', 'the personification and archetype of evil in various cultures', 'content', 'thing', 'spirit']
    24