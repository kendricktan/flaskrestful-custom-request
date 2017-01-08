import msgpack
import requests

print('Sending acceptable POST request in msgpack data...')
d = {'data': 'potatoes and molasses'}
r = requests.post('http://localhost:5000/', data=msgpack.packb(d),
                  headers={'Accept': 'application/msgpack', 'Content-Type': 'application/msgpack'})
print(r.text)

print('----' * 20)

print('Sending acceptable POST request in JSON data...')
r = requests.post('http://localhost:5000/', data=d,
                  headers={'Accept': '*', 'Content-Type': 'application/json'})
print(r.text)
