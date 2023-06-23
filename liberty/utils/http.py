from functools import lru_cache
from urllib.parse import parse_qs, urlparse
from json import loads

MAX_LINE = 64*1024
MAX_HEADERS = 100





class HttpServerError:

	class HTTPError(Exception):
		def __init__(self, status, reason, body=None):
			super()
			self.status = status
			self.reason = reason
			self.body = body


	class IncorrectResponseData(Exception):
		"""
		Error while returning file,
		Maybe you are not returning an instance of the class "Response"
		"""
		def __init__(*args, **kwargs):
			Exception.__init__(*args, **kwargs)



	class JsonProcessingError(Exception):
		"""
		Error while converting to json
		"""
		def __init__(*args, **kwargs):
			Exception.__init__(*args, **kwargs)


	class ReadHtmlError(Exception):
		"""
		Error when trying to read or open Html file
		"""
		def __init__(*args, **kwargs):
			Exception.__init__(*args, **kwargs)





class HttpServerObjects:


	class Request:
		def __init__(self, method, target, version, headers, rfile):
			self.method = method
			self.target = target
			self.version = version
			self.headers = headers
			self.rfile = rfile

		@property
		def path(self):
			return self.url.path

		@property
		@lru_cache(maxsize=None)
		def args(self):
			return parse_qs(self.url.query)

		@property
		@lru_cache(maxsize=None)
		def url(self):
			return urlparse(self.target)

		@property
		def body(self):
			size = self.headers.get('Content-Length')
			if not size:
				return None
			return self.rfile.read(int(size))

		@property
		def data(self):
			body = self.body
			if body is None: return None
			try:
				return loads(body)
			except:
				body = str(body)[2:-2]
				bufer = dict()
				for part in body.split("&"):
					values = part.split("=")
					bufer[values[0]] = values[1]

				return bufer

	class Response:
		def __init__(self, status: int = 200, reason: str = "OK", headers=None, body=None):
			self.status = status
			self.reason = reason
			self.headers = headers
			self.body = body



class HtmlFile:
	def __init__(self, path: str, encoding: str = None, **kwargs):
		self.path = path
		self.encoding = encoding
		self.text = self.read_file()
		if kwargs:self.set_kwargs(kwargs)


	def read_file(self):
		try:
			with open(self.path, "r", encoding=self.encoding) as file:
				return file.read()
		except Exception as e:raise HttpServerError.ReadHtmlError(e)


	def set_kwargs(self, kwargs: dict):
		for key, value in kwargs.items():
			self.text=self.text.replace('{'+key+'}', value)