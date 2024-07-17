from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('logout', views.logout),

    path('listCourses', views.listCourses),
    path('selectCourses', views.selectCourses),
    path('listSelected', views.listSelectedCourses),

    path('admin/uploadCoursesList', views.uploadCoursesList),
    path('admin/downloadSelectionData', views.downloadSelectionData),
]
