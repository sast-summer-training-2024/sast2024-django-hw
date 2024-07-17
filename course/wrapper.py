"""
Wrapper for JSON API endpoints
"""
import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from sast2024_django_hw import settings


def api(allowed_methods: list[str] = None, needs_auth: bool = True):
    """
    Decorator for all API views, checks for allowed methods, handles OPTIONS requests,
    parses JSON body and returns JSON response.

    This function never throws, and always returns a JsonResponse (for all but OPTIONS requests).

    The decorated function may have a data (JSON data), request (raw HTTPRequest), method (string request method)
    or user parameter with *args, **kwargs, and should return an object or a tuple of (status, string).

    Any api accepts an OPTIONS request and returns a response with the allowed methods in the "Allow" header.

    If an API requires valid session but the user is not logged in, the API will return 403 status code:
    {
        "ok": false,
        "error": "Invalid Session"
    }

    If an API is called with a method not in the allowed_methods list, the API will return 405 status code:
    {
        "ok": false,
        "error": "Method not allowed"
    }

    If an API is called with a bad JSON request, the API will return 400 status code:
    {
        "ok": false,
        "error": "Malformed JSON request"
    }

    If an API is called 1. Not with GET verb; 2. With a Content-Type other than application/json, the API will return
    400 status code:
    {
        "ok": false,
        "error": "Content type not recognized"
    }

    If a FieldMissingError or FieldTypeError is thrown, the API will return 400 status code.

    If any internal error occurs, the API will return 500 status code. In debug mode it will trigger a django 500 page
    with detailed stack trace in it; in release mode it will return:
    {
        "ok": false,
        "error": "Internal server error"
    }
    """

    if allowed_methods is None:
        allowed_methods = ["GET"]

    if "OPTIONS" not in allowed_methods:
        allowed_methods.append("OPTIONS")

    def decorator(function):
        def decorated(request: HttpRequest, *args, **kwargs) -> HttpResponse:
            # Always allow OPTIONS requests
            if request.method == "OPTIONS":
                response = HttpResponse()
                response["Allow"] = ", ".join(allowed_methods)
                return response

            # Check for allowed methods
            if request.method not in allowed_methods:
                return JsonResponse(status=405, data={
                    "ok": False,
                    "error": "Method not allowed"
                }, headers={
                    "Allow": ", ".join(allowed_methods)
                })

            # Check for authentication
            if needs_auth and not request.user.is_authenticated:
                return JsonResponse(status=403, data={
                    "ok": False,
                    "error": "Invalid Session"
                })

            # Try to parse JSON body (if any)
            data: dict | None = None
            if request.method != "GET" and request.content_type != "" and request.body != b"":
                if request.content_type != "application/json":
                    return JsonResponse(status=400, data={
                        "ok": False,
                        "error": f"Content type \"{request.content_type}\" not recognized"
                    })

                try:
                    data = json.loads(request.body)
                except json.JSONDecodeError as e:
                    return JsonResponse(status=400, data={
                        "ok": False,
                        "error": f"Malformed JSON request:\nf{e}"
                    })

            try:
                kwargs["request"] = request
                kwargs["user"] = request.user
                kwargs["data"] = data

                response_data = function(*args, **kwargs)

                if isinstance(response_data, tuple):
                    status, data = response_data
                    return JsonResponse(status=status, data={
                        "ok": False,
                        "error": data
                    })

                return JsonResponse({
                    "ok": True,
                    "data": response_data,
                })

            except Exception as e:
                if settings.DEBUG:
                    raise

                return JsonResponse(status=500, data={
                    "ok": False,
                    "error": f"Internal server error: {e}"
                })

        return decorated

    return decorator

