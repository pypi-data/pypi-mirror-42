from .views import Invoker

from .command.handler import registry
from .command.handler.handler import Handler


class CommandHandler:
    def __init__(self, app, **kwargs):
        prefix = kwargs.pop("rulePrefix", "")
        suffix = kwargs.pop("ruleSuffix", "command")

        app.add_url_rule(
            rule="{}/{}".format(prefix, suffix),
            view_func=Invoker.as_view("__command_handler_invoker_view_{}_{}".format(prefix, suffix), **kwargs),
            methods=["POST"],
        )

    def addHandler(self, handler, command, schema, **kwargs):
        wrapper = Handler(handler, **kwargs)
        registry.add(command, wrapper, schema)
