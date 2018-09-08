# LILACS -  CONTEXT

Text by itself is pretty limited, a good bot needs to be able to keep context


What is a context for LILACS? 

contexts are fine descriptors, such as time and noise, but also higher-level abstractions like events, locations, names of databases, and so forth.

A context will received the parsed data from the understanding step, and it can then manipulate that data 

Each context object returns mutated data, and optionally some bias to influence the final decision

    def execute(self, data=None):
        for change in self.accuracy_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.availability_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.influence_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        for change in self.meaning_changes:
            data, emotions = change.execute(data)
            self.emotions += emotions
        return data, self.emotions
        
Contexts can execute changes in the parsed data, what kind of changes ?


# meaning changes


 meaning of cues depends on social factors: for example,
        whistling that indicates game highlight in basketball matches is a meaningless sound in tennis.
        Meaning of the cues may depend on historical factors, too
        (e.g., the users’ laughter during a dialog may be interpreted as either happy or sarcastic,
        depending on the previous statements).
        
# Influence changes

 Importance of the same input cues may vary in different contexts (often, also due to social factors):
        for example, presence of young children may strongly affect the choice of TV programmes to watch in one family,
        whereas adults may dominate in another family. Task factors play this role, too:
        for example, noise or illumination cues may be more or less important, depending on a search goal.

# Accuracy changes

cues may be recognised more or less reliably in different contexts, often due to computational factors;
        for example, the accuracy of image analysis depends on image resolution.
        When sensor data are collected in uncontrolled conditions, the environmental factors significantly influence
        the accuracy of input cues: for example, image background affects the accuracy of object detection.
        Historical factors may degrade the accuracies, too, when the models become outdated; for example,
        growing hair may decrease the face recognition accuracy.
        
# Availability Changes

The same input cues may be abundant in some situations and missing in others.
Most often this happens in uncontrolled conditions: for example, results of video analysis may be unavailable
if users bypass a camera. Social factors may cause incomplete data, too: if it is polite to stay silent,
audio cues will be unavailable.
        
 

       
       
What kind of contexts can LILACS track automatically?

# Historical

Historical factors embrace anything in the past that may affect current state, " \
                  "for example, user or system actions," \
                  " changes in user’s mood or appearance over time, " \
                  "and recently viewed movies.


# Social Contexxt

Social factors include rules and customs of interaction between humans, " \
                  "for example, gender/age-dependent behaviour " \
                  "and what is considered polite in different situations.
                  
                  
# Environmental Context

Environmental factors are anything in surroundings that may affect sensor readings, " \
                  "for example, background noise and light."

# TaskContext

Task factors present specific users’ objectives, for example, " \
                  "purpose of information search and available time."
                  
# Computational Context

Computational factors specify system settings, " \
                  "for example, availability or quality of a certain data type (such as image resolution), " \
                  "computational power, and algorithm capabilities."