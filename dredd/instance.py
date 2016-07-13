class Instance(object):
    STATUS_UP = "UP"
    STATUS_DOWN = "DOWN"

    def __init__(self, id, name, address, asg, status):
        self.id = id
        self.name = name
        self.address = address
        self.asg = asg
        self.status = status
