from unittest import TestCase
from unittest.mock import MagicMock

from command_handler.command.handler.registry import Registry
from command_handler.request.validator.asserts.command import command
from command_handler.request.validator.exceptions import AssertionFailedException
from command_handler.request.validator.request import Request


class CommandRequestValidatorTest(TestCase):
    def setUp(self):
        self.flaskRequest = MagicMock()
        self.registry = Registry()
        self.request = Request(self.flaskRequest, self.registry)

        self.registry.add("foo.bar.baz", lambda x: x, {})

    def testRaisesExceptionWhenRequestIsEmpty(self):
        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Either `payload` or `command` field is missing")

    def testRaisesExceptionWhenRequestContainsPayloadOnly(self):
        self.flaskRequest.get_json.return_value = {
            "payload": {},
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Either `payload` or `command` field is missing")

    def testRaisesExceptionWhenRequestContainsCommandNameOnly(self):
        self.flaskRequest.get_json.return_value = {
            "command": "foo.bar.baz",
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Either `payload` or `command` field is missing")

    def testReturnsNoneWhenRequestContainsBothPayloadAndCommandName(self):
        self.flaskRequest.get_json.return_value = {
            "command": "foo.bar.baz",
            "payload": {},
        }

        self.assertIsNone(command(self.request))

    def testRaisesExceptionWhenPayloadIsNotADict(self):
        self.flaskRequest.get_json.return_value = {
            "command": "foo.bar.baz",
            "payload": "foo",
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Field `payload` is not a dictionary")

    def testRaisesExceptionWhenCommandNameIsNotAString(self):
        self.flaskRequest.get_json.return_value = {
            "command": [],
            "payload": {},
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Field `command` is not a string")

    def testRaisesExceptionWhenGivenCommandIsNotDefinedInCommandRegistry(self):
        self.flaskRequest.get_json.return_value = {
            "command": "foo.bar",
            "payload": {},
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Value of field `command` is not valid command key")

    def testRaisesExceptionWhenGivenCommandDoesNotMatchSchema(self):
        self.registry.add("foo.bar", lambda x: x, {
            "type": "object",
            "properties": {
                "foo": {"type": "number"},
                "bar": {"type": "string"},
            },
            "required": [
                "foo",
                "bar",
            ],
        })

        self.flaskRequest.get_json.return_value = {
            "command": "foo.bar",
            "payload": {},
        }

        with self.assertRaises(AssertionFailedException) as cm:
            command(self.request)

        self.assertEqual(cm.exception.code, 400)
        self.assertEqual(str(cm.exception), "Value of field `payload` does not match schema of requested command")
