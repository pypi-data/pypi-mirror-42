from unittest import TestCase
from unittest.mock import call, Mock

from command_handler.request.validator.request import Request


class RequestTest(TestCase):
    def testCallsForReqistryUseRegistryAttribute(self):
        flaskRequest = Mock(foo="bar")
        registry = Mock(foo="baz")

        request = Request(flaskRequest, registry)
        request.registry.bar()
        request.registry.baz("foo.bar")

        self.assertEqual("baz", request.registry.foo)
        registry.assert_has_calls([
            call.bar(),
            call.baz("foo.bar"),
        ])
        flaskRequest.assert_not_called()

    def testAllNonRegistryCallsUseRequestAttribute(self):
        flaskRequest = Mock(foo="bar")
        registry = Mock(foo="baz")

        request = Request(flaskRequest, registry)
        request.bar()
        request.baz("foo.bar")

        self.assertEqual("bar", request.foo)
        request.assert_has_calls([
            call.bar(),
            call.baz("foo.bar"),
        ])
        registry.assert_not_called()
