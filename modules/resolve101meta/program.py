#! /usr/bin/env python

import sys
import json
import re

sys.path.append('../../libraries/101meta')
import const101
import tools101

wikiUrl = unicode('http://101companies.org/wiki/{0}')
# loading of the dumps this module depends on
repo = json.load(open(const101.pullRepoDump, 'r'))
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
wiki = json.load(open(const101.wikiDump, 'r'))["wiki"]


### HELPER FUNCTIONS
def encodeForUrl(ns, name):
    if not ns: return name.replace(' ', '_')
    return ns.encode("utf8") + ':' + name.encode("utf8").replace(' ', '_')

def findWikiEntry(val, namespace, title, map):
    for page in wiki['pages']:
        if page['page']['page']['p'] == namespace and page['page']['page']['n'] == title.replace('_', ' '):
            map[val] = {
                '101wiki': wikiUrl.format(encodeForUrl(namespace,title)),
                'headline': page['page'].get('headline', '<unresolved>')
            }
            return

    map[val] = {'101wiki': '<unresolved>', 'headline': '<unresolved>'}
    problems.append({'missingWikiPage': wikiUrl.format(encodeForUrl(namespace, title))})

def handleMention(unit, key, map, namespace):
    if key in unit:
        val = unit[key]
        if not val in map:
            findWikiEntry(val, namespace, val, map)

def handleContribution(name, map):
    repoUrl = repo.get(name, '<unresolved>')
    if repoUrl == '<unresolved>': problems.append({'missing repo url' : name})

    pageName = page['page']['page']['p'] + ':' + page['page']['page']['n']
    map[name] = {
        '101wiki' : wikiUrl.format(pageName),
        '101repo' : repoUrl,
        'headline': page['page'].get('headline', '<unresolved>')
    }


### MAIN PROGRAM
# variables that will form the dump later on
terms = dict()
concepts = dict()
features = dict()
languages = dict()
technologies = dict()
contributions = dict()
results = dict()
results["terms"] = terms
results["concepts"] = concepts
results["features"] = features
results["languages"] = languages
results["technologies"] = technologies
results["contributions"] = contributions
problems = list()

# First part - check metadata values - they are supposed to have a page in the wiki
for rule in rules:
    for unit in rule['rule']['metadata']:
        handleMention(unit, "concept",   concepts,     None)
        handleMention(unit, "language",  languages,    'Language')
        handleMention(unit, "dependsOn", technologies, 'Technology')
        handleMention(unit, "inputOf",   technologies, 'Technology')
        handleMention(unit, "outputOf",  technologies, 'Technology')
        handleMention(unit, "partOf",    technologies, 'Technology')
        handleMention(unit, "term",      terms,        '101term')
        handleMention(unit, "feature",   features,     'Feature')


# Second part - check that contributions in the wiki actually exist (have a repository link)
for page in wiki['pages']:
    if page['page']['page']['p'] == 'Contribution':
        handleContribution(page['page']['page']['n'], contributions)

# creation of the dump
dump = dict()
dump["results"] = results
dump["numbers"] = dict()
dump["numbers"]["numbersOfTerms"] = len(terms)
dump["numbers"]["numbersOfConcepts"] = len(concepts)
dump["numbers"]["numbersOfFeatures"] = len(features)
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
dump["numbers"]["numbersOfContributions"] = len(contributions)
dump["problems"] = problems
tools101.releaseDump(dump, const101.resolutionDump)