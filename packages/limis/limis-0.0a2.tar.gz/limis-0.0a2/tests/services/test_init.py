import http
import logging
import time
import threading

from unittest import TestCase

from tornado.web import RequestHandler
from tornado.websocket import WebSocketHandler
from websocket import create_connection

from limis.server import Server
from limis.services import messages
from limis.services import Service
from limis.services.components import Resource


class TestService(TestCase):
    class TestHTTPRequestHandler(RequestHandler):
        response = 'hello world'

        def get(self):
            self.write(self.response)

    class TestWebSocketHandler(WebSocketHandler):
        response_on_message = 'websocket message received: {}'

        def on_message(self, message):
            self.write_message(self.response_on_message.format(message))

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
        path = 'component'

        component = Resource(path=path, http_handler=None, websocket_handler=None)

        service = Service(name='service', components=[])

        with self.assertLogs(logger=self.logger, level='WARNING') as log:
            service.add_component(component)

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_WITH_NO_HANDLER.format(component.component_name, 'service')))

        with self.assertRaises(ValueError):
            with self.assertLogs(logger=self.logger, level='ERROR') as log:
                invalid_component = 'invalid_component'
                service.add_component(invalid_component)

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_INVALID_COMPONENT_CLASS.format(invalid_component.__class__)))

    def test_init(self):
        service = Service(name='service', components=[])

    def test_init_component_with_no_handler(self):
        test_response = '<html><title>404: Not Found</title><body>404: Not Found</body></html>'
        path = 'component'

        component = Resource(path=path, http_handler=None, websocket_handler=None)

        with self.assertLogs(logger=self.logger, level='WARNING') as log:
            service = Service(name='service', components=[component])

        self.assertTrue(log.output[0].find(
            messages.SERVICE_ADD_COMPONENT_WITH_NO_HANDLER.format(component.component_name, 'service')))

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        http_response = TestService.__get_http_response('localhost', http_server.port, 'GET', '/{}'.format(path))
        self.assertEqual(http.client.NOT_FOUND, http_response[0])
        self.assertEqual(test_response, http_response[1])

    def test_init_component_with_http_handler(self):
        path = 'component'

        component = Resource(path=path, http_handler=self.TestHTTPRequestHandler, websocket_handler=None)

        service = Service(name='service', components=[component])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        http_response = TestService.__get_http_response('localhost', http_server.port, 'GET', '/{}'.format(path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

    def test_init_component_with_websocket_handler(self):
        path = 'component'

        component = Resource(path=path, http_handler=None, websocket_handler=self.TestWebSocketHandler)

        service = Service(name='service', components=[component])

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port, path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

    def test_init_component_with_http_and_websocket_handler(self):
        path = 'component'

        component = Resource(path=path,
                             http_handler=self.TestHTTPRequestHandler, websocket_handler=self.TestWebSocketHandler)

        service = Service(name='service', components=[component])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)
        http_response = TestService.__get_http_response('localhost', http_server.port, 'GET', '/{}'.format(path))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port, path))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

    def test_init_multiple_components_with_http_and_websocket_handler(self):
        path1 = 'component1'

        component1 = Resource(path=path1,
                              http_handler=self.TestHTTPRequestHandler, websocket_handler=self.TestWebSocketHandler)

        path2 = 'component1'

        component2 = Resource(path=path2,
                              http_handler=self.TestHTTPRequestHandler, websocket_handler=self.TestWebSocketHandler)

        service = Service(name='service', components=[component1, component2])

        thread = threading.Thread(target=TestService.__run_http_server, args=(service.http_router,))
        thread.daemon = True
        thread.start()

        thread = threading.Thread(target=TestService.__run_websocket_server, args=(service.websocket_router,))
        thread.daemon = True
        thread.start()

        time.sleep(1)
        http_response = TestService.__get_http_response('localhost', http_server.port, 'GET', '/{}'.format(path1))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        http_response = TestService.__get_http_response('localhost', http_server.port, 'GET', '/{}'.format(path2))

        self.assertEqual(http.client.OK, http_response[0])
        self.assertEqual(self.TestHTTPRequestHandler.response, http_response[1])

        message = 'test message'

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port, path1))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()

        websocket = create_connection('ws://localhost:{}/{}'.format(websocket_server.port, path1))
        websocket.send(message)

        response = websocket.recv()

        self.assertEqual(response, self.TestWebSocketHandler.response_on_message.format(message))

        websocket.close()
