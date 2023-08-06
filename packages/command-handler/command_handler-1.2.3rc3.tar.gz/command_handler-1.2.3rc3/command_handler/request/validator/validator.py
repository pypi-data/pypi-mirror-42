from .request import Request


class Validator:
    def __init__(self, registry, asserts):
        self.registry = registry
        self.asserts = asserts

    def test(self, request):
        request = Request(request, self.registry)
        for a in self.asserts:
            a(request)
