import binascii

from django.http import HttpRequest
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User

from .models import Student, Course
from .wrapper import api


@api(allowed_methods=["POST"], needs_auth=False)
def login(request: HttpRequest, data: dict, **kwargs):
    """Login to the system. If the user does not exist, create one.

    Parameters:
        request (HttpRequest): The request object.
        data (dict): The JSON data sent with the request, in format {"username": "test"}

    Returns:
        Standard error message for failures; nothing for success.
    """

    if type(data) is not dict or "username" not in data or type(data["username"]) is not str:
        return 400, "Bad request"

    username: str = data["username"]

    if len(username) == 0 or len(username) > 50:
        return 400, "Invalid username"

    # TODO: If user does not exist, create one; else, login to that user.
    if not User.objects.filter(username="test").exists():
        u = User.objects.create_user(username="test", password="")
        Student.objects.create(id="000", user=u)

    auth_login(request, User.objects.get(username="test"))
    # END TODO

    return


@api(allowed_methods=["POST"])
def logout(request: HttpRequest, **kwargs):
    """Logout the current user and invalidate session.

    Parameters:
        request (HttpRequest): The request object.

    Returns:
        Nothing.
    """

    # TODO: Logout the user
    raise NotImplementedError()
    # END TODO


@api()
def listCourses(user: User, **kwargs):
    """List all courses

    Parameters:
        user (User): The current user object, auto-filled by @api decorator.

    Returns:
        `data` contains a list of courses in JSON format. Example: [{
            "id": "PKU009",
            "name": "History of Chinese Economic Thought",
            "teacher": "Prof. Zhou Jianbo",
            "department": "Economics",
            "time": "Thu 08:00-10:00"
        }, ...]
    """

    # TODO: Retrieve all courses from DB and return them
    courses = [{"id": "PKU009", "name": "History of Chinese Economic Thought", "teacher": "Prof. Zhou Jianbo",
                "department": "Economics", "time": "Thu 08:00-10:00"}]
    return courses
    # END TODO


@api(allowed_methods=["POST"])
def selectCourses(user: User, data: dict, **kwargs):
    """Select courses based on POST data

    Parameters:
        user (User): The current user object, auto-filled by @api decorator.
        data (dict): The JSON data sent with the request, in format {"courses": ["PKU001", "PKU009"]}

    Returns:
        Standard error message for failures; nothing for success.
    """

    # TODO: Validate input and select courses for the current user
    selected = ["PKU001", "PKU009"]

    # TODO: Update database and handle exceptions
    student = Student.objects.get(user=user)
    student.selectedCourses.clear()
    for course in selected:
        student.selectedCourses.add(Course.objects.get(id=course))
    # END TODO


@api(allowed_methods=["GET"])
def listSelectedCourses(user: User, **kwargs):
    """List all selected courses for the current user

    Parameters:
        user (User): The current user object, auto-filled by @api decorator.

    Returns:
        `data` contains a list of selected courses in JSON format. Example: [{
            "id": "PKU009",
            "name": "History of Chinese Economic Thought",
            "teacher": "Prof. Zhou Jianbo",
            "department": "Economics",
            "time": "Thu 08:00-10:00"
        }, ...]
    """

    return [{"id": c.id, "name": c.name, "teacher": c.teacher, "department": c.department,
             "time": c.time} for c in Student.objects.get(user=user).selectedCourses.all()]


@api(allowed_methods=["POST"])
def uploadCoursesList(user: User, data: dict, **kwargs):
    """Receives a jsonl file as base64 content and parses it to create courses.

    Parameters:
        user (User): The current user object, auto-filled by @api decorator.
        data (dict): The JSON data sent with the request, in format {"file": "base64content"}

    Returns:
        Standard error message for failures; nothing for success.
    """

    # TODO: Validate user permissions
    if not user.is_superuser:
        return 403, "Forbidden"
    # END TODO

    import base64
    import json

    content = ""
    try:
        content = base64.b64decode(data["file"]).decode()
    except KeyError:
        return 400, "Bad request"
    except binascii.Error:
        return 400, f"Malformed base64 content"

    for line in content.split("\n"):
        # TODO: Parse each line and create a Course object, (optionally, validate it), and save to DB
        pass
        # END TODO

    return


@api()
def downloadSelectionData(user: User, **kwargs):
    """Generates a jsonl file containing the selected courses of all students.

    Parameters:
        user (User): The current user object, auto-filled by @api decorator.

    Returns:
        `data` contains the base64 encoded content of the jsonl file.
    """

    # TODO: Validate user permissions
    if not user.is_superuser:
        return 403, "Forbidden"
    # END TODO

    import base64
    import json

    # TODO: Generate the jsonl file content
    return base64.b64encode(json.dumps([{}]).encode()).decode()
    # END TODO


def notFound(request: HttpRequest):
    from django.http import JsonResponse

    return JsonResponse(status=404, data={
        "ok": False,
        "error": "Not Found"
    })
