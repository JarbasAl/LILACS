from lilacs.knowledge.data_sources.dbpedia_api import dbpedia_keyword_api, dbpedia_prefix_api

from pprint import pprint


class LILACSKnowledge(object):
    def __init__(self, bus=None):
        self.bus = bus

    def dbpedia_thing(self, keyword):
        return dbpedia_keyword_api(keyword)

    def dbpedia_place(self, keyword):
        return dbpedia_keyword_api(keyword, "place")

    def dbpedia_species(self, keyword):
        return dbpedia_keyword_api(keyword, "species")

    def dbpedia_person(self, keyword):
        return dbpedia_keyword_api(keyword, "person")

    def dbpedia_organisation(self, keyword):
        return dbpedia_keyword_api(keyword, "organization")

    def dbpedia_work(self, keyword):
        return dbpedia_keyword_api(keyword, "work")

    def dbpedia_class(self, keyword, dbpedia_class):
        return dbpedia_keyword_api(keyword, dbpedia_class)

    def dbpedia_prefix(self, keyword):
        return dbpedia_prefix_api(keyword)

    def dbpedia_sparql(self, query):
        pass


if __name__ == "__main__":
    LILACS = LILACSKnowledge()
    concept = "dog"
    #pprint(LILACS.dbpedia_species(concept)[0])
    """
    {'categories': [{'label': 'Scavengers',
                     'uri': 'http://dbpedia.org/resource/Category:Scavengers'},
                    {'label': 'Cosmopolitan species',
                     'uri': 'http://dbpedia.org/resource/Category:Cosmopolitan_species'},
                    {'label': 'Dogs',
                     'uri': 'http://dbpedia.org/resource/Category:Dogs'},
                    {'label': 'Sequenced genomes',
                     'uri': 'http://dbpedia.org/resource/Category:Sequenced_genomes'}],
     'classes': [{'label': 'mammal', 'uri': 'http://dbpedia.org/ontology/Mammal'},
                 {'label': 'owl#Thing',
                  'uri': 'http://www.w3.org/2002/07/owl#Thing'},
                 {'label': 'animal', 'uri': 'http://dbpedia.org/ontology/Animal'},
                 {'label': 'species', 'uri': 'http://dbpedia.org/ontology/Species'},
                 {'label': 'eukaryote',
                  'uri': 'http://dbpedia.org/ontology/Eukaryote'}],
     'description': 'The domestic dog (Canis lupus familiaris), is a subspecies of '
                    'the gray wolf (Canis lupus), a member of the Canidae family '
                    'of the mammilian order Carnivora. The term "domestic dog" is '
                    'generally used for both domesticated and feral varieties. The '
                    'dog may have been the first animal to be domesticated, and '
                    'has been the most widely kept working, hunting, and companion '
                    'animal in human history.',
     'label': 'Dog',
     'redirects': [],
     'refCount': 2684,
     'templates': [],
     'uri': 'http://dbpedia.org/resource/Dog'}
    """
    #assert LILACS.dbpedia_prefix(concept)[0] == LILACS.dbpedia_species(concept)[0]
    #assert LILACS.dbpedia_thing(concept)[0] == LILACS.dbpedia_species(concept)[0]
    #pprint(LILACS.dbpedia_person(concept)[0])
    """
    {'categories': [{'label': 'People self-identifying as substance abusers',
                 'uri': 'http://dbpedia.org/resource/Category:People_self-identifying_as_substance_abusers'},
                {'label': 'Rappers from Los Angeles, California',
                 'uri': 'http://dbpedia.org/resource/Category:Rappers_from_Los_Angeles,_California'},
                {'label': 'American film producers',
                 'uri': 'http://dbpedia.org/resource/Category:American_film_producers'},
                {'label': 'People acquitted of murder',
                 'uri': 'http://dbpedia.org/resource/Category:People_acquitted_of_murder'},
                {'label': 'Crips',
                 'uri': 'http://dbpedia.org/resource/Category:Crips'},
                {'label': 'Participants in American reality television series',
                 'uri': 'http://dbpedia.org/resource/Category:Participants_in_American_reality_television_series'},
                {'label': 'Actors from Los Angeles, California',
                 'uri': 'http://dbpedia.org/resource/Category:Actors_from_Los_Angeles,_California'},
                {'label': 'African-American television actors',
                 'uri': 'http://dbpedia.org/resource/Category:African-American_television_actors'},
                {'label': 'Priority Records artists',
                 'uri': 'http://dbpedia.org/resource/Category:Priority_Records_artists'},
                {'label': 'Living people',
                 'uri': 'http://dbpedia.org/resource/Category:Living_people'},
                {'label': 'No Limit Records artists',
                 'uri': 'http://dbpedia.org/resource/Category:No_Limit_Records_artists'},
                {'label': 'Snoop Dogg',
                 'uri': 'http://dbpedia.org/resource/Category:Snoop_Dogg'},
                {'label': 'American cannabis activists',
                 'uri': 'http://dbpedia.org/resource/Category:American_cannabis_activists'},
                {'label': 'American music industry executives',
                 'uri': 'http://dbpedia.org/resource/Category:American_music_industry_executives'},
                {'label': 'G-funk',
                 'uri': 'http://dbpedia.org/resource/Category:G-funk'},
                {'label': 'Hip hop record producers',
                 'uri': 'http://dbpedia.org/resource/Category:Hip_hop_record_producers'},
                {'label': 'Hip hop activists',
                 'uri': 'http://dbpedia.org/resource/Category:Hip_hop_activists'},
                {'label': 'West Coast hip hop musicians',
                 'uri': 'http://dbpedia.org/resource/Category:West_Coast_hip_hop_musicians'},
                {'label': 'African-American film actors',
                 'uri': 'http://dbpedia.org/resource/Category:African-American_film_actors'},
                {'label': 'American hip hop record producers',
                 'uri': 'http://dbpedia.org/resource/Category:American_hip_hop_record_producers'},
                {'label': 'Hip hop singers',
                 'uri': 'http://dbpedia.org/resource/Category:Hip_hop_singers'},
                {'label': 'African American record producers',
                 'uri': 'http://dbpedia.org/resource/Category:African_American_record_producers'},
                {'label': 'African American rappers',
                 'uri': 'http://dbpedia.org/resource/Category:African_American_rappers'},
                {'label': 'American music video directors',
                 'uri': 'http://dbpedia.org/resource/Category:American_music_video_directors'},
                {'label': 'People convicted of drug offenses',
                 'uri': 'http://dbpedia.org/resource/Category:People_convicted_of_drug_offenses'},
                {'label': 'Members of the Nation of Islam',
                 'uri': 'http://dbpedia.org/resource/Category:Members_of_the_Nation_of_Islam'},
                {'label': 'Death Row Records artists',
                 'uri': 'http://dbpedia.org/resource/Category:Death_Row_Records_artists'},
                {'label': 'Pseudonymous rappers',
                 'uri': 'http://dbpedia.org/resource/Category:Pseudonymous_rappers'},
                {'label': 'American voice actors',
                 'uri': 'http://dbpedia.org/resource/Category:American_voice_actors'},
                {'label': 'American people of Native American descent',
                 'uri': 'http://dbpedia.org/resource/Category:American_people_of_Native_American_descent'},
                {'label': 'People from Long Beach, California',
                 'uri': 'http://dbpedia.org/resource/Category:People_from_Long_Beach,_California'},
                {'label': '1971 births',
                 'uri': 'http://dbpedia.org/resource/Category:1971_births'}],
     'classes': [{'label': 'owl#Thing',
                  'uri': 'http://www.w3.org/2002/07/owl#Thing'},
                 {'label': 'person', 'uri': 'http://dbpedia.org/ontology/Person'},
                 {'label': 'artist', 'uri': 'http://dbpedia.org/ontology/Artist'},
                 {'label': 'musical artist',
                  'uri': 'http://dbpedia.org/ontology/MusicalArtist'},
                 {'label': 'music group', 'uri': 'http://schema.org/MusicGroup'},
                 {'label': 'person', 'uri': 'http://schema.org/Person'},
                 {'label': 'http://xmlns.com/foaf/0.1/ person',
                  'uri': 'http://xmlns.com/foaf/0.1/Person'},
                 {'label': 'agent', 'uri': 'http://dbpedia.org/ontology/Agent'}],
     'description': 'Calvin Cordozar Broadus, Jr. (born October 20, 1971), better '
                    'known by his stage name Snoop Dogg (formerly known as Snoop '
                    'Doggy Dogg), is an American rapper, record producer, and '
                    'actor. Snoop is best known as a rapper in the West Coast hip '
                    "hop scene, and for being one of Dr. Dre's most notable "
                    'protégés. Snoop Dogg was a Crip gang member while in high '
                    'school. Shortly after graduation, he was arrested for cocaine '
                    'possession and spent six months in Wayside County Jail.',
     'label': 'Snoop Dogg',
     'redirects': [],
     'refCount': 1689,
     'templates': [],
     'uri': 'http://dbpedia.org/resource/Snoop_Dogg'}
    """