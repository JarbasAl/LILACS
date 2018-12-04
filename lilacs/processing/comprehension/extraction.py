import requests
from lilacs.util.parse import extract_datetime, extract_number
from lilacs.processing.comprehension.NER import spacy_NER_demo, spacy_NER, \
    FOX_NER, allennlp_NER_demo, polyglot_NER, polyglot_NER_demo
import geocoder
import spotlight
import datetime
from lilacs.settings import SPOTLIGHT_URL
from pprint import pprint


# use the source https://cogcomp.org/page/demo_view/Wikifier
# demo down
def wikifier(text):
    url = "https://cogcomp.org/demo_files/Wikifier.php"
    data = {"lang": "en", "text": text}
    r = requests.post(url, data=data)
    return r.json()


def spotlight_annotate(text):
    return spotlight.annotate(SPOTLIGHT_URL, text)


def dandelion_annotate(text):
    from lilacs.settings import DANDELION_API
    from dandelion import DataTXT
    datatxt = DataTXT(app_id=DANDELION_API, app_key=DANDELION_API)
    response = datatxt.nex(text)
    return response.annotations


def location_extraction(text):
    ents = spacy_NER_demo(text)
    locations = []
    if not (len(ents)):
        ents = [(text, "?")]
    searched = []
    for ent, ent_type in ents:
        if ent_type not in ["person", "location", "?",
                            "gpe"] or ent.lower() in searched:
            continue
        searched.append(ent.lower())
        location_data = geocoder.geonames(ent, method='details', key='jarbas')
        if not location_data.ok:
            location_data = geocoder.osm(ent)
        if not location_data.ok:
            location_data = geocoder.google(ent)
        if not location_data.ok:
            location_data = geocoder.geocodefarm(ent)

        # just making it slow
        # if not location_data.ok:
        #    location_data = geocoder.arcgis(ent)
        # if not location_data.ok:
        #    location_data = geocoder.bing(ent)
        # if not location_data.ok:
        #    location_data = geocoder.canadapost(ent)
        # if not location_data.ok:
        #    location_data = geocoder.yandex(ent)
        # if not location_data.ok:
        #    location_data = geocoder.tgos(ent)

        # api key required
        # if not location_data.ok:
        #    location_data = geocoder.baidu(ent)
        # if not location_data.ok:
        #    location_data = geocoder.gaode(ent)
        # if not location_data.ok:
        #    location_data = geocoder.locationiq(ent)
        # if not location_data.ok:
        #    location_data = geocoder.mapbox(ent)
        # if not location_data.ok:
        #    location_data = geocoder.mapquest(ent)
        # if not location_data.ok:
        #    location_data = geocoder.maxmind(ent)
        # if not location_data.ok:
        #    location_data = geocoder.opencage(ent)
        # if not location_data.ok:
        #    location_data = geocoder.tamu(ent)
        # if not location_data.ok:
        #    location_data = geocoder.tomtom(ent)
        # if not location_data.ok:
        #    location_data = geocoder.w3w(ent)

        if location_data.ok:
            locations.append(location_data.json)
    return locations


# location_extraction("Where is Chiang Mai?")


def date_extraction(text):
    from epitator.annotator import AnnoDoc
    from epitator.date_annotator import DateAnnotator
    doc = AnnoDoc(text)
    doc.add_tiers(DateAnnotator())
    annotations = doc.tiers["dates"].spans
    if len(annotations):
        return [a.metadata["datetime_range"] for a in annotations]
    return []


# pprint(date_extraction("From March 5 until April 7 1988"))


def count_extraction(text):
    from epitator.annotator import AnnoDoc
    from epitator.count_annotator import CountAnnotator
    doc = AnnoDoc(text)
    doc.add_tiers(CountAnnotator())
    annotations = doc.tiers["counts"].spans
    return annotations


# use the source
# https://github.com/UKPLab/emnlp2017-relation-extraction
def relation_extraction(text):
    # DO NOT ABUSE, dev purposes only
    url = "http://semanticparsing.ukp.informatik.tu-darmstadt.de:5000/relation-extraction/parse/"
    relations = []
    try:
        data = requests.post(url, json={"inputtext": text}).json()
        data = data["relation_graph"]
        if data:
            tokens = data["tokens"]

            for edge in data["edgeSet"]:
                source = []
                target = []
                for i in edge["left"]:
                    source.append(tokens[i])
                for i in edge["right"]:
                    target.append(tokens[i])
                source = " ".join(source)
                target = " ".join(target)
                relation = edge["lexicalInput"]
                relations.append((source, relation, target))
    except:
        pass
    return relations


