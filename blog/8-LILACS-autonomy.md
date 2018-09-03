# LILACS - Autonomy

we have a framework that allows our system to understand and react, but most of the time the system will remain idle

how can we simulate free will and have the system decide what to do when left to itself?

What things can it do that are beneficial? A obvious case is having LILACS learn by itself, or creating new things

# Modeling Free will

Once again let's look to how humans behave to model LILACS around it

Humans have needs they want to satisfy, lets start our autonomous decision making from there


CIA stands for Control, Identity and Arousal, which is the general priority order in which we experience them.

    Our Sense of Control tells us when we are safe and can bend our environment to our purposes. 
    Our Sense of Identity tells us who we are, especially relative to other people.
    Our Sense of Arousal tells us that we are learning, improving and evolving. It also helps us compete.


For a sense of control, we seek:

- Completion, certainty and winning tell we are getting there.
- Understanding and consistency help us predict (and hence control) what will happen.
- Repetition confirms our beliefs and models as still valid.

For a sense of identity, we seek:

- Belonging to a group lends us the identity of the group.
- To stay in the group we must conform to their rules.
- The esteem of others raises our sense of identity and affords us status.
- Everyone likes a winner so we try to succeed.
- Being able to explain casts us as expert and rational.

For a sense of arousal, we are driven when:

- Boredom and curiosity kick us into action.
- Achievable challenges act to stimulate us.
- Novelty attracts us.
- Anticipation of pleasurable or painful arousal attracts or repels us (although pain can still be better than no arousal).


If we simulate these senses, we can have a starting point to determine what the system needs, but what is a need?

# Fundamental Needs

Manfred Max-Neef classified 9 Fundamental human needs

They are constant through all human cultures and across historical time periods. 
What changes over time and between cultures is the strategies by which these needs (and created desires) are satisfied. 
Human needs can be understood as a system—i.e., they are interrelated and interactive. 
In this system, there is no hierarchy of needs (apart from the basic need for subsistence or survival) rather, simultaneity, complementarity and trade-offs are features of the process of needs satisfaction.


| Need | Being (qualities) | Having (things) | Doing (actions) | Interacting (settings) | 
|:--------------:|:----------:|:------------:|:----------:|:------------:|
|   Subsistence	 | physical and mental health | food, shelter, work |  feed, clothe, rest, work | living environment, social setting |
|   Protection	 |    care, adaptability, autonomy | social security, health systems, work    |  co-operate, plan, take care of, help | social environment, dwelling |
|   Affection	 |    respect, sense of humour, generosity, sensuality   |     friendships, family, relationships with nature   |  share, take care of, express emotions | privacy, intimate spaces of togetherness |
|   Understanding |    critical capacity, curiosity, intuition    |     literature, teachers, policies   |  analyse, study, meditate, investigate,	 | schools, families, universities, communities |
|   Participation |    receptiveness, dedication, sense of humour		    |     responsibilities, duties, work, rights	    |  cooperate, dissent, express opinions | associations, parties, churches, neighbourhoods |
|   Leisure	  |    imagination, tranquility, spontaneity    |    games, parties, peace of mind	   |  day-dream, remember, relax, have fun	 | landscapes, intimate spaces, places to be alone |
|   Creation	  |    imagination, boldness, inventiveness, curiosity	    |     abilities, skills, work, techniques    |  invent, build, design, work, compose, interpret	 | spaces for expression, workshops, audiences |
|   Identity	  |    sense of belonging, self-esteem, consistency    |    language, religions, work, customs, values, norms	|  get to know oneself, grow, commit oneself	| places one belongs to, everyday settings |
|   Freedom	  |    autonomy, passion, self-esteem, open-mindedness	    |     equal rights	    |  dissent, choose, run risks, develop awareness | anywhere |


We can further classify needs in 3 analogues to our senses in order to fit everything together

Survival - Survival needs are basic for evolution, in particular that we survive long enough to have children and ensure they also survive long enough to also procreate, so our genes continue to be propagated. The survival instinct continues even after having children and we will fight for our very last breath.

Homeostasis - Related to survival needs, we tend to seek consistency, preferring the easy comfort of the familiar over the effortful confusion of the strange. When we are somehow disrupted, where what it normal and expected does not happen, the easiest course is to head backwards towards the familiar, seeking to re-establish old patterns and positions.

