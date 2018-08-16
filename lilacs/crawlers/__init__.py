from lilacs.nodes.concept import ConceptDatabase
from threading import Thread
import random


class BaseCrawler(object):
    def __init__(self, db=None, max_crawl=200, threaded=True, debug=False):
        self.db = db or ConceptDatabase(debug=debug)
        self.crawl_list = []
        self.con_list = []
        self.new_cons = []
        self.crawling = False
        self.current_node = None
        self.start_node = None
        self.last_node = None
        self.total_steps = 0
        self.steps = 0
        self.threaded = threaded
        self.max_crawl = max_crawl
        self.crawl_thread = None

    def con_exists(self, con_type, con_source, con_target):
        con = self.db.search_connection_by_type(con_type)
        for c in con:
            if c.target is None or c.source is None:
                print("deleting a malformed connection", c)
                self.db.session.delete(c)
                continue
            if c.target.name == con_source and c.source.name == con_target:
                return True
        return False

    def _crawl_loop(self):
        while self.crawling:
            self.crawl_one()
        self.stop_crawling()

    def select_connections(self):
        # select relevant connections from current node
        out = self.current_node.out_connections
        return out

    def choose_next_node(self, connections):
        # pick a random next node
        nodes = [n for n in self.db.get_concepts()
                 if n and n.name and n.name not in self.crawl_list
                 and not n.type in ["link", "example", "meaning", "fact"]
                 and not n.name.startswith("http")
                 and len(n.name) < 20]
        if not len(nodes):
            return None
        next_node = random.choice(nodes)
        print("** next", next_node.name)
        return next_node

    def execute_action(self, connections):
        # execute an action in current node with selected connections
        print("current", self.current_node.name)
        # return newly made connections
        new_cons = []
        return new_cons

    def crawl_one(self):
        # check for end of crawl
        if self.max_crawl > 0 and self.steps > self.max_crawl:
            self.stop_crawling()
            return

        # process this node and prepare next one
        self.steps += 1
        self.total_steps += 1
        self.crawl_list.append(self.current_node.name)

        cons = self.select_connections()
        self.new_cons = self.execute_action(cons)
        print("** new cons", str(self.new_cons))
        self.con_list.extend(self.new_cons)
        next_node = self.choose_next_node(cons)
        if next_node:
            self.last_node = self.current_node
            self.current_node = next_node
        else:
            self.on_dead_end()

    def on_dead_end(self):
        # crawling reached a node with no connections
        self.stop_crawling()

    def default_node(self, start_node=None):
        return self.choose_next_node(None)

    def start_crawling(self, start_node=None):
        if start_node is None or isinstance(start_node, str):
            start_node = self.default_node(start_node)
            if not start_node:
                self.stop_crawling()
                return
        self.start_node = start_node
        # start crawling process in start_node
        if self.crawling:
            self.stop_crawling()
        self.current_node = start_node
        if self.current_node:
            self.crawling = True
            if self.threaded:
                self.crawl_thread = Thread(target=self._crawl_loop)
                self.crawl_thread.setDaemon(True)
                self.crawl_thread.start()
            else:
                self._crawl_loop()

    def stop_crawling(self):
        # stop the current crawling process
        self.crawling = False
        self.last_node = self.current_node
        self.current_node = None
        self.crawl_thread = None
        self.steps = 0

