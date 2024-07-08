from time import sleep
import serial
import sys
import logging
import sys

# notes:
# '\r', '\n', and '+' are control characters that must be escaped in binary data
#
# Prologix commands:
# ++addr [1-29]
# ++auto [0 | 1 | 2 | 3]
# ++clr
# ++eoi [0 | 1]
# ++eos [0 | 2 | 3 | 4]
# ++eot_enable [0 | 1]
# ++eot_char [<char>]
# ++help (unsupported)
# ++ifc
# ++llo [all]
# ++loc [all]
# ++lon (unsupported)
# ++mode [0 | 1]
# ++read [eoi | <char>]
# ++read_tmo_ms <time>
# ++rst
# ++savecfg
# ++spoll [<PAD> | all | <PAD1> <PAD2> <PAD3> ...]
# ++srq
# ++status [<byte>]
# ++trg [PAD1 ... PAD15]
# ++ver [real]
#
# Custom AR488 commands:
# ++allspoll
# ++dl
# ++default
# ++macro [1-9]
# ++ppoll
# ++setvstr [string]
# ++srqauto [0 | 1]
# ++repeat count delay cmdstring
# ++tmbus [value]
# ++verbose


class AR448Instrument(object):
    """Class to represent AR488 USB-GPIB adapter.

    The AR488 is an Arduino-based USB-GPIB adapter.
    For details see: https://github.com/Twilight-Logic/AR488
    """
    ser=None
    def __init__(self, gpibAddr, comPort, baud_rate=115200, timeout=0.5, silent=True):
        logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG,)
        self._verbose=silent
        self.gpibAddr=gpibAddr
        
        try:
            ##import serial.tools.list_ports
            
            self.ser = serial.Serial(port=comPort, baudrate=baud_rate, timeout=timeout)
            #
            ''' sleep so that UCB  can establish itself'''
            sleep(2)

            ''' This command enables or disables the assertion of the EOI signal. When a data message is sent in
            binary format, the CR/LF terminators cannot be differentiated from the binary data bytes. In this
            circumstance, the EOI signal can be used as a message terminator. When ATN is not asserted and
            EOI is enabled, the EOI signal will be briefly asserted to indicate the last character sent in a multi-
            byte sequence. Some instruments require their command strings to be terminated with an EOI
            signal in order to properly detect the command.
            The EOI line is also used in conjunction with ATN to initiate a parallel poll, however, this command
            has no bearing on that activity.
            When issued without a parameter, the command will return the current configuration
            Modes:
            controller, device
            Syntax:
                    ++eoi [0|1]
                    where 0 disables and 1 enables asserting EOI to signal the last character sent
            '''
            #self.write("++eoi 0\n\r") 

            ''' Version of the AR488 interface'''
            stri = self.query("++ver\n\r")
            print(stri.decode("UTF-8"))

            ''' set the ar488 to 0 device  1 controller'''
            self.write("++mode 1\n\r")

            ''' set the GBIP adrress'''
            self.set_address(self.gpibAddr)

            '''Assert the GPIB IFC signal for 150 microseconds, making the AR488 the Controller-in-Charge on
                the GPIB bus.
                Modes:
                    controller
                Syntax:
                    ++ifc
            '''
            self.write("++ifc\n\r")

            ''' Specifies the GPIB termination character. When data from the host (e.g. a command sequence) is
                received over USB, all non-escaped LF, CR or Esc characters are removed and replaced by the GPIB
                termination character, which is appended to the data sent to the instrument. This command does
                not affect data being received from the instrument.
                When issued without a parameter, the command will return the current configuration

                Modes: controller, device
                Syntax: ++eos [0|1|2|3]
            '''
            #self.write("++eos 0\n\r")

            '''
            End of receive. While ++eos (end of send) selects the terminator to add to commands and data
            being sent to the instrument, the ++eor command selects the expected termination sequence
            when receiving data from the instrument.
            The following termination sequences are supported:
            Option      Sequence        Hex
            0           CR + LF         0D 0A
            1           CR              0D
            2           LF              0A
            3           None            N/A
            4           LF + CR         0A 0D
            5           ETX             03
            6           CR + LF + ETX   0D 0A 03
            7           EOI signal      N/A

            The default termination sequence is CR + LF. If the command is specified with one of the above
            numeric options, then the corresponding termination sequence will be used to detect the end of
            the data being transmitted from the instrument. If the command is specified without a parameter,
            then it will return the current setting. If option 7 (EOI) is selected, then ++read eoi is implied for all
            ++read instructions as well as any data being retuned by the instrument in response to direct
            instrument commands. An EOI is expected to be signalled by the instrument with the last
            character of any transmission sent. All characters sent over the GPIB bus are passed to the serial
            port for onward transmission to the host computer.
            Modes: controller
            Syntax:++eor[0-9]
            '''
            #self.write("++eor 4\n\r")

            '''
            Configure the instrument to automatically send data back to the controller. When auto is enabled,
            the user does not have to issue ++read commands repeatedly. This command has additional
            options when compared with the Prologix version.
            When set to zero, auto is disabled.
            When set to 1, auto is designed to emulate the Prologix setting. The controller will automatically
            attempt to read a response from the instrument after any instrument command or, in fact, any
            character sequence that is not a controller command beginning with ‘++’, has been sent.
            When set to 2, auto is set to “on-query” mode. The controller will automatically attempt to read
            the response from the instrument after a character sequence that is not a controller command
            beginning with ‘++’ is sent to the instrument, but only if that sequence ends in a ‘?’ character, i.e.
            it is a query command such as ‘*IDN?’.
            When set to 3, auto is set to “continuous” mode. The controller will execute continuous read
            operations after the first ++read command is issued, returning a continuous stream of data from
            the instrument. The command can be terminated by turning off auto with ++auto 0 or performing
            a reset with ++rst.
            Modes: controller
            Syntax:  ++auto [0|1|2|3]
            where 0 disables and 1 enables automatically sending data to the controller
            
            NOTE:
            Some instruments generate a “Query unterminated or “-420” error if they are addressed after
            sending an instrument command that does not generate a response. This simply means that the
            instrument has no information to send and this error may be ignored. Alternatively, auto can be
            turned off (++auto 0) and a ++read command issued following the instrument command to read
            the instrument response.
            '''
            #self.write("++auto 1\n\r")     
            
        except:
            sys.exit("error opening serial port {}".format(comPort))
        
        if not self._verbose:
            print("Init")

   


    def __del__(self):
        self.ser.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.ser.close()

    # Raw GPIB read/write commands
    def write(self, message):
        """Write message to GPIB bus.
        """
        if self.gpibAddr is not None and not message.startswith("++") :
            len = self.ser.write("++addr {}\n\r".format(self.gpibAddr).encode("UTF-8"))
        
        len = self.ser.write("{}".format(message).encode("ASCII"))
        
        if not self._verbose:
            if self.gpibAddr is not None and not message.startswith("++") :
                print(">> ++addr {}".format(self.gpibAddr))
            print(">> {}".format(message.encode("ASCII")))

    def read(self):
        result= bytearray()
        """Read from GPIB bus. return bytearry"""
        byteReadline = self.ser.readline()
        result=result + byteReadline
        #waitin = self.ser.in_waiting
        #print ("read length {}", len(byteReadline))
        while ( len(byteReadline)> 0) :
            #print("Read Loop")
            byteReadline = self.ser.readline()
            #print ("read-length {}", len(byteReadline))
            result=result+ byteReadline
        if not self._verbose:
            print("<< len {} :".format(len(result)) + result.decode("UTF-8"))
        return result
   
    def simplequery1(self, message):
        "Write message to GPIB bus and read results."""
        self.write(message)
        return self.read()
    
    def query(self, cmd):
        retry  = 4
        gotIt  = False
        result = bytearray()
        
        while retry>0 and not gotIt:
            if not self._verbose:
                print("-- retry:"+str(retry))
            self.write(cmd)
            #sleep(0.5)
            
            self.write("++read eoi\n\r")
            stri = self.read()
            #i=0
            while len(stri) > 0 :
                gotIt =True
                result=result +stri
                stri = self.read()
        retry-=1
        # Convert the string to a list of hexadecimal values
        if not self._verbose:    
            print(' '.join(f'{x:02x}' for x in result))
            #print(">>>>Query result:" +result)
        #result= stri
        return result
    
    # Prologix commands
    def set_address(self, address):
        """Specify address of GPIB device with which to communicate.

        When the AR488 is in device mode rather than controller mode, this
        instead sets the address of the AR488.
        """
        self.write("++addr {}\n\r".format(address))

    def get_current_address(self):
        "Return the currently specified address."""
        self.write("++addr\n\r")
        return self.read()
    
    def set_mode(self, en):
        self.write("++mode {}".format(en))

    def get_mode(self):
        self.write("++mode\n\r")
        return self.read()
    

