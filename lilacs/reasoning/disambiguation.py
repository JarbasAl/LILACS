from nltk.corpus import wordnet as wn
from lilacs.reasoning import LILACSTextAnalyzer
from lilacs.exceptions import InvalidMetric
from pywsd.lesk import simple_lesk, adapted_lesk, cosine_lesk, original_lesk
from pywsd.similarity import max_similarity
from pywsd.baseline import max_lemma_count
from jarbas_utils.log import LOG


class LILACSDisambiguation(LILACSTextAnalyzer):
    """
    1) Path Similarity: Return a score denoting how similar two word senses are,
    based on the shortest path that connects the senses in the is-a
    (hypernym/hypnoym) taxonomy.

    2) Leacock-Chodorow (LCH) Similarity: Return a score denoting how similar
     two word senses are, based on the shortest path that connects the senses
     (as Path Similarity) and the maximum depth of the taxonomy in which the
     senses occur.

    3) Wu-Palmer (WUP) Similarity: Return a score denoting how similar
    two word senses are, based on the depth of the two senses in the taxonomy
    and that of their Least Common Subsumer (most specific ancestor node).

    4) Resnik (RES) Similarity: Return a score denoting how similar two word
    senses are, based on the Information Content (IC) of the Least Common
    Subsumer (most specific ancestor node).

    5) Jiang-Conrath (JCN) Similarity: Return a score denoting how similar two
    word senses are, based on the Information Content (IC) of the Least Common
    Subsumer (most specific ancestor node) and that of the two input Synsets.

    6) Lin Similarity: Return a score denoting how similar two word senses are,
    based on the Information Content (IC) of the Least Common Subsumer
    (most specific ancestor node) and that of the two input Synsets.
    """
    @staticmethod
    def max_lemma_count(ambiguous_word):
        return max_lemma_count(ambiguous_word)

    @staticmethod
    def _get_pos(sent, word):
        tags = LILACSDisambiguation.postag(sent)
        idx = LILACSDisambiguation.tokenize(sent).index(word)
        pos = tags[idx][1]
        return pos[0].lower()

    @staticmethod
    def max_lin_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        return max_similarity(context_sentence, ambiguous_word, "lin", pos=pos)

    @staticmethod
    def max_path_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        # "path", "lch", "wup", "res", "jcn", "lin"
        return max_similarity(context_sentence, ambiguous_word, "path",
                              pos=pos)

    @staticmethod
    def max_wup_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        # "path", "lch", "wup", "res", "jcn", "lin"
        return max_similarity(context_sentence, ambiguous_word, "wup",
                              pos=pos)

    @staticmethod
    def max_lch_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        # "path", "lch", "wup", "res", "jcn", "lin"
        return max_similarity(context_sentence, ambiguous_word, "lch",
                              pos=pos)

    @staticmethod
    def max_jcn_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        # "path", "lch", "wup", "res", "jcn", "lin"
        return max_similarity(context_sentence, ambiguous_word, "jcn",
                              pos=pos)

    @staticmethod
    def max_res_similarity(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        # "path", "lch", "wup", "res", "jcn", "lin"
        return max_similarity(context_sentence, ambiguous_word, "res",
                              pos=pos)

    @staticmethod
    def original_lesk(context_sentence, ambiguous_word, pos=None):
        return original_lesk(context_sentence, ambiguous_word)

    @staticmethod
    def simple_lesk(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        return simple_lesk(context_sentence, ambiguous_word, pos=pos)

    @staticmethod
    def cosine_lesk(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        return cosine_lesk(context_sentence, ambiguous_word, pos=pos)

    @staticmethod
    def adapted_lesk(context_sentence, ambiguous_word, pos=None):
        if pos is None: # False -> ignore, None -> auto
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)
        elif pos:
            pos = pos[0]
        if pos not in ["n", "v"]:
            pos = None
        return adapted_lesk(context_sentence, ambiguous_word, pos=pos)

    @staticmethod
    def disambiguate(context_sentence, ambiguous_word, multiple=False,
                     ignores=None):
        pos = LILACSDisambiguation._get_pos(context_sentence, ambiguous_word)

        algos = {
            # lesk
            "simple_lesk": LILACSDisambiguation.simple_lesk,
            "original_lesk": LILACSDisambiguation.original_lesk,
            "adapted_lesk": LILACSDisambiguation.adapted_lesk,
            "cosine_lesk": LILACSDisambiguation.cosine_lesk,

            # content similarity
            "max_lin_similarity": LILACSDisambiguation.max_lin_similarity,
            "max_jcn_similarity": LILACSDisambiguation.max_jcn_similarity,
            "max_res_similarity": LILACSDisambiguation.max_res_similarity,

            # path similarity
            "max_path_similarity": LILACSDisambiguation.max_path_similarity,
            "max_wup_similarity": LILACSDisambiguation.max_wup_similarity,
            "max_lch_similarity": LILACSDisambiguation.max_lch_similarity,

            # word2vec
            "sense2vec": LILACSDisambiguation.sensevec_disambiguate,
            "word2vec": LILACSDisambiguation.vec_disambiguate
        }

        ignores = ignores or ["max_lin_similarity",
                              "max_jcn_similarity",
                              "max_lch_similarity"]
        for i in ignores:
            if i not in algos:
                LOG.error("Invalid disambiguation metric " + i)
                LOG.debug("Valid disambiguation metrics are:" +
                          str(list(algos.keys())))
                raise InvalidMetric
            algos.pop(i)

        metric = 1 / (1 + len(algos))

        candidates = {}

        # score bonus for pos_tag senses
        for ss in wn.synsets(ambiguous_word):
            if ss not in candidates:
                candidates[ss] = 0

            # If POS is specified.
            if pos and ss.pos() == pos:
                candidates[ss] += metric

        # score bonus whenever a algo agrees
        for algo in algos:
            ss = algos[algo](context_sentence, ambiguous_word, pos)
            candidates[ss] += metric
            # If POS-tag mismatch
            if pos and ss.pos() != pos:
                # penalty!
                candidates[ss] -= metric / 2

        candidates = sorted(candidates.items(), key=lambda x: x[1],
                            reverse=True)
        best_sense = candidates[0][0]
        if multiple:
            return candidates
        return best_sense

    @staticmethod
    def vec_disambiguate(context_sentence, ambiguous_word, pos=None,
                         multiple=False):
        if pos is None:
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)

        best_score = 0
        best_sense = LILACSDisambiguation.max_lemma_count(ambiguous_word)
        candidates = []
        for ss in wn.synsets(ambiguous_word):

            # If POS is specified.
            if pos and ss.pos() != pos:
                continue

            score = LILACSDisambiguation.w2v_similarity_match(
                context_sentence, ss.definition())
            if score > best_score:
                best_score = score
                best_sense = ss
            candidates.append((ss, score))
        if multiple:
            return candidates
        return best_sense

    @staticmethod
    def sensevec_disambiguate(context_sentence, ambiguous_word, pos=None,
                         multiple=False):
        if pos is None:
            pos = LILACSDisambiguation._get_pos(context_sentence,
                                                ambiguous_word)

        best_score = 0
        best_sense = LILACSDisambiguation.max_lemma_count(ambiguous_word)
        candidates = []
        for ss in wn.synsets(ambiguous_word):

            # If POS is specified.
            if pos and ss.pos() != pos:
                continue

            score = LILACSDisambiguation.s2v_similarity_match(
                context_sentence, ss.definition())
            if score > best_score:
                best_score = score
                best_sense = ss
            candidates.append((ss, score))
        if multiple:
            return candidates
        return best_sense

