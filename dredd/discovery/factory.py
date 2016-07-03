from eureka import Eureka


class Factory(object):
    def get_discovery(self, name, url):
        if name == 'eureka':
            return Eureka(url=url)
        else:
            raise NotImplementedError('Unknown discovery mechanism. Options are: eureka, consul')
