__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle, static_file


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.route('/status', callback=self.status)
        self.route("/index", callback=self.index)
        self.route("/js/<filename>", callback=self.js)

    def status(self):
        return {"status": "alive"}

    def index(self):
        return static_file("index.html", root="templates/")

    def js(self, filename):
        return static_file(filename, root="js/")

if __name__ == '__main__':
    app = Api()
    # app = UrlServer()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
