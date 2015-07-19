__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle, static_file


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.route('/status', callback=self.status)
        self.route("/index", callback=self.index)

    def status(self):
        return {"status": "alive"}

    def index(self):
        return static_file("index.html", root="templates/")

if __name__ == '__main__':
    app = Api()
    # app = UrlServer()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
