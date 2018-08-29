# LILACS - EMOTIONS

do you want your bot to pass the turing test?

Bots should be able to detect sarcasm and have emotional awareness

# Emotions as bias

Contexts change and provide data, but the way they provide bias is in the form or emotions

but how do we represent emotions in LILACS?

reference - https://positivepsychologyprogram.com/emotion-wheel/

    
# Plutchik's wheel of emotions

In 1980, Robert Plutchik constructed diagram of emotions visualising eight basic emotions: joy, trust, fear, surprise, sadness, disgust, anger and anticipation. 

Emotions can be mild or intense; for example, distraction is a mild form of surprise, and rage is an intense form of anger.

![dyads](https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Plutchik-wheel.svg/350px-Plutchik-wheel.svg.png  "dyads")

The 2012 book The Hourglass of Emotions was based on Robert Plutchik's model, but categorised the emotions into four sentic dimensions. 
It contrasted anger, anticipation, joy, and trust as positive emotions, and fear, surprise, sadness and disgust as negative.

| dimension/flow |      3     |       2      |      1     |      -1      |    -2    |     -3    |
|:--------------:|:----------:|:------------:|:----------:|:------------:|:--------:|:---------:|
|   sensitivity  |    rage    |     anger    |  annoyance | apprehension |   fear   |   terror  |
|    attention   |  vigilance | anticipation |  interest  |  distraction | surprise | amazement |
|  pleasantness  |   ecstasy  |      joy     |  serenity  |  pensiveness |  sadness |   grief   |
|    aptitude    | admiration |     trust    | acceptance |    boredom   |  disgust |  loathing |


# Emotion Algebra

Based on this some new data types were created, with lilacs you can just add emotions and do all kinds of algebra with it!

- [dimensions](/examples/dimension_algebra.py)
- [emotions](/examples/emotion_algebra.py)
- [feelings](/examples/feeling_algebra.py)
- [composite emotions](/examples/composite_emotion_algebra.py)


# Tagging the emotion in the user

Now that we have the tools to handle emotions, lets understand the user emotion and use it as context

LILACS come with a big LEXICON, you can analyze individual words

        def get_color(word):
            if word in LEXICON:
                return LEXICON[word]["color"]
            return None
        
        
        def get_emotion(word):
            if word in LEXICON:
                return LEXICON[word]["emotion"]
            return None
        
        
        def get_sentiment(word):
            if word in LEXICON:
                return LEXICON[word]["sentiment"]
            return None
        
        
        def get_subjectivity(word):
            if word in LEXICON:
                return LEXICON[word]["subjectivity"]
            return None
        
        
        def get_orientation(word):
            if word in LEXICON:
                return LEXICON[word]["orientation"]
            return None
            
 This does not take us too far, using individual words we don't capture nuances of speech
 
 Let's use trained a [classifier](https://www.paralleldots.com/api/demos)
 
        
        
        TEST_SENTENCES = ['I love mom\'s cooking',  # happy
                      'I love how you never reply back..',  # sarcasm
                      'I love cruising with my homies',  # excited
                      'I love messing with yo mind!!',  # fear
                      'I love you and now you\'re just gone..',  # sad
                      'This is shit',  # angry
                      'This is the shit']  # excited
        for t in TEST_SENTENCES:
            print(best_emotion(t))
          
        """ ## output  ##
        joy
        annoyance
        joy
        anticipation
        sadness
        anger
        joy
        """
            

 
 # Emoji processing
 
But maybe we can do even better, emojis capture the nuances of emotion, and deepmoji gives excelent results!
  
  
      TEST_SENTENCES = ['I love mom\'s cooking',
                          'I love how you never reply back..',
                          'I love cruising with my homies',
                          'I love messing with yo mind!!',
                          'I love you and now you\'re just gone..',
                          'This is shit',
                          'This is the shit']
        for t in TEST_SENTENCES:
            print(get_emojis(t))
            

The output captures the nuances of emotion better than a simple classifier

  
[':stuck_out_tongue_closed_eyes:', ':heart_eyes:', ':heart:', ':blush:', ':yellow_heart:']

[':unamused:', ':expressionless:', ':angry:', ':neutral_face:', ':broken_heart:']

[':sunglasses:', ':ok_hand:', ':v:', ':relieved:', ':100:']

[':stuck_out_tongue_winking_eye:', ':smiling_imp:', ':smirk:', ':wink:', ':speak_no_evil:']

[':broken_heart:', ':pensive:', ':disappointed:', ':sleepy:', ':cry:']

[':angry:', ':rage:', ':disappointed:', ':unamused:', ':triumph:']

[':headphones:', ':notes:', ':ok_hand:', ':sunglasses:', ':smirk:']


How do we translate this into an emotion? I ended up looking up some corpus of data on emojis

        # useful packages
        # https://github.com/carpedm20/emoji
        
        # reference data
        # https://emojipedia.org/
        # https://www.webfx.com/tools/emoji-cheat-sheet/
        
        
        # reference studies
        # http://www.diva-portal.org/smash/get/diva2:927073/FULLTEXT01.pdf
        # https://www.insight-centre.org/sites/default/files/publications/ianwood-emotionworkshop.pdf
        # https://pdfs.semanticscholar.org/2c96/0b44cb415ff9455ab8eccdcc3cadfb8b74b6.pdf


        # https://github.com/bfelbo/DeepMoji/blob/master/emoji_overview.png?raw=true
        DEEPMOJI_MAP = {...}

        # many thanks to impearker! he hand tagged these emotions
        # check his company twitter @avemDNS a website is on the way!
        EMOJI_TO_EMOTION = {...}

        # https://github.com/words/emoji-emotion/blob/master/faces.txt#L49
        # Affin polarity, can be replicated with lilacs.nlp.sentiment_analysis.get_sentiment("your emoji instead of text")
        EMOJI_POLARITY = {...}
        
        # https://github.com/wooorm/emoticon/blob/master/support.md
        EMOJI_TO_EMOTICON = {...}

        
 In the end hand tagging emotions to emojis worked best
 
 
    for t in TEST_SENTENCES:
        print(get_emotions(t))
            
    #['Zeal', 'Love', 'Love', 'Joy', 'Remorse']
    #['Annoyance', 'boredom', 'Annoyance', 'boredom', 'Despair']
    #['Serenity', 'Optimism', 'Optimism', 'Optimism', 'Awe']
    #['Delight', 'Pride', 'Bemusement', 'Zeal', 'Disfavor']
    #['Despair', 'Disappointment', 'boredom', 'Sadness', 'Pessimism']
    #['Annoyance', 'Outrage', 'boredom', 'Annoyance', 'Cynicism']
    #['Zeal', 'Delight', 'Optimism', 'Serenity', 'Bemusement']