Growth - An alternative to the familiarity of homeostasis is to set out and explore new territory. Rather than comfort, we may seek to learn, enjoying the arousal we get from exploring novel situations. Whether we revert to homeostatic familiarity or venture out into novelty and growth may depend on several factors, in particular the perceived risk and our risk bias in terms of the extent to which we enjoy the physical or psychological dangers of the unknown. The situation can significantly affect this tendency, for example we may seek growth in learning to ski while being quite conservative our choice of friends.


# Secondary/Psychogenic Needs

In 1938, Henry Murray developed a system of needs as part of his theory of personality, which he called 'personology.' 

He argued that everyone had a set of universal basic needs, with individual differences on these needs leading to the uniqueness of personality through varying dispositional tendencies for each need; in other words, specific needs are more important to some than to others. 

Secondary (Psychogenic) needs emerge from or are influenced by primary needs. Murray identified 17 secondary needs, each belonging to one of eight need domains: Ambition, Materialism, Status, Power, Sado-Masochism, Social-Conformance, Affection, and Information. Needs in each domain have similar themes underpinning them; for instance, the Ambition domain contains all those needs which relate to achievement and recognition.


| Domain | Need | Representative behavior |
|:--------------:|:----------:|:------------:|
| Ambition | Superiority | To seek validation for power (Often split into Achievement and Recognition) |
| Ambition | Achievement | To accomplish difficult tasks, overcoming obstacles and becoming expert |
| Ambition | Recognition | To seek praise and commendation for accomplishments |
| Ambition | Exhibition | To impress others through one's actions and words, even if these are shocking. (Often combined with Recognition) |
| Materialism |	Acquisition	|To gain possession over an object |
| Materialism |	Conservance	| To maintain the condition of an object |
| Materialism |	Order | To make things clean, neat and tidy |
| Materialism |	Retention | To keep possession over an object |
| Materialism |	Construction | To organize or build an object or objects |
| Defense of status | Inviolacy	| To prevent harm to self-respect or "good-name" |
| Defense of status | Infavoidance | To avoid failure and humiliation |
| Defense of status | Defendance |To defend oneself against attack or blame, hiding any failure of the self. |
| Defense of status	| Counteraction | To make up for failure by trying again, seeking pridefully to overcome obstacles. |
| Defense of status | Seclusion | To be isolated from others (opposite from Exhibition) |
| Human power |	Dominance | To control one's environment or the people in it through command or persuasion |
| Human power |	Deference | To admire a superior person; praising them, yielding to them, following their rules. |
| Human power  | Autonomy | To resist the influence of others and strive for independence |
| Human power |	Contrariance | To act unique, different from the norm |
| Human power |	Infavoidance | To avoid being humiliated or embarrassed. |
| Sado-Masochistism | Abasement | To surrender and submit to others, accept blame and punishment. To enjoy pain and misfortune |
| Sado-Masochistism | Aggression | To forcefully overcome, control, punish, or harm someone |
| Social-Conformance | Blame avoidance|	To inhibit asocial behavior to avoid blame or ostracism |
| Affection between people | Affiliation| To be close and loyal to another person, pleasing them and winning their friendship and attention |
| Affection between people | Rejection|	To separate oneself from a negatively viewed object or person, excluding or abandoning it. |
| Affection between people | Nurturance| To help the helpless, feeding them and keeping them from danger |
| Affection between people | Succorance	| To have one's needs satisfied by someone or something. Includes being loved, nursed, helped, forgiven and consoled |
| Affection between people | Play | To have fun, laugh and relax, enjoy oneself |
| Exchange of information |	Cognizance | To understand, be curious, ask questions, and acquire new knowledge |
| Exchange of information |	Exposition | To find and demonstrate relations between facts. |


We can assign to each of these a type and a number of fundamental needs they help fulfil


# Solving a need

We can start building a framework to simulate needs, the senses tell us what basic needs we have to satisfy
 
But what does the bot need to actually do after selecting a need?

We can pick one of the more specific Psychogenic needs that include our base need, we are left with the problem of mapping the representative behaviours to meaningful actions our bot can perform


