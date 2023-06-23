from liberty import HttpServer, HtmlFile
from json import loads

server = HttpServer()
@server.route("/", ["POST"])
def on_index(request):
	data = request.data
	return server.json_response({"key": f"hello, {data.get('name', 'friend')}"})



if __name__ == "__main__":
	server.run()