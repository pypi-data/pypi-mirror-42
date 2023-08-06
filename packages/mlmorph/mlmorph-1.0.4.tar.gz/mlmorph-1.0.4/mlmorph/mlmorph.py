#!/usr/bin/env python

"""
Simple python interface for mlmorph using liblibhfst-python.
"""

from sys import stdin
import os
import regex
import libhfst
from pkg_resources import resource_filename, resource_exists


def getTransducer(fsa):
    istr = libhfst.HfstInputStream(fsa)
    transducers = []
    while not (istr.is_eof()):
        transducers.append(istr.read())
    istr.close()
    return transducers[0]


class Analyser:

    def __init__(self):
        """Construct Mlmorph Analyser"""
        self.fsa = None
        resource_path = 'data/malayalam.a'
        if resource_exists(__name__, resource_path):
            self.fsa = resource_filename(__name__, resource_path)
        if not self.fsa:
            raise ValueError('Could not read the fsa.')
        self.transducer = None
        self.analyser = None
        self.analyser_regex = regex.compile(
            r"((?P<root>([^<])+)(?P<tags>(<[^>]+>)+))+")
        self.pos_regex = regex.compile(r"(<(?P<tag>([^>]+))>)+")

    def getAnalyser(self):
        if not self.transducer:
            self.transducer = getTransducer(self.fsa)
        analyser = libhfst.HfstTransducer(self.transducer)
        analyser.invert()
        analyser.remove_epsilons()
        analyser.lookup_optimize()
        return analyser

    def analyse(self, token, weighted=True):
        """Perform a simple morphological analysis lookup. """
        if not self.analyser:
            self.analyser = self.getAnalyser()
        analysis_results = self.analyser.lookup(token)
        if not weighted:
            return analysis_results

        processed_result = []
        for aindex in range(len(analysis_results)):
            parsed_result = self.parse_analysis(analysis_results[aindex])
            processed_result.append(
                (analysis_results[aindex][0], parsed_result['weight']))
        return sorted(processed_result, key=lambda tup: tup[1])

    def parse_analysis(self, analysis_result):
        result = {}
        if analysis_result is None:
            return result

        analysis = analysis_result[0]
        if analysis[0] == '<':
            analysis = ' ' + analysis
        match = self.analyser_regex.match(analysis)
        roots = match.captures("root")
        morphemes = []
        for rindex in range(len(roots)):
            morpheme = {}
            morpheme['root'] = roots[rindex]
            tags = match.captures("tags")[rindex]
            morpheme['pos'] = self.pos_regex.match(tags).captures("tag")
            morphemes.append(morpheme)

        result['morphemes'] = morphemes
        result['weight'] = self.get_weight(morphemes)
        return result

    def get_weight(self, analysis):
        """Analysis with less weight is the best analysis."""
        morpheme_length = len(analysis)
        weight = morpheme_length*100
        for i in range(morpheme_length):
            pos = analysis[i]['pos']
            root = analysis[i]['root']
            for j in range(len(pos)):
                # In general, favor simplicity
                # Prefer analysis with less number of tags
                # Prefer anaysis with small length roots
                weight += len(pos)*5 + len(root)*2 + \
                    self.get_pos_weight(pos[j])*3
        return weight

    def get_pos_weight(self, pos):
        """Get the relative weight of a pos tag. Less weight is the preferred pos tag."""
        WEIGHTS = {
            # Prefer verbs than nouns
            'v': 1,
            'n': 2,
            # Among three letter codes, prefer adv. Then adj, Then pronoun
            'adv': 3,
            'adj': 4,
            'coordinative': 4,
            'v-n-compound': 4,
            'prn': 5,
            # Favor cvb-adv-part-past മുൻവിനയെച്ചം without using its length
            'past': 4,
            'cvb-adv-part-past': 5,
            # Proper noun has high cost
            'np': 5
        }
        # Use the WEIGHTS or fallback to length
        return WEIGHTS.get(pos, len(pos))


class Generator:
    def __init__(self):
        """Construct Mlmorph Generator"""
        self.fsa = None
        resource_path = 'data/malayalam.a'
        if resource_exists(__name__, resource_path):
            self.fsa = resource_filename(__name__, resource_path)
        if not self.fsa:
            raise ValueError('Could not read the fsa.')
        self.transducer = None
        self.generator = None
        self.pos_regex = regex.compile(r"(<(?P<tag>([^>]+))>)+")

    def generate(self, token):
        """Perform a simple morphological generator lookup."""
        if not self.generator:
            self.generator = self.getGenerator()
        return self.generator.lookup(token)

    def getGenerator(self):
        if not self.transducer:
            self.transducer = getTransducer(self.fsa)
        generator = libhfst.HfstTransducer(self.transducer)
        generator.remove_epsilons()
        generator.lookup_optimize()
        return generator
