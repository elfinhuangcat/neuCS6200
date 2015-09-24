#! /usr/bin/python2
from HTMLParser import HTMLParser

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
        if tag == "a" and len(attrs) > 0:
            attrd = dict(attrs)
            if "href" in attrd.keys():
                # attrd["href"] is the link
                if (attrd["href"].startswith("http://en.wikipedia.org/wiki/") or
                    attrd["href"].startswith("https://en.wikipedia.org/wiki/")):
                    # Absolute en.wikipedia.org links
                    if ('#' not in attrd["href"] and
                        ':' not in attrd["href"][5:] and # the only difference
                        "&action=edit" not in attrd["href"] and
                        not (attrd["href"].endswith("wiki/Main_Page") or
                             attrd["href"].endswith("wiki/Main_Page/"))):
                        self.links.append(attrd["href"])
                elif attrd["href"].startswith("/wiki"):
                    # Relative wiki links
                    if ('#' not in attrd["href"] and
                        ':' not in attrd["href"] and # the only diffrence
                        "&action=edit" not in attrd["href"] and
                        not (attrd["href"].endswith("wiki/Main_Page") or
                             attrd["href"].endswith("wiki/Main_Page/"))):
                        self.links.append("https://en.wikipedia.org" + 
                                          attrd["href"])
        elif tag == "body":
            self.body = True # Flag begin body content
    def handle_endtag(self, tag):
        if tag == "body" and self.body:
            self.body = False # Flag end body content
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
        
        
