from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("create_room/", views.create_room, name="create-room"),
    path("update_room/<str:pk>/", views.update_room, name="update-room"),
    path("delete_room/<str:pk>/", views.delete_room, name="delete-room"),
]
