from django.http import HttpRequest

from .wrapper import api


@api(allowed_methods=["POST"], needs_auth=False)
def login(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api(allowed_methods=["POST"])
def logout(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api()
def listCourses(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api(allowed_methods=["POST"])
def selectCourses(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api(allowed_methods=["POST"])
def listSelectedCourses(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api(allowed_methods=["POST"])
def uploadCoursesList(request: HttpRequest, **kwargs):
    raise NotImplementedError()


@api()
def downloadSelectionData(request: HttpRequest, **kwargs):
    raise NotImplementedError()


def notFound(request: HttpRequest):
    from django.http import JsonResponse

    return JsonResponse(status=404, data={
        "ok": False,
        "error": "Not Found"
    })
