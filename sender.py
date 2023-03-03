import threading
import time
from client import run_client


def createThread(imei):
    i=1
    x=1
    while True:
        thread = threading.Thread(target=run_client, args=(imei + str(i), ))
        time.sleep(1)
        thread.start()
        # print("above -=-=-=-=-=-=-==--=-")
        print(x)
        i+=1
        x+=1
        if i == 20:
            # print("inside    >>>>>>>")
            i = 1
            # print(i)

createThread("8643940408337")