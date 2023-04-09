from django.urls import path

from . import views

app_name = "pet"
urlpatterns = [
    #
    path("pet/", views.lc_pet, name="list-create"),
    path("pet/<int:pk>/", views.rdu_pet, name="read-delete-update"),
]
