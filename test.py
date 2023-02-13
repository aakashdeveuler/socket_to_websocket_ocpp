import json

from socket_to_websocket import data_final 

f = open('test.txt', 'r')
currData = data_final
list = json.loads(currData)
print(type(list),list , "\n                        ")
data = list[3]
print(type(data), data, "\n                        ")