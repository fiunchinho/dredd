class Instance(object):
    STATUS_UP = "UP"
    STATUS_DOWN = "DOWN"

    def __init__(self, id, name, dns, asg, status):
        self.id = id
        self.name = name
        self.dns = dns
        self.asg = asg
        self.status = status
