class Instance(object):
    STATUS_UP = "UP"
    STATUS_DOWN = "DOWN"

    def __init__(self, id, name, address, status):
        self.id = id
        self.name = name
        self.address = address
        self.status = status
