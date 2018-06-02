import serial, time

class Gpib_communicator:
    def __init__(self):
        self.address = ""
        ser = None

    def set_serial(self, serial_port):
        self.ser = serial.Serial(serial_port)
        self.ser.timeout = 0.001
    
    def get_serial(self):
        return self.ser.port

    # Note that this "adress" is ony the single GPIB address number
    # i.e. for "GPIB0::17::INSTR" you must only input 17
    def set_address(self, address):
        self.ser.write(('++addr'+str(address)+'\n').encode('utf-8'))

    def get_address(self):
        return self.query('++addr\n',delay=0.005,timeout=0.03)

    def write(self, message):
        self.ser.write(message.encode('utf-8'))

    def read(self, timeout=0.0, term_char='\n'):
        msg = ''
        self.write('++read\n')
        start = time.perf_counter()
        while True: #Wait for first data to be available
            b = self.ser.read()
            if b != b'':
                msg = msg + b.decode('utf-8')
                break
            if time.perf_counter() - start > timeout:
                return ''

        while True: #Read the rest of the data
            b = self.ser.read()
            if b == term_char.encode('utf-8'):
                msg = msg + b.decode('utf-8')
                break
            if b == b'':
                break
            msg = msg + b.decode('utf-8')
        return msg

    def query(self, message, delay=0.0, timeout=0.0):
        self.write(message)
        time.sleep(delay)
        return self.read(timeout=timeout)

    def read_stb(self):
        self.write('++spoll\n')
        return int(self.read())
