import requests

res = requests.get("http://127.0.0.1/news/")
print(res.json())