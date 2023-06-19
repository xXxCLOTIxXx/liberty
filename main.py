import asyncio
import json
from aiohttp import web
import liberty.serverLib as api


routes = web.RouteTableDef()
app = api.Liberty()

@routes.get('/index')
async def index_handler(request):
	file = api.HtmlFile(path="html/index.html", encoding="utf-8")
	return app.html_response(text=file)


@routes.get('/index_change')
async def index_handler(request):
	file = api.HtmlFile(path="html/index_change.html", encoding="utf-8", name="Fried")
	return app.html_response(text=file)




@routes.get('/')
async def index_handler_text(request):
	return app.html_response(text="HI")

@routes.get('/json')
async def json_handler(request):
	return app.json_response(text={"key": "hi"})



if __name__ == "__main__":
	asyncio.run(app.run(routes=routes))
