from django.urls import path
from .views import RegistationView, LoginView, RefreshTokenView, LogoutView

urlpatterns = [
        path("register", RegistationView.as_view(), name="registration"),
        path("login", LoginView.as_view(), name="login"),
        path("refresh-token", RefreshTokenView.as_view(), name="refreshtoken"),
        path("logout", LogoutView.as_view(), name="logout")
]