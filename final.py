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
m = b'00000000000004b98e0900000186b64a1da000000000000000000000000000000000012f0016000800f00100500100150000c80000450200ed6300710e012f01000a00b5000000b60000004200000018000000ce000000430c59004400000011009d0012fc4b0013ff4b000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b64a11e80000000000000000000000000000000000000016000800f00100500100150000c80000450200ed6300710e012f00000a00b5000000b60000004200000018000000ce000000430c5c004400000011002f0012fc670013fe6c000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b64a02480000000000000000000000000000000000000016000800f00100500100150000c80000450200ed6300710f012f00000a00b5000000b60000004200000018000000ce000000430c6100440000001100390012fc660013fe83000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b649f2a800000000000000000000000000000000012f0016000800f00100500100150000c80000450200ed6300710f012f00000a00b5000000b60000004200000018000000ce000000430c65004400000011003e0012fc680013fe61000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b649e3080000000000000000000000000000000000000016000800f00100500100150000c80000450200ed6300710f012f01000a00b5000000b60000004200000018000000ce000000430c6c00440000001100240012fc6a0013fe59000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b649d3680000000000000000000000000000000000000016000800f00100500100150000c80000450200ed63007110012f01000a00b5000000b60000004200000018000000ce000000430c74004400000011002d0012fc480013fe8b000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b649c3c80000000000000000000000000000000000000016000800f00100500100150000c80000450200ed63007110012f01000a00b5000000b60000004200000018000000ce000000430c7400440000001100d70012fc360013000f000200f100000000027c000000000002000b0000000217e996aa000e0000000147d997c1000000000186b649b42800000000000000000000000000000000012f0016000800f00100500100150000c80000450200ed63007112012f01000a00b5000000b60000004200000018000000ce0000'

def extract_between_strings(start, end, text):
    pattern = re.escape(start) + r'(.*?)' + re.escape(end)
    match = re.search(pattern, text)
    if match:
        return start + match.group(1) + end
    else:
        return None
dataFromClient = binascii.hexlify(m)
print("Slash(\) removed from byte")
print(dataFromClient)
print("oioioioioioioioioioio")
dataFromClient = codecs.decode(m, 'utf-8')
print("String form of byte")
print(dataFromClient)
print("oioioioioioioioioioio")
print((dataFromClient[16:18]))
if dataFromClient == DISCONNECT_MESSAGE:
    connected = False
   
elif len(dataFromClient) == 0:
    print("Empty Message")   

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
    
elif(dataFromClient[:4] == "000f"): # IMEI Message (000f383636393037303533323933373333)
    # imei is from imei[2:17]
    imei = (bytearray.fromhex(dataFromClient).decode())
    # print(len(imei))
    # print(imei[2:17])
    # print(type(imei))
    imeiCheck = "01"
    print(print(imeiCheck.encode())) # converts imeiCheck to b'01
    
elif(dataFromClient[16:18] == "8e"):
    # this is State message (longitude, latitude)
    stateCheck = "00000002"
    print(stateCheck.encode()) # converts stateCheck to b'00000002
    
elif(bytearray.fromhex(dataFromClient[:2]).decode()=='['):
    dataFromClient = bytearray.fromhex(dataFromClient).decode()
    print(dataFromClient)
else:
    print("Received Message in not in Records !!!")