from .utils.http import (
	MAX_LINE,
	MAX_HEADERS,
	HttpServerError,
	HttpServerObjects,
	HtmlFile

)
from .utils.colors import *


import json
import socket
import sys
from email.parser import Parser
from os import system as shell
from typing import Union
from traceback import print_exc




class HttpServerCore:
	routes = list()
	errors = list()

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
		print(f"{GREEN}The server was started at: {self._host}:{self._port}{RED}\nPress Ctrl + C to exit{RESET}")
		try:self.serve_forever()
		except KeyboardInterrupt:
			pass
		except OSError as e:
			print(f"{RED}[!] {e}{RESET}")


	def show_err(self):
		if self._show_info:
			print(RED)
			print_exc()
			print(RESET)



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
					self.show_err()
		finally:
			serv_sock.close()


	def serve_client(self, connect):
		try:
			request = self.parse_request(connect)
			resp = self.handle_request(request)
			self.send_response(connect, resp)
			if self._show_info:print(f"{BLACK}{BG_GREEN}[{request.method}][{request.version}][{request.headers.get('Host')}]{BG_RESET}{ORANGE}#~ {request.target}{RESET}")
		except ConnectionResetError:
			connect = None
		except HttpServerError.IncorrectResponseData:
			self.show_err()
			self.send_error(connect, None, request)
		except Exception as e:
			self.send_error(connect, e, request)

		if connect:
			try:request.rfile.close()
			except:pass
			connect.close()



	def parse_request(self, connect):
		read = connect.makefile('rb')
		method, target, ver = self.parse_request_line(read)
		headers = self.parse_headers(read)
		host = headers.get('Host')
		if not host:
			raise HttpServerError.HTTPError(400, 'Bad request', 'Host header is missing')
		if host not in (self._server_name, f'{self._server_name}:{self._port}'):
			raise HttpServerError.HTTPError(404, 'Not found')
		return HttpServerObjects.Request(method, target, ver, headers, read)


	def parse_request_line(self, file):
		raw = file.readline(MAX_LINE + 1)
		if len(raw) > MAX_LINE:
			raise HttpServerError.HTTPError(400, 'Bad request', 'Request line is too long')
		req_line = str(raw, 'iso-8859-1')
		words = req_line.split()
		if len(words) != 3:
			raise HttpServerError.HTTPError(400, 'Bad request', 'Malformed request line')
		method, target, ver = words
		if ver != 'HTTP/1.1':
			raise HttpServerError.HTTPError(505, 'HTTP Version Not Supported')

		return method, target, ver


	def parse_headers(self, file):
		headers = []
		while True:
			line = file.readline(MAX_LINE + 1)
			if len(line) > MAX_LINE:
				raise HttpServerError.HTTPError(494, 'Request header too large')
			if line in (b'\r\n', b'\n', b''):
				break
			headers.append(line)
			if len(headers) > MAX_HEADERS:
				raise HttpServerError.HTTPError(494, 'Too many headers')

		sheaders = b''.join(headers).decode('iso-8859-1')
		return Parser().parsestr(sheaders)





	def handle_request(self, request):
		for route in self.routes:
			if request.path == route.get("endpoint"):
				if request.method in route.get("methods", []):
					return route.get("func")(request)
				raise HttpServerError.HTTPError(405, 'Method Not Allowed')
		raise HttpServerError.HTTPError(404, 'Not found')


	def send_response(self, connect, response):
		if not isinstance(response, HttpServerObjects.Response):
			raise HttpServerError.IncorrectResponseData("The object must be an instance of the Response class.")
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

	def send_error(self, connect, error, request):
		try:
			status = error.status
			reason = error.reason
			text = (error.body or reason)
			body = f'<title>{reason}{status}</title><H1>{status}<br>{text}</H1>'.encode('utf-8')
		except:
			status = 500
			reason = b'Internal Server Error'
			body = b'<title>Internal Server Error</title><H1>500<br>Internal Server Error</H1>'
			error = HttpServerError.HTTPError(500, 'Internal Server Error')

		if self._show_info:print(f"{BLACK}{BG_ORANGE}[{request.method}][{request.version}][{request.headers.get('Host')}][{reason} {status}]{BG_RESET}{RED}#~ {request.target} {RESET}")
		try:
			for err in self.errors:
				if status == err.get('status'):
					return self.send_response(connect, err.get("func")(error))
		except:
			self.show_err()
			status = 500
			reason = b'Internal Server Error'
			body = b'<title>Internal Server Error</title><H1>500<br>Internal Server Error</H1>'

		response = HttpServerObjects.Response(status, reason,[('Content-Length', len(body)), ("Content-Type", "text/html; charset=utf-8"), ("Accept-Charset", "utf-8")], body)
		self.send_response(connect, response)




class HttpServer(HttpServerCore):
	def __init__(self, host: str = "localhost", port: int = 8080, server_name: str = None, info: bool = True):
		HttpServerCore.__init__(self, host, port, server_name, info)


	def route(self, endpoints: str, methods: list = ["GET", "POST"]):
		def add_route(func):
			self.routes.append({"func": func, "methods": methods, "endpoint": endpoints})

			return self.routes

		return add_route


	def error(self, status: int):
		def add_error(func):
			self.errors.append({"func": func, "status": status})

			return self.errors
		return add_error


	def make_response(self, text: str, status: int = 200, reason: str = "OK", headers: dict = None):
		return HttpServerObjects.Response(status, reason, headers if headers else [('Content-Length', len(text))], text)


	def html_response(self, text: Union[str, HtmlFile] , status: int = 200, reason: str = "OK", headers: dict = {}):
		if isinstance(text, HtmlFile):
			text = text.text
		buf = [('Content-Length', len(text))]
		for key, value in headers.items():
			buf.append((key, value))
		buf.append(("Accept-Charset", "utf-8"))
		buf.append(("Content-Type", "text/html; charset=utf-8"))
		return self.make_response(
			text,
			status,
			reason,
			buf
			)


	def json_response(self, jspn_value, status: int = 200, reason: str = "OK", headers: dict = {}):
		if isinstance(jspn_value, dict):jspn_value = json.dumps(jspn_value)
		buf = [('Content-Length', len(jspn_value))]
		for key, value in headers.items():
			buf.append((key, value))
		buf.append(("Accept-Charset", "utf-8"))
		buf.append(("Content-Type", "application/json"))
		return self.make_response(
			jspn_value,
			status,
			reason,
			buf
			)