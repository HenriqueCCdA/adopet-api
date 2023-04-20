from django.urls import path

from . import views

app_name = "pet"
urlpatterns = [
    #
    path("pet/", views.lc_pet, name="list-create-pet"),
    path("pet/<int:pk>/", views.rdu_pet, name="read-delete-update-pet"),
    #
    path("adoption/", views.c_adoption, name="create-adoption"),
    path("adoption/<int:pk>/", views.rd_adoption, name="read-delete-adoption"),
]
