from lilacs.memory.data_sources import LILACSKnowledge
from lilacs.processing import LILACSTextAnalyzer
from lilacs.processing.crawlers import DummyCrawler


class RelationCruncher(DummyCrawler):
    analyzer = LILACSTextAnalyzer()
    knowledge = LILACSKnowledge()

    def execute_action(self, connections):
        print("\n** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        node_data = self.knowledge.dbpedia_thing(self.current_node.name)
        if not len(node_data):
            print("no dbpedia results")
            return []
        node_data = node_data[0]
        label = node_data["label"]
        if label.lower() != self.current_node.name.lower():
            #print("dbpedia label does not match node name, synonym proposal")
            print("** triple:", (self.current_node.name, "same as", label))
        description = node_data["description"]
        description = self.analyzer.coreference_resolution(description)
        triples = self.analyzer.possible_relations(description.split("."))
        for t in triples:
            print("** triple:", t)
        #facts = self.analyzer.extract_facts(label, description)
        #print("** facts:", facts)
        new_nodes = self.analyzer.extract_nouns(description)
        print("** new nodes:", new_nodes)
        self.more_nodes += [str(n).strip() for n in new_nodes if str(n).strip() not in self.crawl_list]
        return new_cons


class RelationshipCruncher(DummyCrawler):
    analyzer = LILACSTextAnalyzer()
    knowledge = LILACSKnowledge()

    def execute_action(self, connections):
        print("\n** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        node_data = self.knowledge.dbpedia_thing(self.current_node.name)
        if not len(node_data):
            print("no dbpedia results")
            return []
        node_data = node_data[0]
        label = node_data["label"]
        if label.lower() != self.current_node.name.lower():
            #print("dbpedia label does not match node name, synonym proposal")
            print("** triple:", (self.current_node.name, "same as", label))
        description = node_data["description"]
        description = self.analyzer.normalize(description)
        triples = self.analyzer.interesting_triples(description)
        for t in triples:
            print("** triple:", t)
        #facts = self.analyzer.extract_facts(label, description)
        #print("** facts:", facts)
        new_nodes = self.analyzer.extract_nouns(description)
        #print("** new nodes:", new_nodes)
        self.more_nodes += new_nodes
        return new_cons



if __name__ == "__main__":
    c = RelationCruncher(threaded=False)
    c.start_crawling("god")
    print(c.crawl_list)
    print(c.total_steps)
