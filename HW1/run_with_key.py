from crawler import *

if __name__ == '__main__':
    print("Crawl with key phrase \'concordance\':")
    seed = "https://en.wikipedia.org/wiki/Hugh_of_Saint-Cher"
    key = 'concordance'
    withkey_crawler = MyCrawler(seed, key)
    withkey_crawler.crawl()
    withkey_crawler.output_result()
