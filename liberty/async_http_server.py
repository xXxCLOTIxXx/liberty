
from .utils.http import (
	HttpServerError,
	HttpServerObjects,
	HtmlFile

)
from .utils.colors import *

import asyncio
from aiohttp import web
from typing import Optional, Any, Union
import json
from os import system as shell



class AsyncHttpServer:
	def __init__(self, host: str = "localhost", port: int = 8080):
		self.host, self.port = host, port

	async def run(self, routes: web.RouteTableDef, host: str = None, port: int = None):
		shell("clear || cls")
		if host: self.host = host
		if port: self.port = port
		app = web.Application()
		app.add_routes(routes)
		runner = web.AppRunner(app)
		await runner.setup()
		site = web.TCPSite(runner, self.host, self.port)
		await site.start()
		print(f"{GREEN}The server was started at: {self.host}:{self.port}{RED}\nPress Ctrl + C to exit{RESET}")
		while True:
			await asyncio.sleep(3600)


	def response(self,
		body: Any = None,
		status: int = 200,
		reason: Optional[str] = None,
		text: Optional[str] = None,
		headers: Optional = None,
		content_type: Optional[str] = None,
		charset: Optional[str] = None,
		zlib_executor_size: Optional[int] = None,
		zlib_executor: Optional = None,
		) -> None:

		return web.Response(
				body=body,
				status=status,
				reason=reason,
				text=text,
				headers=headers,
				content_type=content_type,
				charset=charset,
				zlib_executor_size=zlib_executor_size,
				zlib_executor=zlib_executor)


	def json_response(
		self,
		text: Optional[str] = None,
		body: Optional[bytes] = None,
		status: int = 200,
		reason: Optional[str] = None,
		headers: Optional = None,
		content_type: str = "application/json",
		dumps: json.JSONEncoder = json.dumps) -> web.Response:
		if text:
			try:text = dumps(text)
			except Exception as e:raise HttpServerError.JsonProcessingError(e)

		return self.response(
			text=text,
			body=body,
			status=status,
			reason=reason,
			headers=headers,
			content_type=content_type,
		)


	def html_response(self,
		text: Union[str, HtmlFile],
		status: int = 200,
		headers: Optional = None,
		) -> web.Response:
		if isinstance(text, HtmlFile):
			text=text.text

		return self.response(
			text=text,
			status=status,
			headers=headers,
			content_type="text/html",
		)
