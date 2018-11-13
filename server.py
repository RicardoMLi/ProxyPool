import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver

from tornado.options import define, options
from tornado.web import RequestHandler
from implement.scheduler import Scheduler
from implement.db import RedisClient

define('port', type=int, default=8000, help='run server on the given port')


class IndexHandler(RequestHandler):
	def get(self):
		self.write('<h1>欢迎使用代理池</h1>')


class GetProxyHandler(RequestHandler):

	def get(self):
		redis = RedisClient()
		self.write(redis.get())

def main():
	tornado.options.parse_command_line()
	app = tornado.web.Application(
			[('/',IndexHandler),
			('/get',GetProxyHandler),
			],
			debug = True
		)
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	tornado.ioloop.IOLoop.current().start()

if __name__ == '__main__':
	s = Scheduler()
	s.run()
	main()
