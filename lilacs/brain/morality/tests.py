import random


class MFQ20(object):
    key = """
Harm:
    EMOTIONALLY - Whether or not someone suffered emotionally 
    WEAK - Whether or not someone cared for someone weak or vulnerable
Fairness:
    TREATED - Whether or not some people were treated differently than others
    UNFAIRLY - Whether or not someone acted unfairly
Ingroup:
    LOVECOUNTRY - Whether or not someone’s action showed love for his or her country 
    BETRAY - Whether or not someone did something to betray his or her group
Authority:
    RESPECT - Whether or not someone showed a lack of respect for authority 
    TRADITIONS - Whether or not someone conformed to the traditions of society 
Purity:
    DECENCY - Whether or not someone violated standards of purity and decency
    DISGUSTING - Whether or not someone did something disgusting
  
Harm:
    COMPASSION - Compassion for those who are suffering is the most crucial virtue.
    ANIMAL - One of the worst things a person could do is hurt a defenseless animal.
Fairness:
    FAIRLY - When the government makes laws, the number one principle should be ensuring that everyone is treated fairly.
    JUSTICE – Justice is the most important requirement for a society. 
Ingroup:
    HISTORY - I am proud of my country’s history.
    FAMILY - People should be loyal to their family members, even when they have done something wrong.  
Authority:
    KIDRESPECT - Respect for authority is something all children need to learn.
    SEXROLES - Men and women each have different roles to play in society.
Purity:
    HARMLESSDG - People should not do things that are disgusting, even if no one is harmed. 
    UNNATURAL - I would call some acts wrong on the grounds that they are unnatural.

"""

    questions_part1 = ['Whether or not someone suffered emotionally',
                       'Whether or not some people were treated differently than others',
                       'Whether or not someone’s action showed love for his or her country',
                       'Whether or not someone showed a lack of respect for authority',
                       'Whether or not someone violated standards of purity and decency',
                       'Whether or not someone was good at math',
                       'Whether or not someone cared for someone weak or vulnerable',
                       'Whether or not someone acted unfairly',
                       'Whether or not someone did something to betray his or her group',
                       'Whether or not someone conformed to the traditions of society',
                       'Whether or not someone did something disgusting']

    questions_part2 = [
        'Compassion for those who are suffering is the most crucial virtue.',
        'When the government makes laws, the number one principle should be ensuring '
        'that everyone is treated fairly.',
        'I am proud of my country’s history.',
        'Respect for authority is something all children need to learn.',
        'People should not do things that are disgusting, even if no one is harmed.',
        'It is better to do good than to do bad.',
        'One of the worst things a person could do is hurt a defenseless animal.',
        'Justice is the most important requirement for a society.',
        'People should be loyal to their family members, even when they have done '
        'something wrong.',
        'Men and women each have different roles to play in society.',
        'I would call some acts wrong on the grounds that they are unnatural.']

    @staticmethod
    def part1():
        intro = """
        Part 1. When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? Please rate each statement using this scale:

       [0] = not at all relevant (This consideration has nothing to do with my judgments of right and wrong)
       [1] = not very relevant
       [2] = slightly relevant
       [3] = somewhat relevant
       [4] = very relevant
       [5] = extremely relevant (This is one of the most important factors when I judge right and wrong)"""
        print(intro)
        answers = []
        for q in MFQ30.questions_part1:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 8
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return answers

    @staticmethod
    def part2():
        intro = """
        Part 2. Please read the following sentences and indicate your agreement or disagreement:

       [0] = Strongly disagree
       [1] = Moderately disagree
       [2] = Slightly disagree
       [3] = Slightly agree
       [4] = Moderately agree
       [5] = Strongly agree"""
        print(intro)
        answers = []
        for q in MFQ30.questions_part2:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 8
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return answers

    @staticmethod
    def score(answers):
        """COMPUTE MFQ_HARM_AVG = MEAN(emotionally,weak,animal,compassion) .
        COMPUTE MFQ_FAIRNESS_AVG = MEAN(unfairly,treated,justice,fairly) .
        COMPUTE MFQ_INGROUP_AVG = MEAN(betray,lovecountry,history,family) .
        COMPUTE MFQ_AUTHORITY_AVG = MEAN(traditions,respect,sexroles,kidrespect) .
        COMPUTE MFQ_PURITY_AVG = MEAN(disgusting,decency,harmlessdg,unnatural) .
        COMPUTE MFQ_PROGRESSIVISM = MEAN (MFQ_HARM_AVG, MFQ_FAIRNESS_AVG) - MEAN (MFQ_INGROUP_AVG, MFQ_AUTHORITY_AVG, MFQ_PURITY_AVG).
        execute.."""
        score = {"harm": 0, "fairness": 0, "ingroup": 0, "authority": 0,
                 "purity": 0, "progressivism": 0}
        harm_answers = answers[:2] + answers[10:12]
        fairness_answers = answers[2:4] + answers[12:14]
        ingroup_answers = answers[4:6] + answers[16:18]
        authority_answers = answers[6:8] + answers[18:20]
        purity_answers = answers[8:10] + answers[20:22]

        score["harm"] = sum(harm_answers) / len(harm_answers)
        score["fairness"] = sum(fairness_answers) / len(fairness_answers)
        score["ingroup"] = sum(ingroup_answers) / len(ingroup_answers)
        score["authority"] = sum(authority_answers) / len(authority_answers)
        score["purity"] = sum(purity_answers) / len(purity_answers)
        score["progressivism"] = \
            ((score["harm"] + score["fairness"]) / 2) - \
            ((score["ingroup"] + score["authority"] + score["purity"]) / 3)
        return score

    @staticmethod
    def test():
        return MFQ20.score(MFQ20.part1() + MFQ20.part2())

    @staticmethod
    def test_random():
        print("MFQ20 Test")

        intro = """
          Part 1. When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? Please rate each statement using this scale:

         [0] = not at all relevant (This consideration has nothing to do with my judgments of right and wrong)
         [1] = not very relevant
         [2] = slightly relevant
         [3] = somewhat relevant
         [4] = very relevant
         [5] = extremely relevant (This is one of the most important factors when I judge right and wrong)
         """
        print(intro)
        answers = []
        for q in MFQ20.questions_part1:
            a = random.randint(0, 5)
            print("Q: ", q, "A: ", a)
            answers.append(a)
        intro = """
          Part 2. Please read the following sentences and indicate your agreement or disagreement:

         [0] = Strongly disagree
         [1] = Moderately disagree
         [2] = Slightly disagree
         [3] = Slightly agree
         [4] = Moderately agree
         [5] = Strongly agree
         """
        print(intro)
        for q in MFQ20.questions_part2:
            a = random.randint(0, 5)
            print("Q: ", q, "A: ", a)
            answers.append(a)
        return MFQ20.score(answers)


