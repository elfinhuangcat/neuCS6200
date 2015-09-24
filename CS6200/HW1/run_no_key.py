from crawler import *

if __name__ == '__main__':
    print("Crawl without key phrase:")
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    nokey_crawler = MyCrawler(seed, '')
    nokey_crawler.crawl()
    nokey_crawler.output_result()
