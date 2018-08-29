# LILACS - reactions

now we gave it emotions, what good can that possibly do? This post will not tell answer why bots should have emotions, but it will tell you what they are good for

Everything in this post is two sided, it works for reading humans, but i will focus on LILACS own emotions!


# Basic Survival Behaviours

Even in animals emotions are not without purpose

According to Plutchik’s Sequential Model, emotions are activated due to specific stimuli, which set off certain behavioral patterns. (Krohn, 2007)

He identified the following survival behaviors that drive our actions:

        Protection: Withdrawal, retreat
        (activated by fear and terror)
        
        Destruction: Elimination of barrier to the satisfaction of needs
        (activated by anger and rage)
        
        Incorporation: Ingesting nourishment
        (activated by acceptance)
        
        Rejection: Riddance response to harmful material
        (activated by disgust)
        
        Reproduction: Approach, contract, genetic exchanges
        (activated by joy and pleasure)
        
        Reintegration: Reaction to loss of nutrient product
        (activated by sadness and grief)
        
        Exploration: Investigating an environment
        (activated by curiosity and play)
        
        Orientation: Reaction to contact with unfamiliar object
        (activated by surprise)
        (Screenr, 2017)

This means that when our emotions are activated, they are done so to elicit one of the survival behaviors. Of course, all of this happens on a subconscious level.



# Selecting a reaction

There is [a paper](https://www.hindawi.com/journals/tswj/2015/434826/) named Lightweight Adaptation of Classifiers to Users and Contexts: Trends of the Emerging Domain


in the LILACS pipeline we currently have on hold:

- tagged concepts
- parsed question data
- text emotional analysis
- [context data augmentation]()


i split the decision in 3 parts;

- feature selection (the question parser step)
- context, data augmentation + reaction bias (emotion algebra)
- emotional reaction (reaction pre-selection based on emotion)
- model selection (final reaction to execute)

model selection uses the following criteria

        # pre selection
        reactions = []
        for reaction in reaction_whitelist:
            # useful reaction
            if reaction.can_solve(data):
                reactions.append(reaction)
            # wants do something but cant solve
            elif reaction.wants_to_execute():
                reactions.append(reaction)

TODO finish

# The 8 basic Behavioral Reactions

Since our bot has emotions, lets use it to select a behaviour, but what is a behaviour?

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/survival.jpg) 


LILACS models a behaviour as a piece of code that runs with the previously tagged data, emotions set the behaviour, then there are a bunch of reactions registered in the system

Context and emotions will affect which reaction is executed

Reactions can be thought off as intent domains for skills

How do we make these reactions be useful in the context of AI assistant?


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
    

# Retain or Repeat
     
When trying to teach something to LILACS this is the expected reaction

If question understanding detects a teaching command there is a bias for this

    "retain or repeat": {
            "function": "gain resources",
            "cognite appraisal": "possess",
            "trigger": "gain of value",
            "base_emotion": "serenity",
            "behaviour": "incorporation"
        },

# attack

If we say something that LILACS is pretty sure its wrong it should try to correct us

Profanity detection is a bias for this reaction


    "attack": {
            "function": "destroy obstacle",
            "cognite appraisal": "enemy",
            "trigger": "obstacle",
            "base_emotion": "annoyance",
            "behaviour": "destruction"
        },

# stop

    "stop": {
            "function": "gain time",
            "cognite appraisal": "orient self",
            "trigger": "unexpected event",
            "base_emotion": "distraction",
            "behaviour": "orientation"
        },

# cry

Something wrong, biased for if errors occur, signal for user intervention

    "cry": {
            "function": "reattach to lost object",
            "cognite appraisal": "abandonment",
            "trigger": "loss of value",
            "base_emotion": "pensiveness",
            "behaviour": "reintegration"
        },
        
        
# map

When not interacting with user this should be biased for, so the system can improve by itself

        "map": {
            "function": "knowledge of territory",
            "cognite appraisal": "examine",
            "trigger": "new territory",
            "base_emotion": "interest",
            "behaviour": "exploration"
        }

# groom

Question detected is a bias for this reaction

Often these reactions will employ [crawlers]() to answer questions  

       "groom": {
            "function": "mutual support",
            "cognite appraisal": "friend",
            "trigger": "member of one's group",
            "base_emotion": "acceptance",
            "behaviour": "reproduction"
        },
        
# escape

Abort conversation, deflect user

Impolitness detection is a bias for this reaction


        "escape": {
            "function": "safety",
            "cognite appraisal": "danger",
            "trigger": "threat",
            "base_emotion": "apprehension",
            "behaviour": "protection"
        },



# vomit

This reaction should trigger when the question did not make sense ( not enough data/need clarification )
 
    "vomit": {
            "function": "eject poison",
            "cognite appraisal": "poison",
            "trigger": "unpalatable object",
            "base_emotion": "boredom",
            "behaviour": "rejection"
        },
        
        
# How do we expect this system to behave, robot feelings are unpredictable!

Along the process LILACS emotions are used as bias to help choose the right reaction

bias introduced:

- empathy bias (mirror user)
- good manners detector
- profanity detector
- teaching detector
- question detector

Other processes can introduced bias by changing the neurotransmitter levels