class MFQ30(object):
    key = """Harm:
    EMOTIONALLY - Whether or not someone suffered emotionally 
    WEAK - Whether or not someone cared for someone weak or vulnerable
    CRUEL - Whether or not someone was cruel

Fairness:
    TREATED - Whether or not some people were treated differently than others
    UNFAIRLY - Whether or not someone acted unfairly
    RIGHTS - Whether or not someone was denied his or her rights

Ingroup:
    LOVECOUNTRY - Whether or not someone’s action showed love for his or her country 
    BETRAY - Whether or not someone did something to betray his or her group
    LOYALTY - Whether or not someone showed a lack of loyalty

Authority:
    RESPECT - Whether or not someone showed a lack of respect for authority 
    TRADITIONS - Whether or not someone conformed to the traditions of society 
    CHAOS - Whether or not an action caused chaos or disorder

Purity:
    DECENCY - Whether or not someone violated standards of purity and decency
    DISGUSTING - Whether or not someone did something disgusting
    GOD - Whether or not someone acted in a way that God would approve of
Harm:
    COMPASSION - Compassion for those who are suffering is the most crucial virtue.
    ANIMAL - One of the worst things a person could do is hurt a defenseless animal.
    KILL - It can never be right to kill a human being.

Fairness:
    FAIRLY - When the government makes laws, the number one principle should be ensuring that everyone is treated fairly.
    JUSTICE – Justice is the most important requirement for a society. 
    RICH - I think it’s morally wrong that rich children inherit a lot of money while poor children inherit nothing.

Ingroup:
    HISTORY - I am proud of my country’s history.
    FAMILY - People should be loyal to their family members, even when they have done something wrong.  
    TEAM - It is more important to be a team player than to express oneself.

Authority:
    KIDRESPECT - Respect for authority is something all children need to learn.
    SEXROLES - Men and women each have different roles to play in society.
    SOLDIER - If I were a soldier and disagreed with my commanding officer’s orders, I would obey anyway because that is my duty.

Purity:
    HARMLESSDG - People should not do things that are disgusting, even if no one is harmed. 
    UNNATURAL - I would call some acts wrong on the grounds that they are unnatural.
    CHASTITY - Chastity is an important and valuable virtue. 

"""

    questions_part1 = ['Whether or not someone suffered emotionally',
                       'Whether or not some people were treated differently than others',
                       'Whether or not someone’s action showed love for his or her country',
                       'Whether or not someone showed a lack of respect for authority',
                       'Whether or not someone violated standards of purity and decency',
                       'Whether or not someone was good at math',
                       'Whether or not someone cared for someone weak or vulnerable',
                       'Whether or not someone acted unfairly',
                       'Whether or not someone did something to betray his or her group',
                       'Whether or not someone conformed to the traditions of society',
                       'Whether or not someone did something disgusting',
                       'Whether or not someone was cruel',
                       'Whether or not someone was denied his or her rights',
                       'Whether or not someone showed a lack of loyalty',
                       'Whether or not an action caused chaos or disorder',
                       'Whether or not someone acted in a way that God would approve of']

    questions_part2 = [
        'Compassion for those who are suffering is the most crucial virtue.',
        'When the government makes laws, the number one principle should be ensuring '
        'that everyone is treated fairly.',
        'I am proud of my country’s history.',
        'Respect for authority is something all children need to learn.',
        'People should not do things that are disgusting, even if no one is harmed.',
        'It is better to do good than to do bad.',
        'One of the worst things a person could do is hurt a defenseless animal.',
        'Justice is the most important requirement for a society.',
        'People should be loyal to their family members, even when they have done '
        'something wrong.',
        'Men and women each have different roles to play in society.',
        'I would call some acts wrong on the grounds that they are unnatural.',
        'It can never be right to kill a human being.',
        'I think it’s morally wrong that rich children inherit a lot of money while '
        'poor children inherit nothing.',
        'It is more important to be a team player than to express oneself.',
        'If I were a soldier and disagreed with my commanding officer’s orders, I '
        'would obey anyway because that is my duty.',
        'Chastity is an important and valuable virtue.']

    @staticmethod
    def part1():
        intro = """
        Part 1. When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? Please rate each statement using this scale:

       [0] = not at all relevant (This consideration has nothing to do with my judgments of right and wrong)
       [1] = not very relevant
       [2] = slightly relevant
       [3] = somewhat relevant
       [4] = very relevant
       [5] = extremely relevant (This is one of the most important factors when I judge right and wrong)"""
        print(intro)
        answers = []
        for q in MFQ30.questions_part1:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 8
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return answers

    @staticmethod
    def part2():
        intro = """
        Part 2. Please read the following sentences and indicate your agreement or disagreement:
        
       [0] = Strongly disagree
       [1] = Moderately disagree
       [2] = Slightly disagree
       [3] = Slightly agree
       [4] = Moderately agree
       [5] = Strongly agree"""
        print(intro)
        answers = []
        for q in MFQ30.questions_part2:
            answered = False
            while not answered:
                a = input(q)
                try:
                    assert 0 < int(a) < 8
                    answers.append(int(a))
                    answered = True
                except:
                    pass
        return answers

    @staticmethod
    def score(answers):
        """*Moral Foundations Questionnaire syntax for calculating foundation scores for MFQ30, August 22 2008.

        COMPUTE MFQ_HARM_AVG = MEAN(emotionally,weak,cruel,animal,kill,compassion) .
        COMPUTE MFQ_FAIRNESS_AVG = MEAN(rights,unfairly,treated,justice,fairly,rich) .
        COMPUTE MFQ_INGROUP_AVG = MEAN(loyalty,betray,lovecountry,team,history,family) .
        COMPUTE MFQ_AUTHORITY_AVG = MEAN(traditions,respect,chaos,sexroles,soldier,kidrespect) .
        COMPUTE MFQ_PURITY_AVG = MEAN(disgusting,decency,god,harmlessdg,unnatural,chastity) .
        COMPUTE MFQ_PROGRESSIVISM = MEAN (MFQ_HARM_AVG, MFQ_FAIRNESS_AVG) - MEAN (MFQ_INGROUP_AVG, MFQ_AUTHORITY_AVG, MFQ_PURITY_AVG).
        execute."""
        score = {"harm": 0, "fairness": 0, "ingroup": 0, "authority": 0,
                 "purity": 0, "progressivism": 0}
        harm_answers = answers[:3] + answers[15:18]
        fairness_answers = answers[3:6] + answers[18:21]
        ingroup_answers = answers[6:9] + answers[21:24]
        authority_answers = answers[9:12] + answers[24:27]
        purity_answers = answers[12:15] + answers[27:30]

        score["harm"] = sum(harm_answers) / len(harm_answers)
        score["fairness"] = sum(fairness_answers) / len(fairness_answers)
        score["ingroup"] = sum(ingroup_answers) / len(ingroup_answers)
        score["authority"] = sum(authority_answers) / len(authority_answers)
        score["purity"] = sum(purity_answers) / len(purity_answers)
        score["progressivism"] = \
            ((score["harm"] + score["fairness"]) / 2) - \
            ((score["ingroup"] + score["authority"] + score["purity"]) / 3)
        return score

    @staticmethod
    def test():
        return MFQ30.score(MFQ30.part1() + MFQ30.part2())

    @staticmethod
    def test_random():
        print("MFQ30 Test")

        intro = """
          Part 1. When you decide whether something is right or wrong, to what extent are the following considerations relevant to your thinking? Please rate each statement using this scale:

         [0] = not at all relevant (This consideration has nothing to do with my judgments of right and wrong)
         [1] = not very relevant
         [2] = slightly relevant
         [3] = somewhat relevant
         [4] = very relevant
         [5] = extremely relevant (This is one of the most important factors when I judge right and wrong)
         """
        print(intro)
        answers = []
        for q in MFQ30.questions_part1:
            a = random.randint(0, 5)
            print("Q: ", q, "A: ", a)
            answers.append(a)
        intro = """
          Part 2. Please read the following sentences and indicate your agreement or disagreement:

         [0] = Strongly disagree
         [1] = Moderately disagree
         [2] = Slightly disagree
         [3] = Slightly agree
         [4] = Moderately agree
         [5] = Strongly agree
         """
        print(intro)
        for q in MFQ30.questions_part2:
            a = random.randint(0, 5)
            print("Q: ", q, "A: ", a)
            answers.append(a)
        return MFQ30.score(answers)



if __name__ == "__main__":
    from pprint import pprint

    pprint(MFQ20.test_random())
