# Define a custom User class to work with django-social-auth
from django.db import models
from django.contrib.auth.models import User

class Board (models.Model):
    creator = models.ForeignKey(User)
    created_date = models.DateField(auto_now=True)


class Item(models.Model):
    title = models.CharField(max_length=140)
    created_date = models.DateField(auto_now=True, auto_now_add=True)
    due_date = models.DateField(blank=True,null=True,)
    completed = models.BooleanField()
    board = models.ForeignKey(Board)
    completed_date = models.DateField(blank=True,null=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    priority = models.PositiveIntegerField(max_length=3)

    # Model method: Has due date for an instance of this object passed?
    def overdue_status(self):
        "Returns whether the item's due date has passed or not."
        if datetime.date.today() > self.due_date :
            return 1

    def __unicode__(self):
        return self.title

    # Auto-set the item creation / completed date
    def save(self):
        # If Item is being marked complete, set the completed_date
        if self.completed :
            self.completed_date = datetime.datetime.now()
        super(Item, self).save()


    class Meta:
        ordering = ["priority"]

class CustomUserManager(models.Manager):
    def create_user(self, username, email):
        return self.model._default_manager.create(username=username)


class CustomUser(models.Model):
    username = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    def is_authenticated(self):
        return True

