import falcon
try:
    import ujson as json
except ImportError:
    import json
from marshmallow import ValidationError, Schema

from iron_falcon.resource import Action


def dump_response_strategy(marshmallow_version):
    if marshmallow_version == 2:
        def dump(schema, data):
            return schema.dump(data).data

        return dump
    else:
        def dump3(schema, data):
            return schema.dump(data)

        return dump3


def marshmallow_strategy(marshmallow_version, dump_response):
    if marshmallow_version == 2:
        def load(schema, data):
            return schema.load(data).data
    else:
        def load3(schema, data):
            return schema.load(data)
        load = load3

    if dump_response:
        dump = dump_response_strategy(marshmallow_version)
    else:
        dump = load

    return load, dump


class MarshmallowHandler:

    def __init__(self, marshmallow_version=2, dump_response=False):
        self.load, self.dump = marshmallow_strategy(marshmallow_version, dump_response)

    @staticmethod
    def load(schema, data):
        pass

    @staticmethod
    def dump(schema, data):
        pass


class IronMiddleware:

    def __init__(self, action_query_param_key="action", marshmallow_version=2, dump_response=False):
        self._action_query_param_key = action_query_param_key
        self._mh = MarshmallowHandler(marshmallow_version, dump_response)
        self._schema_init_params = {}
        if marshmallow_version == 2:
            self._schema_init_params = dict(strict=True)

    def _validate_action(self, req: falcon.Request, action: Action):
        c_action_schema = getattr(action, 'schema', None)
        c_action_query_params_schema = getattr(action, 'query_params_schema', None)

        if c_action_query_params_schema:
            action_query_params_schema: Schema = c_action_query_params_schema(**self._schema_init_params)
            req.context['params'] = self._mh.load(action_query_params_schema, req.params)

        if c_action_schema:
            action_schema: Schema = c_action_schema(**self._schema_init_params)
            body = json.loads(req.stream.read())
            req.context['body'] = self._mh.load(action_schema, body)

        req.context['action'] = action

    def process_resource(self, req, resp, resource, params):
        try:
            if req.method not in resource.allowed_methods:
                raise falcon.HTTPMethodNotAllowed(
                    resource.allowed_methods
                )
            if resource.actions is None:
                return

            if req.method == 'GET':
                action: Action = resource.actions['get']
                self._validate_action(req, action)
            elif req.method == 'POST':
                action_name = req.params.get(self._action_query_param_key)
                if action_name:
                    action: Action = resource.actions.get(action_name)
                    if action is None:
                        raise falcon.HTTPBadRequest(
                            description="action `{}` is unacceptable".format(action_name)
                        )
                else:
                    action: Action = resource.actions["post"]
                    if action is None:
                        raise falcon.HTTPMethodNotAllowed()

                self._validate_action(req, action)
        except ValidationError as err:
            raise falcon.HTTPBadRequest(
                description=err.messages
            )

    def process_response(self, req, resp, resource, req_succeeded):
        try:
            if req_succeeded and resource.actions is not None:
                body = None
                action = None
                if req.method == 'GET':
                    action: Action = resource.actions['get']
                elif req.method == 'POST' and req.context.get('action'):
                    action: Action = req.context.get('action')  # resource.actions[req.params['action']]
                if action:
                    c_action_response_schema = getattr(action, 'response_schema', None)
                    if c_action_response_schema:
                        action_response_schema: Schema = c_action_response_schema(**self._schema_init_params)
                        body = self._mh.dump(action_response_schema, resp.context['body'])
                if body:
                    resp.media = body
                elif resp.context.get('body'):
                    resp.media = resp.context['body']
        except ValidationError as err:
            print(err.messages)
            raise falcon.HTTPInternalServerError()
