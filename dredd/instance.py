class Instance(object):
    def __init__(self, id, name, dns, asg, status):
        self.id = id
        self.name = name
        self.dns = dns
        self.asg = asg
        self.status = status
