from lilacs.knowledge.crawlers import BaseCrawler
#from lilacs.memory.data_sources.reddit_hivemind import get_similar


class RelatedCrawler(BaseCrawler):
    def execute_action(self, connections):
        print("** current", self.current_node.name)
        # execute an action in current node
        new_cons = []
        cons = {}#get_similar(self.current_node.name)
        for con in cons.get("results"):
            c = self.db.add_connection(self.current_node.name, con["text"], strength=con["score"]*100)
            if c is not None:
                new_cons.append(c)

        return new_cons


if __name__ == "__main__":
    c = RelatedCrawler(threaded=False)
    c.start_crawling()
    print(c.crawl_list)
    print(c.total_steps)
