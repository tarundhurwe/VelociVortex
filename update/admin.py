from django.contrib import admin
from .models import UserProfile, WorkHistory, Project, PersonalLink


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profile_picture", "description", "current_title", "rating")
    search_fields = ("user__username", "description")


@admin.register(WorkHistory)
class WorkHistoryAdmin(admin.ModelAdmin):
    list_display = ("work_id", "user", "company_name", "start_date", "end_date")
    search_fields = ("user__username", "company_name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("project_id", "user", "title", "description", "link", "image")
    search_fields = ("user__username", "title")


@admin.register(PersonalLink)
class PersonalLinkAdmin(admin.ModelAdmin):
    list_display = ("user", "website_name", "link")
    search_fields = ("user__username", "website_name")
