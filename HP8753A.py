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

    inst8753A.write("CHAN2\n\r")
    
    #result = inst8753A.query("outpCALK\n\r")
    result = inst8753A.query("outpplot\n\r")
    print ("leght {}", len(result))
    print(' '.join(f'{x:02x}' for x in result))
    sys.stdout.write("\n\n\'"+result.decode("utf-8")+"\'\n")