class LILACSextractor(object):
    nlp = None

    def __init__(self, bus=None, nlp=None):
        self.bus = bus
        if LILACSextractor.nlp is None and nlp is not None:
            LILACSextractor.nlp = nlp

    @staticmethod
    def extract_location(text):
        return location_extraction(text)

    @staticmethod
    def extract_date(text, current_date=None):
        if current_date is None:
            current_date = datetime.datetime.now()
        return extract_datetime(text, current_date)

    @staticmethod
    def extract_date_range(text):
        return date_extraction(text)

    @staticmethod
    def extract_count(text):
        return count_extraction(text)

    @staticmethod
    def extract_number(text):
        return extract_number(text)

    @staticmethod
    def extract_relations(text):
        return relation_extraction(text)

    @staticmethod
    def extract_entities(text, engine="spacy_demo"):
        from lilacs.processing import LILACSTextAnalyzer
        text = LILACSTextAnalyzer.coreference_resolution(text)
        if engine == "spacy_demo":
            return spacy_NER_demo(text)
        elif engine == "fox":
            return FOX_NER(text)
        elif engine == "polyglot_demo":
            return polyglot_NER_demo(text)
        elif engine == "polyglot":
            return polyglot_NER(text)
        elif engine == "allennlp_demo":
            return allennlp_NER_demo(text)
        return spacy_NER(text, LILACSextractor.nlp)

    @staticmethod
    def annotate(text, engine="spotlight"):
        if engine == "spotlight":
            return LILACSextractor.spotlight_annotate(text)
        return LILACSextractor.dandelion_annotate(text)

    @staticmethod
    def spotlight_annotate(text):
        return spotlight_annotate(text)

    @staticmethod
    def dandelion_annotate(text):
        return dandelion_annotate(text)


