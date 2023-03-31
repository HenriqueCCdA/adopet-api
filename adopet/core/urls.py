from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    path("tutores/", views.TutorLC.as_view(), name="list-create-tutor"),
    path("tutores/<int:pk>/", views.TutorRDU.as_view(), name="read-delete-update-tutor"),
]
