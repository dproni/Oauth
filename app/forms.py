from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User,Group
from app.models import *
import datetime

class Addboard(ModelForm):

    class Meta:
        model = Board

class AddItem(ModelForm):

    class Meta:
#        exclude = ('board',)
        model = Item