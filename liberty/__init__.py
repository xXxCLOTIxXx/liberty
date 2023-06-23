"""
Author: Xsarz
Enjoy using!
"""

from .utils.http import (
	MAX_LINE,
	MAX_HEADERS,
	HttpServerError,
	HttpServerObjects,
	HtmlFile

)

from .utils import colors
from .async_http_server import AsyncHttpServer
from .http_server import HttpServer, HttpServerCore

from os import system as s
from requests import get

__title__ = 'liberty'
__author__ = 'Xsarz'
__license__ = 'MIT'
__copyright__ = 'Copyright 2023 Xsarz'
__version__ = '1.0.31'
__newest__ = get("https://pypi.org/pypi/liberty.py/json").json()["info"]["version"]



if __version__ != __newest__:
	s('cls || clear')
	print(f'{colors.ORANGE}{__title__} made by {__author__}\nPlease update the library. Your version: {__version__}  A new version: {__newest__}{colors.DEFAULT}')