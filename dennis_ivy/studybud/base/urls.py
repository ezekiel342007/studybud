from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", views.register_user, name="register"),
    path("", views.home, name="home"),
    path("room/<str:pk>/", views.room, name="room"),
    path("profile/<str:pk>/", views.user_profile, name="user-profile"),
    path("create_room/", views.create_room, name="create-room"),
    path("update_room/<str:pk>/", views.update_room, name="update-room"),
    path("delete_room/<str:pk>/", views.delete_room, name="delete-room"),
    path("delete_message/<str:pk>/", views.delete_message, name="delete-message"),
]
