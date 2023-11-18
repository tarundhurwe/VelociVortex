from django.urls import path
from .views import RegistationView, LoginView

urlpatterns = [
        path("register", RegistationView.as_view(), name="registration"),
        path("login", LoginView.as_view(), name="login")
]