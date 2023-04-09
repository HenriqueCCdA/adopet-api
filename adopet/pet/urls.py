from django.urls import path

from . import views

app_name = "pet"
urlpatterns = [
    #
    path("pet/<int:pk>/", views.rdu_pet, name="read-delete-update"),
]
