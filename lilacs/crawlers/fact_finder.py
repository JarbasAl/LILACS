from lilacs.crawlers.nlp_crawler import NLPCrawler
from lilacs.data_sources.wikipedia import get_wikipedia
from lilacs.nlp.parse import extract_facts
import random


class FactFinderCrawler(NLPCrawler):
    def choose_next_node(self, connections):
        # pick a random next node
        nodes = [n for n in self.db.get_concepts() if n.name not in self.crawl_list and not n.name.startswith("http") and not n.type == "fact"]
        if not len(nodes):
            return None
        next_node = random.choice(nodes)
        print("** next", next_node.name)
        return next_node

    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        summary = get_wikipedia(self.current_node.name).get("summary")
        if summary:
            facts = extract_facts(self.current_node.name, summary, nlp=self.nlp, coref_nlp=self.coref_nlp)
            for fact in facts:
                print("new fact about ", self.current_node.name, ":", fact)
                fact = str(fact)
                c = self.db.search_concept_by_name(fact)
                if not c:

                    c = self.db.add_concept(fact, type="fact", description="fact about " + self.current_node.name)
                    c = self.db.add_connection(self.current_node.name, c.name, "fact")
                    if c is not None:
                        new_cons.append(c)
        return new_cons


if __name__ == "__main__":
    c = FactFinderCrawler(threaded=False)
    c.start_crawling("elon musk")
    print(c.crawl_list)
    print(c.total_steps)
