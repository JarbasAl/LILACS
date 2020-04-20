##### Code extracted from pattern.en
# TODO remove non essential code, only need to import
# from lilacs.spacy_extensions.verbs import conjugate, \
#     PAST, PRESENT, SINGULAR, PLURAL

import re
import os
from lilacs.settings import LEXICONS_DIR

PUNCTUATION = ".,;:!?()\[]{}`'\"@#$^&*+-|=~_”—“"

# Conjugation is the inflection of verbs by tense, person, number, mood and aspect.

# VERB TENSE:
INFINITIVE, PRESENT, PAST, FUTURE = INF, PRES, PST, FUT = \
    "infinitive", "present", "past", "future"

# VERB PERSON:
# 1st person = I or we (plural).
# 2nd person = you.
# 3rd person = he, she, it or they (plural).
FIRST, SECOND, THIRD =  1, 2, 3

# VERB NUMBER:
# singular number = I, you, he, she, it.
#   plural number = we, you, they.
SINGULAR, PLURAL =  SG, PL =  "singular", "plural"

# VERB MOOD:
#  indicative mood = a fact: "the cat meowed".
#  imperative mood = a command: "meow!".
# conditional mood = a hypothesis: "a cat *will* meow *if* it is hungry".
# subjunctive mood = a wish, possibility or necessity: "I *wish* the cat *would* stop meowing".
INDICATIVE, IMPERATIVE, CONDITIONAL, SUBJUNCTIVE =   IND, IMP, COND, SJV = \
    "indicative", "imperative", "conditional", "subjunctive"

# VERB ASPECT:
# imperfective aspect = a habitual or ongoing action: "it was midnight; the cat meowed".
#   perfective aspect = a momentary or completed action: "I flung my pillow at the cat".
#  progressive aspect = a incomplete action in progress: "the cat was meowing".
# Note: the progressive aspect is a subtype of the imperfective aspect.
IMPERFECTIVE, PERFECTIVE, PROGRESSIVE =  IPFV, PFV, PROG = \
    "imperfective", "perfective", "progressive"

# Imperfect = past tense + imperfective aspect.
# Preterite = past tense + perfective aspect.
IMPERFECT = "imperfect"
PRETERITE = "preterite"

# Participle = present tense  + progressive aspect.
PARTICIPLE, GERUND = "participle", "gerund"

# Continuous aspect ≈ progressive aspect.
CONTINUOUS = CONT = "continuous"

_ = None  # prettify the table =>

