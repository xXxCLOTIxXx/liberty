import requests
from json import dumps

print(requests.post("http://localhost:8080/", data={"name": "Oleg", "job": 'teacher'}).text)