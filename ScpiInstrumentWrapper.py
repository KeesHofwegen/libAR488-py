from time import sleep
import serial
import sys
import string
from AR448Instrument import *

class ScpiInstrumentWrapper(object):
    '''
    Wrapper for visa/AR488 connected instruments supporting SCPI language
    possible resources are:
        - COM<NR> where '<NR>' is the COM-port number
        - GPIB::<ADDR> where <ADDR> is the GPIB address of the instrument
        - TCPIP::<IPADDR> where <IPADDR> is the ip address of the instrument
        - AR488::COM<NR>::GPIB::<ADDR> if the instrument is connected via AR488
          USB-GPIB adapter. <NR> is the COM-port number of the Prologix adapter
          and <ADDR> is the GPIB address of the instrument
        - USB identifiers e.g. 'RSNRP::0x000c::101628'
    '''
    def __init__(self, resource):
        self.resource = resource
        if resource[0:5].lower() == 'ar488':
            # device is connected via prologix adapter
            resource = resource.split('::')
            comport = resource[1]
            gpibAddr = int(resource[-1])
            self._inst = AR448Instrument(gpibAddr,comport)
        else:
            print("No Ar488 controller found ")
            exit()
            
    def query(self, cmd):
        ret = self._inst.query(cmd.strip('\n'))
        return ret
    def simplequery(self, cmd):
        ret = self._inst.simplequery(cmd.strip('\n'))
        return ret
    def ask(self, cmd):
        return self.query(cmd)

    def write(self, cmd):
        self._inst.write(cmd)
    def read(self,):
        return self._inst.read()

    def getErr( self ):
        err = self.ask( 'SYST:ERR?' )
        (errno, errstr) = string.split( err, ',', 1)
        return (int(errno),errstr)

    def checkErr(self):
        '''
        Asks the instrument for errors and raises an exception if there is an error
        '''
        err = self.getErr()
        if err[0] != 0:
            name = self.__class__.__name__
            raise Exception('%s Remote Control Error: ' %name + str(err[0]) + ', ' + err[1])

    def reset( self ):
        '''
        perform an instrument reset
        '''
        self.write( '*RST' )
        return

    def clear( self ):
        '''
        Clear instrument status byte
        '''
        self.write( '*CLS' )
        return

    def getIdent( self ):
        '''
        Get device ID
        '''
        return self.ask( '*IDN?' )

    def wait( self, timeout=None ):
        '''
        Wait for operation to complete
        ''' 
        if timeout!= None:
            to = self._inst.timeout
            self._inst.timeout = timeout        
            self.ask('*OPC?')
            self._inst.timeout = to
        else:
            self.ask('*OPC?') 

    @property
    def timeout(self,):
        return self._inst.timeout

    @timeout.setter        
    def timeout(self, timeout):        
        self._inst.tim

class resoureManager(object):

 def __init__(silent=False):
     #print(self.serial_ports())
    resoureManager._verbose=silent

 def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

