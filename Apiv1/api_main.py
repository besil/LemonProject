__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle, static_file, request
from elasticsearch import Elasticsearch


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.es = Elasticsearch()
        self.route('/status', callback=self.status)
        self.route("/index", callback=self.index)
        self.route("/search", callback=self.search, method='POST')
        # self.route("/test/search", callback=self.test_search)
        self.route("/test", callback=self.test)
        self.route("/js/<filename>", callback=self.js)

    def status(self):
        return {"status": "alive"}

    @staticmethod
    def index():
        return static_file("index.html", root="templates/")

    def search(self):
        # pprint(request)
        # pprint("request.forms: {}".format(request.forms))
        # pprint("request.forms.keys(): {}".format(request.forms.keys()))
        # pprint("request.json: {}".format( request.json) )

        params = request.json
        query = params['query']

        print("Searching for: {}".format(query))
        docs = self.es.search(index="text_data", fields=["_id", "score"], size=200, body={
            "query": {
                "match": {
                    "data": query
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

        d = dict()
        d['query'] = query
        d['data'] = hits['hits']
        return d;

    # def test_search(self):
    #     print("Here in test/search")
    #     d = dict()
    #     d['data'] = ["ciao", "mondo"]
    #     return d

    def test(self):
        return static_file("test.html", root="templates/")

    def js(self, filename):
        return static_file(filename, root="js/")

if __name__ == '__main__':
    app = Api()
    # app = UrlServer()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