# Unique index per tense (= tense + person + number + mood + aspect + negated? + aliases).
# The index is used to describe the format of the verb lexicon file.
# The aliases can be passed to Verbs.conjugate() and Tenses.__contains__().
TENSES = {
    None: (None, _, _, _, _, False, (None,)),
    # ENGLISH   SPANISH   GERMAN    DUTCH     FRENCH
    0: (INF, _, _, _, _, False, ("inf",)),
    # to be     ser       sein      zijn      être
    1: (PRES, 1, SG, IND, IPFV, False, ("1sg",)),
    # I am        soy       bin       ben       suis
    2: (PRES, 2, SG, IND, IPFV, False, ("2sg",)),
    # you are       eres      bist      bent      es
    3: (PRES, 3, SG, IND, IPFV, False, ("3sg",)),
    # (s)he is        es        ist       is        est
    4: (PRES, 1, PL, IND, IPFV, False, ("1pl",)),
    # we are       somos     sind      zijn      sommes
    5: (PRES, 2, PL, IND, IPFV, False, ("2pl",)),
    # you are       sois      seid      zijn      êtes
    6: (PRES, 3, PL, IND, IPFV, False, ("3pl",)),
    # they are       son       sind      zijn      sont
    7: (PRES, _, PL, IND, IPFV, False, ("pl",)),  # are
    8: (PRES, _, _, IND, PROG, False, ("part",)),
    # being     siendo              zijnd     étant
    9: (PRES, 1, SG, IND, IPFV, True, ("1sg-",)),  # I am not
    10: (PRES, 2, SG, IND, IPFV, True, ("2sg-",)),  # you aren't
    11: (PRES, 3, SG, IND, IPFV, True, ("3sg-",)),  # (s)he isn't
    12: (PRES, 1, PL, IND, IPFV, True, ("1pl-",)),  # we aren't
    13: (PRES, 2, PL, IND, IPFV, True, ("2pl-",)),  # you aren't
    14: (PRES, 3, PL, IND, IPFV, True, ("3pl-",)),  # they aren't
    15: (PRES, _, PL, IND, IPFV, True, ("pl-",)),  # aren't
    16: (PRES, _, _, IND, IPFV, True, ("-",)),  # isn't
    17: (PST, 1, SG, IND, IPFV, False, ("1sgp",)),
    # I was       era       war       was       étais
    18: (PST, 2, SG, IND, IPFV, False, ("2sgp",)),
    # you were      eras      warst     was       étais
    19: (PST, 3, SG, IND, IPFV, False, ("3sgp",)),
    # (s)he was       era       war       was       était
    20: (PST, 1, PL, IND, IPFV, False, ("1ppl",)),
    # we were      éramos    waren     waren     étions
    21: (PST, 2, PL, IND, IPFV, False, ("2ppl",)),
    # you were      erais     wart      waren     étiez
    22: (PST, 3, PL, IND, IPFV, False, ("3ppl",)),
    # they were      eran      waren     waren     étaient
    23: (PST, _, PL, IND, IPFV, False, ("ppl",)),  # were
    24: (PST, _, _, IND, PROG, False, ("ppart",)),
    # been      sido      gewesen   geweest   été
    25: (PST, _, _, IND, IPFV, False, ("p",)),  # was
    26: (PST, 1, SG, IND, IPFV, True, ("1sgp-",)),  # I wasn't
    27: (PST, 2, SG, IND, IPFV, True, ("2sgp-",)),  # you weren't
    28: (PST, 3, SG, IND, IPFV, True, ("3sgp-",)),  # (s)he wasn't
    29: (PST, 1, PL, IND, IPFV, True, ("1ppl-",)),  # we weren't
    30: (PST, 2, PL, IND, IPFV, True, ("2ppl-",)),  # you weren't
    31: (PST, 3, PL, IND, IPFV, True, ("3ppl-",)),  # they weren't
    32: (PST, _, PL, IND, IPFV, True, ("ppl-",)),  # weren't
    33: (PST, _, _, IND, IPFV, True, ("p-",)),  # wasn't
    34: (PST, 1, SG, IND, PFV, False, ("1sg+",)),
    # I           fui                           fus
    35: (PST, 2, SG, IND, PFV, False, ("2sg+",)),
    # you           fuiste                        fus
    36: (PST, 3, SG, IND, PFV, False, ("3sg+",)),
    # (s)he           fue                           fut
    37: (PST, 1, PL, IND, PFV, False, ("1pl+",)),
    # we           fuimos                        fûmes
    38: (PST, 2, PL, IND, PFV, False, ("2pl+",)),
    # you           fuisteis                      fûtes
    39: (PST, 3, PL, IND, PFV, False, ("3pl+",)),
    # they           fueron                        furent
    40: (FUT, 1, SG, IND, IPFV, False, ("1sgf",)),
    # I           seré                          serai
    41: (FUT, 2, SG, IND, IPFV, False, ("2sgf",)),
    # you           serás                         seras
    42: (FUT, 3, SG, IND, IPFV, False, ("3sgf",)),
    # (s)he           será                          sera
    43: (FUT, 1, PL, IND, IPFV, False, ("1plf",)),
    # we           seremos                       serons
    44: (FUT, 2, PL, IND, IPFV, False, ("2plf",)),
    # you           seréis                        serez
    45: (FUT, 3, PL, IND, IPFV, False, ("3plf",)),
    # they           serán                         seron
    46: (PRES, 1, SG, COND, IPFV, False, ("1sg->",)),
    # I           sería                         serais
    47: (PRES, 2, SG, COND, IPFV, False, ("2sg->",)),
    # you           serías                        serais
    48: (PRES, 3, SG, COND, IPFV, False, ("3sg->",)),
    # (s)he           sería                         serait
    49: (PRES, 1, PL, COND, IPFV, False, ("1pl->",)),
    # we           seríamos                      serions
    50: (PRES, 2, PL, COND, IPFV, False, ("2pl->",)),
    # you           seríais                       seriez
    51: (PRES, 3, PL, COND, IPFV, False, ("3pl->",)),
    # they           serían                        seraient
    52: (PRES, 2, SG, IMP, IPFV, False, ("2sg!",)),
    # you           sé        sei                 sois
    521: (PRES, 3, SG, IMP, IPFV, False, ("3sg!",)),  # (s)he
    53: (PRES, 1, PL, IMP, IPFV, False, ("1pl!",)),
    # we                     seien               soyons
    54: (PRES, 2, PL, IMP, IPFV, False, ("2pl!",)),
    # you           sed       seid                soyez
    541: (PRES, 3, PL, IMP, IPFV, False, ("3pl!",)),  # you
    55: (PRES, 1, SG, SJV, IPFV, False, ("1sg?",)),
    # I           sea       sei                 sois
    56: (PRES, 2, SG, SJV, IPFV, False, ("2sg?",)),
    # you           seas      seist               sois
    57: (PRES, 3, SG, SJV, IPFV, False, ("3sg?",)),
    # (s)he           sea       sei                 soit
    58: (PRES, 1, PL, SJV, IPFV, False, ("1pl?",)),
    # we           seamos    seien               soyons
    59: (PRES, 2, PL, SJV, IPFV, False, ("2pl?",)),
    # you           seáis     seiet               soyez
    60: (PRES, 3, PL, SJV, IPFV, False, ("3pl?",)),
    # they           sean      seien               soient
    61: (PRES, 1, SG, SJV, PFV, False, ("1sg?+",)),  # I
    62: (PRES, 2, SG, SJV, PFV, False, ("2sg?+",)),  # you
    63: (PRES, 3, SG, SJV, PFV, False, ("3sg?+",)),  # (s)he
    64: (PRES, 1, PL, SJV, PFV, False, ("1pl?+",)),  # we
    65: (PRES, 2, PL, SJV, PFV, False, ("2pl?+",)),  # you
    66: (PRES, 3, PL, SJV, PFV, False, ("3pl?+",)),  # they
    67: (PST, 1, SG, SJV, IPFV, False, ("1sgp?",)),
    # I           fuera     wäre                fusse
    68: (PST, 2, SG, SJV, IPFV, False, ("2sgp?",)),
    # you           fueras    wärest              fusses
    69: (PST, 3, SG, SJV, IPFV, False, ("3sgp?",)),
    # (s)he           fuera     wäre                fût
    70: (PST, 1, PL, SJV, IPFV, False, ("1ppl?",)),
    # we           fuéramos  wären               fussions
    71: (PST, 2, PL, SJV, IPFV, False, ("2ppl?",)),
    # you           fuerais   wäret               fussiez
    72: (PST, 3, PL, SJV, IPFV, False, ("3ppl?",)),
    # they           fueran    wären               fussent
}

