import binascii
import codecs
import re

DISCONNECT_MESSAGE = "!DISCONNECT"
connected = True

# Assuming TCU will always give data similar to "state".
# If data is coming similar to "rsp", then don't do binascii.hexlify()
state = b'\x00\x00\x00\x00\x00\x00\x00\x89\x8e\x01\x00\x00\x01\x86\xa1\xf5\xa9\xc8\x00.\x11\xfdT\x11\x00\x10s\x00\xc8\x00\xae\x06\x00\x00\x00\x00\x00\x16\x00\x08\x00\xf0\x00\x00P\x00\x00\x15\x05\x00\xc8\x00\x00E\x01\x00\xed\x02\x00qd\x01/\x00\x00\n\x00\xb5\x00\x0f\x00\xb6\x00\x0c\x00B/\xf3\x00\x18\x00\x00\x00\xce\xcd,\x00C\x10)\x00D\x003\x00\x11\xff\xce\x00\x12\xff\xcc\x00\x13\x03\xd5\x00\x02\x00\xf1\x00\x00\x9d\xdb\x02|\x06xQ\x0c\x00\x02\x00\x0b\x00\x00\x00\x02\x17\xe9\x96\xaa\x00\x0e\x00\x00\x00\x01G\xd9\x97\xc1\x00\x00\x01\x00\x00\xae\xb7'
state2 =  b'\x00C\x0e\xe8\x00D\x00\x00\x00\x11\xff\x16\x00\x12\xfe\xfa\x00\x13\xfcI\x00\x02\x00\xf1\x00\x00\x00\x00\x02|\x00\x00\x00\x00\x00\x02\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x86\xb5\x9e\xab\x00\x00.\x12\x01\t\x11\x00\x0c\xde\x00\xd2\x00\x89\x0b\x00\x00\x00\x00\x00\x16\x00\x08\x00\xf0\x00\x00P\x04\x00\x15\x00\x00\xc8\x00\x00E\x01\x00\xedc\x00qH\x01/\x00\x00\n\x00\xb5\x00\x0f\x00\xb6\x00\x0c\x00B0k\x00\x18\x00\x00\x00\xce\x00\x00\x00C\x0e\xe8\x00D\x00\x00\x00\x11\xff\x16\x00\x12\xfe\xf9\x00\x13\xfcJ\x00\x02\x00\xf1\x00\x00\x00\x00\x02|\x00\x00\x00\x00\x00\x02\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\xfc\xd1'
rsp = b'5B332C2236303861323461642D316532332D343763372D623939632D333764376238663338363032222C7B22737461747573223A224163636570746564222C2263757272656E7454696D65223A22323032332D30332D30325431303A34323A33342E3233355A222C22696E74657276616C223A31343430307D5D'
rsp2 = b'\x00\x00\x00\x00\x00\x00\x00{\r\x01\x06\x00\x00\x00sd\x05\x9e\x13[2,"0113230b040300471234567891011","BootNotification",{"chargePointVendor":"Euler","chargePointModel":"GPT"}]\r\n\x01\x00\x00\x00\x93'


def extract_between_strings(start, end, text):
    pattern = re.escape(start) + r'(.*?)' + re.escape(end)
    match = re.search(pattern, text)
    if match:
        return start + match.group(1) + end
    else:
        return None
dataFromClient = binascii.hexlify(rsp2)
print("Slash(\) removed from byte")
print(dataFromClient)
print("oioioioioioioioioioio")
dataFromClient = codecs.decode(dataFromClient, 'utf-8')
print("String form of byte")
print(dataFromClient)
print("oioioioioioioioioioio")
print(dataFromClient[14:15])
if dataFromClient == DISCONNECT_MESSAGE:
    connected = False
   
elif(dataFromClient[14:16]=='7b'):  # Notification Messages
    # dataFromClient = dataFromClient[38:256]
    # dataFromClient = bytearray.fromhex(dataFromClient).decode()
    dataFromClient = extract_between_strings("5b", "7d5d", dataFromClient)
    # print(dataFromClient[17:30])
    dataFromClient = bytearray.fromhex(dataFromClient).decode()
    print("=--------------------")
    print(dataFromClient)
    # print(x)
    print("=--------------------")
    
    # list = json.loads(dataFromClient)
    # data=list[3]
    # dataID = list[1]
    # action = list[2]
    
    # receivedData = asyncio.run(main(data, dataID, action))
    # clientConnected.send(receivedData.encode())
    
elif(int(dataFromClient[:4],16) == 15): # IMEI Message (000f383636393037303533323933373333)
    # imei is from imei[2:17]
    imei = (bytearray.fromhex(dataFromClient).decode())
    # print(len(imei))
    # print(imei[2:17])
    # print(type(imei))
    imeiCheck = "01"
    print(print(imeiCheck.encode())) # converts imeiCheck to b'01
    
elif(int(dataFromClient[:8],16) == 0):
    # this is State message (longitude, latitude)
    stateCheck = "00000002"
    print(stateCheck.encode()) # converts stateCheck to b'00000002
    
elif(bytearray.fromhex(dataFromClient[:2]).decode()=='['):
    dataFromClient = bytearray.fromhex(dataFromClient).decode()
    print(dataFromClient)
else:
    print("Received Message in not in Records !!!")