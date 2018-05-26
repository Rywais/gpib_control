import visa

class Gpib_communicator:
    def __init__(self):
        self.address = ""
        self.rm = visa.ResourceManager()
        self.inst = None

    def set_rm(self, rm):
        self.rm = visa.ResourceManager(rm)

    def set_address(self, address):
        self.address = address
        self.inst = self.rm.open_resource(address)

    def get_address(self):
        return self.address

    def write(self, message):
        self.inst.write(message)

    def query(self, message, delay=0.06):
        return self.inst.query(message)

