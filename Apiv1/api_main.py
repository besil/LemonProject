__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle, static_file
from elasticsearch import Elasticsearch

class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.es = Elasticsearch()
        self.route('/status', callback=self.status)
        self.route("/index", callback=self.index)
        self.route("/search/<query>", callback=self.search, method='POST')
        # self.route("/test/search", callback=self.test_search)
        self.route("/test", callback=self.test)
        self.route("/js/<filename>", callback=self.js)

    def status(self):
        return {"status": "alive"}

    def index(self):
        return static_file("index.html", root="templates/")

    def search(self, query):
        print("Searching for: {}".format(query))
        docs = self.es.search(index="text_data", body={"query": {"match_all": {}}})
        hits = docs['hits']
        print("Tot documents found: {}".format(len(hits)))
        d = dict()
        d['query'] = query
        d['data'] = hits
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
