# -*- coding: utf-8 -*-
import json
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado import gen


class CheckServerHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        data = {'status': 'OK'}
        data = json.dumps(data)
        self.write(data)

    @gen.coroutine
    def post(self):
        machine = self.get_argument("machine")
        inner_status = self.get_argument("inner")
        datetime = self.get_argument("datetime")
        received = {'machine': machine,
                    'status': inner_status,
                    'datetime': datetime}
        print(received)
        data = {'status': 'OK'}
        data = json.dumps(data)
        self.write(data)


class CardTypesHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        data = {'types': ['discount', 'bonus', 'loyalty']}
        data = json.dumps(data)
        print('Send types: ' + data)
        self.write(data)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.write('OK GET')

    @gen.coroutine
    def post(self):
        self.write('OK POST')


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/server_status", CheckServerHandler),
            (r"/card_types", CardTypesHandler),
            (r"/.*", MainHandler),
        ]
        settings = dict(
            app_title='Marynado',
            xsrf_cookies=False,  # Turn ON and add csrf tokens to forms
            cookie_secret="hgqimqierg#qcieohgc*qoeihx@#qeihr",
            debug=True,
            login_url="/auth/login/"
        )
        super(Application, self).__init__(handlers, **settings)


if __name__ == "__main__":
    application = Application()
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen('8888')
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()
