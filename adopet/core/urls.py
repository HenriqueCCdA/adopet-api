from django.urls import path

from . import views

app_name = "core"
urlpatterns = [
    #
    path("tutores/", views.TutorLC.as_view(), name="list-create-tutor"),
    path("tutores/<int:pk>/", views.TutorRDU.as_view(), name="read-delete-update-tutor"),
    #
    path("abrigos/", views.shelter_list_create, name="list-create-shelter"),
    path("abrigos/<int:pk>/", views.shelter_read_delete_update, name="read-delete-update-shelter"),
]
