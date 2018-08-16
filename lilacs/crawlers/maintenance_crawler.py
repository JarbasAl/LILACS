from lilacs.crawlers import BaseCrawler
import random


class MaintenanceCrawler(BaseCrawler):
    # if node contains both, remove second
    # " if is key can not be item"

    # elon musk -> person, elon musk -> drug
    # remove elon musk -> drug
    removes = {"person": "drug"}

    def fix_types(self):
        if self.current_node.name.startswith("http") and not self.current_node.type == "link":
            print("fixing type", self.current_node.name, self.current_node.type, "-> link")
            self.current_node.type = "link"
            self.db.commit()
        else:
            ents = [("person", "person"),
                    ("agent","entity"),
                    ("thing", "thing")]
            for (l, t) in ents:
                for con in self.current_node.out_connections:
                    if con.type == "label":
                        if con.target.name == l and not self.current_node.type == t:

                            print("fixing type", self.current_node.name, self.current_node.type, "->", t)
                            self.current_node.type = t
                            self.db.commit()
                            return

    def fix_empty_cons(self):
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

    def fix_references_to_self(self):
        # references to self person -> person
        types = ["label", "instance of"]
        for t in types:
            if self.con_exists(t, self.current_node.name, self.current_node.name):
                cons = self.current_node.out_connections
                for c in cons:
                    if c.target.name == self.current_node.name and c.type == t:
                        print("removing reference to self ", self.current_node.name)
                        c.target.out_connections.remove(c)
                        self.current_node.in_connections.remove(c)
                        self.db.commit()

    def fix_incompatible_labels(self):
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

    def expand_synonyms(self):
        # synonyms and antonyms should be bidirectional
        pass

    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        self.fix_types()
        self.fix_empty_cons()
        self.fix_references_to_self()
        self.fix_incompatible_labels()
        self.expand_synonyms()
        return []


if __name__ == "__main__":
    c = MaintenanceCrawler(threaded=False)
    c.start_crawling("elon musk")
    print(c.crawl_list)
    print(c.total_steps)
