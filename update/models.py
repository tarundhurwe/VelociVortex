from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    profile_picture = models.ImageField(
        upload_to="images/profile", blank=True, null=True
    )
    current_title = models.CharField(max_length=255, default="", blank=True, null=True)
    description = models.TextField()
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(10)])


class WorkHistory(models.Model):
    work_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    title = models.CharField(max_length=150, blank=False, null=False, default="")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "Work History"
        unique_together = ("user", "start_date", "end_date")


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField()
    image = models.ImageField(upload_to="images/projects", blank=True, null=True)


class PersonalLink(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    link = models.URLField()

    class Meta:
        unique_together = ("user", "link")


class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.CharField(max_length=255)
    level = models.IntegerField(default=0, validators=[MaxValueValidator(10)])

    class Meta:
        unique_together = ("user", "skill")
