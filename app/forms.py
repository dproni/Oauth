from django import forms
from app.models import *
from django.contrib.auth.models import User
from django.core.validators import email_re

def is_valid_email(email):
    return True if email_re.match(email) else False

class AddFriendForm(forms.Form):
    friend = forms.EmailField()

    def is_valid(self, request):
        friend = request.POST['friend']
        if is_valid_email(friend) and friend.endswith('gmail.com'):
            return True
        return False

    def save(self, request):
        a, _ = User.objects.get_or_create(email = request.POST['friend'], username = request.POST['friend'])
        friend, _       = Friends.objects.get_or_create(creator = request.user, friend = a)
        friend.save()
        print 'dsdadas'
