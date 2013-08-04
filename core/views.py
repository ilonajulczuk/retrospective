from django.shortcuts import render, redirect
from core.models import Retrospective, User, Project
from core.forms import (
  LearnedForm, FailedForm, SuccessForm, RetrospectiveGeneralForm,
  ProjectForm)
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index(request):
    context = {"info": "Hello!"}
    return render(request, 'core/index.html', context)


def introduction(request):
  return render(request, 'core/introduction.html')

@login_required()
def create_learned(request):
    if 'retrospective_id' not in request.session:
        user = User.objects.all()[0]
        retrospective = Retrospective.objects.create(user=user)
        request.session['retrospective_id'] = retrospective.id
    
    if request.method == 'POST':
        form = LearnedForm(request.POST)
        print "evaluate form!"
        if form.is_valid():
            learned = form.save()
            learned.retrospective_id = request.session['retrospective_id']
            learned.save()
            if 'more' not in request.POST:
                return redirect('/core/create/failed', learned=learned)

    form = LearnedForm()
    context = {"username": "me",
               "question": "What did I learn?",
               "form": form,
               "action": "/core/create/learned",
               }
    return render(request, 'core/generic_form.html', context)

@login_required()
def create_failed(request):
    if request.method == 'POST':
        form = FailedForm(request.POST)

        if form.is_valid():
            failed = form.save()
            failed.retrospective_id = request.session['retrospective_id']
            failed.save()
            if 'more' not in request.POST:
                return redirect('/core/create/succeeded')

    form = FailedForm()
    context = {"username": "me",
               "question": "In what did I fail?",
               "form": form,
               "action": "/core/create/failed",
               }
    return render(request, 'core/generic_form.html', context)

@login_required()
def create_succeeded(request):
    if request.method == 'POST':
        form = SuccessForm(request.POST)
        if form.is_valid():
            succeeded = form.save()
            succeeded.retrospective_id = request.session['retrospective_id']
            succeeded.save()
            if 'more' not in request.POST:
                return redirect('/core/create/general')

    form = SuccessForm()
    context = {"username": "me",
               "question": "In what did I succeed?",
               "form": form,
               "action": "/core/create/succeeded"}
    return render(request, 'core/generic_form.html', context)

@login_required()
def general_retrospection(request):
    if request.method == 'POST':
        summary = request.POST['summary']
        direction = request.POST['direction']
        r_id = request.session['retrospective_id']
        retrospective = Retrospective.objects.get(id=r_id)
        retrospective.summary = summary
        retrospective.direction = direction
        retrospective.save()
        return redirect('/core/create/done')

    
    form = RetrospectiveGeneralForm()

    context = {"username": "me",
               "question": "What are my general conclusions?",
               "form": form,
               "single": True,
               "action": "/core/create/general"}
    return render(request, 'core/generic_form.html', context)

@login_required() 
def finish_creation(request):
    r_id = request.session['retrospective_id']
    retrospective = Retrospective.objects.get(id=r_id)
    context = {"username": "me",
               "retrospective": retrospective}

    return render(request, 'core/finish_creation.html', context)

@login_required()
def thanks(request):
    request.session.pop('retrospective_id')
    return render(request, 'core/thanks.html')

@login_required()
def profile_dashboard(request):
    user = request.user
    current_projects = Project.objects.filter(user=user)
    context = {
        "projects": current_projects,
    }
    return render(request, 'core/dashboard.html', context)


@login_required()
def logout_view(request):
    logout(request)
    return redirect('/core/')


@login_required()
def create_project(request):
    user = request.user
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        project = Project.objects.create(
            title=title, description=description,
            user_id=user.id)
        if project:
            if 'more' not in request.POST:
                return redirect('/core/')

    form = ProjectForm()
    context = {
               "username": "me",
               "question": "Describe your project",
               "form": form,
               "action": "/core/create/project"}
    return render(request, 'core/generic_form.html', context)