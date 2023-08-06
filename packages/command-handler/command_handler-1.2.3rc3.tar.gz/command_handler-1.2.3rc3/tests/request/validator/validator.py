from sys import modules
from unittest import TestCase
from unittest.mock import Mock, patch

from command_handler.request.validator.validator import Validator


class ValidatorTest(TestCase):
    def testTestCallsEachAssertPassedToInitWithGivenRequest(self):
        asserts = [
            Mock(),
            Mock(),
            Mock(),
            Mock(),
        ]

        request = patch.object(modules["command_handler.request.validator.validator"], "Request").start()
        request.request = Mock()
        request.registry = Mock()

        Validator(request.registry, asserts).test(request.request)
        for a in asserts:
            a.assert_called()
            args, kwargs = a.call_args
            self.assertEqual(request(), args[0])
            self.assertEqual(request().request, args[0].request)
            self.assertEqual(request().registry, args[0].registry)
