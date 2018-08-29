# -*- coding: utf-8 -*-
# https://github.com/clemtoy/WNAffect

import os
import sys
import nltk
from nltk.corpus import WordNetCorpusReader
import xml.etree.ElementTree as ET
from os.path import dirname, join


class WNAffectEmotion(object):
    """Defines an emotion."""

    emotions = {}  # name to emotion (str -> Emotion)

    def __init__(self, name, parent_name=None):
        """Initializes an Emotion object.
            name -- name of the emotion (str)
            parent_name -- name of the parent emotion (str)
        """

        self.name = name
        self.parent = None
        self.level = 0
        self.children = []

        if parent_name:
            self.parent = WNAffectEmotion.emotions[parent_name] if parent_name else None
            self.parent.children.append(self)
            self.level = self.parent.level + 1

    def get_level(self, level):
        """Returns the parent of self at the given level.
            level -- level in the hierarchy (int)
        """

        em = self
        while em.level > level and em.level >= 0:
            em = em.parent
        return em

    def __str__(self):
        """Returns the emotion string formatted."""

        return self.name

    def nb_children(self):
        """Returns the number of children of the emotion."""

        return sum(child.nb_children() for child in self.children) + 1

    @staticmethod
    def printTree(emotion=None, indent="", last='updown'):
        """Prints the hierarchy of emotions.
            emotion -- root emotion (Emotion)
        """

        if not emotion:
            emotion = WNAffectEmotion.emotions["root"]

        size_branch = {child: child.nb_children() for child in emotion.children}
        leaves = sorted(emotion.children, key=lambda emotion: emotion.nb_children())
        up, down = [], []
        if leaves:
            while sum(size_branch[e] for e in down) < sum(size_branch[e] for e in leaves):
                down.append(leaves.pop())
            up = leaves

        for leaf in up:
            next_last = 'up' if up.index(leaf) is 0 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(emotion.name))
            WNAffectEmotion.printTree(leaf, indent=next_indent, last=next_last)
        if last == 'up':
            start_shape = '┌'
        elif last == 'down':
            start_shape = '└'
        elif last == 'updown':
            start_shape = ' '
        else:
            start_shape = '├'
        if up:
            end_shape = '┤'
        elif down:
            end_shape = '┐'
        else:
            end_shape = ''
        print('{0}{1}{2}{3}'.format(indent, start_shape, emotion.name, end_shape))
        for leaf in down:
            next_last = 'down' if down.index(leaf) is len(down) - 1 else ''
            next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(emotion.name))
            WNAffectEmotion.printTree(leaf, indent=next_indent, last=next_last)


class WNAffect(object):
    """WordNet-Affect resource."""

    def __init__(self, wordnet16_dir=None, wn_domains_dir=None):
        """Initializes the WordNet-Affect object."""
        wordnet16_dir = wordnet16_dir or join(dirname(__file__), "wordnet-1.6")
        wn_domains_dir = wn_domains_dir or join(dirname(__file__), "wn-domains-3.2")
        cwd = os.getcwd()
        nltk.data.path.append(cwd)
        wn16_path = "{0}/dict".format(wordnet16_dir)
        self.wn16 = WordNetCorpusReader(os.path.abspath("{0}/{1}".format(cwd, wn16_path)), nltk.data.find(wn16_path))
        self.flat_pos = {'NN': 'NN', 'NNS': 'NN', 'JJ': 'JJ', 'JJR': 'JJ', 'JJS': 'JJ', 'RB': 'RB', 'RBR': 'RB',
                         'RBS': 'RB', 'VB': 'VB', 'VBD': 'VB', 'VGB': 'VB', 'VBN': 'VB', 'VBP': 'VB', 'VBZ': 'VB'}
        self.wn_pos = {'NN': self.wn16.NOUN, 'JJ': self.wn16.ADJ, 'VB': self.wn16.VERB, 'RB': self.wn16.ADV}
        self._load_emotions(wn_domains_dir)
        self.synsets = self._load_synsets(wn_domains_dir)

    def _load_synsets(self, wn_domains_dir):
        """Returns a dictionary POS tag -> synset offset -> emotion (str -> int -> str)."""

        tree = ET.parse("{0}/wn-affect-1.1/a-synsets.xml".format(wn_domains_dir))
        root = tree.getroot()
        pos_map = {"noun": "NN", "adj": "JJ", "verb": "VB", "adv": "RB"}

        synsets = {}
        for pos in ["noun", "adj", "verb", "adv"]:
            tag = pos_map[pos]
            synsets[tag] = {}
            for elem in root.findall(".//{0}-syn-list//{0}-syn".format(pos, pos)):
                offset = int(elem.get("id")[2:])
                if not offset: continue
                if elem.get("categ"):
                    synsets[tag][offset] = WNAffectEmotion.emotions[elem.get("categ")] if elem.get(
                        "categ") in WNAffectEmotion.emotions else None
                elif elem.get("noun-id"):
                    synsets[tag][offset] = synsets[pos_map["noun"]][int(elem.get("noun-id")[2:])]

        return synsets

    def _load_emotions(self, wn_domains_dir):
        """Loads the hierarchy of emotions from the WordNet-Affect xml."""

        tree = ET.parse("{0}/wn-affect-1.1/a-hierarchy.xml".format(wn_domains_dir))
        root = tree.getroot()
        for elem in root.findall("categ"):
            name = elem.get("name")
            if name == "root":
                WNAffectEmotion.emotions["root"] = WNAffectEmotion("root")
            else:
                WNAffectEmotion.emotions[name] = WNAffectEmotion(name, elem.get("isa"))

    def get_emotion(self, word, pos):
        """Returns the emotion of the word.
            word -- the word (str)
            pos -- part-of-speech (str)
        """

        if pos in self.flat_pos:
            pos = self.flat_pos[pos]
            synsets = self.wn16.synsets(word, self.wn_pos[pos])
            if synsets:
                for synset in synsets:
                    offset = synset.offset()
                    if offset in self.synsets[pos]:
                        return self.synsets[pos][offset]
        return None

    def get_emotion_synset(self, offset):
        """Returns the emotion of the synset.
            offset -- synset offset (int)
        """

        for pos in self.flat_pos.values():
            if offset in self.synsets[pos]:
                return self.synsets[pos][offset]
        return None


if __name__ == "__main__":
    wordnet16, wndomains32, word, pos = sys.argv[1:5]
    wna = WNAffect(wordnet16, wndomains32)
    print(wna.get_emotion(word, pos))