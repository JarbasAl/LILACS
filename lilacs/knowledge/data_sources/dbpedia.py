from __future__ import print_function
from lilacs.settings import SPOTLIGHT_URL
import spotlight
import requests
import sys
import os
import hashlib
import pickle
import re
from SPARQLWrapper import SPARQLWrapper, JSON
from SPARQLWrapper.SPARQLExceptions import QueryBadFormed
from lilacs.knowledge.data_sources.resources import OWL_FILE


class DbpediaOntology(object):
    '''
    This class encapsulates the dbpedia ontology and gives acces to it
    '''

    def __init__(self):
        self.__resource_folder__ = os.path.dirname(os.path.realpath(__file__)) + '/resources'
        self.list_labels = set()  # An unique list of ontology labels
        self.superclass_for_class = {}
        self.__load_subclasses__()
        self.__nsmap = {}  ##mapping of namespaces

    def __get_owl_root_node__(self):
        try:
            from lxml import etree
        except:
            import xml.etree.cElementTree as etree
        owl_file = self.__resource_folder__ + '/' + OWL_FILE
        owl_root = etree.parse(owl_file).getroot()
        self.nsmap = owl_root.nsmap.copy()
        self.nsmap['xmlns'] = self.nsmap.pop(None)
        return owl_root

    def __load_subclasses__(self):
        owl_root = self.__get_owl_root_node__()
        for class_obj in owl_root.findall('{%s}Class' % owl_root.nsmap['owl']):
            onto_label = class_obj.get('{%s}about' % owl_root.nsmap['rdf'])
            self.list_labels.add(onto_label)
            subclass_of_obj = class_obj.find('{%s}subClassOf' % owl_root.nsmap['rdfs'])
            if subclass_of_obj is not None:
                superclass_label = subclass_of_obj.get('{%s}resource' % owl_root.nsmap['rdf'])
                self.superclass_for_class[onto_label] = superclass_label

    def is_leaf_class(self, onto_label):
        """
        Checks if the ontology label provided (for instance http://dbpedia.org/ontology/SportsTeam) is a leaf in the DBpedia ontology tree or not
        It is a leaf if it is not super-class of any other class in the ontology
        @param onto_label: the ontology label
        @type onto_label: string
        @return: whether it is a leaf or not
        @rtype: bool
        """
        is_super_class = False
        for subclass, superclass in list(self.superclass_for_class.items()):
            if superclass == onto_label:
                is_super_class = True
                break
        if not is_super_class and onto_label not in self.list_labels:
            return None

        return not is_super_class

    def get_ontology_path(self, onto_label):
        '''
        Returns the path of ontology classes for the given ontology label (is-a relations)
        @param onto_label: the ontology label (could be http://dbpedia.org/ontology/SportsTeam or just SportsTeam)
        @type onto_label: str
        @return: list of ontology labels
        @rtype: list
        '''
        thing_label = '%sThing' % self.nsmap['owl']
        if onto_label == thing_label:
            return [thing_label]
        else:
            if self.nsmap[
                'xmlns'] not in onto_label:  # To allow things like "SportsTeam instead of http://dbpedia.org/ontology/SportsTeam
                onto_label = self.nsmap['xmlns'] + onto_label

            if onto_label not in self.superclass_for_class:
                return []
            else:
                super_path = self.get_ontology_path(self.superclass_for_class[onto_label])
                super_path.insert(0, onto_label)
                return super_path

    def get_depth(self, onto_label):
        '''
        Returns the depth in the ontology hierarchy for the given ontology label (is-a relations)
        @param onto_label: the ontology label (could be http://dbpedia.org/ontology/SportsTeam or just SportsTeam)
        @type onto_label: str
        @return: depth
        @rtype: int
        '''
        path = self.get_ontology_path(onto_label)
        return len(path)


