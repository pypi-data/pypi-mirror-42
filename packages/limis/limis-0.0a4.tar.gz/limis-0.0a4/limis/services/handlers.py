from typing import Type

from tornado.web import RequestHandler

from limis.services import Component


class ComponentHandler(RequestHandler):
    """
    Generic component http handler.

    Initialization sets the component class which can be accessed from request methods.
    """
    def initialize(self, component_class: Type[Component]):
        """
        Initializes request handler, called before request handler http method.

        :param component_class: The class of the component which the handler is assigned to.
        """
        self.component_class = component_class
