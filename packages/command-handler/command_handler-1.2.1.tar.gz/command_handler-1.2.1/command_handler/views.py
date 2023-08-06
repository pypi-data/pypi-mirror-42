from flask import request
from flask.views import MethodView
from json import dumps
from jsonschema.exceptions import SchemaError
from logging import getLogger

from command_handler.request.exceptions import InvalidRequestException
from command_handler.command.handler import registry
from command_handler.request.validator import ValidatorFactory

LOGGER = getLogger(__name__)


class Invoker(MethodView):
    def __init__(self, **kwargs):
        asserts = kwargs.get("validators", [])
        for a in ["command", "json"]:
            if a not in asserts:
                asserts.append(a)

        self.registry = registry
        self.validator = ValidatorFactory.create(registry, asserts)

    def post(self, *args, **kwargs):
        response = {}
        code = 202
        headers = {
            "Content-type": "application/json"
        }

        try:
            self.validator.test(request)

            # it is already validated by `command` and `json` asserts
            data = request.get_json()
            if not ("command" in data and "payload" in data):
                return response, 400, headers

            command = data["command"]
            handler = self.registry[command][0]

            payload = data["payload"]
            command = data["command"]

            handler(payload, command)
        except SchemaError:
            code = 500
            response["error"] = "Command payload schema error"
        except InvalidRequestException as e:
            code = e.code
            response["error"] = str(e)
        except BaseException as e:
            code = 500
            response["error"] = "Internal server error"

            LOGGER.error(e)

        return dumps(response), code, headers
