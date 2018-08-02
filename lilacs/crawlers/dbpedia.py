from lilacs.crawlers import BaseCrawler
import random

from lilacs.data_sources.dbpedia import DbpediaEnquirer, DbpediaOntology
from lilacs.nodes import Concept


class DBpediaBaseCrawler(BaseCrawler):
    dbpedia = DbpediaEnquirer()
    ontology = DbpediaOntology()

    def select_connections(self):
        # select relevant connections from current node
        up = self.current_node.out_connections
        return up

    def choose_next_node(self):
        # pick the next node, ignore htp links
        try:
            cons = [c for c in self.current_node.out_connections if c.type == "label"]
            nodes = [c.source for c in cons if c.source.name != self.current_node.name and c.source.name not in self.crawl_list and not c.source.name.startswith("http")]
            if not len(nodes):
                # go back to previous node
                print("** no next node, going back to start")
                possible_nodes = [con.target for con in self.start_node.out_connections if con.target.name not in self.crawl_list and not con.target.name.startswith("http")]
                if len(possible_nodes):
                    return random.choice(possible_nodes)
                return None
            next_node = random.choice(nodes)
            print("** next", next_node.name)
            return next_node
        except Exception as e:
            print("** error", e)
        return None

    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        instance_of = self.dbpedia.get_dbpedia_labels_for_dblink(self.current_node.name)
        for con in instance_of:
            if not self.con_exists("label", self.current_node.name, con):
                new_node = self.db.add_concept(con)
                if new_node is None:
                    new_node = self.db.first_concept_by_name(con)
                c = self.db.add_connection_by_id(self.current_node.id, new_node.name, "label")
                new_cons.append(c)

        cons = self.dbpedia.get_dbpedia_cons_for_dblink(self.current_node.name)
        for c, t in cons:
            c = self.db.add_connection_by_id(self.current_node.id, t, c)
            new_cons.append(c)
        print("** new cons", [(c.type, c.target_concept[0].name) for c in new_cons])
        return [c for c in new_cons if c is not None]

    def default_node(self, start_node=None):
        if isinstance(start_node, str):
            nodes = self.db.search_concept_by_name(start_node)
            if len(nodes):
                return nodes[0]
            start_node = self.db.add_concept(start_node)
            if start_node:
                return start_node
            else:
                self.stop_crawling()
        elif isinstance(start_node, Concept):
            return start_node
        return None

    def on_dead_end(self):
        # crawling reached a node with no connections
        print("** dead end!")
        self.stop_crawling()


if __name__ == "__main__":
    c = DBpediaBaseCrawler(threaded=False)
    c.start_crawling("elon musk")
    print(c.crawl_list)
    print(c.total_steps)
