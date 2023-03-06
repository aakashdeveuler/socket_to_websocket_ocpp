import binascii
import codecs
import json
DISCONNECT_MESSAGE = "!DISCONNECT"

state = b'\x00\x00\x00\x00\x00\x00\x00\x89\x8e\x01\x00\x00\x01\x86\xa1\xf5\xa9\xc8\x00.\x11\xfdT\x11\x00\x10s\x00\xc8\x00\xae\x06\x00\x00\x00\x00\x00\x16\x00\x08\x00\xf0\x00\x00P\x00\x00\x15\x05\x00\xc8\x00\x00E\x01\x00\xed\x02\x00qd\x01/\x00\x00\n\x00\xb5\x00\x0f\x00\xb6\x00\x0c\x00B/\xf3\x00\x18\x00\x00\x00\xce\xcd,\x00C\x10)\x00D\x003\x00\x11\xff\xce\x00\x12\xff\xcc\x00\x13\x03\xd5\x00\x02\x00\xf1\x00\x00\x9d\xdb\x02|\x06xQ\x0c\x00\x02\x00\x0b\x00\x00\x00\x02\x17\xe9\x96\xaa\x00\x0e\x00\x00\x00\x01G\xd9\x97\xc1\x00\x00\x01\x00\x00\xae\xb7'
rsp = b'5B332C2236303861323461642D316532332D343763372D623939632D333764376238663338363032222C7B22737461747573223A224163636570746564222C2263757272656E7454696D65223A22323032332D30332D30325431303A34323A33342E3233355A222C22696E74657276616C223A31343430307D5D'

print(type(rsp), rsp, "-=-=---=-=-=-=-=-=-=-=-=-=-")
if type(rsp) == bytes:
    print("xxxxxxxxxxxxxxxxxxxxxxxx")
dataFromClient = binascii.hexlify(rsp)
# dataFromClient = clientConnected.recv(1024)
x = codecs.decode(rsp, 'utf-8')
print("data from client :",x)
print("Len of client ", len(x))
print(type(x), "dataFromClient")

print("oioioioioioioioioioio")
print(bytearray.fromhex(x).decode())
print("oioioioioioioioioioio")

if dataFromClient == DISCONNECT_MESSAGE:
# print(f"Client {clientAddress} disconnected")
    connected = False
elif(int(dataFromClient[:4],16) == 15):
    imeiCheck = "01"
    print("imei received .... ")
    if (bytes.fromhex(dataFromClient[4:],16).decode('utf-8')) == 866907053293733:
        print("got it")
    print(int(dataFromClient[4:],16))
    # clientConnected.send(imeiCheck.encode())
    print("Check sent ")
# time.sleep(2)
# latlang = binascii.hexlify(clientConnected.recv(1024))
# print("Received latlong ")
# print(latlang)    
# print("Len of client ", len(latlang))
# clientConnected.send('00000002'.encode())
# print("check 2 sent ")

elif(dataFromClient[:8]) == "00000000":
    stateCheck = "00000002"
    # clientConnected.send(stateCheck.encode())
    print("state response sent")


else:
    print("=--------------------")
    print(dataFromClient)
    print(dataFromClient[:4])
    print("=--------------------")

# list = json.loads(dataFromClient)
# data=list[3]
# dataID = list[1]
# action = list[2]
