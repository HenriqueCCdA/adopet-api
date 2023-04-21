from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

app_name = "accounts"
urlpatterns = [
    #
    path("", views.version, name="version"),
    #
    path("tutores/", views.tutor_list_create, name="list-create-tutor"),
    path("tutores/<int:pk>/", views.tutor_read_delete_update, name="read-delete-update-tutor"),
    #
    path("abrigos/", views.shelter_list_create, name="list-create-shelter"),
    path("abrigos/<int:pk>/", views.shelter_read_delete_update, name="read-delete-update-shelter"),
    #
    path("login/", obtain_auth_token, name="login"),
    #
    path("whoami/", views.whoami, name="whoami"),
]
