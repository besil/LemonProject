__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle, static_file, request
from elasticsearch import Elasticsearch
from pprint import pprint


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.es = Elasticsearch()
        self.route('/status', callback=self.status)
        self.route("/index", callback=self.index)
        self.route("/search", callback=self.search, method='POST')
        self.route("/test", callback=self.test)
        self.route("/js/<filename>", callback=self.js)

    def status(self):
        return {"status": "alive"}

    @staticmethod
    def index():
        return static_file("index.html", root="templates/")

    def search(self):
        params = request.json
        query = params['query']
        limit = params['limit']

        print("Searching for: {}".format(query))
        docs = self.es.search(index="text_data", fields=["_id", "score"], size=limit, body={
            "query": {
                "bool": {
                    "must": {
                        "prefix": {
                            "data": query
                        }
                    }
                }
            }
        })

        hits = docs['hits']
        # print("Tot documents retrived: {}".format(len(hits)))
        # pprint(docs.keys())
        # pprint(hits)
        print("hits.keys(): {}".format(hits.keys()))
        # print( "hits['hits']: {}".format(hits['hits']))

        # for i in range(10):
        #     print( hits['hits'][i] )
        data = hits['hits']
        total = hits['total']
        pprint(data)
        pprint("Total documents found: {}".format(total))

        d = dict()
        d['query'] = query
        d['data'] = data
        d['limit'] = limit
        d['total'] = total
        return d;

    def test(self):
        return static_file("test.html", root="templates/")

    def js(self, filename):
        return static_file(filename, root="js/")


if __name__ == '__main__':
    app = Api()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
