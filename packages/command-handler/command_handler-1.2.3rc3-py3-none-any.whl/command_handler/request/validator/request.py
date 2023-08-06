class Request:
    def __init__(self, request, registry):
        self.request = request
        self.registry = registry

    def __getattr__(self, name):
        return getattr(self.request, name)
