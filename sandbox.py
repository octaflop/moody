from nltk.corpus import wordnet as wn
import nltk
import opml
import feedparser
import redis
import uuid

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
    #storycorpus['timestamps'] = []
    storycorpus['urls'] = []
    storycorpus['uuids'] = []

    for ii in range(0, len(stories)):
        entries = stories[ii]['entries']
        for e in range(0,len(entries)):
            storycorpus['summaries'].append(entries[e]['summary'])
            #storycorpus['timestamps'].append(entries[e]['updated'])
            storycorpus['urls'].append(entries[e]['link'])
            storycorpus['uuids'].append(uuid.uuid1())

    return storycorpus

def push_story(summaries=None, urls=None, uuids=None):
    """
    also requires **kwargs
    """
    # create redis instance
    r = redis.Redis()
    #redis story id
    for ii in range(0,len(urls)):
        sid = r.incr('global.sid')
        r.set('story:%s:uuid' % sid, uuids[ii])
        clean_summary = nltk.clean_html(summaries[ii])
        r.set('story:%s:summary' % sid, clean_summary)
        r.set('story:%s:url' % sid, urls[ii])
        r.set('story:uuid:%s' % uuids[ii], sid)

def get_story(sid=False):#, uuid=False):
    # create redis instance
    r = redis.Redis()
   # if uuid:
   # sid = r.get('story:uuid:%s' % uuid)
   # elif sid:
    uuid = r.get('story:%s:uuid' % sid)
   # else:
   #     False
    summary = r.get('story:%s:summary' % sid)
    url = r.get('story:%s:url' % sid)
    return dict(summary=summary, url=url, uuid=uuid, sid=sid)

def story_words(sid):
    # build a normalized list of words from the summary
    r = redis.Redis()
    summary = r.get('story:%s:summary' % sid)
    tokens = nltk.wordpunct_tokenize(summary)
    text = nltk.Text(tokens)
    words = [w.lower() for w in text]
    return words

def story_vocab(sid):
    words = story_words(sid)
    vocab = sorted(set(words))
    return vocab

if __name__ == "__main__":
     #source = get_source_info()
     #stories = get_stories(**source)
     #story = build_story(stories)
     #push_story(**story)
     sid = 1
     gotten = get_story(sid)

     import pprint
     pprint.pprint(gotten)

     pprint.pprint(story_words(sid))
     pprint.pprint(story_vocab(sid))



"""



def rate_story
"""
