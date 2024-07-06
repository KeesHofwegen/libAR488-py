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
     print("$ reset all")
     inst2019A.write("++dcl\r")
     sleep(5)
     #sleep(2)
     
     ##result = inst2019A.write("RC01\n\r")
     value = input("Start RC00? press anykey\n")
     result = inst2019A.write("RC02\n\r")
     ##sleep(10)
     #result = inst2019A.write("CF10.0MZ\n\r")
     
     

     #sleep(1)
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

     value = input("Start RT ? press anykey\n")
     inst2019A.write("RT\n\r")

     #sleep(10)
     value = input("Start CF20.0MZ ? press anykey\n")
     inst2019A.write("CF20.0MZ\n\r")


     #sleep(10)
     value = input("Start QU ? press anykey\n")
     result = inst2019A.query("QU\n\r")
     sys.stdout.write("result:"+result)
     value = input("Start Sweep ? press anykey\n")
     

     for i in range(1,11):
          print("{}".format(i))
          inst2019A.write("UP\n\r")
          sleep(0.5)


     #print("$ reset 2019A instrument again")
     #inst2019A.write("*rst\n\r")

     print("$ restore local (front panel) control of 2019A")
     inst2019A.write("++loc\r\n")
     print("$ reset all")
     inst2019A.write("++dcl\r")
     sleep(5)
     print("end")   