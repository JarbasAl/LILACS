# https://www.hindawi.com/journals/tswj/2015/434826/


class DataChange(object):

    def __init__(self, name, data=None):
        self.name = name
        self.data = data or {}
        self.initialize()
        self._handlers = []
        self.emotions = []

    def initialize(self):
        pass

    def execute(self, data=None):
        data = data or self.data
        for handler in self._handlers:
            try:
                data, emotion = handler(data)
                self.emotions.append(emotion)
            except Exception as e:
                print(e)
        return data, self.emotions

    def register_handler(self, handler):
        self._handlers.append(handler)


class BaseSituationalContext(object):
    description = "fine descriptors, such as time and noise, " \
                  "but also higher-level abstractions like events, locations, names of databases, and so forth."
    meaning_changes = []
    influence_changes = []
    accuracy_changes = []
    availability_changes = []

    def __init__(self):
        self.emotions = []

    def register_meaning_change(self, change, handler, data=None):
        """
        meaning of cues depends on social factors: for example,
        whistling that indicates game highlight in basketball matches is a meaningless sound in tennis.
        Meaning of the cues may depend on historical factors, too
        (e.g., the users’ laughter during a dialog may be interpreted as either happy or sarcastic,
        depending on the previous statements).

        :param change:
        :param handler:
        :param data:
        :return:
        """
        data = data or {}
        data["type"] = "meaning"
        c = DataChange(change, data)
        c.register_handler(handler)
        self.meaning_changes.append(c)

    def register_influence_change(self, change, handler, data=None):
        """
        Importance of the same input cues may vary in different contexts (often, also due to social factors):
        for example, presence of young children may strongly affect the choice of TV programmes to watch in one family,
        whereas adults may dominate in another family. Task factors play this role, too:
        for example, noise or illumination cues may be more or less important, depending on a search goal.

        :param change:
        :param handler:
        :param data:
        :return:
        """
        data = data or {}
        data["type"] = "influence"
        c = DataChange(change, data)
        c.register_handler(handler)
        self.influence_changes.append(c)

    def register_accuracy_change(self, change, handler, data=None):
        """
        cues may be recognised more or less reliably in different contexts, often due to computational factors;
        for example, the accuracy of image analysis depends on image resolution.
        When sensor data are collected in uncontrolled conditions, the environmental factors significantly influence
        the accuracy of input cues: for example, image background affects the accuracy of object detection.
        Historical factors may degrade the accuracies, too, when the models become outdated; for example,
        growing hair may decrease the face recognition accuracy.
        :param change:
        :param handler:
        :param data:
        :return:
        """
        data = data or {}
        data["type"] = "accuracy"
        c = DataChange(change, data)
        c.register_handler(handler)
        self.accuracy_changes.append(c)

    def register_availability_change(self, change, handler, data=None):
        """
        The same input cues may be abundant in some situations and missing in others.
        Most often this happens in uncontrolled conditions: for example, results of video analysis may be unavailable
        if users bypass a camera. Social factors may cause incomplete data, too: if it is polite to stay silent,
        audio cues will be unavailable.
        :param change:
        :param handler:
        :param data:
        :return:
        """
        data = data or {}
        data["type"] = "availability"
        c = DataChange(change, data)
        c.register_handler(handler)
        self.availability_changes.append(c)

    def execute(self, data=None):
        for change in self.meaning_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.influence_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.accuracy_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.availability_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        return data, self.emotions


class HistoricalContext(BaseSituationalContext):
    description = "	Historical factors embrace anything in the past that may affect current state, " \
                  "for example, user or system actions," \
                  " changes in user’s mood or appearance over time, " \
                  "and recently viewed movies."

    def __init__(self):
        BaseSituationalContext.__init__(self)


class SocialContext(BaseSituationalContext):
    description = "	Social factors include rules and customs of interaction between humans, " \
                  "for example, gender/age-dependent behaviour " \
                  "and what is considered polite in different situations."

    def __init__(self):
        BaseSituationalContext.__init__(self)


class EnvironmentalContext(BaseSituationalContext):
    description = "Environmental factors are anything in surroundings that may affect sensor readings, " \
                  "for example, background noise and light."

    def __init__(self):
        BaseSituationalContext.__init__(self)


class TaskContext(BaseSituationalContext):
    description = "Task factors present specific users’ objectives, for example, " \
                  "purpose of information search and available time."

    def __init__(self):
        BaseSituationalContext.__init__(self)


class ComputationalContext(BaseSituationalContext):
    description = "Computational factors specify system settings, " \
                  "for example, availability or quality of a certain data type (such as image resolution), " \
                  "computational power, and algorithm capabilities."

    def __init__(self):
        BaseSituationalContext.__init__(self)