import gpib
import visa, pyvisa

class Newport_1830_c:

    #Notes:
    # - Delays are necessary for pyVisa to operate properly. Note the 
    #   0.006 second delays for query calls and there is a suggested
    #   additional 0.006 delay after queries or 0.009 after write commands

    BIT_PARAM_ERROR = 1 << 0
    BIT_COMMAND_ERROR = 1 << 1
    BIT_SATURATION = 1 << 2
    BIT_OVER_RANGE = 1 << 3
    BIT_MESSAGE_AVAIL = 1 << 4
    BIT_BUSY = 1 << 5
    BIT_SERVICE_REQUEST = 1 << 6
    BIT_READ_DONE = 1 << 7

    status_byte = 0

    def __init__(self):
        self.address = ''
        self.rm = ''
        self.comm = gpib.Gpib_communicator()

    def set_address(self, address):
        self.comm.set_address(address)

    def get_address(self):
        return self.comm.get_address()
    
    def set_wavelen(self, wavelen: int):
        wavelen_str = str(wavelen)

        if len(wavelen_str) <= 4 and len(wavelen_str) > 0:
            #Pad it
            wavelen_str = '0'*(4 - len(wavelen_str)) + wavelen_str
            wavelen_str = 'W' + wavelen_str + '\n'
            self.comm.write(wavelen_str)
            
    def measure_power(self):
        return self.comm.query('D?\n', delay=0.06)

    def auto_calibrate(self):
        self.comm.write('O\n')

    def update_status(self):
        stat = self.comm.query('Q?\n', delay=0.06)

        stat = int(stat)
        self.status_byte = stat
        return self.status_byte

    def clear_status(self):
        self.comm.write('C\n')

    def clear_comms(self):
        try:
            while True:
                self.comm.read()
        except pyvisa.errors.VisaIOError:
            pass

