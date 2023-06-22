"""
Author: Xsarz
Enjoy using!
"""

from .utils.exceptions import (
	JsonProcessingError,
	ReadHtmlError
)
from .utils.objects import (
	HtmlFile,
	HttpServerObjects
)
from .utils.http_constants import *
from .utils import helpers, colors
from .async_http_server import AsyncHttpServer
from .http_server import HttpServer

from os import system as s
from json import loads
from requests import get

__title__ = 'liberty'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Xsarz'
__version__ = '1.0'
__newest__ = __version__#loads(get("").text)["info"]["version"]



if __version__ != __newest__:
	s('cls || clear')
	print(f'{colors.ORANGE}{__title__} made by {__author__}\nPlease update the library. Your version: {__version__}  A new version: {__newest__}{colors.DEFAULT}')