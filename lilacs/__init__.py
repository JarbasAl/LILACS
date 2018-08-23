import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from os.path import join
from lilacs.nlp import get_nlp, get_corefnlp
from lilacs.nlp.spotting import LILACSQuestionParser, BasicTeacher
from lilacs.nodes.concept import ConceptDatabase
from lilacs.nlp.parse import extract_facts, extract_entities, normalize
from lilacs.data_sources.dictionary import extract_dictionary_connections
from lilacs.data_sources.conceptnet import extract_conceptnet_connections
from lilacs.data_sources.dbpedia import DbpediaEnquirer
from lilacs.data_sources.reddit_hivemind import get_similar
from lilacs.data_sources.wikidata import extract_wikidata_connections
from lilacs.data_sources.wikipedia import extract_wikipedia_connections
from lilacs.settings import MODELS_DIR, SENSE2VEC_MODEL
#import sense2vec
import time
from profanity.profanity import contains_profanity
from lilacs.context.emotions.tag import best_emotion
from lilacs.context.core import UserEmotionContext


class LILACS(object):
    nlp = get_nlp()
    coref_nlp = None
    teacher = BasicTeacher()
    parser = LILACSQuestionParser()
    s2v = None

    def __init__(self, debug=False):
        self.db = ConceptDatabase(debug=debug)
        self.past_actions = []
        self.contexts = []
        self.feelings = []
        self.status = {}
        self.status_update("boot")
        self.reaction_handlers = {
            "retain or repeat": [],
            "groom": [],
            "escape": [],
            "stop": [],
            "cry": [],
            "vomit": [],
            "attack": [],
            "map": []
        }
        self._build_base_reactions()

    def _build_base_reactions(self):
        # when teaching, retain or repeat, base = serenity
        name = "retain or repeat"
        self.register_reaction(name, self.handle_retain_or_repeat)
        # when wrong, cry, base = pensiveness
        name = "cry"
        self.register_reaction(name, self.handle_cry)
        # when user wrong, attack, base = annoyance
        name = "attack"
        self.register_reaction(name, self.handle_attack)
        # when told to stop, stop, base = distraction
        name = "stop"
        self.register_reaction(name, self.handle_stop)
        # when can learn, map, base = interest
        name = "map"
        self.register_reaction(name, self.handle_map)
        # when can answer, groom, base = acceptance
        name = "groom"
        self.register_reaction(name, self.handle_groom)
        # when unknown, escape, base = apprehension
        name = "escape"
        self.register_reaction(name, self.handle_escape)
        # when not enough data/need clarification, vomit, base = boredom
        name = "vomit"
        self.register_reaction(name, self.handle_vomit)

    # 8 basic survival instincts
    def handle_retain_or_repeat(self, data):
        pass

    def handle_attack(self, data):
        pass

    def handle_stop(self, data):
        pass

    def handle_cry(self, data):
        pass

    def handle_map(self, data):
        pass

    def handle_groom(self, data):
        pass

    def handle_escape(self, data):
        pass

    def handle_vomit(self, data):
        pass

    # reactions
    def react(self, utterance):
        # TODO set some bias emotions or context

        data = self.feature_selection(utterance)
        possible_reactions = self.emotional_reaction(utterance)
        # execute all contexts to mutate data
        for context in self.contexts:
            data, emotions = context.execute(data)
            # add emotions from contexts
            for e in emotions:
                self.add_emotion(e)
        reaction = self.model_selection(data, possible_reactions)
        return reaction.execute(data)

    def emotional_reaction(self, text):
        # how does the user feel
        user_emotion_data = self.extract_user_emotions(text)

        # how do i feel about the text content
        deepmoji_data = self.extract_text_emotions(text)

        # profanity bias
        if contains_profanity(text):
            self.add_emotion("disgust")

        # TODO reactions from emotions
        reactions = []
        return reactions

    # pipeline
    def feature_selection(self, text):
        """
        extract data and situational context from text

        :param text:
        :return:
        """
        # is question?
        data = self.parser.parse(text)
        question_type = data["question_type"]
        if question_type == "teach":
            teacher_data = self.teacher.parse(text)
            # bias for selecting learning behaviour
            self.add_emotion("serenity")
            return teacher_data
        return data

    def model_selection(self, data, reaction_whitelist=None):
        # pre selection
        reactions = []
        for reaction in reaction_whitelist:
            # useful reaction
            if reaction.can_solve(data):
                reactions.append(reaction)
            # wants do something but cant solve
            elif reaction.wants_to_execute():
                reactions.append(reaction)
        # TODO select best reaction here
        return None

    def add_emotion(self, name):
        emotion = name
        # TODO use emotion object
        self.feelings.append(emotion)

    def register_reaction(self, reaction_type, handler):
        assert reaction_type in self.reaction_handlers.keys()

        self.reaction_handlers[reaction_type].append(handler)

    def set_context(self, context):
        self.contexts.insert(0, context)

    # emotion parsing
    def extract_text_emotions(self, text):
        return {}

    def extract_user_emotions(self, text):
        # create context
        self.set_context(UserEmotionContext())
        # return emotion data
        return {"user_emotion": best_emotion(text)}

    # TODO historical context
    def status_update(self, action, data=None):
        data = data or {}
        self.status["last_action_timestamp"] = time.time()
        self.status["last_action_data"] = data
        self.status["last_action"] = action
        self.past_actions.append(dict(self.status))

    # text parsing
    def normalize(self, text):
        return normalize(text, True, True, self.coref_nlp)

    def extract_named_entities(self, text):
        ents = extract_entities(text)
        self.status_update("NER", ents)
        return ents

    def extract_facts(self, subject, text):
        text = self.normalize(text)
        facts = extract_facts(subject, text, self.nlp)
        self.status_update("extract_facts", facts)
        return facts

    # data aquisition
    def get_related_entities(self, subject, sense="auto"):
        data = get_similar(subject, sense)
        cons = []
        for r in data.get("results"):
            cons.append((r["text"].strip(), (r["score"] * 100) - 30))
        self.status_update("sense2vec", cons)
        return cons

    def populate_node(self, subject):
        dbpedia = DbpediaEnquirer()
        cons = dbpedia.get_dbpedia_cons_for_dblink(subject)
        for c, t in cons:
            print((c, t, 55))
        ents = extract_conceptnet_connections(subject)
        for c in ents:
            print(c)
        ents = extract_wikidata_connections(subject)
        for c in ents:
            print(c)
        #ents = self.get_related_entities(subject)
        #for c in ents:
        #    c = ("related", c[0], c[1])
        #    print(c)


    # nodes
    def add_node(self, subject, description="", node_type="idea"):
        self.db.add_concept(subject, description, type=node_type)

    def add_connection(self, source_name, target_name, con_type="related"):
        return self.db.add_connection(source_name, target_name, con_type)

    @property
    def concepts(self):
        return self.db.get_concepts()

    @property
    def connections(self):
        return self.db.get_connections()

    @property
    def total_concepts(self):
        return self.db.total_concepts()

    @property
    def total_connections(self):
        return self.db.total_connections()


if __name__ == "__main__":
    l = LILACS()
    l.populate_node("elon musk")