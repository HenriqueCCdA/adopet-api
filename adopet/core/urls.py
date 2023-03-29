from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("tutores/", views.TutorList.as_view(), name="list-tutor"),
    path("tutores/<int:pk>/", views.TutorRDU.as_view(), name="read-delete-update-tutor"),
]
