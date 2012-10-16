# Define a custom User class to work with django-social-auth
from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    name        = models.CharField(max_length=200)
    owner       = models.ForeignKey(User)
    finished    = models.BooleanField(default=False)
    shared      = models.BooleanField(default=False)

class Viewer(models.Model):
    name        = models.ForeignKey(User)
    tasks       = models.ForeignKey(Task)

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)

class CustomUser(models.Model):
    username    = models.CharField(max_length=128)
    last_login  = models.DateTimeField(blank=True, null=True)

    objects     = CustomUserManager()

    def is_authenticated(self):
        return True

