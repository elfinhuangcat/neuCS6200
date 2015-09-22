#! /usr/bin/python2
from HTMLParser import HTMLParser
import urllib
from collections import deque


class MyHTMLParser(HTMLParser):
    """
    Takes in the source code of a page. 
    This parser only takes care of looking for all valid links.
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []      # a list of result links
    def handle_starttag(self, tag, attrs):
        if tag == "a" and len(attrs) > 0:
            attrd = dict(attrs)
            if "href" in attrd.keys():
                # attrd["href"] is the link
                if ("#" not in attrd["href"] and
                    ":" not in attrd["href"] and 
                    "&action=edit" not in attrd["href"] and 
                    "en.wikipedia.org/wiki/Main_Page" not in attrd["href"]):
                    # See if it is a page in WIKI:
                    if (attrd["href"].startswith("/") and
                        "www." not in attrd["href"] and
                        ".com" not in attrd["href"] and 
                        ".org" not in attrd["href"]):
                        self.links.append("https://en.wikipedia.org" + 
                                          attrd["href"])
                    elif (attrd["href"].startswith("http://en.wikipedia.org") or
                          attrd["href"].startswith("https://en.wikipedia.org")):
                        self.links.append(attrd["href"])
                    elif ("en.wikipedia.org" in attrd["href"]):
                        self.links.append(attrd["href"])
    def return_result_links(self):
        return self.links


if __name__ == '__main__':
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    f = urllib.urlopen(seed)
    crawler = MyHTMLParser()
    crawler.feed(f.read())
    result = crawler.return_result_links()
    f.close()
    record = open("TESTRECORD", "w")
    for item in result:
        record.write("Link:  " + item + "\n")
        
        