# Map tenses and aliases to unique index.
# Aliases include:
# - a short number: "s", "sg", "singular" => SINGULAR,
# - a short string: "1sg" => 1st person singular present,
# - a unique index:  1    => 1st person singular present,
# -  Penn treebank: "VBP" => 1st person singular present.
TENSES_ID = {}
TENSES_ID[INFINITIVE] = 0
for i, (tense, person, number, mood, aspect, negated, aliases) in\
        TENSES.items():
    for a in aliases + (i,):
        TENSES_ID[i] = \
            TENSES_ID[a] = \
            TENSES_ID[(tense, person, number, mood, aspect, negated)] = i
    if number == SG:
        for sg in ("s", "sg", "singular"):
            TENSES_ID[(tense, person, sg, mood, aspect, negated)] = i
    if number == PL:
        for pl in ("p", "pl", "plural"):
            TENSES_ID[(tense, person, pl, mood, aspect, negated)] = i

# Map Penn Treebank tags to unique index.
for tag, tense in (
        ("VB", 0),  # infinitive
        ("VBP", 1),  # present 1 singular
        ("VBZ", 3),  # present 3 singular
        ("VBG", 8),  # present participle
        ("VBN", 24),  # past participle
        ("VBD", 25)):  # past
    TENSES_ID[tag.lower()] = tense


