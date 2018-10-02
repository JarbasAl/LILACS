import random
from pprint import pprint


class Dirty12(object):
    _keys = {
        "machiavellianism": ["1", "5", "7", "10"],
        "psychopathy": ["2", "4", "6", "9"],
        "narcissism": ["3", "8", "11", "12"]
    }

    questions = ['I tend to manipulate others to get my way.',
                 'I tend to lack remorse.',
                 'I tend to want others to admire me.',
                 'I tend to be unconcerned with the morality of my actions.',
                 'I have used deceit or lied to get my way.',
                 'I tend to be callous or insensitive.',
                 'I have used flattery to get my way.',
                 'I tend to seek prestige or status.',
                 'I tend to be cynical.',
                 'I tend to exploit others toward my own end.',
                 'I tend to expect special favors from others.',
                 'I want others to pay attention to me.']

    @staticmethod
    def score(answers):
        result = {
            "machiavellianism": 0,
            "psychopathy": 0,
            "narcissism": 0,
            "total": 0
        }
        for k in Dirty12._keys:
            for question in Dirty12._keys[k]:
                a = int(question) - 1
                result[k] += int(answers[a])

                result["total"] += int(answers[a])

            # cast from 0 to 1
            # result[k] = result[k]/len(questions)
            result[k] = result[k] / (7 * len(Dirty12._keys[k]))

        # cast from 0 to 1
        result["total"] = result["total"] / (7 * len(Dirty12.questions))
        return result

    @staticmethod
    def test():
        print("\nDirty12 Test\n1 strongly disagree\n2 disagree\n3 neutral\n4 agree\n5 strongly agree\n\nStart:\n")
        answers = []
        for q in Dirty12.questions:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 8
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return Dirty12.score(answers)

    @staticmethod
    def test_random():
        ans = {1: "strongly disagree", 2: "disagree", 3: "slightly disagree",
               4: "neutral", 5: "slightly agree", 6: "agree", 7: "strongly agree"}
        print("Dirty12 Test")
        print(ans)
        print("Start:\n")
        answers = []
        for q in Dirty12.questions:
            a = random.randint(1, 7)
            print("Q: " + q, "A: " + ans[a])
            answers.append(a)
        return Dirty12.score(answers)


