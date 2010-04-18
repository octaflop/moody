#!/usr/bin/env python

from butler import *
def test(value, expected_result):
    print "Value: %s" str(value)
    print "Expected: %s" str(value)
    if value == expected_result:
        print "passes"
        return True
    else:
        print "error"
        return False

def bootstrap():
    #only needed for first run of redis (for testing)
    build_fixture()
    # update stories
    source = get_source_info()
    stories = get_stories(**source)
    stories = build_stories(**stories)
    # only needed to push stories
    # pushes all stories to redis
    push_story(**stories)

def test():
    if get_story(90):
        sid = 90
        test(like_article(sid), True)
        test(dislike_article(sid+1), True)
        print "article %i scored %i" % (sid+30, score_article(sid+30))
        print get_ranked_stories()
    else:
        bootstrap()
        test()

if __name__ == "__main__":
    test()

