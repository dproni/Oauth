from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.messages.api import get_messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from social_auth import __version__ as version
from social_auth.utils import setting
from app.models import *
from app.forms import *

import logging
logger = logging.getLogger('errors.log')

def home(request):
    """Home view, displays login mechanism"""
    if request.user.is_authenticated():
#        try:
#            Board.objects.get(creator=request.user.id)
#        except:
#            board = Board(creator=User.objects.get(id=request.user.id))
#            board.name=request.user.email
#            board.save()
        return HttpResponseRedirect('/main') # redirect to main
    else:
        return render_to_response('main.html', {'version': version},
                                  RequestContext(request))

@csrf_exempt
@login_required
def main(request):
    """Login complete view, displays user data"""

    if request.POST:
        form = AddItem(request.POST)

        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/main')
            except :
                messages.error(request)

    else:
        form = AddItem(request.POST)

    creator = request.user.id
    boards  = Board.objects.filter(creator=creator)
    items = {}
    for i in boards:
        tasks = Item.objects.filter(board=i.id)
        items[i] = tasks
#    items   = [item for item in Item.objects.filter(board=board)]
#    items = Item.objects.filter(board=boards)
    ctx = {
        'items': items,
        'form': form,
        'boards': boards,
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    a = RequestContext(request)
    return render_to_response('done.html', ctx, a)

@csrf_exempt
@login_required
def addBoard(request):
    """Login complete view, displays user data"""

    if request.POST:
        form = Addboard(request.POST)

        if form.is_valid():
            try:
                form.save()
                return HttpResponseRedirect('/main')
            except :
                messages.error(request)

    else:
        form = Addboard(request.POST)

    items   = Item.objects.all()
    boards  = Board.objects.filter(creator=request.user.id),

    ctx = {
        'items': items,
        'form': form,
        'board': boards,
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    a = RequestContext(request)
    return render_to_response('done.html', ctx, a)

@csrf_exempt
@login_required
def addTask(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    a = RequestContext(request)
    return render_to_response('done.html', ctx, a)

@login_required
def shareTask(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    a = RequestContext(request)
    return render_to_response('done.html', ctx, a)

@login_required
def deleteTask(request, task_id):
    """delete task"""
    try:
        task = Item.objects.get(id=task_id)
        task.delete()
    except Exception:
        logger.error("task doesn't exist")
    return HttpResponseRedirect('/main')

@login_required
def deleteBoard(request, board_id):
    """delete board"""
    try:
        board = Board.objects.get(id=board_id)
        for task in Item.objects.filter(board=board_id):
            task.delete()
        board.delete()
    except Exception:
        logger.error("board doesn't exist")
    return HttpResponseRedirect('/main')

@login_required
def shareBoard(request):
    """Login complete view, displays user data"""
    ctx = {
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    a = RequestContext(request)
    return render_to_response('done.html', ctx, a)


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