class Hexaco(object):
    thresholds = {  # 90% 10% 50%
        "honesty-humility": {
            "sincerity": {"high": 4.25, "low": 2.14, "average": 3.25},
            "fairness": {"high": 4.63, "low": 2.13, "average": 3.38},
            "greed-avoidance": {"high": 4, "low": 1.38, "average": 2.63},
            "modesty": {"high": 3, "low": 3, "average": 3.63},
            "total": {"high": 3.97, "low": 2.41, "average": 3.22}
        },
        "emotionality": {
            "fearfulness": {"high": 4, "low": 1.88, "average": 3},
            "anxiety": {"high": 4.63, "low": 2.63, "average": 3.75},
            "dependence": {"high": 4.25, "low": 2, "average": 3.25},
            "sentimentality": {"high": 4.38, "low": 2.38, "average": 3.5},
            "total": {"high": 3.97, "low": 2.41, "average": 3.34}
        },
        "extraversion": {
            "social-self-esteem": {"high": 4.63, "low": 3, "average": 4},
            "social-boldness": {"high": 4.25, "low": 1.88, "average": 3.13},
            "sociability": {"high": 4.5, "low": 2.5, "average": 3.63},
            "liveliness": {"high": 4.5, "low": 2.5, "average": 3.63},
            "total": {"high": 3.97, "low": 2.41, "average": 3.5}
        },
        "agreeableness": {
            "forgiveness": {"high": 3.88, "low": 1.75, "average": 2.75},
            "gentleness": {"high": 4.13, "low": 2.25, "average": 3.25},
            "flexibility": {"high": 3.75, "low": 1.75, "average": 2.75},
            "patience": {"high": 4.38, "low": 2, "average": 3.25},
            "total": {"high": 3.97, "low": 2.41, "average": 3}
        },
        "conscientiousness": {
            "organization": {"high": 4.38, "low": 2.13, "average": 3.38},
            "diligence": {"high": 4.71, "low": 2.99, "average": 3.88},
            "perfectionism": {"high": 4.38, "low": 2.38, "average": 3.63},
            "prudence": {"high": 4, "low": 2.13, "average": 3.25},
            "total": {"high": 3.97, "low": 2.41, "average": 3.31}
        },
        "openness-to-experience": {
            "aesthetic-appreciation": {"high": 4.38, "low": 2, "average": 3.25},
            "inquisitiveness": {"high": 4.38, "low": 1.88, "average": 3.13},
            "creativity": {"high": 4.63, "low": 2.25, "average": 3.63},
            "unconventionality": {"high": 4.25, "low": 2.63, "average": 3.38},
            "total": {"high": 3.97, "low": 2.41, "average": 3.22}
        },
        "interstitial": {"altruism": {"high": 3, "low": 3, "average": 3.88}}
    }
    _keys = {
        "honesty-humility": {
            "sincerity": ["6R", "30", "54R", "78"],
            "fairness": ["12R", "36R", "60", "84R"],
            "greed-avoidance": ["18", "42R", "66R", "90R"],
            "modesty": ["24", "48", "72R", "96R"]
        },
        "emotionality": {
            "fearfulness": ["5", "29R", "53", "77R"],
            "anxiety": ["11", "35R", "59R", "83"],
            "dependence": ["17", "41R", "65", "89R"],
            "sentimentality": ["23", "47", "71", "95R"]
        },
        "extraversion": {
            "social-self-esteem": ["4", "28", "52R", "76R"],
            "social-boldness": ["10R", "34", "58", "82R"],
            "sociability": ["16R", "40", "64", "88"],
            "liveliness": ["22", "46", "70R", "94R"]
        },
        "agreeableness": {
            "forgiveness": ["3", "27", "51R", "75R"],
            "gentleness": ["9R", "33", "57", "81"],
            "flexibility": ["15R", "39", "63R", "87R"],
            "patience": ["21R", "45", "69", "93R"]
        },
        "conscientiousness": {
            "organization": ["2", "26", "50R", "74R"],
            "diligence": ["8", "32", "56R", "80R"],
            "perfectionism": ["14", "38R", "62", "86"],
            "prudence": ["20R", "44R", "68", "92R"]
        },
        "openness-to-experience": {
            "aesthetic-appreciation": ["1R", "25R", "49", "73"],
            "inquisitiveness": ["7", "31", "55R", "79R"],
            "creativity": ["13R", "37", "61", "85R"],
            "unconventionality": ["19R", "43", "67", "91R"]
        },
        "interstitial": {"altruism": ["97", "98", "99R", "100R"]}
    }

    questions = ['I would be quite bored by a visit to an art gallery.',
                 'I clean my office or home quite frequently.',
                 'I rarely hold a grudge, even against people who have badly wronged me.',
                 'I feel reasonably satisfied with myself overall.',
                 'I would feel afraid if I had to travel in bad weather conditions.',
                 'If I want something from a person I dislike, I will act very nicely toward '
                 'that person in order to get it.',
                 "I'm interested in learning about the history and politics of other "
                 'countries.',
                 'When working, I often set ambitious goals for myself.',
                 'People sometimes tell me that I am too critical of others.',
                 'I rarely express my opinions in group meetings.',
                 "I sometimes can't help worrying about little things.",
                 'If I knew that I could never get caught, I would be willing to steal a '
                 'million dollars.',
                 'I would like a job that requires following a routine rather than being '
                 'creative. ',
                 'I often check my work over repeatedly to find any mistakes.',
                 "People sometimes tell me that I'm too stubborn.",
                 'I avoid making "small talk" with people.',
                 'When I suffer from a painful experience, I need someone to make me feel '
                 'comfortable.',
                 'Having a lot of money is not especially important to me.',
                 'I think that paying attention to radical ideas is a waste of time.',
                 'I make decisions based on the feeling of the moment rather than on careful '
                 'thought.',
                 'People think of me as someone who has a quick temper.',
                 'I am energetic nearly all the time.',
                 'I feel like crying when I see other people crying.',
                 'I am an ordinary person who is no better than others.',
                 "I wouldn't spend my time reading a book of poetry.",
                 'I plan ahead and organize things, to avoid scrambling at the last minute.',
                 'My attitude toward people who have treated me badly is "forgive and forget".',
                 'I think that most people like some aspects of my personality.',
                 'I don’t mind doing jobs that involve dangerous work.',
                 "I wouldn't use flattery to get a raise or promotion at work, even if I "
                 'thought it would succeed.',
                 'I enjoy looking at maps of different places.',
                 'I often push myself very hard when trying to achieve a goal.',
                 'I generally accept people’s faults without complaining about them.',
                 "In social situations, I'm usually the one who makes the first move.",
                 'I worry a lot less than most people do.',
                 'I would be tempted to buy stolen property if I were financially tight.',
                 'I would enjoy creating a work of art, such as a novel, a song, or a '
                 'painting.',
                 "When working on something, I don't pay much attention to small details.",
                 'I am usually quite flexible in my opinions when people disagree with me.',
                 'I enjoy having lots of people around to talk with.',
                 'I can handle difficult situations without needing emotional support from '
                 'anyone else.',
                 'I would like to live in a very expensive, high-class neighborhood.',
                 'I like people who have unconventional views.',
                 "I make a lot of mistakes because I don't think before I act.",
                 'I rarely feel anger, even when people treat me quite badly.',
                 'On most days, I feel cheerful and optimistic.',
                 "When someone I know well is unhappy, I can almost feel that person's pain "
                 'myself.',
                 'I wouldn’t want people to treat me as though I were superior to them.',
                 'If I had the opportunity, I would like to attend a classical music concert.',
                 'People often joke with me about the messiness of my room or desk.',
                 'If someone has cheated me once, I will always feel suspicious of that '
                 'person.',
                 'I feel that I am an unpopular person.',
                 'When it comes to physical danger, I am very fearful.',
                 "If I want something from someone, I will laugh at that person's worst jokes.",
                 'I would be very bored by a book about the history of science and '
                 'technology.  ',
                 'Often when I set a goal, I end up quitting without having reached it.',
                 'I tend to be lenient in judging other people.',
                 "When I'm in a group of people, I'm often the one who speaks on behalf of the "
                 'group.',
                 'I rarely, if ever, have trouble sleeping due to stress or anxiety.',
                 'I would never accept a bribe, even if it were very large.',
                 'People have often told me that I have a good imagination.',
                 'I always try to be accurate in my work, even at the expense of time.',
                 'When people tell me that I’m wrong, my first reaction is to argue with them.',
                 'I prefer jobs that involve active social interaction to those that involve '
                 'working alone.',
                 'Whenever I feel worried about something, I want to share my concern with '
                 'another person.',
                 'I would like to be seen driving around in a very expensive car.',
                 'I think of myself as a somewhat eccentric person.',
                 'I don’t allow my impulses to govern my behavior.',
                 'Most people tend to get angry more quickly than I do.',
                 'People often tell me that I should try to cheer up.',
                 'I feel strong emotions when someone close to me is going away for a long '
                 'time.',
                 'I think that I am entitled to more respect than the average person is.',
                 'Sometimes I like to just watch the wind as it blows through the trees.',
                 'When working, I sometimes have difficulties due to being disorganized.',
                 'I find it hard to fully forgive someone who has done something mean to me.',
                 'I sometimes feel that I am a worthless person.',
                 "Even in an emergency I wouldn't feel like panicking.",
                 "I wouldn't pretend to like someone just to get that person to do favors for "
                 'me.',
                 'I’ve never really enjoyed looking through an encyclopedia.',
                 'I do only the minimum amount of work needed to get by. ',
                 'Even when people make a lot of mistakes, I rarely say anything negative.',
                 'I tend to feel quite self-conscious when speaking in front of a group of '
                 'people.',
                 'I get very anxious when waiting to hear about an important decision.',
                 'I’d be tempted to use counterfeit money, if I were sure I could get away '
                 'with it.',
                 "I don't think of myself as the artistic or creative type.",
                 'People often call me a perfectionist.',
                 'I find it hard to compromise with people when I really think I’m right.',
                 'The first thing that I always do in a new place is to make friends.',
                 'I rarely discuss my problems with other people.',
                 'I would get a lot of pleasure from owning expensive luxury goods.',
                 'I find it boring to discuss philosophy.',
                 'I prefer to do whatever comes to mind, rather than stick to a plan.',
                 'I find it hard to keep my temper when people insult me.',
                 'Most people are more upbeat and dynamic than I generally am.',
                 'I remain unemotional even in situations where most people get very '
                 'sentimental.',
                 'I want people to know that I am an important person of high status.',
                 'I have sympathy for people who are less fortunate than I am.',
                 'I try to give generously to those in need.',
                 'It wouldn’t bother me to harm someone I didn’t like.',
                 'People see me as a hard-hearted person.']
    traits = {
        "honesty-humility": {
            "facets": ["sincerity", "fairness", "greed-avoidance", "modesty"],
            "adjectives": ["sincere", "honest", "faithful", "loyal", "modest", "unassuming", "deceitful",
                           "greedy", "pretentious", "hypocritical", "boastful", "pompous"]

        },

        "emotionality": {
            "facets": ["fearfulness", "anxiety", "dependence", "sentimentality"],
            "adjectives": ["emotional", "oversensitive", "sentimental", "fearful", "anxious", "vulnerable", "tough",
                           "independent", "self-assured", "stable"]

        },
        "extraversion": {
            "facets": ["social-self-esteem", "social-boldness", "sociability", "liveliness"],
            "adjectives": ["outgoing", "lively", "extraverted", "sociable", "talkative", "cheerful", "active", "shy",
                           "passive", "withdrawn", "introverted", "quiet", "reserved"]

        },
        "agreeableness": {
            "facets": ["forgivingness", "gentleness", "flexibility", "patience"],
            "adjectives": ["patient", "tolerant", "peaceful", "mild", "agreeable",
                           "lenient", "gentle", "quarrelsome", "stubborn", "choleric"]

        },
        "conscientiousness": {
            "facets": ["organization", "diligence", "perfectionism", "prudence"],
            "adjectives": ["organized", "disciplined", "diligent", "careful", "thorough", "precise",
                           "sloppy", "negligent", "reckless", "azy", "irresponsible", "absent-minded"]

        },
        "openness-to-experience": {
            "facets": ["aesthetic-appreciation", "inquisitiveness", "ceativity", "unconventionality"],
            "adjectives": ["intellectual", "creative", "unconventional", "innovative",
                           "ironic", "unimaginative", "conventional"]

        }
    }
    scale = {
        "honesty-humility": {
            "sincerity": "tendency to be genuine in interpersonal relations. Low scorers will flatter others or pretend to like them in order to obtain favors, whereas high scorers are unwilling to manipulate others.",
            "fairness": "tendency to avoid fraud and corruption. Low scorers are willing to gain by cheating or stealing, whereas high scorers are unwilling to take advantage of other individuals or of society at large.",
            "greed-avoidance": "tendency to be uninterested in possessing lavish wealth, luxury goods, and signs of high social status. Low scorers want to enjoy and to display wealth and privilege, whereas high scorers are not especially motivated by monetary or social-status considerations.",
            "modesty": "tendency to be modest and unassuming. Low scorers consider themselves as superior and as entitled to privileges that others do not have, whereas high scorers view themselves as ordinary people without any claim to special treatment"
        },
        "emotionality": {
            "fearfulness": "tendency to experience fear. Low scorers feel little fear of injury and are relatively tough, brave, and insensitive to physical pain, whereas high scorers are strongly inclined to avoid physical harm.",
            "anxiety": " tendency to worry in a variety of contexts. Low scorers feel little stress in response to difficulties, whereas high scorers tend to become preoccupied even by relatively minor problems",
            "dependence": "one's need for emotional support from others. Low scorers feel self-assured and able to deal with problems without any help or advice, whereas high scorers want to share their difficulties with those who will provide encouragement and comfort.",
            "sentimentality": " tendency to feel strong emotional bonds with others. Low scorers feel little emotion when saying good-bye or in reaction to the concerns of others, whereas high scorers feel strong emotional attachments and an empathic sensitivity to the feelings of others."
        },
        "extraversion": {
            "social-self-esteem": "tendency to have positive self-regard, particularly in social contexts. High scorers are generally satisfied with themselves and consider themselves to have likable qualities, whereas low scorers tend to have a sense of personal worthlessness and to see themselves as unpopular.",
            "social-boldness": "one's comfort or confidence within a variety of social situations. Low scorers feel shy or awkward in positions of leadership or when speaking in public, whereas high scorers are willing to approach strangers and are willing to speak up within group settings.",
            "sociability": "tendency to enjoy conversation, social interaction, and parties. Low scorers generally prefer solitary activities and do not seek out conversation, whereas high scorers enjoy talking, visiting, and celebrating with others.",
            "liveliness": " one's typical enthusiasm and energy. Low scorers tend not to feel especially cheerful or dynamic, whereas high scorers usually experience a sense of optimism and high spirits."
        },
        "agreeableness": {
            "forgiveness": "one's willingness to feel trust and liking toward those who may have caused one harm. Low scorers tend 'hold a grudge' against those who have offended them, whereas high scorers are usually ready to trust others again and to re-establish friendly relations after having been treated badly.",
            "gentleness": "tendency to be mild and lenient in dealings with other people. Low scorers tend to be critical in their evaluations of others, whereas high scorers are reluctant to judge others harshly.",
            "flexibility": "one's willingness to compromise and cooperate with others. Low scorers are seen as stubborn and are willing to argue, whereas high scorers avoid arguments and accommodate others' suggestions, even when these may be unreasonable.",
            "patience": "tendency to remain calm rather than to become angry. Low scorers tend to lose their tempers quickly, whereas high scorers have a high threshold for feeling or expressing anger."
        },
        "conscientiousness": {
            "organization": "tendency to seek order, particularly in one's physical surroundings. Low scorers tend to be sloppy and haphazard, whereas high scorers keep things tidy and prefer a structured approach to tasks.",
            "diligence": "tendency to work hard. Low scorers have little self-discipline and are not strongly motivated to achieve, whereas high scorers have a strong 'work ethic' and are willing to exert themselves.",
            "perfectionism": "tendency to be thorough and concerned with details. Low scorers tolerate some errors in their work and tend to neglect details, whereas high scorers check carefully for mistakes and potential improvements.",
            "prudence": "tendency to deliberate carefully and to inhibit impulses. Low scorers act on impulse and tend not to consider consequences, whereas high scorers consider their options carefully and tend to be cautious and self-controlled."
        },
        "openness-to-experience": {
            "aesthetic-appreciation": "one's enjoyment of beauty in art and in nature. Low scorers tend not to become absorbed in works of art or in natural wonders, whereas high scorers have a strong appreciation of various art forms and of natural wonders.",
            "inquisitiveness": "tendency to seek information about, and experience with, the natural and human world. Low scorers have little curiosity about the natural or social sciences, whereas high scorers read widely and are interested in travel.",
            "creativity": "one's preference for innovation and experiment. Low scorers have little inclination for original thought, whereas high scorers actively seek new solutions to problems and express themselves in art.",
            "unconventionality": "tendency to accept the unusual. Low scorers avoid eccentric or nonconforming persons, whereas high scorers are receptive to ideas that might seem strange or radical.",
        },
        "interstitial": {
            "altruism": "tendency to be sympathetic and soft-hearted toward others. High scorers avoid causing harm and react with generosity toward those who are weak or in need of help, whereas low scorers are not upset by the prospect of hurting others and may be seen as hard-hearted."}
    }

    @staticmethod
    def score(answers):
        result = {
            "honesty-humility": {
                "sincerity": 0,
                "fairness": 0,
                "greed-avoidance": 0,
                "modesty": 0,
                "average": 0
            },
            "emotionality": {
                "fearfulness": 0,
                "anxiety": 0,
                "dependence": 0,
                "sentimentality": 0,
                "average": 0
            },
            "extraversion": {
                "social-self-esteem": 0,
                "social-boldness": 0,
                "sociability": 0,
                "liveliness": 0,
                "average": 0
            },
            "agreeableness": {
                "forgiveness": 0,
                "gentleness": 0,
                "flexibility": 0,
                "patience": 0,
                "average": 0
            },
            "conscientiousness": {
                "organization": 0,
                "diligence": 0,
                "perfectionism": 0,
                "prudence": 0,
                "average": 0
            },
            "openness-to-experience": {
                "aesthetic-appreciation": 0,
                "inquisitiveness": 0,
                "creativity": 0,
                "unconventionality": 0,
                "average": 0
            },
            "interstitial": {
                "altruism": 0,
                "average": 0}
        }
        for k in Hexaco._keys:
            for s in Hexaco._keys[k]:
                questions = Hexaco._keys[k][s]
                for q in questions:
                    if q.isdigit():
                        a = int(q) - 1
                        result[k][s] += int(answers[a])
                    else:
                        a = int(q.replace("R", "")) - 1
                        # reverse
                        if int(answers[a]) == 5:
                            answers[a] = 1
                        elif int(answers[a]) == 4:
                            answers[a] = 2
                        elif int(answers[a]) == 2:
                            answers[a] = 4
                        elif int(answers[a]) == 5:
                            answers[a] = 1
                        result[k][s] += int(answers[a])
                result[k][s] = result[k][s] / len(questions)
                result[k]["average"] += result[k][s]
            result[k]["average"] = result[k]["average"] / len(Hexaco._keys[k])

        return result

    @staticmethod
    def test():
        ans = {1: "strongly disagree", 2: "disagree", 3: "neutral", 4: "agree", 5: "strongly agree"}
        print("Hexaco Test\n")
        print(ans)
        print("Start:\n")
        answers = []
        for q in Hexaco.questions:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 6
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return Hexaco.score(answers)

    @staticmethod
    def test_random():
        ans = {1: "strongly disagree", 2: "disagree", 3: "neutral", 4: "agree", 5: "strongly agree"}
        print("Hexaco Test\n")
        print(ans)
        print("Start:\n")
        answers = []
        for q in Hexaco.questions:
            a = random.randint(1, 5)
            print("Q: " + q, "A: " + ans[a])
            answers.append(a)
        return Hexaco.score(answers)


