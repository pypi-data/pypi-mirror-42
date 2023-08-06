#!/usr/bin/env python
import sys
import logging
import json
import tornado.web
import tornado.ioloop
from tornado.options import define, options, parse_command_line


define('port', default=8888, help='port', type=int)
parse_command_line()


def _tran_to_json(items):
    if isinstance(items,dict):
        new_item = {}
        for k,v in items.items():
            new_item[k] = _tran_to_json(v)
        return new_item
    elif isinstance(items, list):
        new_item = []
        for x in items:
            new_item.append(_tran_to_json(x))
        return new_item
    elif isinstance(items, (str, int, float)):
        return items
    elif sys.version >= '3' and isinstance(items, bytes):
        try:
            data = items.decode('ascii')
            return data
        except:
            return str(items)
    else:
        return str(items)


class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        if self.request.headers.get('Content-Type') == 'application/json':
            body = json.loads(self.request.body)
        else:
            body = self.request.body
        data = _tran_to_json({'path': self.request.uri,
                  'method': self.request.method,
                  'headers': dict(self.request.headers),
                  'remote_ip': self.request.remote_ip,
                  'protocol': self.request.protocol,
                  'arguments': self.request.arguments,
                  'body': body
                  })
        self.ret = json.dumps(data, indent=True, ensure_ascii=False)
        print(self.ret)

    def get(self):
        self.write(self.ret)

    def post(self):
        self.write(self.ret)

    def head(self):
        self.write(self.ret)

    def patch(self):
        self.write(self.ret)

    def put(self):
        self.write(self.ret)

    def delete(self):
        self.write(self.ret)


def make_app():
    return tornado.web.Application([(r"/.*", MainHandler),])


def main():
    app = make_app()
    app.listen(options.port)
    logging.info('start webserver on port {}'.format(options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
