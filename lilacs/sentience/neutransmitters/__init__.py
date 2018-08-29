#
from lilacs.messagebus.message import Message
from lilacs.util.log import LOG
from lilacs.messagebus.client.ws import WebsocketClient
from lilacs.sentience.emotions.emotions import get_emotion
from threading import Thread
import numpy as np
import math


class Neurotransmitter(object):
    def __init__(self, name, bus=None):
        self._name = name
        self.total = 0
        self.total_created = 0
        self.total_consumed = 0
        if bus:
            self.bus = bus
            self._t = None
        else:
            self.bus = WebsocketClient()
            self._t = Thread(target=self._connect)
            self._t.setDaemon(True)
            self._t.start()

        self.bus.on("lilacs.neuro." + self._name + ".total", self.handle_total)

    def handle_total(self, message):
        n = message.data.get("n", 0)
        self.total = n

    def _connect(self):
        self.bus.run_forever()

    def create(self, n=1):
        self.total_created += n
        self.bus.emit(Message("lilacs.neuro." + self._name + ".create",
                              {"ammount": n}))

    def consume(self, n=1):
        self.total_consumed += n
        self.bus.emit(Message("lilacs.neuro." + self._name + ".consume",
                              {"ammount": n}))

    def __del__(self):
        if self.bus:
            self.bus.remove("lilacs.neuro." + self._name + ".total", self.handle_total)
            self.bus.close()
        if self._t:
            self._t.join(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()


class Dopamine(Neurotransmitter):
    def __init__(self, bus=None):
        Neurotransmitter.__init__(self, "dopamine", bus)


class Serotonin(Neurotransmitter):
    def __init__(self, bus=None):
        Neurotransmitter.__init__(self, "serotonine", bus)


class Adrenaline(Neurotransmitter):
    def __init__(self, bus=None):
        Neurotransmitter.__init__(self, "adrenaline", bus)


class NeuroRepository(object):
    def __init__(self, bus):
        self.dopamine = 0
        self.serotonine = 0
        self.adrenaline = 0

        # dimension of emotion cube
        # max diagonal size = 6 to fit the flows ( - 3 to 3)
        diagonal_size = 6 / math.sqrt(3)

        # lets scale it by 100
        self.max_transmitters = diagonal_size * 100

        if bus:
            self._t = None
            self.bus = bus
        else:
            self.bus = WebsocketClient()
            self._t = Thread(target=self._connect)
            self._t.setDaemon(True)
            self._t.start()
        self.bus.on("lilacs.neuro.dopamine.create", self.handle_increase_dopamine)
        self.bus.on("lilacs.neuro.dopamine.consume", self.handle_decrease_dopamine)
        self.bus.on("lilacs.neuro.serotonine.create", self.handle_increase_serotonine)
        self.bus.on("lilacs.neuro.serotonine.consume", self.handle_decrease_serotonine)
        self.bus.on("lilacs.neuro.adrenaline.create", self.handle_increase_adrenaline)
        self.bus.on("lilacs.neuro.adrenaline.consume", self.handle_decrease_adrenaline)

        self.bus.on("lilacs.neuro.dopamine.request", self.handle_total_dopamine)
        self.bus.on("lilacs.neuro.serotonine.request", self.handle_total_serotonine)
        self.bus.on("lilacs.neuro.adrenaline.request", self.handle_total_adrenaline)

    # octant mappings
    @staticmethod
    def vec_to_octant(vec):
        if not isinstance(vec, list):
            # numpy
            vec = vec.tolist()
        if vec[0] > 50 and vec[1] > 50 and vec[2] > 50:
            return 1
        elif vec[0] < 50 and vec[1] > 50 and vec[2] > 50:
            return 2
        elif vec[0] < 50 and vec[1] < 50 and vec[2] > 50:
            return 3
        elif vec[0] > 50 and vec[1] < 50 and vec[2] > 50:
            return 4
        elif vec[0] > 50 and vec[1] > 50 and vec[2] < 50:
            return 5
        elif vec[0] < 50 and vec[1] > 50 and vec[2] < 50:
            return 6
        elif vec[0] < 50 and vec[1] < 50 and vec[2] < 50:
            return 7
        elif vec[0] > 50 and vec[1] < 50 and vec[2] < 50:
            return 8

    @staticmethod
    def octant_to_emotion(octant):
        if octant == 1:
            return "interest"
        if octant == 2:
            return "annoyance"
        if octant == 3:
            return "pensiveness"
        if octant == 4:
            return "acceptance"
        if octant == 5:
            return "serenity"
        if octant == 6:
            return "apprehension"
        if octant == 7:
            return "distraction"
        if octant == 8:
            return "boredom"

    @staticmethod
    def octant_to_dimension_vector(octant):

        # neutrality / center of the cube
        n = np.array([50, 50, 50])
        # s d a
        if octant == 1:
            return n + np.array([100, 100, 100])
        if octant == 2:
            return n + np.array([0, 100, 100])
        if octant == 3:
            return n + np.array([0, 0, 100])
        if octant == 4:
            return n + np.array([100, 0, 100])
        if octant == 5:
            return n + np.array([100, 100, 0])
        if octant == 6:
            return n + np.array([0, 100, 0])
        if octant == 7:
            return n + np.array([0, 0, 0])
        if octant == 8:
            return n + np.array([100, 0, 1])

    # properties
    @property
    def octant(self):
        # https://en.wikipedia.org/wiki/Octant_(solid_geometry)
        # lilacs/sentience/neutransmitter-emotion.jpg
        #   s d a
        # 1 + + +
        # 2 - + +
        # 3 - - +
        # 4 + - +
        # 5 + + -
        # 6 - + -
        # 7 - - -
        # 8 + - -
        return self.vec_to_octant(self.neural_vec)

    @property
    def dimension_vector(self):
        return self.octant_to_dimension_vector(self.octant)

    @property
    def neural_vec(self):
        return np.array([self.serotonine, self.dopamine, self.adrenaline])

    @property
    def neural_flow(self):
        return np.linalg.norm(self.neural_vec)

    @property
    def cross_neural_vec(self):
        # lets define a secondary emotion as the cross product of the neural vec and the base dimension
        # this creates a composite emotion
        return np.cross(self.neural_vec, self.dimension_vector)

    @property
    def cross_neural_flow(self):
        return np.linalg.norm(self.cross_neural_vec)

    @property
    def base_emotion(self):
        return get_emotion(self.octant_to_emotion(self.octant))

    @property
    def secondary_emotion(self):
        octant = self.vec_to_octant(self.cross_neural_vec)
        return get_emotion(self.octant_to_emotion(octant))

    @property
    def composite_emotion(self):
        # emotion algebra in action
        return self.base_emotion * self.secondary_emotion

    @property
    def feeling(self):
        # emotion algebra in action
        return self.base_emotion + self.secondary_emotion

    @property
    def emotion_flow(self):
        return self.dimension_to_emotion_flow(self.dimension_vector, self.octant)

    def dimension_to_emotion_flow(self, dimension_vector, octant):
        # flow is the dot product of the dimension vector with the neural vector
        flow = np.dot(dimension_vector, self.neural_vec)
        # positive octants
        if octant in [1, 2, 4, 5]:
            return flow
        # negative octants
        else:
            return flow * -1

    @property
    def valence(self):
        if self.octant in [1, 2, 4, 5]:
            return 1
        return -1

    # now defining a single 4D emotion vector
    @property
    def sensitivity(self):
        if self.valence > 0:
            octant = 2
        else:
            octant = 6
        vector = self.octant_to_dimension_vector(octant)
        return self.dimension_to_emotion_flow(vector, octant)

    @property
    def attention(self):
        if self.valence > 0:
            octant = 1
        else:
            octant = 7
        vector = self.octant_to_dimension_vector(octant)
        return self.dimension_to_emotion_flow(vector, octant)

    @property
    def pleasantness(self):
        if self.valence > 0:
            octant = 5
        else:
            octant = 3
        vector = self.octant_to_dimension_vector(octant)
        return self.dimension_to_emotion_flow(vector, octant)

    @property
    def aptitude(self):
        if self.valence > 0:
            octant = 4
        else:
            octant = 8
        vector = self.octant_to_dimension_vector(octant)
        return self.dimension_to_emotion_flow(vector, octant)

    @property
    def emotion_vector(self):
        return np.array([self.sensitivity, self.attention, self.pleasantness, self.aptitude])

    # messagebus interaction
    def _connect(self):
        self.bus.run_forever()

    def handle_total_dopamine(self, message):
        self.bus.emit(Message("lilacs.neuro.dopamine.total", {"n": self.dopamine}))

    def handle_total_adrenaline(self, message):
        self.bus.emit(Message("lilacs.neuro.adrenaline.total", {"n": self.adrenaline}))

    def handle_total_serotonine(self, message):
        self.bus.emit(Message("lilacs.neuro.serotonine.total", {"n": self.serotonine}))

    def handle_increase_dopamine(self, message):
        n = message.data.get("n", 1)
        self.dopamine += n
        self.dopamine = self.max_transmitters if self.dopamine > self.max_transmitters else self.dopamine
        LOG("dopamine created: " + str(n))
        self.handle_total_dopamine(message)

    def handle_increase_serotonine(self, message):
        n = message.data.get("n", 1)
        self.serotonine += n
        self.serotonine = self.max_transmitters if self.serotonine > self.max_transmitters else self.serotonine
        LOG("serotonine created: " + str(n))
        self.handle_total_serotonine(message)

    def handle_increase_adrenaline(self, message):
        n = message.data.get("n", 1)
        self.adrenaline += n
        self.adrenaline = self.max_transmitters if self.adrenaline > self.max_transmitters else self.adrenaline
        LOG("adrenaline created: " + str(n))
        self.handle_total_adrenaline(message)

    def handle_decrease_dopamine(self, message):
        n = message.data.get("n", 1)
        self.dopamine -= n
        self.dopamine = 0 if self.dopamine < 0 else self.dopamine
        LOG("dopamine consumed: " + str(n))
        self.handle_total_dopamine(message)

    def handle_decrease_serotonine(self, message):
        n = message.data.get("n", 1)
        self.serotonine -= n
        self.serotonine = 0 if self.serotonine < 0 else self.serotonine
        LOG("serotonine consumed: " + str(n))
        self.handle_total_serotonine(message)

    def handle_decrease_adrenaline(self, message):
        n = message.data.get("n", 1)
        self.adrenaline -= n
        self.adrenaline = 0 if self.adrenaline < 0 else self.adrenaline
        LOG("adrenaline consumed: " + str(n))
        self.handle_total_adrenaline(message)

    # cleanup and shutdown
    def shutdown(self):
        self.bus.remove("lilacs.neuro.dopamine.create", self.handle_increase_dopamine)
        self.bus.remove("lilacs.neuro.dopamine.consume", self.handle_decrease_dopamine)
        self.bus.remove("lilacs.neuro.serotonine.create", self.handle_increase_serotonine)
        self.bus.remove("lilacs.neuro.serotonine.consume", self.handle_decrease_serotonine)
        self.bus.remove("lilacs.neuro.adrenaline.create", self.handle_increase_adrenaline)
        self.bus.remove("lilacs.neuro.adrenaline.consume", self.handle_decrease_adrenaline)
        self.bus.remove("lilacs.neuro.dopamine.request", self.handle_total_dopamine)
        self.bus.remove("lilacs.neuro.serotonine.request", self.handle_total_serotonine)
        self.bus.remove("lilacs.neuro.adrenaline.request", self.handle_total_adrenaline)

    def __del__(self):
        try:
            self.shutdown()
        except:
            pass
        if self.bus:
            self.bus.close()
        if self._t:
            self._t.join(0)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__del__()
