from lilacs.crawlers.dbpedia_crawler import DBpediaBaseCrawler


class LabelCrawler(DBpediaBaseCrawler):
    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        instance_of = self.dbpedia.get_dbpedia_labels_for_dblink(self.current_node.name)
        for con in instance_of:
            c = self.db.add_connection(self.current_node.name, con, "label")
            if c is not None:
                new_cons.append(c)

        cons = self.dbpedia.get_dbpedia_cons_for_dblink(self.current_node.name)
        for c, t in cons:
            c = self.db.add_connection(self.current_node.name, t, c)
            if c is not None:
                new_cons.append(c)

        return new_cons


if __name__ == "__main__":
    c = LabelCrawler(threaded=False)
    c.start_crawling("dog")
    print(c.crawl_list)
    print(c.total_steps)
