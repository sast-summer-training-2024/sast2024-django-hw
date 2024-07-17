from django.http import HttpRequest


def login(request: HttpRequest):
    raise NotImplementedError()


def logout(request: HttpRequest):
    raise NotImplementedError()


def listCourses(request: HttpRequest):
    raise NotImplementedError()


def selectCourses(request: HttpRequest):
    raise NotImplementedError()


def listSelectedCourses(request: HttpRequest):
    raise NotImplementedError()


def uploadCoursesList(request: HttpRequest):
    raise NotImplementedError()


def downloadSelectionData(request: HttpRequest):
    raise NotImplementedError()


def notFound(request: HttpRequest):
    from django.http import HttpResponseNotFound

    return HttpResponseNotFound('{"ok": false, "message": "Not Found"}', headers={'Content-Type': 'application/json'})
