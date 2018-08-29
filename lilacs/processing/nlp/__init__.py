#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

from lilacs.settings import SPACY_MODEL
import en_coref_md
import spacy


def get_nlp():
    nlp = spacy.load(SPACY_MODEL)
    return nlp


def get_corefnlp():
    nlp = en_coref_md.load()
    return nlp
