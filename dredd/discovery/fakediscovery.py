class FakeDiscovery:
    def __init__(self, url=None):
        self.url = url
        self._instances = []

    def instances(self):
        return self._instances

    def add(self, instance):
        self._instances.append(instance)
