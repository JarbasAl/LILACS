from lilacs.sentience.emotions.deepmoji import get_emotions, get_emojis
from lilacs.processing.nlp.sentiment_analysis import get_sentiment
from lilacs.processing.nlp.politness import get_politness


class LILACSEmotionalReactor(object):
    def __init__(self, bus=None):
        self.bus = bus

    @staticmethod
    def sentiment_analysis(text):
        return get_sentiment(text)

    @staticmethod
    def politeness_analysis(text):
        return get_politness(text)

    @staticmethod
    def emotion_analysis(text):
        return get_emotions(text)

    @staticmethod
    def emoji_reaction(text):
        return get_emojis(text)


if __name__ == "__main__":
    from pprint import pprint

    TEST_SENTENCES = ['I love mom\'s cooking',
                      'I love how you never reply back..',
                      'I love cruising with my homies',
                      'I love messing with yo mind!!',
                      'I love you and now you\'re just gone..',
                      'Thank you for your help',
                      'This is shit',
                      'This is the shit']

    LILACS = LILACSEmotionalReactor()

    for text in TEST_SENTENCES:
        print("\n" + text)
        pprint(LILACS.sentiment_analysis(text))
        pprint(LILACS.emotion_analysis(text))
        pprint(LILACS.politness_analysis(text))
        pprint(LILACS.emoji_reaction(text))

    # output
    """
       
I love mom's cooking
3.0
['Zeal', 'Love', 'Joy', 'Remorse']
{'confidence': '91%',
 'isrequest': False,
 'label': 'neutral',
 'text': "I love mom's cooking"}
[':stuck_out_tongue_closed_eyes:',
 ':heart_eyes:',
 ':heart:',
 ':blush:',
 ':yellow_heart:']

I love how you never reply back..
3.0
['Annoyance', 'boredom', 'Despair']
{'confidence': '95%',
 'isrequest': False,
 'label': 'neutral',
 'text': 'I love how you never reply back..'}
[':unamused:',
 ':expressionless:',
 ':angry:',
 ':neutral_face:',
 ':broken_heart:']

I love cruising with my homies
3.0
['Serenity', 'Optimism', 'Awe']
{'confidence': '99%',
 'isrequest': False,
 'label': 'neutral',
 'text': 'I love cruising with my homies'}
[':sunglasses:', ':ok_hand:', ':v:', ':relieved:', ':100:']

I love messing with yo mind!!
3.0
['Delight', 'Pride', 'Bemusement', 'Zeal', 'Disfavor']
{'confidence': '98%',
 'isrequest': False,
 'label': 'neutral',
 'text': 'I love messing with yo mind!!'}
[':stuck_out_tongue_winking_eye:',
 ':smiling_imp:',
 ':smirk:',
 ':wink:',
 ':speak_no_evil:']

I love you and now you're just gone..
3.0
['Despair', 'Disappointment', 'boredom', 'Sadness', 'Pessimism']
{'confidence': '93%',
 'isrequest': False,
 'label': 'neutral',
 'text': "I love you and now you're just gone.."}
[':broken_heart:', ':pensive:', ':disappointed:', ':sleepy:', ':cry:']

Thank you for your help
4.0
['Pride', 'Joy', 'Optimism', 'Delight']
{'confidence': '83%',
 'isrequest': False,
 'label': 'polite',
 'text': 'Thank you for your help'}
[':pray:', ':relaxed:', ':blush:', ':relieved:', ':+1:']

This is shit
-4.0
['Annoyance', 'Outrage', 'boredom', 'Cynicism']
{'confidence': '81%',
 'isrequest': False,
 'label': 'impolite',
 'text': 'This is shit'}
[':angry:', ':rage:', ':disappointed:', ':unamused:', ':triumph:']

This is the shit
-4.0
['Zeal', 'Delight', 'Optimism', 'Serenity', 'Bemusement']
{'confidence': '80%',
 'isrequest': False,
 'label': 'impolite',
 'text': 'This is the shit'}
[':headphones:', ':notes:', ':ok_hand:', ':sunglasses:', ':smirk:']

    """