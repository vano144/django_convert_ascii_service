import json
import sys
from functools import wraps
from django.http import HttpResponse
from django.http.multipartparser import MultiPartParser
from ascii_app.ascii_converter.log_system import Log


##
# This decorator wraps standard view method to obtain possible exception on server,
#  writing it in console and return it to client in json
# @param function decorated function
def handle_errors(function):

    @wraps(function)
    def wrap(*args, **kwargs):
        try:
            ans = function(*args, **kwargs)
            return ans
        except Exception:
            error_type, error_value, __shit = sys.exc_info()
            result = {
                "type": str(error_type),
                "value": str(error_value),
            }
            Log.log.exception("", exc_info=True)
            return HttpResponse(json.dumps(result, indent=2), content_type="application/json", status=500)

    return wrap


##
# This decorator wraps standard view method to get json from client
#  and set special attribute to django's request object
# @param function decorated function
def set_json(function):

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.method == "POST":
            try:
                setattr(request, "json_data", json.loads(request.body.decode('utf-8')))
            except Exception:
                print("BAD JSON")
        ans = function(request, *args, **kwargs)
        return ans

    return wrap


##
# This decorator wraps standard view method to get json from client
#  and set special attribute to django's request object
# @param function decorated function
def set_json1(function):

    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.method == "POST":
            try:
                json_data = {}
                request.POST = request.POST.dict()
                for key in request.POST.keys():
                    json_data[str(key)] = json.loads(request.POST[key])
                setattr(request, "json_data", json_data)
            except Exception:
                raise Exception("BAD JSON")
        ans = function(request, *args, **kwargs)
        return ans

    return wrap


##
# This decorator wraps standard view method to return client json
def rest_api_call(function):

    @wraps(function)
    def wrap(request, *args, **kwargs):
        ans = function(request, *args, **kwargs)
        return HttpResponse(json.dumps(ans, indent=2), content_type="application/json; charset=utf-8")

    return wrap