if __name__ == "__main__":
    from pprint import pprint

    LILACS = LILACSextractor()

    assert LILACS.extract_number("it's over nine thousand") == 9000

    now = datetime.datetime.now()
    # print(now)
    # pprint(LILACS.extract_date("tomorrow i will finish LILACS", now))
    # output
    # 2018-09-11 01:55:07.639843
    # [datetime.datetime(2018, 9, 12, 0, 0), 'i will finish lilacs']

    assert LILACS.extract_date_range("From March 5 until April 7 1988") == [
        [datetime.datetime(1988, 3, 5, 0, 0),
         datetime.datetime(1988, 4, 8, 0, 0)]]

    test_text = """London is the capital and most populous city of England and the United Kingdom.
    Standing on the River Thames in the south east of the island of Great Britain, London has been a major settlement for 2 millennia.
    It was founded by the Romans, who named it Londinium. London's ancient core, the City of London, which covers an area of only 1.12 square miles (2.9 km2), largely retains its medieval boundaries. Since at least the 19th century, "London" has also referred to the metropolis around this core, historically split between Middlesex, Essex, Surrey, Kent and Hertfordshire, which today largely makes up Greater London, a region governed by the Mayor of London and the London Assembly."""

    # entities = LILACS.extract_entities(test_text)
    # pprint(entities)
    # output
    # [('London', 'gpe'),
    #  ('England', 'gpe'),
    #  ('the United Kingdom', 'gpe'),
    #  ('the River Thames', 'fac'),
    #  ('Great Britain', 'gpe'),
    #  ('London', 'gpe'),
    #  ('two millennia', 'date'),
    #  ('Romans', 'norp'),
    #  ('Romans', 'norp'),
    #  ('Londinium', 'gpe'),
    #  ('London', 'gpe'),
    #  ('the City of London', 'gpe'),
    #  ('only 1.12 square miles', 'quantity'),
    #  ('2.9 km2', 'quantity'),
    #  ('at least the 19th century', 'date'),
    #  ('London', 'gpe'),
    #  ('Middlesex', 'gpe'),
    #  ('Essex', 'gpe'),
    #  ('Surrey', 'gpe'),
    #  ('Kent', 'gpe'),
    #  ('Hertfordshire', 'gpe'),
    #  ('today', 'date'),
    #  ('Greater London', 'loc'),
    #  ('London', 'gpe'),
    #  ('the London Assembly', 'org')]

    # relations = LILACS.extract_relations(test_text)
    # pprint(relations)
    # output
    # [('London', 'ALL_ZERO', 'England'),
    #  ('London', 'country', 'United Kingdom'),
    #  ('London', 'instance of', 'capital'),
    #  ('London', 'instance of', 'populous city'),
    #  ('England', 'ALL_ZERO', 'United Kingdom'),
    #  ('England', 'instance of', 'capital'),
    #  ('England', 'instance of', 'populous city'),
    #  ('United Kingdom', 'ALL_ZERO', 'capital'),
    #  ('United Kingdom', 'ALL_ZERO', 'populous city'),
    #  ('capital', 'ALL_ZERO', 'populous city')]

    # locations = LILACSextractor.extract_location(test_text)
    # pprint(locations)
    # output
    # [{'accuracy': 0.975489576540198,
    #   'address': 'London, Greater London, England, SW1A 2DU, UK',
    #   'bbox': {'northeast': [51.6673219, 0.0323526],
    #            'southwest': [51.3473219, -0.2876474]},
    #   'city': 'London',
    #   'confidence': 1,
    #   'country': 'UK',
    #   'country_code': 'gb',
    #   'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
    #   'importance': 0.975489576540198,
    #   'lat': 51.5073219,
    #   'lng': -0.1276474,
    #   'ok': True,
    #   'osm_id': '107775',
    #   'osm_type': 'node',
    #   'place_id': '100145',
    #   'place_rank': '15',
    #   'postal': 'SW1A 2DU',
    #   'quality': 'city',
    #   'raw': {'address': {'city': 'London',
    #                       'country': 'UK',
    #                       'country_code': 'gb',
    #                       'postcode': 'SW1A 2DU',
    #                       'state': 'England',
    #                       'state_district': 'Greater London'},
    #           'boundingbox': ['51.3473219',
    #                           '51.6673219',
    #                           '-0.2876474',
    #                           '0.0323526'],
    #           'category': 'place',
    #           'display_name': 'London, Greater London, England, SW1A 2DU, UK',
    #           'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
    #           'importance': 0.975489576540198,
    #           'lat': '51.5073219',
    #           'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
    #                      'https://osm.org/copyright',
    #           'lon': '-0.1276474',
    #           'osm_id': '107775',
    #           'osm_type': 'node',
    #           'place_id': '100145',
    #           'place_rank': '15',
    #           'type': 'city'},
    #   'region': 'England',
    #   'state': 'England',
    #   'status': 'OK',
    #   'type': 'city'},
    #  {'accuracy': 0.993048074613031,
    #   'address': 'England, UK',

    #   ...

    #  {'accuracy': 0.879660058396959,
    #   'address': 'City of London, London, Greater London, England, EC2V 5AE, UK',
    #   'bbox': {'northeast': [51.6756177, 0.0680017],
    #            'southwest': [51.3556177, -0.2519983]},
    #   'city': 'City of London',
    #   'confidence': 1,
    #   'country': 'UK',
    #   'country_code': 'gb',
    #   'county': 'London',
    #   'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
    #   'importance': 0.879660058396959,
    #   'lat': 51.5156177,
    #   'lng': -0.0919983,
    #   'ok': True,
    #   'osm_id': '27365030',
    #   'osm_type': 'node',
    #   'place_id': '141740',
    #   'place_rank': '16',
    #   'postal': 'EC2V 5AE',
    #   'quality': 'city',
    #   'raw': {'address': {'city': 'City of London',
    #                       'country': 'UK',
    #                       'country_code': 'gb',
    #                       'county': 'London',
    #                       'postcode': 'EC2V 5AE',
    #                       'state': 'England',
    #                       'state_district': 'Greater London'},
    #           'boundingbox': ['51.3556177',
    #                           '51.6756177',
    #                           '-0.2519983',
    #                           '0.0680017'],
    #           'category': 'place',
    #           'display_name': 'City of London, London, Greater London, England, '
    #                           'EC2V 5AE, UK',
    #           'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_place_city.p.20.png',
    #           'importance': 0.879660058396959,
    #           'lat': '51.5156177',
    #           'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
    #                      'https://osm.org/copyright',
    #           'lon': '-0.0919983',
    #           'osm_id': '27365030',
    #           'osm_type': 'node',
    #           'place_id': '141740',
    #           'place_rank': '16',
    #           'type': 'city'},
    #   'region': 'England',
    #   'state': 'England',
    #   'status': 'OK',
    #   'type': 'city'},

    #   ...

    #  {'accuracy': 0.7819360330017749,
    #   'address': 'Kent, South East, England, UK',
    #   'bbox': {'northeast': [51.4822724, 1.4517689],
    #            'southwest': [50.9104763, 0.0335249]},
    #   'confidence': 1,
    #   'country': 'UK',
    #   'country_code': 'gb',
    #   'county': 'Kent',
    #   'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_boundary_administrative.p.20.png',
    #   'importance': 0.7819360330017749,
    #   'lat': 51.2474823,
    #   'lng': 0.7105077,
    #   'ok': True,
    #   'osm_id': '172385',
    #   'osm_type': 'relation',
    #   'place_id': '198778295',
    #   'place_rank': '12',
    #   'quality': 'administrative',
    #   'raw': {'address': {'country': 'UK',
    #                       'country_code': 'gb',
    #                       'county': 'Kent',
    #                       'state': 'England',
    #                       'state_district': 'South East'},
    #           'boundingbox': ['50.9104763', '51.4822724', '0.0335249', '1.4517689'],
    #           'category': 'boundary',
    #           'display_name': 'Kent, South East, England, UK',
    #           'icon': 'https://nominatim.openstreetmap.org/images/mapicons/poi_boundary_administrative.p.20.png',
    #           'importance': 0.7819360330017749,
    #           'lat': '51.2474823',
    #           'licence': 'Data © OpenStreetMap contributors, ODbL 1.0. '
    #                      'https://osm.org/copyright',
    #           'lon': '0.7105077',
    #           'osm_id': '172385',
    #           'osm_type': 'relation',
    #           'place_id': '198778295',
    #           'place_rank': '12',
    #           'type': 'administrative'},
    #   'region': 'England',
    #   'state': 'England',
    #   'status': 'OK',
    #   'type': 'administrative'},
    #  {'accuracy': 0.743998870648923,
    #   'address': 'Hertfordshire, East of England, England, UK',
    #   'bbox': {'northeast': [52.0805364, 0.195567],
    #            'southwest': [51.5995828, -0.7457892]},
    #   'confidence': 1,
    #   'country': 'UK',
    #   'country_code': 'gb',
    #   'county': 'Hertfordshire',

    #   ...

    #   }]

    # annotations = LILACS.annotate(test_text)
    # pprint(annotations)
    # output
    """

[{'URI': 'http://dbpedia.org/resource/Greater_London',
  'offset': 0,
  'percentageOfSecondRank': 2.0763189316436016e-05,
  'similarityScore': 0.9999778324259112,
  'support': 4571,
  'surfaceForm': 'London',
  'types': 'Wikidata:Q3455524,Schema:Place,Schema:AdministrativeArea,DBpedia:Region,DBpedia:PopulatedPlace,DBpedia:Place,DBpedia:Location,DBpedia:AdministrativeRegion'},
 {'URI': 'http://dbpedia.org/resource/Capital_city',
  'offset': 14,
  'percentageOfSecondRank': 2.143566429464659e-07,
  'similarityScore': 0.9999995979453287,
  'support': 8100,
  'surfaceForm': 'capital',
  'types': ''},

 ...


 {'URI': 'http://dbpedia.org/resource/Roman_Britain',
  'offset': 241,
  'percentageOfSecondRank': 0.027343760304466284,
  'similarityScore': 0.9715019889945219,
  'support': 6051,
  'surfaceForm': 'Romans',
  'types': 'Wikidata:Q3455524,Schema:Place,Schema:AdministrativeArea,DBpedia:Region,DBpedia:PopulatedPlace,DBpedia:Place,DBpedia:Location,DBpedia:AdministrativeRegion'},
 {'URI': 'http://dbpedia.org/resource/Londinium',
  'offset': 262,
  'percentageOfSecondRank': 1.806786374851336e-09,
  'similarityScore': 0.9999999981931751,
  'support': 450,
  'surfaceForm': 'Londinium',
  'types': ''},
 {'URI': 'http://dbpedia.org/resource/Greater_London',
  'offset': 273,
  'percentageOfSecondRank': 2.0763189316436016e-05,
  'similarityScore': 0.9999778324259112,
  'support': 4571,
  'surfaceForm': 'London',
  'types': 'Wikidata:Q3455524,Schema:Place,Schema:AdministrativeArea,DBpedia:Region,DBpedia:PopulatedPlace,DBpedia:Place,DBpedia:Location,DBpedia:AdministrativeRegion'},

....

 {'URI': 'http://dbpedia.org/resource/Middle_Ages',
  'offset': 394,
  'percentageOfSecondRank': 0.0003615768940138939,
  'similarityScore': 0.9995167139063358,
  'support': 29551,
  'surfaceForm': 'medieval',
  'types': ''},
 {'URI': 'http://dbpedia.org/resource/Century',
  'offset': 439,
  'percentageOfSecondRank': 0.0015267328225673285,
  'similarityScore': 0.9978642520373232,
  'support': 1347,
  'surfaceForm': 'century',
  'types': ''},

...


 {'URI': 'http://dbpedia.org/resource/Mayor',
  'offset': 658,
  'percentageOfSecondRank': 0.00023661355713781133,
  'similarityScore': 0.999708913147703,
  'support': 19123,
  'surfaceForm': 'Mayor',
  'types': ''},
  {'URI': 'http://dbpedia.org/resource/London_Assembly',
  'offset': 682,
  'percentageOfSecondRank': 7.363265257106634e-09,
  'similarityScore': 0.9999999926367309,
  'support': 775,
  'surfaceForm': 'London Assembly',
  'types': 'Wikidata:Q43229,Wikidata:Q24229398,Wikidata:Q11204,DUL:SocialPerson,DUL:Agent,Schema:Organization,DBpedia:Organisation,DBpedia:Legislature,DBpedia:Agent'}]
    """
