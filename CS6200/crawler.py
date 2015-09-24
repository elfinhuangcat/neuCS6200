from htmlparser import *
from collections import deque
import urllib
import sys  
import time

reload(sys)  
sys.setdefaultencoding('utf8')
class MyCrawler:
    def __init__(self, seed, phrase):
        self.cur_queue = deque([])
        self.next_queue = deque([])
        self.result_links = []
        self.cur_lv = 1 # current depth
        self.MAXDEPTH = 5
        self.MAXLINKS = 1000
        self.SEED = seed
        self.KEY = phrase
        self.visited = set() # A set of visited pages
    def crawl(self):
        self.cur_queue.append(self.SEED)
        while (self.cur_lv < (self.MAXDEPTH + 1) and
               len(self.result_links) <= self.MAXLINKS and 
               (len(self.cur_queue) > 0 or len(self.next_queue) > 0)):
            time_start = time.time()
            cur_link = self.cur_queue.popleft()
            if cur_link not in self.visited:
                self.visited.add(cur_link)
                ###DEBUGGG
                print("Visited: " + cur_link)
                page = urllib.urlopen(cur_link)
                # page = requests.get(cur_link)
                parser = MyHTMLParser(self.KEY)
                if self.cur_lv == 1:
                    # The seed page is always valid
                    parser.set_valid()

                parser.feed(page.read())
                page.close() # IMPORTANT!

                if parser.get_valid(): 
                    self.result_links.append(cur_link)
                    for item in parser.return_result_links():
                        if item not in self.visited:
                            self.next_queue.append(item)

            if len(self.cur_queue) == 0:
                # Go to next level?
                self.cur_queue = self.next_queue
                self.next_queue = deque([])
                self.cur_lv += 1
            
            time_end = time.time()
            #if time_end - time_start < 1:
            #    time.sleep(1 - (time_end - time_start)) # be polite
        if len(self.result_links) > self.MAXLINKS:
            self.result_links = self.result_links[:self.MAXLINKS]
    def output_result(self):
        print("The result list length: " + str(len(self.result_links)))
        print("Crawled depth: " + str(self.cur_lv - 1))
        print("Total visited pages: " + str(len(self.visited)))
        if self.KEY:
            result_f = open("with_key_result", "w")
            for link in self.result_links:
                result_f.write(link + "\n")
            print("The crawled urls are stored in file: " + "with_key_result")
            result_f.close()
        else:
            result_f = open("no_key_result", "w")
            for link in self.result_links:
                result_f.write(link + "\n")
            print("The crawled urls are stored in file: " + "no_key_result")
            result_f.close()


if __name__ == '__main__':
    print("Crawl without key phrase:")
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    nokey_crawler = MyCrawler(seed, '')
    nokey_crawler.crawl()
    nokey_crawler.output_result()

    print("Crawl with key phrase \'concordance\':")
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    key = 'concordance'
    withkey_crawler = MyCrawler(seed, key)
    withkey_crawler.crawl()
    withkey_crawler.output_result()
            
