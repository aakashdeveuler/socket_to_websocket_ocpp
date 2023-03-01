from client import rc
import threading

def create_sub(imei):
    rc1 = rc()
    rc1.run_client(imei)


def createThread(imei):
    for i in range(1, 11):
        imei += str(i)
        thread = threading.Thread(target=create_sub, args=(imei, ))
        thread.start()

createThread("8643940408337")