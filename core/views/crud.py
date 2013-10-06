
import json
from django.shortcuts import render, redirect
from core.models import Retrospective, User, Project
from core.workflow import Workflow, EntrySchema
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.context_processors import csrf
from core.forms import (
  LearnedForm, FailedForm, SuccessForm, RetrospectiveGeneralForm,
  ProjectForm)
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse


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
                return redirect('/accounts/profile')

    form = ProjectForm()
    context = {
               "username": "me",
               "question": "Describe your project",
               "form": form,
               "action": "/core/create/project"}
    return render(request, 'core/generic_form.html', context)


@login_required()
def create_mailing_configuration(request):
    user = request.user

    if request.method == 'POST':
        day_of_the_week = request.POST['day_of_the_week']
        mailing_configuration, _ = MailConfiguration.objects.get_or_create(
            user_id=user.id
        )
        mailing_configuration.day_of_the_week = day_of_the_week
        mailing_configuration.save()

        if mailing_configuration:
            return redirect('/accounts/profile')

    form = BasicMailConfigurationForm()
    context = {
               "username": user.username,
               "question": "Configure mailing",
               "form": form,
               "action": "/core/create/mailing",
               "single": True}
    return render(request, 'core/generic_form.html', context)


@login_required()
def change_project(request):
    user = request.user

    if request.method == 'POST':
        project_id = request.session.get('id', None)
        if project_id is None:
            raise Http404
        project = Project.objects.filter(user=user).get(id=project_id)
        form = ProjectForm(request.POST, instance=project)
        form.save()
        return redirect('/accounts/profile')

    project_id = request.GET['id']
    request.session['id'] = project_id
    project = Project.objects.filter(user=user).get(id=project_id)
    form = ProjectForm(instance=project)
    context = {
               "username": user.username,
               "question": "Update you project",
               "form": form,
               "action": "/core/change/project"}
    return render(request, 'core/generic_form.html', context)


@login_required()
def create_workflow(request):
    if request.method == 'POST':
        return redidrect('/accounts/profile')
    context = {
        "predefined_workflows": "predefined workflows",
        "predefined_entries": "predefined_entries",
    }
    context.update(csrf(request))
    return render(request, 'core/workflow_editor.html', context)

@login_required()
def save_workflow(request):
    if request.method == 'POST':
        forms_info = json.loads(request.POST['forms'])
        user = request.user
        schema = EntrySchema.objects.create(creator=user, fields=forms_info)
        
        workflow = Workflow.objects.create(
            creator=user,
            entries_metadata="{}",
        )
        workflow.entryschemas.add(schema)
        
    return HttpResponse(status=201)

@login_required()
def create_learned(request):
    if 'retrospective_id' not in request.session:
        user = request.user
        retrospective = Retrospective.objects.create(user=user)
        request.session['retrospective_id'] = retrospective.id

    if request.method == 'POST':
        form = LearnedForm(request.POST)
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
    else:    
        form = FailedForm(initial={'retrospective_id':request.session['retrospective_id']})
    
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
    else:
        form = SuccessForm(initial={'retrospective_id':request.session['retrospective_id']})
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

    context = {
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