class DbpediaEnquirer(object):
    """
    This class allows to query dbpedia using the Virtuoso SPARQL endpoint and gives access to different type of information
    """

    def __init__(self, endpoint='http://dbpedia.org/sparql'):
        self.__endpoint__ = endpoint
        self.__thisfolder__ = os.path.dirname(os.path.realpath(__file__))
        self.__cache_folder__ = self.__thisfolder__ + '/.dbpedia_cache'
        self.__dbpedia_ontology__ = DbpediaOntology()

    def __get_name_cached_file(self, query):
        if isinstance(query, str):
            query = query.encode('utf-8')
        cached_file = self.__cache_folder__ + '/' + hashlib.sha256(query).hexdigest()
        return cached_file

    def __get_name_cached_ontology_type(self, dblink):
        if isinstance(dblink, str):
            dblink = dblink.encode('utf-8')
        cached_file = self.__cache_folder__ + '/' + hashlib.sha256(dblink).hexdigest() + '.ontologytype'
        return cached_file

    def __my_query(self, this_query):
        cached_file = self.__get_name_cached_file(this_query)
        if os.path.exists(cached_file):
            fd = open(cached_file, 'rb')
            results = pickle.load(fd)
            fd.close()
        else:
            sparql = SPARQLWrapper(self.__endpoint__)
            sparql.setQuery(this_query)
            sparql.setReturnFormat(JSON)
            query = sparql.query()
            # query.setJSONModule(json)
            results = query.convert()['results']['bindings']
            if not os.path.exists(self.__cache_folder__):
                os.mkdir(self.__cache_folder__)
            fd = open(cached_file, 'wb')
            pickle.dump(results, fd, protocol=-1)
            fd.close()
        return results

    def get_deepest_ontology_class_for_dblink(self, dblink):
        """
        Given a dblink (http://dbpedia.org/resource/Tom_Cruise) gets all the possible ontology classes from dbpedia,
        calculates the depth of each on in the DBpedia ontology and returns the deepest one
        @param dblink: the dbpedia link
        @type dblink: string
        @return: the deespest DBpedia ontology label
        @rtype: string
        """
        deepest = None
        onto_labels = self.get_dbpedia_labels_for_dblink(dblink)
        pair_label_path = []
        for ontolabel in onto_labels:
            this_path = self.__dbpedia_ontology__.get_ontology_path(ontolabel)
            pair_label_path.append((ontolabel, len(this_path)))
        if len(pair_label_path) > 0:
            deepest = sorted(pair_label_path, key=lambda t: -t[1])[0][0]
        return deepest

    def get_all_instances_for_ontology_label(self, ontology_label, log=False):
        """
        Given an ontoloy label (like http://dbpedia.org/ontology/SportsTeam), it will return
        all the entities in DBPEDIA tagged with that label
        @param ontology_label: the ontology label (http://dbpedia.org/ontology/SportsTeam)
        @type ontology_label: str
        @param log: to get log information
        @type log: bool
        @return: list of all dbpedia entities belonging to that ontological type
        @rtype: list
        """

        instances = []
        keep_searching = True
        while keep_searching:
            query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                SELECT ?entity
                WHERE { ?entity rdf:type <%s> }
                LIMIT 10000
                OFFSET %i
                """ % (ontology_label, len(instances))
            # print query
            if log:
                print('Querying dbpedia for', ontology_label, ' OFFSET=', len(instances), file=sys.stderr)

            results = self.__my_query(query)
            if len(results) == 0:
                keep_searching = False
            else:
                for r in results:
                    instances.append(r['entity']['value'])
        return instances

    def query_dbpedia_for_dblink(self, dblink):
        """
        Returns a dictionary with all the triple relations stored in DBPEDIA for the given entity
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: dictionary with triples
        @rtype: dict
        """
        query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?predicate ?object
                WHERE { <%s> ?predicate ?object }
                """ % dblink
        results = self.__my_query(query)
        return results

    def get_wiki_page_url_for_dblink(self, dblink):
        """
        Returns the wikipedia page url for the given DBpedia link (the relation 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf is checked)
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: the wikipedia URL
        @rtype: str
        """

        dbpedia_json = self.query_dbpedia_for_dblink(dblink)
        lang = wikipage = None
        for dictionary in dbpedia_json:
            predicate = dictionary['predicate']['value']
            object = dictionary['object']['value']

            if predicate == 'http://xmlns.com/foaf/0.1/isPrimaryTopicOf':
                wikipage = object
                break

        return wikipage

    def get_wiki_page_id_for_dblink(self, dblink):
        """
        Returns the wikipedia page id for the given DBpedia link (the relation http://dbpedia.org/ontology/wikiPageID is checked)
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: the wikipedia identifier
        @rtype: str
        """

        dbpedia_json = self.query_dbpedia_for_dblink(dblink)
        lang = wikipageid = None
        for dictionary in dbpedia_json:
            predicate = dictionary['predicate']['value']
            object = dictionary['object']['value']

            if predicate == 'http://dbpedia.org/ontology/wikiPageID':
                wikipageid = object
                break

        return wikipageid

    def get_language_for_dblink(self, dblink):
        """
        Returns the language given a DBpedia link (xml:lang predicate)
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: the language (or None if there is no lang)
        @rtype: str
        """
        dbpedia_json = self.query_dbpedia_for_dblink(dblink)
        lang = None
        for dictionary in dbpedia_json:
            if 'xml:lang' in dictionary['object']:
                lang = dictionary['object']['xml:lang']
                break
        return lang

    def get_wordnet_type_for_dblink(self, dblink):
        """
        Returns the wordnet type for the given DBpedia link (the relation http://dbpedia.org/property/wordnet_type is checked)
        It returns the last part of the WN type ((from http://www.w3.org/2006/03/wn/wn20/instances/synset-actor-noun-1 --> synset-actor-noun-1 )
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: the wordnet type
        @rtype: str
        """
        dbpedia_json = self.query_dbpedia_for_dblink(dblink)
        wordnet_type = None
        for dictionary in dbpedia_json:
            predicate = dictionary['predicate']['value']
            object = dictionary['object']['value']

            if predicate == 'http://dbpedia.org/property/wordnet_type':
                wordnet_type = object.split('/')[-1]  # http://www.w3.org/2006/03/wn/wn20/instances/synset-actor-noun-1
                break

        return wordnet_type

    def is_person(self, dblink):
        """
        Returns True if the link has rdf:type dbpedia:Person, False otherwise
        @param dblink" a dbpedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: whether the dblink is a dbpedia person
        @rtype: str
        """
        dbpedia_json = self.query_dbpedia_for_dblink(dblink)
        for dictionary in dbpedia_json:
            predicate = dictionary['predicate']['value']
            object = dictionary['object']['value']

            if predicate == 'rdf:type' and object == 'http://dbpedia.org/ontology/person':
                return True
        return False

    def _fix_link(self, dblink):
        # fix labels to link
        if not dblink.startswith("http"):

            if " " in dblink:
                dblink = dblink.split(" ")
                for idx, d in enumerate(dblink):
                    if not dblink[idx]:
                        continue
                    if dblink[idx][0].islower():
                        dblink[idx] = dblink[idx][0].upper() + dblink[idx][1:]
                dblink = "_".join(dblink)
            elif dblink[0].islower():
                dblink = dblink[0].upper() + dblink[1:]
            dblink = "http://dbpedia.org/resource/" + dblink
        return dblink

    def _fix_object(self, object):
        object = object.split("/")[-1].split(":")[-1].split("?")[0].split("#")[
            -1].replace("Wikicat", "")
        object = self.camel_to_word(object)
        if object:
            while object[-1].isdigit():
                object = object[:-1]
        return object

    def get_dbpedia_labels_for_dblink(self, dblink):
        """
        Returns the DBpedia ontology labels for the given DBpedia link (the type http://www.w3.org/1999/02/22-rdf-syntax-ns#type will be checked
        and only labels containing  http://dbpedia.org/ontology/* will be returned
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: list of ontology labels
        @rtype: list
        """
        ontology_labels = []
        try:
            dblink = self._fix_link(dblink)
            source = dblink.split("/")[-1]
            dbpedia_json = self.query_dbpedia_for_dblink(dblink)

            ontology_labels = [source]
            for dictionary in dbpedia_json:
                predicate = dictionary['predicate']['value']
                if predicate.endswith("#type"):
                    object = self._fix_object(dictionary['object']['value']).lower().replace("_", "")
                    if object and object not in ontology_labels and not object.startswith("q") and not object[1].isdigit():
                        ontology_labels.append(object)
        except QueryBadFormed:
            dblink = dblink.split("/")[-1]
            link = tag(dblink)[0]
            try:
                return self.get_dbpedia_labels_for_dblink(link)
            except:
                pass
        return ontology_labels[1:]

    def get_dbpedia_cons_for_dblink(self, dblink):
        """
        Returns the DBpedia synonyms for the given DBpedia link (the type http://www.w3.org/1999/02/22-rdf-syntax-ns#type will be checked
        and only labels containing  http://dbpedia.org/ontology/* will be returned
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: list of ontology labels
        @rtype: list
        """
        cons = []
        try:
            dblink = self._fix_link(dblink)
            dbpedia_json = self.query_dbpedia_for_dblink(dblink)
            for dictionary in dbpedia_json:
                predicate = dictionary['predicate']['value']
                if predicate.endswith("#birthDate"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("birthday", object))
                elif predicate.endswith("#subject"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("subject of", object))
                elif predicate.endswith("/gender"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("gender", object))
                elif predicate.endswith("/surname"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("surname", object))
                elif predicate.endswith("/knownFor"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("known for", object))
                elif predicate.endswith("/parent"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("parent", object))
                elif predicate.endswith("/relative"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("relative", object))
                elif predicate.endswith("/title"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("title", object))
                elif predicate.endswith("/nationality"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        if "," in object:
                            t = object.split(",")
                            for object in t:
                                cons.append(("nationality", object.strip()))
                        else:
                            cons.append(("nationality", object))
                elif predicate.endswith("/hypernym"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("hypernym", object))
                        cons.append(("instance of", object))
                        cons.append(("label", object))
                elif predicate.endswith("/almaMater"):
                    object = self._fix_object(dictionary['object']['value']).replace("_", "")
                    if object and object not in cons and not object.startswith("Q") and not object[1].isdigit():
                        cons.append(("studied at", object))
        except QueryBadFormed:
            dblink = dblink.split("/")[-1]
            link = tag(dblink)[0]
            try:
                return self.get_dbpedia_cons_for_dblink(link)
            except:
                pass
        return cons

    def get_external_urls_for_dblink(self, dblink):
        """
        Returns the DBpedia synonyms for the given DBpedia link (the type http://www.w3.org/1999/02/22-rdf-syntax-ns#type will be checked
        and only labels containing  http://dbpedia.org/ontology/* will be returned
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: list of ontology labels
        @rtype: list
        """
        cons = []
        try:
            dblink = self._fix_link(dblink)
            dbpedia_json = self.query_dbpedia_for_dblink(dblink)
            for dictionary in dbpedia_json:
                predicate = dictionary['predicate']['value']
                if predicate.endswith("/wikiPageExternalLink"):
                    object = dictionary['object']['value']
                    if object and object not in cons:
                        cons.append(("url", object))
        except QueryBadFormed:
            dblink = dblink.split("/")[-1]
            link = tag(dblink)[0]
            try:
                return self.get_dbpedia_cons_for_dblink(link)
            except:
                pass
        return cons

    def query_dbpedia_for_unique_dblink(self, dblink):
        """
        Perform a check whether a dbpedia resource is unique
        @param dblink: a dbedia link (http://dbpedia.org/resource/Tom_Cruise)
        @type dblink: str
        @return: dictionary with triples
        @rtype: dict
        """
        query = """
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
                SELECT ?predicate ?object
                WHERE { <%s> ?predicate ?object . FILTER NOT EXISTS { <%s> <http://dbpedia.org/ontology/wikiPageDisambiguates> ?o } }
                """ % (dblink, dblink)
        results = self.__my_query(query)
        return results

    def camel_to_word(self, text):
        words = re.findall('[A-Z][^A-Z]*', text)
        return " ".join(words)


def scrap_resource_page(link):
    u = link.replace("http://dbpedia.org/resource/", "http://dbpedia.org/data/") + ".json"
    data = requests.get(u)
    json_data = data.json()
    dbpedia = {}
    dbpedia["related_subjects"] = []
    dbpedia["picture"] = []
    dbpedia["external_links"] = []
    dbpedia["abstract"] = ""
    for j in json_data[link]:
        if "#seeAlso" in j:
            # complimentary nodes
            for entry in json_data[link][j]:
                value = entry["value"].replace("http://dbpedia.org/resource/", "").replace("_", " ").encode("utf8")
                if value not in dbpedia["related_subjects"]:
                    dbpedia["related_subjects"].append(value)
        elif "wikiPageExternalLink" in j:
            # links about this subject
            for entry in json_data[link][j]:
                value = entry["value"].encode("utf8")
                dbpedia["external_links"].append(value)
        elif "subject" in j:
            # relevant nodes
            for entry in json_data[link][j]:
                value = entry["value"].replace("http://dbpedia.org/resource/Category:", "").replace("_", " ").encode(
                    "utf8")
                if value not in dbpedia["related_subjects"]:
                    dbpedia["related_subjects"].append(value)
        elif "abstract" in j:
            # english description
            dbpedia["abstract"] = \
                [abstract['value'] for abstract in json_data[link][j] if abstract['lang'] == 'en'][0].encode("utf8")
        elif "depiction" in j:
            # pictures
            for entry in json_data[link][j]:
                value = entry["value"].encode("utf8")
                dbpedia["picture"].append(value)
        elif "isPrimaryTopicOf" in j:
            # usually original wikipedia link
            for entry in json_data[link][j]:
                value = entry["value"].encode("utf8")
                # dbpedia["primary"].append(value)
        elif "wasDerivedFrom" in j:
            # usually wikipedia link at scrap date
            for entry in json_data[link][j]:
                value = entry["value"].encode("utf8")
                # dbpedia["derived_from"].append(value)
        elif "owl#sameAs" in j:
            # links to dbpedia in other languages
            for entry in json_data[link][j]:
                value = entry["value"].encode("utf8")
                if "resource" in value:
                    # dbpedia["same_as"].append(value)
                    pass

    return dbpedia


def tag(text):
    urls = []
    try:
        annotations = spotlight.annotate(SPOTLIGHT_URL, text)
        for annotation in annotations:
            score = annotation["similarityScore"]
            # entry we are talking about
            subject = annotation["surfaceForm"]
            # print("subject: " + subject)
            offset = annotation["offset"]
            types = annotation["types"].split(",")
            for type in types:
                if type != "":
                    pass
                    # print("parent: " + type)
            # dbpedia link
            url = annotation["URI"]
            # print("link: " + url)
            urls.append(url)
    except spotlight.SpotlightException as e:
        print(e)
    return urls


if __name__ == '__main__':
    my_dbpedia = DbpediaEnquirer()
    ontology = DbpediaOntology()
    query = "Elon Musk"
    #labels = my_dbpedia.get_dbpedia_labels_for_dblink(query)
    #print(labels)
    # for label in labels:
    #    print('Ontological path for', label, ontology.get_ontology_path(label))
    #labels = my_dbpedia.get_dbpedia_cons_for_dblink(query)
    #print(labels)
    labels = my_dbpedia.get_external_urls_for_dblink(query)