if __name__ == "__main__":
    from lilacs.processing.comprehension.reasoning import LILACSMultipleChoiceReasoner

    l = LILACSMultipleChoiceReasoner()

    def dirty12_test():
        choices = ["strongly disagree",
                   "disagree",
                   "slightly disagree",
                   "neutral",
                   "slightly agree",
                   "agree",
                   "strongly agree"]
        te_answers = []
        vec_answers = []
        for q in Dirty12.questions:
            a1 = l.vector_similarity(q, choices)
            #a2 = l.textual_entailment(q, choices)
            vec_answers.append(a1 + 1)
            #te_answers.append(a2 + 1)
            print(q, choices[a1])
            #print(q, choices[a1], choices[a2])
        #print("textual entailment score:", Dirty12.score(te_answers))
        print("Vector similarity score:", Dirty12.score(vec_answers))

    def hexaco_test():
        choices = ["strongly disagree",
                   "disagree",
                   "neutral",
                   "agree",
                   "strongly agree"]
        te_answers = []
        vec_answers = []
        for q in Hexaco.questions:
            a1 = l.vector_similarity(q, choices)
            #a2 = l.textual_entailment(q, choices)
            vec_answers.append(a1 + 1)
            #te_answers.append(a2 + 1)
            print(q, choices[a1])
            #print(q, choices[a1], choices[a2])
        #print("textual entailment score:", Hexaco.score(te_answers))
        print("Vector similarity score:", Hexaco.score(vec_answers))

    dirty12_test()
    hexaco_test()