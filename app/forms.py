from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from app.models import *
import datetime

class Addboard(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super(Addboard, self).__init__(*args, **kwargs)

    class Meta:
        model = Board