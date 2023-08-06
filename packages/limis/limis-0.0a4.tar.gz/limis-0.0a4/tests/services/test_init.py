import http
import logging
import time
import threading

from unittest import TestCase
from tornado.websocket import WebSocketHandler
from websocket import create_connection

from limis.server import Server
from limis.services import messages
from limis.services import Service
from limis.services.components import Resource
from limis.services.handlers import ComponentHandler


class TestService(TestCase):
    class TestHTTPRequestHandler(ComponentHandler):
        response = 'hello world'

        def get(self):
            self.write(self.response)

    class TestWebSocketHandler(ComponentHandler, WebSocketHandler):
        response_on_message = 'websocket message received: {}'

        def on_message(self, message):
            self.write_message(self.response_on_message.format(message))

    class TestResource(Resource):
        component_name = 'test_resource'
        component_path = 'test_resource'
        test_attribute = 'test attribute'

    class TestResource1(Resource):
        component_name = 'test_resource_1'
        component_path = 'test_resource_1'

    @staticmethod
    def __get_http_response(host, port, method, path):
        http_client = http.client.HTTPConnection(host, port)
        http_client.request(method, path)

        http_client_response = http_client.getresponse()

        status = http_client_response.status
        response = http_client_response.read().decode('utf-8')

        http_client.close()

        return status, response

    @staticmethod
    def __run_http_server(router):
        global http_server

        http_server = Server(router, port=8000)
        http_server.logger.disabled = True
        http_server.start()

    @staticmethod
    def __run_websocket_server(router):
        global websocket_server

        websocket_server = Server(router, port=8001)
        websocket_server.logger.disabled = True
        websocket_server.start()

    def setUp(self):
        self.logger = logging.getLogger('limis.services')

    def tearDown(self):
        try:
            if http_server.running:
                http_server.stop_server = True

                while http_server.running:
                    time.sleep(1)

            if websocket_server.running:
                websocket_server.stop_server = True

                while websocket_server.running:
                    time.sleep(1)
        except NameError:
            pass

    def test_add_component(self):
        service = Service(name='service', components=[])

        with self.assertLogs(logger=self.logger, level='WARNING') as log:
            service.add_component(self.TestResource)

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_WITH_NO_HANDLER.format(self.TestResource.component_name, 'service')))

    def test_add_component_with_invalid_component_class(self):
        service = Service(name='service', components=[])

        with self.assertRaises(ValueError):
            with self.assertLogs(logger=self.logger, level='ERROR') as log:
                service.add_component(Service)

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_INVALID_COMPONENT_CLASS.format(Service.__name__)))

    def test_add_Component_with_invalid_component_type(self):
        service = Service(name='service', components=[])

        with self.assertRaises(TypeError):
            with self.assertLogs(logger=self.logger, level='ERROR') as log:
                invalid_component = 'invalid_component'
                service.add_component(invalid_component)

        self.assertTrue(log.output[0].find(messages.SERVICE_ADD_COMPONENT_INVALID_COMPONENT_TYPE))

    def test_init(self):
        service = Service(name='service', components=[])

    def test_init_component_with_no_handler(self):
        test_response = '<html><title>404: Not Found</title><body>404: Not Found</body></html>'

        with self.assertLogs(logger=self.logger, level='WARNING') as log:
            service = Service(name='service', components=[self.TestResource])

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_WITH_NO_HANDLER.format(self.TestResource.component_name, 'service')))

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        http_response = TestService.__get_http_response('localhost', http_server.port,
                                                        'GET', '/{}'.format(self.TestResource.component_path))
        self.assertEqual(http.client.NOT_FOUND, http_response[0])
        self.assertEqual(test_response, http_response[1])

    def test_init_component_with_http_handler(self):
        class TestResourceWithHTTPHandler(self.TestResource):
            component_http_handler = self.TestHTTPRequestHandler

        service = Service(name='service', components=[TestResourceWithHTTPHandler])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        http_response = TestService.__get_http_response('localhost', http_server.port,
                                                        'GET', '/{}'.format(TestResourceWithHTTPHandler.component_path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

    def test_init_component_with_websocket_handler(self):
        class TestResourceWithWebSocketHandler(self.TestResource):
            component_websocket_handler = self.TestWebSocketHandler

        service = Service(name='service', components=[TestResourceWithWebSocketHandler])

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port,
                                                                    TestResourceWithWebSocketHandler.component_path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

    def test_init_component_with_http_and_websocket_handler(self):
        class TestResourceWithBothHandlers(self.TestResource):
            component_http_handler = self.TestHTTPRequestHandler
            component_websocket_handler = self.TestWebSocketHandler

        service = Service(name='service', components=[TestResourceWithBothHandlers])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)
        http_response = TestService.__get_http_response('localhost', http_server.port,
                                                        'GET', '/{}'.format(TestResourceWithBothHandlers.component_path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port,
                                                                    TestResourceWithBothHandlers.component_path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

    def test_init_multiple_components_with_http_and_websocket_handler(self):
        class TestResourceWithBothHandlers(self.TestResource):
            component_http_handler = self.TestHTTPRequestHandler
            component_websocket_handler = self.TestWebSocketHandler

        class TestResource0(TestResourceWithBothHandlers):
            component_name = 'test_resource_0'
            component_path = 'test_resource_0'

        class TestResource1(TestResourceWithBothHandlers):
            component_name = 'test_resource_1'
            component_path = 'test_resource_1'

        service = Service(name='service', components=[TestResource0, TestResource1])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)
        http_response = TestService.__get_http_response('localhost', http_server.port,
                                                        'GET', '/{}'.format(TestResource0.component_path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        http_response = TestService.__get_http_response('localhost', http_server.port,
                                                        'GET', '/{}'.format(TestResource1.component_path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port,
                                                                    TestResource0.component_path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port,
                                                                    TestResource1.component_path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()
