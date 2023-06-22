from liberty import HttpServer, HttpServerObjects


server = HttpServer()
@server.route("/index")
def on_index(request):
	return HttpServerObjects.Response(body="HI")



if __name__ == "__main__":
	server.run()