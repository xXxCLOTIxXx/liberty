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
