#!/usr/bin/env python
# Faris Chebib
# #301103355
# 2010-04-16
from nltk.corpus import wordnet as wn
import nltk
import os
import opml
import feedparser
import redis
import uuid
from pylab import intersect1d, intersect1d_nu, array

def get_source_info():
    """
    get stories from opml list
    """
    DEFAULT_OPML = 'http://hosting.opml.org/dave/validatorTests/clean/subscriptionList.opml'
    titles = []
    htmlUrls = []
    xmlUrls = []
    outline = opml.parse(DEFAULT_OPML)
    for ii in outline:
        titles.append(ii.text)
        htmlUrls.append(ii.htmlUrl)
        xmlUrls.append(ii.xmlUrl)
    return dict(htmlUrls=htmlUrls, titles=titles, xmlUrls=xmlUrls)


def get_stories(htmlUrls=None, xmlUrls=None, titles=None):
    """
    return story urls with their respective titles
    needs **kwargs
    """
    stories = []
    for ii in xmlUrls:
        stories.append(feedparser.parse(ii))
    return stories

def build_story(stories):
    """
    return all of the stories in their own marked uuid
    """
    storycorpus = {}
    storycorpus['summaries'] = []
    # storycorpus['timestamps'] = [] 
    # only some of the rss feeds have proper
    # dates-stamps. this is pertubing
    storycorpus['urls'] = []
    storycorpus['uuids'] = []
    for ii in range(0, len(stories)):
        entries = stories[ii]['entries']
        for e in range(0, len(entries)):
            storycorpus['summaries'].append(entries[e]['summary'])
            # storycorpus['timestamps'].append(entries[e]['updated']) :(
            storycorpus['urls'].append(entries[e]['link'])
            storycorpus['uuids'].append(uuid.uuid1())
    return storycorpus

def push_story(summaries=None, urls=None, uuids=None):
    """
    best with kwargs
    pushes all stories
    """
    # create redis instance
    r = redis.Redis()
    #redis story id
    for ii in range(0,len(urls)):
        # push a story to the server
        sid = r.incr('global.sid')
        # atomically add a new story with a rank of 1
        r.zadd('site:storyroll', 'story:%s' % sid, 1)
        r.set('story:%s:uuid' % sid, uuids[ii])
        r.set('story:%s:rawhtml' % sid, summaries[ii])
        clean_summary = nltk.clean_html(summaries[ii])
        r.set('story:%s:raw' % sid, clean_summary)
        r.set('story:%s:url' % sid, urls[ii])
        r.set('story:uuid:%s' % uuids[ii], sid)

def get_story(sid=False):#, uuid=False):
    # create redis instance
    r = redis.Redis()
    uuid = r.get('story:%s:uuid' % sid)
    summary = r.get('story:%s:raw' % sid)
    url = r.get('story:%s:url' % sid)
    return dict(summary=summary, url=url, uuid=uuid, sid=sid)

def story_words(sid):
    # build a normalized list of words from the summary
    r = redis.Redis()
    summary = r.get('story:%s:raw' % sid)
    tokens = nltk.wordpunct_tokenize(summary)
    text = nltk.Text(tokens)
    words = [w.lower() for w in text]
    return words

def story_vocab(sid):
    words = story_words(sid)
    vocab = sorted(set(words))
    return vocab

def lemma_builder(words):
    """
    returns a list of lemmas from a list of words
    """
    lemmas = []
    for word in words:
        if wn.lemmas(word):
            lemmas.append(wn.lemmas(word)[0].name)
    return lemmas

def score_article(sid):
    """
    main evaluation 
    ranking function
    """
    rank = 1 # initial rank
    r = redis.Redis()
    corpus_pref = get_preferences()
    corpus_filter = get_filtrations()
    corpus_story = story_words(sid)
    # need a tokenize here TK
    # need lemma_builder
    pref_lemma = lemma_builder(corpus_pref)
    filter_lemma = lemma_builder(corpus_filter)
    story_lemma = lemma_builder(corpus_story)
    intersect_pref = intersect1d(array(corpus_pref), array(corpus_story))
    intersect_filter = intersect1d(array(corpus_filter), array(corpus_story))
    intersect_lemma_pref = intersect1d(array(pref_lemma), array(story_lemma))
    intersect_lemma_filter = intersect1d(array(filter_lemma), array(story_lemma))
    #These may be adjusted with additional factors
    filter_score = 2 * len(intersect_pref) + len(intersect_lemma_pref)
    prefer_score = -(2 * len(intersect_filter) + len(intersect_lemma_pref))
    rank = filter_score + prefer_score
    r.zincrby("site:storyroll", "story:%s" % sid, rank) # RANK IT
    return rank

def like_article(sid):
    r = redis.Redis()
    words = story_words(sid)
    for word in words:
        r.rpush("corpus:preferences", word)
    return True

def dislike_article(sid):
    r = redis.Redis()
    words = story_words(sid)
    for word in words:
        r.rpush("corpus:filtration", word)
    return True

def get_preferences():
    r = redis.Redis()
    preferences = []
    preferences = r.lrange("corpus:preferences", 0, \
        r.llen("corpus:preferences"))
    return preferences

def get_filtrations():
    r = redis.Redis()
    filtrations = []
    filtrations = r.lrange("corpus:filtration", 0, \
        r.llen("corpus:filtration"))
    return filtrations

def build_words(raw):
    tokens = nltk.wordpunct_tokenize(raw)
    text = nltk.Text(tokens)
    words = [w.lower() for w in text]
    return words

def get_ranked_stories():
    """
    get stories and sort by rank
    """
    r = redis.Redis()
    stories = r.zrangebyscore("site:storyroll", -10, 100)
    return stories

def set_fixtures():
    """
    set fixtures into the corpus. only called once in redis
    build a corpus of words the user dislikes
    a testing function from a file in fixtures
    in this case, bob and alice are opposites;
    alice hates what bob likes and vice verse
    our redis database is oriented around alice's preferences
    """
    r = redis.Redis()
    cwd = os.getcwd()
    #fh = open(cwd + '/fixtures/alice_corpus.txt', 'r')
    fh = open(cwd + '/fixtures/alice.txt', 'r')
    alice_corpus = fh.read()
    fh.close()
    alice_corpus = build_words(str(alice_corpus))
    #fh = open(cwd + '/fixtures/bob_corpus.txt', 'r')
    fh = open(cwd + '/fixtures/bob.txt', 'r')
    bob_corpus = fh.read()
    fh.close()
    bob_corpus = build_words(str(bob_corpus))
    for word in alice_corpus:
        r.rpush("corpus:preferences", word)
    for word in bob_corpus:
        r.rpush("corpus:filtration", word)
    return True

if __name__ == "__main__":
     print "cool"

