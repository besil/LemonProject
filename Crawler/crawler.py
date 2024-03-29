__author__ = 'besil'

import utils
utils.check()

import json
import argparse
import logging
from elasticsearch import Elasticsearch
import time, urllib.request
from html.parser import HTMLParser


class Crawler(HTMLParser, object):
    def __init__(self, verbose=False):
        # super(HTMLParser, self).__init__(self)
        HTMLParser.__init__(self)
        self.text_data = ""
        self.skip = False
        self.log = self._initLogger(verbose)

    def get_new_url(self):
        url_server = "http://{}:{}/new".format(utils.url_server_host, utils.url_server_port)

        f = urllib.request.urlopen(url_server)
        return f.read().decode("utf-8")

    def start(self, proceed=lambda crawled_docs: crawled_docs < 1, min_size=4610):
        crawled_docs = 0
        while proceed(crawled_docs):
            # for _ in range(crawls):
            url_data = json.loads(self.get_new_url())
            url = url_data['url']
            doc_id = url_data['doc_id']

            self.log.debug("Crawling {}".format(url))

            f = urllib.request.urlopen(url)
            data = str(f.read().decode("utf-8"))

            self.feed(data)
            self.text_data = self.text_data.strip()
            self.log.debug("Final text_data: {}".format(self.text_data))

            if len(data) > min_size:
                self.persist(doc_id, raw_data=data, text_data=self.text_data)
                self.text_data = ""
                crawled_docs += 1
                if crawled_docs % 10 == 0:
                    self.log.info("Crawled {} documents".format(crawled_docs))
            time.sleep(1)

    def _initLogger(self, verbose=False):
        log = logging.getLogger()

        level = logging.DEBUG if verbose else logging.INFO
        log.setLevel(level)
        # print("Setting level to {}".format(level))

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # fh = logging.FileHandler("{}/deploylog.log".format(self.logdir))
        # fh.setLevel(level)
        # fh.setFormatter(formatter)
        # log.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        log.addHandler(ch)

        return log

    def handle_starttag(self, tag, attrs):
        if 'script' in tag:
            self.skip = True

    def handle_endtag(self, tag):
        if 'script' in tag:
            self.skip = False

    def handle_data(self, data):
        # print("Data is: {}".format(data))
        if not self.skip:
            self.text_data += data.strip() + "\n"

    def persist(self, data):
        raise Exception("Must never be called")

class FileCrawler(Crawler):
    def __init__(self, verbose=False):
        Crawler.__init__(self, verbose=verbose)
        self.log.debug("Chosen FileCrawler implementation")
        self.log.info("Storing data in {} directories".format("data/{raw, text}/"))

    def persist(self, doc_id, raw_data="", text_data=""):
        if raw_data != "":
            with open("data/raw/document_{}.html".format(doc_id), "w") as out:
                out.write(raw_data)
                out.flush()
        if raw_data != "":
            with open("data/text/document_{}.txt".format(doc_id), "w") as out:
                out.write(text_data)
                out.flush()

class ElasticCrawler(Crawler):
    def __init__(self, verbose=False):
        Crawler.__init__(self, verbose=verbose)
        self.log.debug("Chosen ElasticCrawler implementation")
        self.log.info("Available Web UI at http://localhost:9200/_plugin/head/")
        self.es = Elasticsearch()

    def persist(self, doc_id, raw_data="", text_data=""):
        doc = {"id": doc_id, "data": raw_data}
        self.es.index(index="raw_data", doc_type="text", id=doc_id, body=doc)
        doc = {"id": doc_id, "data": text_data}
        self.es.index(index="text_data", doc_type="text", id=doc_id, body=doc)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbosity on")
    parser.add_argument("--crawls", "-c", type=int,
                        help="The number of document to crawl (-1 for infinite)", default=1)
    parser.add_argument("--save", help="Type of saving",
                        choices=["file", "elasticsearch"], default="file")

    args = parser.parse_args()

    crawler_type = FileCrawler if args.save == 'file' else ElasticCrawler
    crawler = crawler_type(verbose=args.verbose)

    proceed = lambda cc: cc < args.crawls if args.crawls > 0 else lambda cc: True
    crawler.start(proceed=proceed)
