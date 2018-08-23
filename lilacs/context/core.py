# these are the default contexts available to lilacs

from lilacs.context import HistoricalContext, SocialContext


class UserActionContext(SocialContext):
    def __init__(self):
        SocialContext.__init__(self, "user action")


class ActionContext(SocialContext):
    def __init__(self):
        SocialContext.__init__(self, "lilacs action")


class UserEmotionContext(SocialContext):
    def __init__(self):
        SocialContext.__init__(self, "user emotion")
        data = {
            "data_type": "emotion"
        }
        self.register_influence_change("inject feeling", self.influence_handler, data)

    def influence_handler(self, data):
        emotions = []
        # add empathy bias, influence from user emotion
        user_emo = data.get("user_emotion")
        if user_emo:
            # decrease emotion intensity
            # TODO account for valence
            emotions.append(user_emo - 1)
        return data, emotions


class EmotionContext(SocialContext):
    def __init__(self):
        SocialContext.__init__(self, "lilacs emotion")
        data = {
            "data_type": "emotion"
        }
        self.register_influence_change("inject feeling", self.influence_handler, data)

    def influence_handler(self, data):
        emotions = data.get("emotions", [])
        return data, emotions


class PastUserActionContext(HistoricalContext):
    def __init__(self):
        HistoricalContext.__init__(self, "past user action")


class PastActionContext(HistoricalContext):
    def __init__(self):
        HistoricalContext.__init__(self, "past lilacs action")


class PastUserEmotionContext(HistoricalContext):
    def __init__(self):
        HistoricalContext.__init__(self, "past user emotion")
        data = {
            "data_type": "emotion"
        }
        self.register_influence_change("inject feeling", self.influence_handler, data)

    def influence_handler(self, data):
        emotions = data.get("emotions", [])

        # add empathy bias, influence from user emotion
        user_emo = data.get("user_emotion")
        if user_emo:
            # decrease emotion intensity
            # TODO account for valence
            emotions.append(user_emo - 2)

        return data, emotions


class PastEmotionContext(HistoricalContext):
    def __init__(self):
        HistoricalContext.__init__(self, "past lilacs emotion")
        data = {
            "data_type": "emotion"
        }
        self.register_influence_change("inject feeling", self.influence_handler, data)

    def influence_handler(self, data):
        emotions = data.get("emotions", [])
        return data, emotions


