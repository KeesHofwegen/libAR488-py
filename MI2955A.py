from ScpiInstrumentWrapper import *
from time import sleep
import sys

if __name__ == "__main__":
    # Hello World!
    import time

    inst2955A  = ScpiInstrumentWrapper("AR488::/dev/ttyUSB0::GPIB::6")
    inst2955A.write("++auto 2\r");
    inst2955A.write("++eoi 1\r");
    print("$ reset all")
    inst2955A.write("++dcl\r")
    sleep(5)
    sys.stdout.write("$ ask for af generator frequency: ")
    ## ask for 1.000KHZ
    
    result = inst2955A.query("RD29\n\r")
    sys.stdout.write(result.decode("UTF-8")+ "\n")
    sleep(2)
     

    print("$ Set screen to 123.5 MHz")
    inst2955A.write("RX;RG;FR123.5MZ;DI100KZ;LV-30DM;SM;FR1KZ;LV50AM;MD1;AC;SN2\n\r")
    sleep(2)

    print("$ ask for full screen page")
    result = inst2955A.query("RD39\n\r")
    sys.stdout.write(result.decode("UTF-8")+"\n")

    two=40;
    while (two>0 and len(result)>0):
        inst2955A.write("++read\n\r")
        result = inst2955A.read()
        sys.stdout.write(result+"\n")
        two = two -1
    
    print("$ restore local (front panel) control of 29955A")
    inst2955A.write("++loc\r\n")

        



    