def tense_id(*args, **kwargs):
    """ Returns the tense id for a given (tense, person, number, mood, aspect, negated).
        Aliases and compound forms (e.g., IMPERFECT) are disambiguated.
    """
    # Unpack tense given as a tuple, e.g., tense((PRESENT, 1, SG)):
    if len(args) == 1 and isinstance(args[0], (list, tuple)):
        if args[0] not in ((PRESENT, PARTICIPLE), (PAST, PARTICIPLE)):
            args = args[0]
    # No parameters defaults to tense=INFINITIVE, tense=PRESENT otherwise.
    if len(args) == 0 and len(kwargs) == 0:
        t = INFINITIVE
    else:
        t = PRESENT
    # Set default values.
    tense = kwargs.get("tense", args[0] if len(args) > 0 else t)
    person = kwargs.get("person", args[1] if len(args) > 1 else 3) or None
    number = kwargs.get("number", args[2] if len(args) > 2 else SINGULAR)
    mood = kwargs.get("mood", args[3] if len(args) > 3 else INDICATIVE)
    aspect = kwargs.get("aspect", args[4] if len(args) > 4 else IMPERFECTIVE)
    negated = kwargs.get("negated", args[5] if len(args) > 5 else False)
    # Disambiguate wrong order of parameters.
    if mood in (PERFECTIVE, IMPERFECTIVE):
        mood, aspect = INDICATIVE, mood
    # Disambiguate INFINITIVE.
    # Disambiguate PARTICIPLE, IMPERFECT, PRETERITE.
    # These are often considered to be tenses but are in fact tense + aspect.
    if tense == INFINITIVE:
        person = number = mood = aspect = None
        negated = False
    if tense in (
    (PRESENT, PARTICIPLE), PRESENT + PARTICIPLE, PARTICIPLE, GERUND):
        tense, aspect = PRESENT, PROGRESSIVE
    if tense in ((PAST, PARTICIPLE), PAST + PARTICIPLE):
        tense, aspect = PAST, PROGRESSIVE
    if tense == IMPERFECT:
        tense, aspect = PAST, IMPERFECTIVE
    if tense == PRETERITE:
        tense, aspect = PAST, PERFECTIVE
    if aspect in (CONTINUOUS, PARTICIPLE, GERUND):
        aspect = PROGRESSIVE
    if aspect == PROGRESSIVE:
        person = number = None
    # Disambiguate CONDITIONAL.
    # In Spanish, the conditional is regarded as an indicative tense.
    if tense == CONDITIONAL and mood == INDICATIVE:
        tense, mood = PRESENT, CONDITIONAL
    # Disambiguate aliases: "pl" =>
    # (PRESENT, None, PLURAL, INDICATIVE, IMPERFECTIVE, False).
    return TENSES_ID.get(tense.lower(),
                         TENSES_ID.get(
                             (tense, person, number, mood, aspect, negated)))


tense = tense_id


# --- VERB CONJUGATIONS -----------------------------------------------------------------------------
# Verb conjugations based on a table of known verbs and rules for unknown verbs.
# Verb conjugations are useful to find the verb infinitive in the parser's lemmatizer.
# For unknown verbs, Verbs.find_lemma() and Verbs.find_lexeme() are called.
# These must be implemented in a subclass with rules for unknown verbs.


