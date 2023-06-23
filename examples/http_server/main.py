from liberty import HttpServer, HtmlFile


server = HttpServer()
@server.route("/index")
def on_index(request):
	name = request.args.get("name", ["Friend"])[0]
	return server.html_response(f"<H>Hello, {name}</H>")

@server.route("/file")
def on_html_file(request):
	name = request.args.get("name", ["Friend"])[0]
	file  = HtmlFile(path="html/test.html", encoding="utf-8", name="Fried")
	return server.html_response(file)



@server.route("/json")
def on_json(request):
	return server.json_response({"resp": "Hello"})


@server.error(404)
def on_404(error):
	return server.make_response("Not Found", status=404, reason="Not Found")



if __name__ == "__main__":
	server.run()