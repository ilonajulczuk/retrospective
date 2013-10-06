from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def index(request):
    context = {"info": "Hello!"}
    return render(request, 'core/index.html', context)


def introduction(request):
  return render(request, 'core/introduction.html')


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/core/')


@login_required()
def thanks(request):
    request.session.pop('retrospective_id', None)
    return render(request, 'core/dashboard.html')


def learn_more(request):
    return render(request, 'core/learn_more.html')

