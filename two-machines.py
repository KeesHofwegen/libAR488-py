from ScpiInstrumentWrapper import *
from resourceManager import *

from time import sleep
import sys
if __name__ == "__main__":
    # Hello World!
    import time

    rm = resoureManager()
    print(rm.serial_ports())

    inst2019A = ScpiInstrumentWrapper("AR488::/dev/ttyUSB0::GPIB::3")
    inst2019A.write("++auto 2\r");
    inst2019A.write("++eoi 1\r");

    inst2955A = ScpiInstrumentWrapper("AR488::/dev/ttyUSB0::GPIB::6")
    inst2955A.write("++auto 2\r");
    inst2955A.write("++eoi 1\r");

    print("$ reset all")
    
    inst2955A.write("++dcl\r")
    sleep(8)

    value = input("Start RC00? press anykey\n")
    result = inst2019A.write("RC02\n\r")

    value = input("Start LV-10DB ? press anykey\n")
    inst2019A.write("LV-10DB\n\r")
    #sleep(1)
    value = input("Start C1 ? press anykey\n")
    inst2019A.write("C1\n\r")
    #sleep(1)
    value = input("Start DE,CF,100.00000,KZ? press anykey\n")
    inst2019A.write("DE CF 100.00000 KZ XS\n\r")

    value = input("Start QU ? press anykey\n")
    result = inst2019A.query("QU\n\r")
    sys.stdout.write("result:"+result)

    sleep(2)
    print("$ ask for full screen page")
    result = inst2955A.query("RD39\n\r")
    sys.stdout.write(result+"\n")
    #hex_array = [hex(ord(int))[2:] for int in result]
    #print( hex_array)
    two=40;
    while (two>0 and len(result)>0):
        inst2955A.write("++read\n\r")
        result = inst2955A.read()
        sys.stdout.write(result+"\n")
        two = two -1
        #hex_array = [hex(ord(int))[2:] for int in result]
        #print( hex_array)
    
