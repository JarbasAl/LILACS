from lilacs.crawlers.dbpedia import DBpediaBaseCrawler

import random


class URLCrawler(DBpediaBaseCrawler):
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
        new_cons = []
        urls = self.dbpedia.get_external_urls_for_dblink(self.current_node.name)
        for con in urls:
            url = con[1]
            if not self.con_exists("link", self.current_node.name, url):
                c = self.db.add_connection_by_id(self.current_node.id, url, "link")
                if c is not None:
                    new_cons.append(c)
        return new_cons


if __name__ == "__main__":
    c = URLCrawler(threaded=False)
    c.start_crawling("elon musk")
    print(c.crawl_list)
    print(c.total_steps)
