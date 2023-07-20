from django.urls import path

from .views import index, UserCreateView

urlpatterns = [
    path("", index, name="home"),
    path("users/create/", UserCreateView.as_view(), name="user-create")
]

app_name = "manager"
