__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle


class UrlServer(Bottle):
    def __init__(self, start_doc=0):
        super(UrlServer, self).__init__()
        self.url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid={}"
        self.current_doc = start_doc

        self.workers = set()
        self.route('/new', callback=self.new_url)

    def new_url(self):
        doc_id = self.current_doc
        self.current_doc += 1
        return {"doc_id": doc_id, "url": self.url.format(doc_id)}


if __name__ == '__main__':
    app = UrlServer(start_doc=49331)
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
