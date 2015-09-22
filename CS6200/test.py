#! /usr/bin/python
from HTMLParser import HTMLParser
import urllib
from collections import deque


class MyCrawler(HTMLParser):
    def __init__(self, seed, phrase):
        HTMLParser.__init__(self)
        self.seed = seed
        self.keyphrase = phrase # If there is no key phrase, it will be F.
        self.depth = 5
        self.limit = 1000
        self.links_found = 0
        self.frontier = deque([])
        self.result = list()
    def handle_starttag(self, tag, attrs):
        if tag == "a" and len(attrs) > 0:
            attrs_dict = dict(attrs)
            if "href" in attrs_dict.keys():
                print("Link found: " + attrs_dict["href"])


if __name__ == '__main__':
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    f = urllib.urlopen(seed)
    crawler = MyCrawler(seed, "")
    crawler.feed(f.read())
    f.close()
        
        
