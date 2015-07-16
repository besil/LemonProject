__author__ = 'besil'

import utils
utils.check()

import json
from elasticsearch import Elasticsearch
import time, urllib.request


class Crawler(object):
    def __init__(self):
        pass

    def get_new_url(self):
        url_server = "http://{}:{}/new".format(utils.url_server_host, utils.url_server_port)

        f = urllib.request.urlopen(url_server)
        return f.read().decode("utf-8")

    def start(self, crawls=1, min_size=5000):
        for _ in range(crawls):
            url_data = json.loads(self.get_new_url())
            url = url_data['url']
            doc_id = url_data['doc_id']
            print("Crawling {}".format(url))

            crawled_docs = 0
            f = urllib.request.urlopen(url)

            data = str(f.read().decode("utf-8"))

            #     # print("{} -> {}: {}".format(outname, len(data), len(data) > 4610))
            if len(data) > min_size:
                self.persist(doc_id, data)

                #         doc = {"id": doc_id, "data": data}
                #         es.index(index="crawling", doc_type="text", id=doc_id, body=doc)
                crawled_docs += 1
                if crawled_docs % 10 == 0: print("Crawled {} documents".format(crawled_docs))
            time.sleep(1)

    def persist(self, data):
        pass


class FileCrawler(Crawler):
    def persist(self, doc_id, data):
        outname = "data/document_{}.html".format(doc_id)
        with open(outname, "w") as out:
            out.write(data)
            out.flush()


class ElasticCrawler(Crawler):
    def __init__(self):
        self.es = Elasticsearch()

    def persist(self, doc_id, data):
        doc = {"id": doc_id, "data": data}
        self.es.index(index="crawling", doc_type="text", id=doc_id, body=doc)


if __name__ == '__main__':
    crawler = FileCrawler()

    crawler.start(crawls=10)
