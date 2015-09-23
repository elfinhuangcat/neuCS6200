#! /usr/bin/python2
from HTMLParser import HTMLParser
import urllib



class MyHTMLParser(HTMLParser):
    def __init__(self, phrase):
        HTMLParser.__init__(self)
        self.links = []      # a list of result links
        self.valid = False
        self.key = phrase
        self.body = False    # track if now is inside the body tag
        if not self.key:
            self.valid = True    # Key phrase is not required. Always valid page.
    def handle_starttag(self, tag, attrs):
        if tag == "a" and len(attrs) > 0 and self.valid:
            attrd = dict(attrs)
            if "href" in attrd.keys():
                # attrd["href"] is the link
                if ("#" not in attrd["href"] and
                    ":" not in attrd["href"] and 
                    "&action=edit" not in attrd["href"] and 
                    "en.wikipedia.org/wiki/Main_Page" not in attrd["href"]):
                    # See if it is a page in WIKI:
                    if (attrd["href"].startswith("/") and
                        not attrd["href"].startswith("//")):
                        self.links.append("https://en.wikipedia.org" + 
                                          attrd["href"])
                    elif (attrd["href"].startswith("http://en.wikipedia.org") or
                          attrd["href"].startswith("https://en.wikipedia.org")):
                        self.links.append(attrd["href"])
                    elif ("en.wikipedia.org" in attrd["href"]):
                        self.links.append(attrd["href"])
        elif tag == "body":
            self.body = True
    def handle_endtag(self, tag):
        if tag == "body" and self.body:
            self.body = False
    def handle_data(self, data):
        # Handle the data with the body tag
        if self.body and self.key in data:
            self.valid = True
    def return_result_links(self):
        return self.links
    def set_valid(self):
        # CAUTION! This can only be used on seed page!
        self.valid = True
    def get_valid(self):
        return self.valid

if __name__ == '__main__':
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    f = urllib.urlopen(seed)
    crawler = MyHTMLParser("concordance")
    crawler.feed(f.read())
    result = crawler.return_result_links()
    f.close()
    record = open("TESTRECORD", "w")
    for item in result:
        record.write("Link:  " + item + "\n")
        
        
