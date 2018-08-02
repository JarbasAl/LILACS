#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from lilacs.settings import SPACY_MODEL
import en_coref_md
import spacy


def get_nlp(use_sense2vec=False):
    nlp = spacy.load(SPACY_MODEL)
    if use_sense2vec:
        from lilacs.data_sources.reddit_hivemind import init_s2v
        nlp = init_s2v(nlp)
    return nlp


def get_corefnlp(use_sense2vec=False):
    nlp = en_coref_md.load()
    if use_sense2vec:
        from lilacs.data_sources.reddit_hivemind import init_s2v
        nlp = init_s2v(nlp)
    return nlp
