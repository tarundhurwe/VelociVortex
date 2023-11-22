from django.urls import path
from .views import UpdateProfile

urlpatterns = [path("", UpdateProfile.post, name="home")]