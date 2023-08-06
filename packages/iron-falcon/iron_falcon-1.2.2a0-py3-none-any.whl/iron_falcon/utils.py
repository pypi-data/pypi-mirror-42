# from typing import List
# import importlib
#
# from iron_falcon.resource import RestResource
#
#
# class Route:
#     def __init__(self, path, resource: RestResource):
#         self.path = path
#         self.resource = resource
#
#
# def route(path: str, resource: RestResource) -> Route:
#     return Route(path, resource)
#
#
# def sub_route(path: str, routes: str) -> List[Route]:
#     url = importlib.import_module(routes)
#     return getattr(url, 'urls.routes', None)

import importlib
import re


def register_sub_resource_routes(main_route_table, sub_resources, sub_resource_prefix):
    for resource in sub_resources:
        i = importlib.import_module(resource)
        for route_key, route in i.routes.items():
            full_route_key = sub_resource_prefix + route_key
            if re.match("//", full_route_key):
                raise ValueError(f"Error when registering sub_routes: {full_route_key}")
            if full_route_key not in main_route_table:
                main_route_table[full_route_key] = route
            else:
                raise Exception()


def register_routes(app, route_table, env=""):
    print("Environment: {}".format(env))
    for resource in route_table.keys():
        actions = getattr(route_table[resource], "actions", {})
        action_names = None
        if actions:
            # validate_resource_actions(route_table[resource])
            action_names = list(actions.keys())
        print("Route: {}, Resource: {}, Actions: {}".format(
            resource,
            route_table[resource].__class__.__name__,
            action_names
        ))
        app.add_route(env + resource, resource=route_table[resource])


def validate_resource_actions(resource):
    https_method_actions = ["GET"]
    for action_name, action in resource.actions.items():
        if action_name.islower() and action_name.upper() in https_method_actions:
            print("Lowercase characters used in HTTP method `{}`. Do you mean `GET`?".format(action_name))
