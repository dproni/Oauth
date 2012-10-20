from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.messages.api import get_messages

from social_auth import __version__ as version
from social_auth.utils import setting
from app.models import *
from app.forms import *
from django.shortcuts import redirect, render
from django.contrib import messages


@login_required()
def add_friend(request):
    addFriend   = AddFriendForm(request)
    if request.method == 'POST':
        if addFriend.is_valid(request):
            addFriend.save(request)
    return redirect(todo)

@login_required()
def delete_friend(request, friend):
    Friends.objects.get(friend=friend).delete()
    return redirect(todo)

@login_required()
def todo(request):
    if request.method == 'POST':
        task = Task(
            name    = request.REQUEST['name'],
            owner   = request.user
                    )
        task.save()
    addFriend   = AddFriendForm()
    tasks       = Task.objects.filter(owner = request.user)
    sharedTasks = Viewer.objects.filter(name = request.user)
    viewers     = Viewer.objects.filter(tasks__in=Task.objects.filter(owner = request.user))
    viewers     = set([i.name.email for i in viewers])
    friends     = Friends.objects.filter(creator = request.user)
    count       = len(tasks) + len(sharedTasks)

    return render(request, 'todo.html', locals())


@login_required()
def update_task(request, id):
    task = Task.objects.get(id = id)
    if request.POST:
        if 'complete' in request.POST:
            if task.owner == request.user:
                task.finished = True
                task.save()
            elif Viewer.objects.get(tasks = task).name == request.user:
                task.finished = True
                task.save()
                Viewer.objects.get(tasks = task).delete()
            return redirect(todo)
        if 'delete' in request.POST:
            if task.owner == request.user:
                task.delete()
            return redirect(todo)
        if 'share' in request.POST:
            email       = request.POST['email']
            user        = User.objects.get(email = email)
            viewer, _   = Viewer.objects.get_or_create(name = user, tasks = task)
            viewer.save()
            task.shared = True
            task.save()
            return redirect(todo)
        if 'GiveBack' in request.POST:
            Viewer.objects.get(tasks=task).delete()
            task.shared = False
            task.save()
            return redirect(todo)
    else:
        return redirect(todo)
#
# REGISTRATION
#


def home(request, *args, **kwards):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/main') # redirect to main
    else:
        return render_to_response('main.html', {'version': version},
                                  RequestContext(request))
@login_required()
def main(request):
    """Home view, displays login mechanism"""
    return render_to_response('main.html', {'version': version},
        RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']

        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', {}, RequestContext(request))

