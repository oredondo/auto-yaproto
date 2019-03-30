import requests
from contextlib import closing

print(requests.get('http://127.0.0.1:5000/api/deploy').text)

while True:
    with closing(requests.get('http://127.0.0.1:5000/api/stream', stream=True)) as r:
        print(r.text)