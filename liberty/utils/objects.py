

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
		except Exception as e:raise ReadHtmlError(e)


	def set_kwargs(self, kwargs: dict):
		for key, value in kwargs.items():
			self.text=self.text.replace('{'+key+'}', value)
