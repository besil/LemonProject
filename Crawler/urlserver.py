__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle
import os

class UrlServer(Bottle):
    def __init__(self, start_doc=0):
        super(UrlServer, self).__init__()
        self.url = "http://curia.europa.eu/juris/document/document_print.jsf?doclang=IT&pageIndex=0&part=1&mode=req&docid={}"
        self.url_count_file = "files/urlcount"

        self.current_doc = self._get_starting_doc(start_doc=start_doc)
        print("Actual doc count is: {}".format(self.current_doc))

        self.workers = set()
        self.route('/new', callback=self.new_url)

    def _get_starting_doc(self, start_doc=0):
        """
        The document count is persisted in files/urlcount file.
        If the UrlServer crashes, the count is not lost.
        If you want to start crawling from the beginning, simply delete the file.
        UrlServer will re-create it, starting from 0
        """
        filename = self.url_count_file
        if not os.path.isfile(filename):
            with open(filename, 'w') as f:
                f.write(str(start_doc))
                f.flush()

        count = -1
        with open(filename, 'r') as fin:
            line = fin.readline()
            if line == "":
                print("Removing and recreating")
                os.remove(filename)
                return self._get_starting_doc()
            count = int(line)
            if count != start_doc:
                print(
                    "Count is different from start_doc={}. Regenerating the file with {}".format(start_doc, start_doc))
                os.remove(filename)
                return self._get_starting_doc(start_doc)
        return count

    def new_url(self):
        doc_id = self.current_doc
        self.current_doc += 1
        with open(self.url_count_file, 'w') as f:
            f.write(str(self.current_doc))
        return {"doc_id": doc_id, "url": self.url.format(doc_id)}


import argparse
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="UrlServer")
    parser.add_argument("--start-doc", "-sd", type=int, default=0, help="Starting document id")

    args = parser.parse_args()

    app = UrlServer(start_doc=args.start_doc)
    # app = UrlServer()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
