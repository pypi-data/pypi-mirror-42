class Validator:
    def __init__(self, registry, asserts):
        self.registry = registry
        self.asserts = asserts

    def test(self, request):
        for a in self.asserts:
            a(request, self.registry)
