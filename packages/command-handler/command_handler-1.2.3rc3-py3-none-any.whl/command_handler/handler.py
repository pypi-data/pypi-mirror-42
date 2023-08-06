from .views import Invoker

from .command.handler import Registry
from .command.handler.handler import Handler


class CommandHandler:
    def __init__(self, app, **kwargs):
        prefix = kwargs.pop("rulePrefix", "")
        suffix = kwargs.pop("ruleSuffix", "command")
        self.registry = Registry()

        app.add_url_rule(
            rule="{}/{}".format(prefix, suffix),
            view_func=Invoker.as_view(
                "__command_handler_invoker_view_{}_{}".format(prefix, suffix),
                registry=self.registry,
                **kwargs
            ),
            methods=["POST"],
        )

    def addHandler(self, handler, command, schema, **kwargs):
        wrapper = Handler(handler, **kwargs)
        self.registry.add(command, wrapper, schema)
