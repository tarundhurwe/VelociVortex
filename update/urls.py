from django.urls import path
from .views import UpdateProfile, UpdateWorkHistory, UpdateProject, UpdatePersonalLinks

urlpatterns = [
    path("profile", UpdateProfile.as_view(), name="update_description"),
    path("project", UpdateProject.as_view(), name="update_project"),
    path("work", UpdateWorkHistory.as_view(), name="update_work_history"),
    path("add-links", UpdatePersonalLinks.as_view(), name="update_personal_links"),
]
