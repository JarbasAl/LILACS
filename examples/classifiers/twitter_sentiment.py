from os.path import join, exists, dirname
from lilacs.spacy_extensions.classifiers.naive import NaiveBayes
from lilacs.parse.features import LILACSFeaturizer
import string
import re
from nltk.corpus import twitter_samples
from lilacs import nlp


class NaiveTwitterSentiment(NaiveBayes):
    def __init__(self, model_path=join(dirname(__file__),
                                       "naive_twitter_sentiment.pkl")):
        super().__init__()
        if exists(model_path):
            # Accuracy: Accuracy: 0.7044
            self.load(model_path)
        else:
            pos_tweets = twitter_samples.strings('positive_tweets.json')
            neg_tweets = twitter_samples.strings('negative_tweets.json')

            # positive tweets words list
            pos_tweets_set = []
            for tweet in pos_tweets:
                pos_tweets_set.append(self.clean_tweets(tweet))

            # negative tweets words list
            neg_tweets_set = []
            for tweet in neg_tweets:
                neg_tweets_set.append(self.clean_tweets(tweet))

            pos_set = []
            for words in pos_tweets_set:
                pos_set.append((self.get_features(words), 'pos'))

            neg_set = []
            for words in neg_tweets:
                neg_set.append((self.get_features(words), 'neg'))

            test_set = pos_set[:2500] + neg_set[:2500]
            train_set = pos_set[2500:] + neg_set[2500:]

            self.train(train_set)
            print("Accuracy:", self.test(test_set))
            self.save(model_path)

    @staticmethod
    def clean_tweets(tweet):

        from nltk.tokenize import TweetTokenizer

        stopwords_english = nlp.Defaults.stop_words

        # Happy Emoticons
        emoticons_happy = set([
            ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)',
            '=)', ':}',
            ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D',
            '=D',
            '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P',
            ':P', 'X-P',
            'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)',
            '>:-)',
            '<3'
        ])

        # Sad Emoticons
        emoticons_sad = set([
            ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L',
            ':<',
            ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(",
            ':\\', ':-c',
            ':c', ':{', '>:\\', ';('
        ])

        # all emoticons (happy + sad)
        emoticons = emoticons_happy.union(emoticons_sad)
        # remove stock market tickers like $GE
        tweet = re.sub(r'\$\w*', '', tweet)

        # remove old style retweet text "RT"
        tweet = re.sub(r'^RT[\s]+', '', tweet)

        # remove hyperlinks
        tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)

        # remove hashtags
        # only removing the hash # sign from the word
        tweet = re.sub(r'#', '', tweet)

        # tokenize tweets
        tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True,
                                   reduce_len=True)
        tweet_tokens = tokenizer.tokenize(tweet)

        tweets_clean = []
        for word in tweet_tokens:
            if (word not in stopwords_english and  # remove stopwords
                    word not in emoticons and  # remove emoticons
                    word not in string.punctuation):  # remove punctuation
                tweets_clean.append(word)

        return tweets_clean

    def get_features(self, document):
        if isinstance(document, str):
            document = self.clean_tweets(document)
        text = " ".join(document)
        features = LILACSFeaturizer.lexicon_features(text)
        features.update(LILACSFeaturizer.bow_features(text))
        return features


if __name__ == "__main__":
    senti = NaiveTwitterSentiment()
    senti.show_most_informative_features(10)
    """
    Most Informative Features
          contains(love) = True              pos : neg    =      8.3 : 1.0
            contains(hi) = True              pos : neg    =      7.0 : 1.0
          contains(week) = True              pos : neg    =      6.6 : 1.0
        contains(follow) = True              pos : neg    =      6.2 : 1.0
           contains(bad) = True              neg : pos    =      5.7 : 1.0
         contains(thank) = True              pos : neg    =      5.4 : 1.0
        contains(friday) = True              pos : neg    =      5.0 : 1.0
          contains(want) = True              neg : pos    =      4.6 : 1.0
          emotion(anger) = True              neg : pos    =      3.8 : 1.0
         contains(great) = True              pos : neg    =      3.7 : 1.0
    """

    TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      "You are awesome!",
                      'This is shit',  # angry
                      'This is the shit']  # excited
    for t in TEST_SENTENCES:
        print("\n" + t)
        print(senti.predict(t))
    exit()
