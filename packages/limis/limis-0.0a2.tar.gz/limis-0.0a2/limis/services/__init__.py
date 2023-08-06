"""
limis services module
"""
import logging

from typing import List

from tornado.routing import PathMatches, Rule, RuleRouter
from tornado.web import Application

from limis.services import messages
from limis.services.components import Component


class Service:
    """
    Service Definition
    """
    def __init__(self, name: str, components: List[Component], path: str = None):
        """
        Initializes the Service class.

        :param name: Service name, will be used as the path if 'path' is not provided.
        :param components: List of service components, must inherit from Component class.
        :param path: Path for service, defaults to name.
        :raises ValueError: Error indicating either the component or handler class is invalid.
        """
        self.logger = logging.getLogger(__name__)

        self.name = name
        self.path = name if path is None else path

        self.http_router = None
        self.http_rules = []
        self.websocket_router = None
        self.websocket_rules = []

        self.logger.debug(messages.SERVICE_INIT_REGISTER_COMPONENTS_STARTED.format(self.name))

        for component in components:
            self.add_component(component)

        self.logger.debug(messages.SERVICE_INIT_REGISTER_COMPONENTS_COMPLETED.format(self.name))

    def add_component(self, component: Component):
        """
        Adds a components handlers to the http or websocket routers respectively.

        :param component: Services component
        """
        if not issubclass(component.__class__, Component):
            msg = messages.SERVICE_ADD_COMPONENT_INVALID_COMPONENT_CLASS.format(component.__class__)

            self.logger.error(msg)
            raise ValueError(msg)

        self.logger.debug(messages.SERVICE_ADD_COMPONENT.format(
            self.name, component.component_name, component.path
        ))

        http_handlers = []
        websocket_handlers = []

        if component.http_handler:
            self.logger.debug(messages.SERVICE_ADD_COMPONENT_REGISTER_HANDLER.format(
                self.name, component.component_name, 'http_handler'
            ))
            http_handlers = [(r'/.*', component.http_handler)]

        if component.websocket_handler:
            self.logger.debug(messages.SERVICE_ADD_COMPONENT_REGISTER_HANDLER.format(
                self.name, component.component_name, 'websocket_handler'
            ))
            websocket_handlers = [(r'/.*', component.websocket_handler)]

        if component.http_handler is None and component.websocket_handler is None:
            self.logger.warning(messages.SERVICE_ADD_COMPONENT_WITH_NO_HANDLER.format(
                component.component_name, self.name))

        http_application = Application(http_handlers)
        websocket_application = Application(websocket_handlers)

        self.http_rules.append(Rule(PathMatches('/{}.*'.format(component.path)), http_application))
        self.websocket_rules.append(Rule(PathMatches('/{}.*'.format(component.path)), websocket_application))

        self.http_router = RuleRouter(self.http_rules)
        self.websocket_router = RuleRouter(self.websocket_rules)
