import logging
import requests
from time import time
from flask import Flask, Response, json, request, g


class VulcanAPIError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class VulcanAPI:
    """Converts your VulcanResource into a Flask RESTful API.

    After defining your VulcanResource, provide it to VulcanAPI to create a Flask REST API.

    The following endpoints will be created for you:

    - GET /api/ping
    - GET|PUT|POST /api/init
    - GET /api/init/<id>
    - GET|PUT|POST /api/fetch-one
    - GET|PUT|POST /api/fetch-all

    Example
        # ...MyVulcanResource defined elsewhere
        my_vulcan_api = VulcanAPI(resource=MyVulcanResource())

        if __name__ == '__main__':
            my_vulcan_api.run()

    The code above starts a Flask Server running on port 5000 by default, 
    this can be configured using kwargs with the run method like so.

        if __name__ == '__main__':
            my_vulcan_api.run(port=8080)

    VulcanApi.run is really a proxy over Flask.run, see the Flask documentation for more details: (http://flask.pocoo.org)
    """

    def __init__(self, resource, name=__name__, register=False):
        self._resource = resource
        self._app = Flask(__name__)
        self._initialize_endpoints()
        if register:
            try:
                res = requests.post(
                    "{}/api/resource".format(os.environ["REGISTRY_BASE_URL"]), json={"data": {"resourceName": name}})
                if res.status_code == 200:
                    logging.info("Registered successfully")
            except:
                logging.error("Failed to register resource")

    def _initialize_endpoints(self):
        """Add predefined URL endpoints, timing, and error-handling to VulcanAPI Flask application.
        """
        self._app.add_url_rule('/api/ping', 'ping', self._handle_get_ping)
        self._app.add_url_rule(
            '/api/init/', 'init', self._handle_init, methods=['GET', 'PUT', 'POST'])
        self._app.add_url_rule(
            '/api/init/<id>', 'init-with-params', self._handle_init_with_params, methods=['GET', 'PUT'])
        self._app.add_url_rule(
            '/api/fetch-one', 'fetch-one', self._handle_fetch_one, methods=['GET', 'PUT', 'POST'])
        self._app.add_url_rule(
            '/api/fetch-all', 'fetch-all', self._handle_fetch_all, methods=['GET', 'PUT', 'POST'])
        self._app.before_request(self._before_request)
        self._app.after_request(self._after_request)
        self._app.register_error_handler(
            VulcanAPIError, self._handle_vulcan_api_error)

    def _handle_get_ping(self):
        """Returns ping response for healthchecks"""
        payload = json.dumps({
            'data': 'pong',
            'type': 'status'
        })
        return Response(payload, mimetype="application/json")

    def _handle_init(self):
        """Calls VulcanResource.init method"""
        try:
            res = self._resource.init()
            payload = json.dumps({'data': res})
            return Response(payload, mimetype="application/json")
        except Exception:
            raise VulcanAPIError("Init method failure")

    def _handle_init_with_params(self, id):
        """Calls VulcanResource.init with params"""
        try:
            context = {
                'id': id
            }
            res = self._resource.init(context)
            payload = json.dumps({'data': res})
            return Response(payload, mimetype="application/json")
        except Exception:
            raise VulcanAPIError("Init method failure")

    def _handle_fetch_one(self):
        """Calls VulcanResource.fetch_one method"""
        try:
            context = request.get_json()
            res = self._resource.fetch_one(context)
            payload = json.dumps({'data': res})
            return Response(payload, mimetype="application/json")
        except Exception:
            raise VulcanAPIError("FetchOne method failure")

    def _handle_fetch_all(self):
        """Calls VulcanResource.fetch_all method"""
        try:
            context = request.get_json()
            res = self._resource.fetch_all(context)
            payload = json.dumps({'data': res})
            return Response(payload, mimetype="application/json")
        except Exception:
            raise VulcanAPIError("FetchAll method failure")

    def _handle_vulcan_api_error(self, error):
        """Handle exceptions when raised"""
        payload = json.dumps({'data': None, 'errors': [error.to_dict()]})
        return Response(
            payload,
            status=error.status_code,
            mimetype='application/json'
        )

    def _before_request(self):
        """Before each request, start timer to capture request start-time in epochs"""
        g.start = time()

    def _after_request(self, response):
        """
        After each request, calculate difference between request start and request end time.
        Decorates response with meta information regarding the time of the request in seconds. 
        """
        diff = time() - g.start
        if self._is_success_response(response):
            # Gross, could be clearer
            response.set_data(bytes(json.dumps(
                {**json.loads(response.get_data()), 'meta': {'time': f"""{(diff % 60)}s"""}}), 'utf-8'))
        return response

    def _is_success_response(self, response):
        return response.response and (200 <= response.status_code < 300)

    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        """VulcanAPI.run is a proxy to flask.app.run, see https://github.com/pallets/flask/blob/master/flask/app.py"""
        self._app.run(host=host, port=port, debug=debug,
                      load_dotenv=load_dotenv, **options)
