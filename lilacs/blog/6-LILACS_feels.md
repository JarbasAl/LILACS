# LILACS - Neurotransmitters


We have tried to make bots understand emotions, but can they have them?

It would be fun to try, but why? this post does not care about that, this is about the How?

Lets have some fun, animals have neurotransmitters, let's copy nature and give 3 of them to LILACS

# Dopamine, Adrenaline, Serotonine


		class Dopamine(Neurotransmitter):
		    def __init__(self, bus=None):
			Neurotransmitter.__init__(self, "dopamine", bus)


		class Serotonin(Neurotransmitter):
		    def __init__(self, bus=None):
			Neurotransmitter.__init__(self, "serotonine", bus)


		class Adrenaline(Neurotransmitter):
		    def __init__(self, bus=None):
			Neurotransmitter.__init__(self, "adrenaline", bus)

now lets make a place to store them and a plug a messagebus into it

        class NeuroRepository(object):
            def __init__(self, bus):
                self.dopamine = 0
                self.serotonine = 0
                self.adrenaline = 0
                self.bus.on("lilacs.neuro.dopamine.create", self.handle_increase_dopamine)
                self.bus.on("lilacs.neuro.dopamine.consume", self.handle_decrease_dopamine)
                self.bus.on("lilacs.neuro.serotonine.create", self.handle_increase_serotonine)
                self.bus.on("lilacs.neuro.serotonine.consume", self.handle_decrease_serotonine)
                self.bus.on("lilacs.neuro.adrenaline.create", self.handle_increase_adrenaline)
                self.bus.on("lilacs.neuro.adrenaline.consume", self.handle_decrease_adrenaline)
        
                self.bus.on("lilacs.neuro.dopamine.request", self.handle_total_dopamine)
                self.bus.on("lilacs.neuro.serotonine.request", self.handle_total_serotonine)
                self.bus.on("lilacs.neuro.adrenaline.request", self.handle_total_adrenaline)
    

# Mapping neurotransmitters to emotions

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/neutransmitter-emotion.jpg) 



you can learn about how LILACS represents and understand emotions here. meanwhile here is a reminder


| dimension/flow |      3     |       2      |      1     |      0     |      -1      |    -2    |     -3    |
|:--------------:|:----------:|:------------:|:----------:|:------------:|:--------:|:---------:|---------:|
|   sensitivity  |    rage    |     anger    |  annoyance | undefined | apprehension |   fear   |   terror  |
|    attention   |  vigilance | anticipation |  interest  | undefined |  distraction | surprise | amazement |
|  pleasantness  |   ecstasy  |      joy     |  serenity  | undefined |  pensiveness |  sadness |   grief   |
|    aptitude    | admiration |     trust    | acceptance | undefined |    boredom   |  disgust |  loathing |



this study does not use plutchicks work, but let's try to adapt it

Split into octants 

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_neuro.png)


dimension to neurotransmitter octant

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_dimension.png)


| dimension/octant|     1     |       2      |      3     |     4      |   5    |    6    |  7  |  8 |
|:--------------:|:----------:|:------------:|:----------:|:------------:|:--------:|:---------:|:---------:|:---------:|
|   sensitivity  |    -    |      +1   |   -    |    -    |   -    |   -1    | -    |   -    | 
|    attention   |  +1 | - |    -    |     -   |   -   |   -    |  -1    |   -    | 
|  pleasantness  |   - |     -     |    -1    |   -    |   +1    |    -    |  -    |   -    | 
|    aptitude    | - |     -   |   -    |    +1    |    -    |   -    |  -   |   -1    | 

each octant/column represents a base emotion


		
![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_basic_emo.png)


we can assign valence, some octants are positive and others are negative


![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_valence.png)
        
        
lets define the dimensions as the vector of the octant diagonals, this simply gives us a direction

		    
![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_pleasantness.png) 
![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_aptitude.png) 
![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_attention.png) 
![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_sensitivity.png) 
            
now we can work with emotion vectors in the neuro transmitter space

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_emotion_vec.png) 


We can also sum emotion vector to create feelings

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_feelings.png) 


Since we are working with vectors we can also multiply vectors

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_cross_product.png) 



# Neutrality

neutrality would be a lack of emotion, in this octant space that is the center of the cube

However we can see that octants  4/8 and 2/6 cancel each other

this allows us to trace a neutrality line

![](https://github.com/JarbasAl/LILACS/blob/emotional_lilacs/lilacs/blog/octant_neutrality.png) 

This represents emotional equilibrium



# how do you feel LILACS ?

TODO

*"i feel 95% boredom and 5% annoyance"*



Since we got here let's start building a freewill module


Neutrality is point zero, prefer reactions that take you towards neutrality



# what for ?

These are used to calculate current feeling

Current feeling is used to select reaction (emotion algebra is used to add bias)

Freewill module selects reaction to go towards Neutrality

in skills you can:
- produce/decrease these to influence emotional reaction
- use this for reinforcement learning 


# usage

TODO
