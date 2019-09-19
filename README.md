# flask-wrappers

Decorators to facilitate flask enpoints implementation

```python
import flask_wrappers as wrappers
```

## Decorators

### @catch

Decorator to catch exceptions and return a meaningful traceback

```python
@wrappers.catch
def my_endpoint():
    raise ValueError()
```

### json_request

Decorator to pass the decoded json body of the request as a dict to the endpoint method.

```python
@wrappers.json_request
def my_endpoint(body):
    return body.get("property_1")
```

### json_request_required:

Decorator to pass the decoded json body of the request as a dict to the endpoint method.
	Validate that the json body contains at least the required properties.

```python	
@wrappers.json_request_required("str:name", "str:job", "int:age", "float:cash")
def my_endpoint(body):
    return body["name"] # safe
```
### querystring_request

Decorator to pass the querystring dict to the endpoint method.
	
```python
@wrappers.querystring_request
def my_endpoint(querystring):
    return querystring.get("property_1")
```

### headers_request

Decorator to pass the headers dict to the endpoint method.
	
```python
@wrappers.headers_request
def my_endpoint(headers):
    return headers.get("property_1")
```

### cookies_request

Decorator to pass the cookies dict to the endpoint method.
	
```python
@wrappers.cookies_request
def my_endpoint(cookies):
    return cookies.get("property_1")
```

### body_request

Decorator to pass the raw body to the endpoint method.
	
```python
@wrappers.body_request
def my_endpoint(body):
    return body.get("property_1")
```

### json_response

Decorator to return the appropriate json response object from anything decodable to json.
	
```python
@wrappers.json_response
def my_endpoint(body):
    l = [10, 8, 5]
    return {'name':  'Test', 'grades': l}, 200
```

### RouteFactory

Class to generate routes for http methods and paths from a flask app or blueprint.

```python
from flask import Blueprint, Flask
import flask_wrappers as wrappers

# create a flask app
app = Flask(__name__)
# or create a blueprint
## app = Blueprint("blueprint_name", __name__)

# create a route_factory from the app
route_factory = wrappers.RouteFactory(app)
```

#### options(route, **options)

Create an endpoint for the route and method OPTIONS

```python
@route_factory.options("/names")
def my_endpoint():
    # logic here
```

#### get(route, **options)

Create an endpoint for the route and method GET

```python
@route_factory.get("/names")
@wrappers.json_response
def my_endpoint():
    return ["Anna", "Alice", "Shila"], 200
```
		
#### post(route, **options)

Create an endpoint for the route and method POST

```python
@route_factory.post("/names")
@wrappers.json_request
@wrappers.json_response
def my_endpoint(body):
    # logic here 
    return "ok", 200
```

#### put(route, **options)

Create an endpoint for the route and method PUT

```python
@route_factory.put("/names")
@wrappers.json_request
@wrappers.json_response
def my_endpoint(body):
    # logic here 
    return "ok", 200
```

#### delete(route, **options)

Create an endpoint for the route and method DELETE

```python
@route_factory.post("/names/<name>")
@wrappers.json_response
def my_endpoint(name):
    # logic here 
    return "ok", 200
```
