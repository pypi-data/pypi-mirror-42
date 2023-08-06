from sys import modules
from unittest import TestCase
from unittest.mock import call, MagicMock, Mock, patch

from command_handler import CommandHandler


class CommandHandlerTest(TestCase):
    def testCommandHandlerReturnsInstanceOfCommandHandler(self):
        app = MagicMock()

        self.assertIsInstance(CommandHandler(app), CommandHandler)

    def testInitCallsAddUrlRuleOnGivenApplication(self):
        app = MagicMock()
        CommandHandler(app)

        app.add_url_rule.assert_called()

    def testInitCallsAddUrlRuleOnGivenApplicationWithUrl(self):
        app = MagicMock()
        CommandHandler(app)

        args, kwargs = app.add_url_rule.call_args
        assert "rule" in kwargs or len(args) >= 1

        url = kwargs.get("rule") if "rule" in kwargs else args[0]
        self.assertEqual(url, "/command")

    def testInitCallsAddUrlRuleOnGivenApplicationWithPrefixedUrl(self):
        app = MagicMock()
        CommandHandler(app, rulePrefix="/foo")

        args, kwargs = app.add_url_rule.call_args
        url = kwargs.get("rule") if "rule" in kwargs else args[0]
        self.assertEqual(url, "/foo/command")

    def testInitCallsAddUrlRuleOnGivenApplicationWithSuffixUrl(self):
        app = MagicMock()
        CommandHandler(app, ruleSuffix="bar")

        args, kwargs = app.add_url_rule.call_args
        url = kwargs.get("rule") if "rule" in kwargs else args[0]
        self.assertEqual(url, "/bar")

    def testInitCallsAddUrlRuleOnGivenApplicationWithViewFunc(self):
        app = MagicMock()

        CommandHandler(app)

        args, kwargs = app.add_url_rule.call_args
        assert "view_func" in kwargs or len(args) >= 3

        view_func = kwargs.get("view_func") if "view_func" in kwargs else args[2]
        with patch("command_handler.views.Invoker.dispatch_request") as dispatcher:
            view_func()

            dispatcher.assert_called()

    def testInitCallsAddUrlRuleOnGivenApplicationWithPostAsOnlyAllowedMethod(self):
        app = MagicMock()
        CommandHandler(app)

        args, kwargs = app.add_url_rule.call_args
        assert "methods" in kwargs

        methods = kwargs.get("methods")
        self.assertIsInstance(methods, list)
        self.assertEqual(len(methods), 1)
        assert "POST" in methods

    def testInitPassesValidatorParamToInvokerInitializer(self):
        app = MagicMock()
        validators = ["foo", "bar"]

        CommandHandler(app, validators=validators)

        args, kwargs = app.add_url_rule.call_args
        view_func = kwargs.get("view_func") if "view_func" in kwargs else args[2]
        with patch("command_handler.views.Invoker.dispatch_request"):
            with patch.object(view_func, "view_class", Mock("command_handler.views.Invoker")) as view_class:
                view_func()

                args, kwargs = view_class.call_args
                assert "validators" in kwargs
                self.assertListEqual(kwargs["validators"], validators)

    def testInitCreatesDifferentViewsWithGivenNamesAndDifferentRegistries(self):
        app = MagicMock()

        with patch("command_handler.views.Invoker.as_view") as view:
            ch1 = CommandHandler(app)
            ch2 = CommandHandler(app, rulePrefix="/foo")
            ch3 = CommandHandler(app, ruleSuffix="bar")

        view.assert_has_calls([
            call("__command_handler_invoker_view__command", registry=ch1.registry),
            call("__command_handler_invoker_view_/foo_command", registry=ch2.registry),
            call("__command_handler_invoker_view__bar", registry=ch3.registry),
        ])
        self.assertNotEqual(ch1.registry, ch2.registry)
        self.assertNotEqual(ch2.registry, ch3.registry)
        self.assertNotEqual(ch1.registry, ch3.registry)

    def testAddHandlerWrappsGivenMethodWithHandlerClassAndAddsItToTheRegistry(self):
        def handler():
            pass

        def handlerDecorator():
            return handler()

        ch = CommandHandler(MagicMock())
        ch.registry = Mock()
        extras = {
            "transformer": lambda x: x,
            "postProcessor": lambda x: None,
        }

        with patch.object(modules["command_handler.handler"], "Handler") as Handler:
            Handler.return_value = handlerDecorator
            ch.addHandler(handler, "foo.bar", {}, **extras)

        Handler.assert_called()
        Handler.assert_has_calls([call(handler,  **extras)])

        ch.registry.add.assert_called()
        ch.registry.add.assert_has_calls([call("foo.bar", handlerDecorator, {})])
