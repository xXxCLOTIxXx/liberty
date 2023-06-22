from .utils.http_exceptions import (
	HTTPError
)
from .utils.objects import HttpServerObjects

from .utils.colors import *
from .utils.http_constants import *

import json
import socket
import sys
from email.parser import Parser
from os import system as shell

from traceback import print_exc




class HttpServerCore:
	routes = list()

	def __init__(self, host: str = "localhost", port: int = 8080, server_name: str = None, info: bool = True):
		self._host = host
		self._port = port
		self._server_name = server_name if server_name else host
		self._users = {}
		self._show_info = info




	def run(self, host: str = None, port: int = None, server_name: str = None):
		shell("clear || cls")
		if host: self._host = host
		if port: self._port = port
		if server_name: self._server_name = server_name
		print(f"The server is running at: {self._host}:{self._port}")
		try:self.serve_forever()
		except KeyboardInterrupt:
			pass


	def serve_forever(self):
		serv_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM, proto=0)
		try:
			serv_sock.bind((self._host, self._port))
			serv_sock.listen()

			while True:
				connect, _ = serv_sock.accept()
				try:
					self.serve_client(connect)
				except:
					print(RED)
					print_exc()
					print(RESET)
		finally:
			serv_sock.close()


	def serve_client(self, connect):
		try:
			request = self.parse_request(connect)
			resp = self.handle_request(request)
			self.send_response(connect, resp)
		except ConnectionResetError:
			connect = None
		except Exception as e:
			self.send_error(connect, e)

		if connect:
			request.rfile.close()
			connect.close()



	def parse_request(self, connect):
		read = connect.makefile('rb')
		method, target, ver = self.parse_request_line(read)
		headers = self.parse_headers(read)
		host = headers.get('Host')
		print(f"{CYAN}[{method}][{ver}][{host}]{BLUE}#~ {target}{RESET}")
		if not host:
			raise HTTPError(400, 'Bad request', 'Host header is missing')
		if host not in (self._server_name, f'{self._server_name}:{self._port}'):
			raise HTTPError(404, 'Not found')
		return HttpServerObjects.Request(method, target, ver, headers, read)


	def parse_request_line(self, file):
		raw = file.readline(MAX_LINE + 1)
		if len(raw) > MAX_LINE:
			raise HTTPError(400, 'Bad request', 'Request line is too long')
		req_line = str(raw, 'iso-8859-1')
		words = req_line.split()
		if len(words) != 3:
			raise HTTPError(400, 'Bad request', 'Malformed request line')
		method, target, ver = words
		if ver != 'HTTP/1.1':
			raise HTTPError(505, 'HTTP Version Not Supported')

		return method, target, ver


	def parse_headers(self, file):
		headers = []
		while True:
			line = file.readline(MAX_LINE + 1)
			if len(line) > MAX_LINE:
				raise HTTPError(494, 'Request header too large')
			if line in (b'\r\n', b'\n', b''):
				break
			headers.append(line)
			if len(headers) > MAX_HEADERS:
				raise HTTPError(494, 'Too many headers')

		sheaders = b''.join(headers).decode('iso-8859-1')
		return Parser().parsestr(sheaders)





	def handle_request(self, request):
		for route in self.routes:
			if request.path == route.get("endpoint") and request.method in route.get("methods", []):
				return route.get("func")(request)
		raise HTTPError(404, 'Not found')


	def send_response(self, connect, response):
		wfile = connect.makefile('wb')
		status_line = f'HTTP/1.1 {response.status} {response.reason}\r\n'
		wfile.write(status_line.encode('iso-8859-1'))

		if response.headers:
			for (key, value) in response.headers:
				header_line = f'{key}: {value}\r\n'
				wfile.write(header_line.encode('iso-8859-1'))

		wfile.write(b'\r\n')

		if response.body:
			wfile.write(response.body.encode("utf-8") if isinstance(response.body, str) else response.body)

		wfile.flush()
		wfile.close()

	def send_error(self, connect, error):
		try:
			status = error.status
			reason = error.reason
			body = (error.body or error.reason).encode('utf-8')
		except:
			status = 500
			reason = b'Internal Server Error'
			body = b'Internal Server Error'
		response = HttpServerObjects.Response(status, reason,[('Content-Length', len(body))], body)
		self.send_response(connect, response)




class HttpServer(HttpServerCore):
	def __init__(self, host: str = "localhost", port: int = 8080, server_name: str = None, info: bool = True):
		HttpServerCore.__init__(self, host, port, server_name, info)


	def route(self, endpoints: str, methods: list = ["GET", "POST"]):
		def add_route(func):
			self.routes.append({"func": func, "methods": methods, "endpoint": endpoints})

			return self.routes

		return add_route
