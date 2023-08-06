from typing import List, Callable, Tuple, Type, NewType, Dict
import falcon

from marshmallow import Schema, fields


class Action:
    """
    example
        :
        class Action:

            name = 'vida'
            schema = ExampleSchema(strict=True)
            method = 'GET'
            def procedure(req, resp, **kwargs):
                resp.context['body'] = {
                    'meaning_of_life': 42,
                }
                return resp

            ...
    """

    # @property
    # def name(self) -> str:
    #     raise NotImplementedError('Action name must be set with str!')

    @property
    def schema(self) -> Schema:
        raise NotImplementedError('You should implement this with a Marshmallow schema!')

    @property
    def query_params_schema(self) -> Schema:
        raise NotImplementedError('You should implement this with a Marshmallow schema!')

    @property
    def response_schema(self) -> Schema:
        raise NotImplementedError('You should implement this with a Marshmallow schema!')

    @property
    def method(self) -> str:
        raise NotImplementedError('You should implement this with a HTTP method name!')

    @property
    def procedure(self, **kwargs) -> Callable[
        [falcon.Request, falcon.Response, dict],
        falcon.Response,
    ]:
        raise NotImplementedError()

    # def validate_body(self, data, only_validate=False):
    #     if only_validate:
    #         self.schema.validate(data)
    #     else:
    #         body = json.loads(data)
    #         self.schema.load(body)


class BaseResourceMixin:

    @property
    def actions(self) -> Dict[str, Action]:
        raise NotImplementedError()

    @property
    def allowed_methods(self) -> List[str]:
        return ['GET', 'POST']

    @property
    def valid_filters(self) -> List[str]:
        return []

    def __init__(self):
        if self.actions is None:
            print("not implemented any action on {}".format(self.__class__))
            return
        for action in self.actions.values():
            if not isinstance(action, Action):
                raise TypeError("{} object in actions is not type of Action".format(action.__class__))

    @staticmethod
    def before_get(req: falcon.Request, **kwargs):
        pass

    @staticmethod
    def after_get(resp: falcon.Response):
        pass

    @staticmethod
    def before_post(req: falcon.Request, **kwargs):
        pass

    @staticmethod
    def after_post(resp: falcon.Response):
        pass

    def filter(self, req):
        # example
        # filter="name::todd|city::denver|title::grand poobah"

        try:
            filter_string = req.params.get('filter')

            filter_string = filter_string.split('"')[1]
            filter_list = filter_string.split('|')

            filters = dict()
            for q_filter in filter_list:
                if q_filter in self.valid_filters:
                    filter_key_value = q_filter.split('::')
                    filters[filter_key_value[0]] = filter_key_value[1]
                else:
                    raise Exception()

            return filters
        except Exception:
            raise falcon.HTTPError(
                falcon.HTTP_400,
                description='Filter error.'
            )

    # def _sort(self, req):
    #     # example
    #     # sort=last_name|first_name|-hire_date
    #
    #     try:
    #         sort_by = req.params.get('sort')
    #         if sort_by:
    #             sort_keys = sort_by.split('|')
    #             for key in sort_keys:
    #                 key_fragments = key.split('-')
    #                 key = key_fragments[-1]
    #
    #                 sort_function = 'asc'
    #                 if key_fragments[0] == '-':
    #                     sort_function = 'desc'

    def on_get(self, req: falcon.Request, resp: falcon.Response, **kwargs) -> None:
        self.before_get(req, **kwargs)
        req.context['action'].procedure(req, resp, resource=self, **kwargs)
        self.after_get(resp)

    def on_post(self, req: falcon.Request, resp: falcon.Response, **kwargs) -> None:
        self.before_post(req, **kwargs)
        req.context['action'].procedure(req, resp, resource=self, **kwargs)
        self.after_post(resp)
