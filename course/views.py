import binascii
import random

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
    if not User.objects.filter(username=username).exists():
        u = User.objects.create_user(username=username, password="")

        # Assign a unique random ID
        Student.objects.create(id=random.randbytes(5).hex(), user=u)

    auth_login(request, User.objects.get(username=username))
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

    auth_logout(request)


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
    return [{"id": c.id, "name": c.name, "teacher": c.teacher, "department": c.department,
             "time": c.time} for c in Course.objects.all()]
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
    if "courses" not in data or type(data["courses"]) is not list:
        return 400, "Invalid format for courses"

    selected = []
    for c in data["courses"]:
        if type(c) is not str:
            return 400, "Invalid type for course id"

        if not Course.objects.filter(id=c).exists():
            return 400, f"No such course with id={c}"

        selected.append(c)

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
        try:
            course = json.loads(line)
            Course.objects.create(id=course["id"], name=course["name"], teacher=course["teacher"],
                                  department=course["department"], time=course["time"])
        except json.JSONDecodeError:
            return 400, f"Malformed JSON: {line}"
        except KeyError:
            return 400, f"Missing key in JSON: {line}"
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
    return base64.b64encode("\n".join([
        json.dumps({
            "id": s.id,
            "name": s.user.username,
            "selected": [c.id for c in s.selectedCourses.all()]
        }) for s in Student.objects.all()
    ]).encode()).decode()
    # END TODO


def notFound(request: HttpRequest):
    from django.http import JsonResponse

    return JsonResponse(status=404, data={
        "ok": False,
        "error": "Not Found"
    })
