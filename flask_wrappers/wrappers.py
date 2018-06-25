from flask import request, Response
import json
import datetime


class __JSONEncoder(json.JSONEncoder):
    """
    JSON Encoder to handle datetime.datetime objects
    """
    #pylint: disable=E0202
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def catch(func):
    """Decorator to catch exceptions and return a meaningful traceback"""
    def __callback(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except:
            import traceback
            return str(traceback.format_exc()), 500
    return __callback


def json_request(func):
    """
    Decorator to pass the decoded json body of the request as a dict to the endpoint method.
    
    >>> @json_request
    >>> def my_endpoint(body: dict) -> str:
    >>>         return body.get("property_1")
    """
    def __callback(*args, **kwargs):
        if type(request.json) is dict:
            body = request.json
        else:
            body = request.json()
        if body is None:
            raise AssertionError("Request body is not application/json")
        return func(body, *args, **kwargs)
    return __callback


class json_request_required:
    """
    Decorator to pass the decoded json body of the request as a dict to the endpoint method.
    Validate that the json body contains at least the required properties.
    
    >>> @json_request_required("str:name", "str:job", "int:age", "float:cash")
    >>> def my_endpoint(body: dict) -> str:
    >>>         return body["name"]        # safe
    """
    def __init__(self, *args):
        self.required = args

    @staticmethod
    def verify_json(obj, required):
        """
        Static method to validate that the json body contains at least the required properties.
        """
        # import datetime
        errors = {}
        __types = {
            "any": "any",
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            # "datetime": datetime.datetime
        }
        for key in required:
            key = str(key)
            _type_name = None
            
            # Validate the declaration of the required property to follow the pattern type:key
            if ":" in key:
                _type_name, key = key.split(":")
                _type_name = _type_name.lower()
            
            if key not in obj:
                errors[key] = "missing"
            elif _type_name is not None and _type_name != "any":
                _type = __types.get(_type_name)
                if _type is None:
                    raise AssertionError(_type_name + " is not a valid type. The valid types are: " + ' '.join(__types.keys()) + ".")
                elif type(obj[key]) is not _type:
                    errors[key] = "is not of type " + _type_name
        return errors

    def __verify_json(self, obj):
        required = self.required
        if len(required) == 0:
            return {}
        if isinstance(required[0], (tuple, list)):
            required = required[0]
        return json_request_required.verify_json(obj, required)

    def __call__(self, func):
        def __callback(body, *args, **kwargs):
            result = self.__verify_json(body)
            if result:
                raise AssertionError("Some keys did not meet the requirements: {0}".format(result))
            return func(body, *args, **kwargs)
        return json_request(__callback)


def querystring_request(func):
    """
    Decorator to pass the querystring dict to the endpoint method.
    
    >>> @querystring_request
    >>> def my_endpoint(querystring: dict) -> str:
    >>>         return querystring.get("property_1")
    """
    def __callback(*args, **kwargs):
        qs = request.args
        if qs is None:
            qs = {}
        return func(qs, *args, **kwargs)
    return __callback


def headers_request(func):
    """
    Decorator to pass the headers dict to the endpoint method.
    
    >>> @headers_request
    >>> def my_endpoint(headers: dict) -> str:
    >>>         return headers.get("property_1")
    """
    def __callback(*args, **kwargs):
        headers = request.headers
        if headers is None:
            headers = {}
        return func(headers, *args, **kwargs)
    return __callback


def cookies_request(func):
    """
    Decorator to pass the cookies dict to the endpoint method.
    
    >>> @cookies_request
    >>> def my_endpoint(cookies: dict) -> str:
    >>>         return cookies.get("property_1")
    """
    def __callback(*args, **kwargs):
        cookies = request.cookies
        if cookies is None:
            cookies = {}
        return func(cookies, *args, **kwargs)
    return __callback


def body_request(func):
    """
    Decorator to pass the raw body to the endpoint method.
    
    >>> @body_request
    >>> def my_endpoint(body: dict) -> str:
    >>>         return body.get("property_1")
    """
    def __callback(*args, **kwargs):
        body = request.data
        if body is None:
            body = {}
        return func(body, *args, **kwargs)
    return __callback


def json_response(func):
    """
    Decorator to return the appropriate json response object from anything decodable to json.
    
    >>> @json_response
    >>> def my_endpoint(body: dict) -> str:
    >>>        l = [10, 8, 5]
    >>>         return {'name':  'Test', 'grades': l}, 200
    Response('{"name":"Test","grades":[10,8,5]}', status=200, mimetype='application/json')
    """
    def __callback(*args, **kwargs):
        result = func(*args, **kwargs)
        if not isinstance(result, (list, tuple)):
            result = result, 200
        
        if len(result) == 0:
            result = "", 200
        elif len(result) == 1:
            result = result[0], 200
        
        return Response(response=json.dumps(result[0], cls=__JSONEncoder), status=result[1], mimetype='application/json')
    return __callback


class RouteFactory:
    """Class to generate routes for http methods and paths."""
    def __init__(self, app):
        self.app = app
    
    def __wrap_route(self, route, method, **options):
        """Decorate the function on the flask @route for the route and method."""
        methods = {m for m in options.get("methods", [])}
        if method not in methods:
            methods.add(method)
        options["methods"] = [m for m in methods]
        def __wrap(func):
            def __callback(*args, **kwargs):
                return func(*args, **kwargs)
            __callback.__name__ = func.__name__ + str(id(__callback))
            return self.app.route(route, **options)(__callback)
        return __wrap

    def options(self, route, **options):
        """
        Create an endpoint for the route and method OPTIONS.
        
        :param route: any flask valid route
        :param options: any flask @route valid option
        :returns: self.app.route(route, methods=['OPTIONS'], **options)
        """
        return self.__wrap_route(route, 'OPTIONS', **options)

    def get(self, route, **options):
        """
        Create an endpoint for the route and method GET.
        
        :param route: any flask valid route
        :param options: any flask @route valid option
        :returns: self.app.route(route, methods=['GET'], **options)
        """
        return self.__wrap_route(route, 'GET', **options)

    def post(self, route, **options):
        """
        Create an endpoint for the route and method POST.
        
        :param route: any flask valid route
        :param options: any flask @route valid option
        :returns: self.app.route(route, methods=['POST'], **options)
        """
        return self.__wrap_route(route, 'POST', **options)

    def put(self, route, **options):
        """
        Create an endpoint for the route and method PUT.
        
        :param route: any flask valid route
        :param options: any flask @route valid option
        :returns: self.app.route(route, methods=['PUT'], **options)
        """
        return self.__wrap_route(route, 'PUT', **options)

    def delete(self, route, **options):
        """
        Create an endpoint for the route and method DELETE.
        
        :param route: any flask valid route
        :param options: any flask @route valid option
        :returns: self.app.route(route, methods=['DELETE'], **options)
        """
        return self.__wrap_route(route, 'DELETE', **options)
