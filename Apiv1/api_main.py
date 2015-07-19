__author__ = 'besil'

import utils

utils.check()
from bottle import Bottle


class Api(Bottle):
    def __init__(self):
        super(Api, self).__init__()
        self.route('/status', callback=self.status)

    def status(self):
        return {"status": "alive"}

if __name__ == '__main__':
    app = Api()
    # app = UrlServer()
    app.run(host=utils.url_server_host, port=utils.url_server_port, debug=True)