class Tenses(list):

    def __contains__(self, tense):
        # t in tenses(verb) also works when t is an alias (e.g. "1sg").
        return list.__contains__(self, TENSES[tense_id(tense)][:-2])


class Verbs(dict):

    def __init__(self, language="en"):
        """ A dictionary of verb infinitives, each linked to a list of conjugated forms.
            Each line in the file at the given path is one verb, with the tenses separated by a comma.
            The format defines the order of tenses (see TENSES).
            The default dictionary defines default tenses for omitted tenses.
        """
        super().__init__()
        self._language = language
        f = [0, 1, 2, 3, 7, 8, 17, 18, 19, 23, 25, 24, 16, 9, 10, 11, 15, 33,
             26, 27, 28, 32]
        self._format = dict((TENSES_ID[id], i) for i, id in enumerate(f))
        self._default = {
            1: 0, 2: 0, 3: 0, 7: 0,
            # present singular => infinitive ("I walk")
            4: 7, 5: 7, 6: 7,  # present plural
            17: 25, 18: 25, 19: 25, 23: 25,  # past singular
            20: 23, 21: 23, 22: 23,  # past plural
            9: 16, 10: 16, 11: 16, 15: 16,  # present singular negated
            12: 15, 13: 15, 14: 15,  # present plural negated
            26: 33, 27: 33, 28: 33,  # past singular negated
            29: 32, 30: 32, 31: 32, 32: 33  # past plural negated
        }
        self._inverse = {}
        self._load()

    def find_lemma(self, verb):
        """ Returns the base form of the given inflected verb, using a rule-based approach.
            This is problematic if a verb ending in -e is given in the past tense or gerund.
        """
        v = verb.lower()
        b = False
        if v in ("'m", "'re", "'s", "n't"):
            return "be"
        if v in ("'d", "'ll"):
            return "will"
        if v in ("'ve"):
            return "have"
        if v.endswith("s"):
            if v.endswith("ies") and len(v) > 3 and v[-4] not in VOWELS:
                return v[:-3] + "y"  # complies => comply
            if v.endswith(("sses", "shes", "ches", "xes")):
                return v[:-2]  # kisses => kiss
            return v[:-1]
        if v.endswith("ied") and re_vowel.search(v[:-3]) is not None:
            return v[:-3] + "y"  # envied => envy
        if v.endswith("ing") and re_vowel.search(v[:-3]) is not None:
            v = v[:-3];
            b = True;  # chopping => chopp
        if v.endswith("ed") and re_vowel.search(v[:-2]) is not None:
            v = v[:-2];
            b = True;  # danced => danc
        if b:
            # Doubled consonant after short vowel: chopp => chop.
            if len(v) > 3 and v[-1] == v[-2] and v[-3] in VOWELS and v[
                -4] not in VOWELS and not v.endswith("ss"):
                return v[:-1]
            if v.endswith(("ick", "ack")):
                return v[:-1]  # panick => panic
            # Guess common cases where the base form ends in -e:
            if v.endswith(("v", "z", "c", "i")):
                return v + "e"  # danc => dance
            if v.endswith("g") and v.endswith(("dg", "lg", "ng", "rg")):
                return v + "e"  # indulg => indulge
            if v.endswith(("b", "d", "g", "k", "l", "m", "r", "s", "t")) \
                    and len(v) > 2 and v[-2] in VOWELS and not v[-3] in VOWELS \
                    and not v.endswith("er"):
                return v + "e"  # generat => generate
            if v.endswith("n") and v.endswith(("an", "in")) and not v.endswith(
                    ("ain", "oin", "oan")):
                return v + "e"  # imagin => imagine
            if v.endswith("l") and len(v) > 1 and v[-2] not in VOWELS:
                return v + "e"  # squabbl => squabble
            if v.endswith("f") and len(v) > 2 and v[-2] in VOWELS and v[
                -3] not in VOWELS:
                return v + "e"  # chaf => chafed
            if v.endswith("e"):
                return v + "e"  # decre => decree
            if v.endswith(("th", "ang", "un", "cr", "vr", "rs", "ps", "tr")):
                return v + "e"
        return v

    def find_lexeme(self, verb):
        """ For a regular verb (base form), returns the forms using a rule-based approach.
        """
        v = verb.lower()
        if len(v) > 1 and v.endswith("e") and v[-2] not in VOWELS:
            # Verbs ending in a consonant followed by "e": dance, save, devote, evolve.
            return [v, v, v, v + "s", v, v[:-1] + "ing"] + [v + "d"] * 6
        if len(v) > 1 and v.endswith("y") and v[-2] not in VOWELS:
            # Verbs ending in a consonant followed by "y": comply, copy, magnify.
            return [v, v, v, v[:-1] + "ies", v, v + "ing"] + [
                v[:-1] + "ied"] * 6
        if v.endswith(("ss", "sh", "ch", "x")):
            # Verbs ending in sibilants: kiss, bless, box, polish, preach.
            return [v, v, v, v + "es", v, v + "ing"] + [v + "ed"] * 6
        if v.endswith("ic"):
            # Verbs ending in -ic: panic, mimic.
            return [v, v, v, v + "es", v, v + "king"] + [v + "ked"] * 6
        if len(v) > 1 and v[-1] not in VOWELS and v[-2] not in VOWELS:
            # Verbs ending in a consonant cluster: delight, clamp.
            return [v, v, v, v + "s", v, v + "ing"] + [v + "ed"] * 6
        if (len(v) > 1 and v.endswith(("y", "w")) and v[-2] in VOWELS) \
                or (
                len(v) > 2 and v[-1] not in VOWELS and v[-2] in VOWELS and v[
            -3] in VOWELS) \
                or (
                len(v) > 3 and v[-1] not in VOWELS and v[-3] in VOWELS and v[
            -4] in VOWELS):
            # Verbs ending in a long vowel or diphthong followed by a consonant: paint, devour, play.
            return [v, v, v, v + "s", v, v + "ing"] + [v + "ed"] * 6
        if len(v) > 2 and v[-1] not in VOWELS and v[-2] in VOWELS and v[
            -3] not in VOWELS:
            # Verbs ending in a short vowel followed by a consonant: chat, chop, or compel.
            return [v, v, v, v + "s", v, v + v[-1] + "ing"] + [
                v + v[-1] + "ed"] * 6
        return [v, v, v, v + "s", v, v + "ing"] + [v + "ed"] * 6

    def _load(self):
        # have,,,has,,having,,,,,had,had,haven't,,,hasn't,,,,,,,hadn't,hadn't
        idx = self._format[TENSES_ID[INFINITIVE]]

        def _read(path, comment=";;;"):
            """ Returns an iterator over the lines in the file at the given path,
                strippping comments and decoding each line to Unicode.
            """
            if path:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        if line.strip().startswith(comment):
                            continue
                        yield line
            raise StopIteration

        for v in _read(self.path):
            v = v.split(",")
            self[v[idx]] = v
            for x in (x for x in v if x):
                self._inverse[x] = v[idx]

    @property
    def path(self):
        return os.path.join(LEXICONS_DIR, "verbs_en.txt")

    @property
    def language(self):
        return self._language

    @property
    def infinitives(self):
        """ Yields a dictionary of (infinitive, [inflections])-items.
        """
        if dict.__len__(self) == 0:
            self._load()
        return self

    @property
    def inflections(self):
        """ Yields a dictionary of (inflected, infinitive)-items.
        """
        if dict.__len__(self) == 0:
            self._load()
        return self._inverse

    @property
    def TENSES(self):
        """ Yields a list of tenses for this language, excluding negations.
            Each tense is a (tense, person, number, mood, aspect)-tuple.
        """
        a = set(TENSES[id] for id in self._format)
        a = a.union(set(TENSES[id] for id in self._default.keys()))
        a = a.union(set(TENSES[id] for id in self._default.values()))
        a = sorted(x[:-2] for x in a if x[-2] is False)  # Exclude negation.
        return a

    def lemma(self, verb, parse=True):
        """ Returns the infinitive form of the given verb, or None.
        """
        if verb.lower() in self._inverse:
            return self._inverse[verb.lower()]
        if verb in self._inverse:
            return self._inverse[verb]
        if parse is True:  # rule-based
            return self.find_lemma(verb)

    def lexeme(self, verb, parse=True):
        """ Returns a list of all possible inflections of the given verb.
        """
        a = []
        b = self.lemma(verb, parse=parse)
        if b in self:
            a = [x for x in self[b] if x != ""]
        elif parse is True:  # rule-based
            a = self.find_lexeme(b)
        u = []
        [u.append(x) for x in a if x not in u]
        return u

    def conjugate(self, verb, *args, **kwargs):
        """ Inflects the verb and returns the given tense (or None).
            For example: be
            - Verbs.conjugate("is", INFINITVE) => be
            - Verbs.conjugate("be", PRESENT, 1, SINGULAR) => I am
            - Verbs.conjugate("be", PRESENT, 1, PLURAL) => we are
            - Verbs.conjugate("be", PAST, 3, SINGULAR) => he was
            - Verbs.conjugate("be", PAST, aspect=PROGRESSIVE) => been
            - Verbs.conjugate("be", PAST, person=1, negated=True) => I wasn't
        """
        id = tense_id(*args, **kwargs)
        # Get the tense index from the format description (or a default).
        i1 = self._format.get(id)
        i2 = self._format.get(self._default.get(id))
        i3 = self._format.get(self._default.get(self._default.get(id)))
        b = self.lemma(verb, parse=kwargs.get("parse", True))
        v = []
        # Get the verb lexeme and return the requested index.
        if b in self:
            v = self[b]
            for i in (i1, i2, i3):
                if i is not None and 0 <= i < len(v) and v[i]:
                    return v[i]
        if kwargs.get("parse", True) is True:  # rule-based
            v = self.find_lexeme(b)
            for i in (i1, i2, i3):
                if i is not None and 0 <= i < len(v) and v[i]:
                    return v[i]

    def tenses(self, verb, parse=True):
        """ Returns a list of possible tenses for the given inflected verb.
        """
        verb = verb.lower()
        a = set()
        b = self.lemma(verb, parse=parse)
        v = []
        if b in self:
            v = self[b]
        elif parse is True:  # rule-based
            v = self.find_lexeme(b)
        # For each tense in the verb lexeme that matches the given tense,
        # 1) retrieve the tense tuple,
        # 2) retrieve the tense tuples for which that tense is a default.
        for i, tense in enumerate(v):
            if tense == verb:
                for id, index in self._format.items():
                    if i == index:
                        a.add(id)
                for id1, id2 in self._default.items():
                    if id2 in a:
                        a.add(id1)
                for id1, id2 in self._default.items():
                    if id2 in a:
                        a.add(id1)

        a = list(TENSES[id][:-2] for id in a)

        # In Python 2, None is always smaller than anything else while in Python 3, comparison with incompatible types yield TypeError.
        # This is why we need to use a custom key function.
        a = Tenses(sorted(a, key=lambda x: 0 if x[1] is None else x[1]))

        return a


VERB, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB"

VOWELS = "aeiouy"
re_vowel = re.compile(r"a|e|i|o|u|y", re.I)
is_vowel = lambda ch: ch in VOWELS

verbs = Verbs()

conjugate, lemma, lexeme, tenses = \
    verbs.conjugate, verbs.lemma, verbs.lexeme, verbs.tenses
