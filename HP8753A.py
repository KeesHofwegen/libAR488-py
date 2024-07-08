from ScpiInstrumentWrapper import *
from resourceManager import *

from time import sleep
import sys
if __name__ == "__main__":
    # Hello World!
    import time

    rm = resoureManager()
    print(rm.serial_ports())

    inst8753A = ScpiInstrumentWrapper("AR488::/dev/ttyUSB0::GPIB::16")
    #inst8753A.write("++verbose 0")
    inst8753A.write("++auto 0")
    
    #inst8753A.write("*IDN?")
    #inst8753A.write("++read")
    #result = inst8753A.read();
    sleep(5)
    result = inst8753A.query("*IDN?\r")
    sys.stdout.write("\'"+result.decode("UTF-8")+"\'\n")

    inst8753A.write("PRES\n\r")
    inst8753A.write("CHAN1\n\r")
    inst8753A.write("DEBUON\n\r")
    sleep(5)
    #result = inst8753A.query("outpCALK\n\r")

    print("get OUTPCALK")
    inst8753A.write("FORM1\n\r")
    result = inst8753A.query("OUTPCALK\n\r")
    print ("length {}", len(result))
    int_len = int.from_bytes(result[2:4], "big") +2
    result = result[0:int_len]

    print ("length {}", len(result))

    print(' '.join(f'{x:02x}' for x in result))
    #sys.stdout.write("\n\n\'"+result.decode("utf-8")+"\'\n")
    file = open('/tmp/CalibrationKitInfo.txt', 'wb')
try:
    ##### Write binary data to file

    file.write(result)
finally:
    ### Close the file

    file.close()


'''
    print("get outpplot")
    result = inst8753A.query("outpplot\n\r")
    print ("length {}", len(result))
    print(' '.join(f'{x:02x}' for x in result))
    sys.stdout.write("\n\n\'"+result.decode("utf-8")+"\'\n")

    file = open('/tmp/binaryfile.PLT', 'wb')
try:
    ##### Write binary data to file

    file.write(result)
finally:
    ### Close the file

    file.close()
'''
