from lilacs.crawlers import BaseCrawler
import random


class LabelFixerCrawler(BaseCrawler):
    # if node contains both, remove second
    # " if is key can not be item"

    # elon musk -> person, elon musk -> drug
    # remove elon musk -> drug
    removes = {"person": "drug"}

    def choose_next_node(self):
        # pick a random next node
        nodes = [n for n in self.db.get_concepts() if n.name not in self.crawl_list and not n.name.startswith("http")]
        if not len(nodes):
            return None
        next_node = random.choice(nodes)
        print("** next", next_node.name)
        return next_node

    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        # remove empty cons
        for c in self.current_node.out_connections:
            if c.target is None or c.source is None:
                print("removing malformed out connection", c)
                self.current_node.out_connections.remove(c)
                self.db.commit()
        for c in self.current_node.in_connections:
            if c.target is None or c.source is None:
                print("removing malformed in connection", c)
                self.current_node.in_connections.remove(c)
                self.db.commit()

        # references to self person -> person
        if self.con_exists("label", self.current_node.name, self.current_node.name):
            cons = self.current_node.out_connections
            for c in cons:
                if c.target.name == self.current_node.name and c.type == "label":
                    print("removing reference to self ", self.current_node.name)
                    c.target.out_connections.remove(c)
                    self.current_node.in_connections.remove(c)
                    self.db.commit()

        # remove forbidden labels
        for key in self.removes:
            # person -> drug (cant be true)
            if self.current_node.name.lower() == key.lower():
                if self.con_exists("label", self.current_node.name, self.removes[key]):
                    cons = self.current_node.up_relationships
                    for c in cons:
                        if c.target.name == self.removes[key] and c.type == "label":
                            print("** removing forbidden label", self.current_node.name, self.removes[key])
                            self.current_node.out_connections.remove(c)
                            self.db.commit()

        # remove incompatible labels
        for key in self.removes:

            # elon musk -> person, elon musk -> drug
            # remove elon musk -> drug
            if self.con_exists("label", self.current_node.name, key) and self.con_exists("label", self.current_node.name, self.removes[key]):
                cons = self.current_node.out_connections
                for c in cons:
                    if c.target.name == self.removes[key] and c.type == "label":
                        print("** removing incompatible ", self.current_node.name, self.removes[key])
                        self.current_node.out_connections.remove(c)
                        self.db.commit()

        return []


if __name__ == "__main__":
    c = LabelFixerCrawler(threaded=False)
    c.start_crawling("elon musk")
    print(c.crawl_list)
    print(c.total_steps)
