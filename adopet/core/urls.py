from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("tutores/", views.TutorList.as_view(), name="tutors"),
]
