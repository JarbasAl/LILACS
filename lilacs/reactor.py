import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from lilacs.reasoning import LILACSQuestionParser, BasicTeacher
from lilacs.knowledge.nodes.short_term import ConceptDatabase
from lilacs.knowledge.data_sources.conceptnet import extract_conceptnet_connections
from lilacs.knowledge.data_sources.dbpedia import DbpediaEnquirer
from lilacs.knowledge.data_sources.wikidata import extract_wikidata_connections
import time
from profanity.profanity import contains_profanity
from lilacs.brain.emotions.tag import best_emotion
from lilacs.brain.emotions.deepmoji import get_emojis
from lilacs.brain.context.core import UserEmotionContext
from lilacs.reasoning import LILACSTextAnalyzer


class LILACSReactor:
    teacher = BasicTeacher()
    parser = LILACSQuestionParser()

    def __init__(self, debug=False):
        self.db = ConceptDatabase(debug=debug)
        self.explanation = []
        self.contexts = []
        self.emotions = []
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
        self.status_update("start")
        self.status_update("receive user question", {"utterance": utterance})
        # TODO set some bias emotions or context

        data = self.feature_selection(utterance)
        possible_reactions = self.emotional_reaction(utterance)
        # execute all contexts to mutate data
        contexts = []
        for context in self.contexts:
            contexts.append(context)
            data, emotions = context.execute(data)
            data["contexts"] = contexts
            data["last_context"] = context
            self.status_update("executed context", data)
            # add emotions from contexts
            for e in emotions:
                self.status_update("context bias", {"bias": e})
                self.add_emotion(e)
        reaction = self.model_selection(data, possible_reactions)
        success = reaction.execute(data)
        data["success"] = success
        self.status_update("executed reaction", data)
        self.status_update("end")
        return success

    def emotional_reaction(self, text):
        # how does the user feel
        user_emotion_data = self.extract_user_emotions(text)

        # how do i feel about the text content
        deepmoji_data = self.extract_text_emotions(text)

        # profanity bias
        if contains_profanity(text):
            self.add_emotion("disgust")
            data = {"bias": "disgust"}
            self.status_update("detected profanity", data)

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
        self.status_update("parsed user question", data)
        if question_type == "teach":
            teacher_data = self.teacher.parse(text)
            self.status_update("parsed user teaching", teacher_data)
            # bias for selecting learning behaviour
            self.add_emotion("serenity")
            teacher_data["bias"] = "serenity"
            self.status_update("added learning bias", teacher_data)
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
        data["emotions"] = self.emotions
        self.status_update("selected reaction", data)
        return None

    def add_emotion(self, name):
        emotion = name
        # TODO use emotion object
        self.emotions.append(emotion)

    def register_reaction(self, reaction_type, handler):
        assert reaction_type in self.reaction_handlers.keys()

        self.reaction_handlers[reaction_type].append(handler)

    def set_context(self, context):
        self.status_update("defined context", context.__dict__)
        self.contexts.insert(0, context)

    def explain(self):
        # find start
        reversed_history = self.explanation.copy()
        reversed_history.reverse()
        relevant = []
        for idx, reason in enumerate(reversed_history):
            if reason["last action"] == "start":
                relevant = reversed_history[:idx]
                relevant.reverse()
        return relevant

    # emotion parsing
    def extract_text_emotions(self, text):
        emojis = get_emojis(text)
        data = {"emojis": emojis}
        self.status_update("deepmoji tagging", data)
        return {}

    def extract_user_emotions(self, text):
        # create context
        self.set_context(UserEmotionContext())
        # return emotion data
        data = {"user_emotion": best_emotion(text)}
        self.status_update("set user emotion context", data)
        return data

    # TODO historical context
    def status_update(self, action, data=None):
        data = data or {}
        self.status["last_action_timestamp"] = time.time()
        self.status["last_action_data"] = data
        self.status["last_action"] = action
        self.explanation.append(dict(self.status))

    # text parsing
    def normalize(self, text):
        return LILACSTextAnalyzer.normalize(text)

    # data aquisition
    def get_related_entities(self, subject, n=3):
        cons = LILACSTextAnalyzer.related_concepts(subject, n)
        self.status_update("sense2vec", {"connections": cons})
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

    # short term memory
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
    l = LILACSReactor()
    l.populate_node("elon musk")