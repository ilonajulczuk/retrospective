
import json
from django.shortcuts import render, redirect
from core.models import Retrospective, User, Project
from core.workflow import Workflow, EntrySchema, Entry
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.context_processors import csrf
from core.forms import (
  LearnedForm, FailedForm, SuccessForm, RetrospectiveGeneralForm,
  ProjectForm)
from mailing.models import (
    BasicMailConfigurationForm,
    MailConfiguration
)
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
        title = request.POST['title']

        user = request.user
        workflow, created = Workflow.objects.get_or_create(
            creator=user,
            title=title,
        )
        if not created:
            workflow.entryschemas.clear()

        entries_metadata = []
        for i, form in enumerate(forms_info):
            entry_title = title + "_%s" % i
            schema, _ = EntrySchema.objects.get_or_create(
                creator=user,
                title=entry_title
            )
            schema.fields = form['data']
            schema.save()
            entries_metadata.append({
                'title': entry_title,
                'number': form['number']
            })
            workflow.entryschemas.add(schema)

        workflow.entries_metadata = json.dumps(entries_metadata)
        workflow.save()
        if created:
            return HttpResponse("{status: 201}")
        else:
            return HttpResponse("{status: 204}")
    else:
        return HttpResponse(status=404)


@login_required()
def delete_workflow(request):
    if request.method == 'POST':
        title = request.POST['title']
        user = request.user

        workflows = Workflow.objects.filter(
            creator=user,
            title=title,
        )
        workflows.delete()

        return HttpResponse("{status: 200}")
    else:
        return HttpResponse("{status: 404}")

def schema_fields_to_html(schema_fields, title):
    html_output = "<h3>%s</h3>" % title
    label = "<label for='%s'>%s:</label>"

    small_input = "<input type='text' id='%s' class='form-control' name='%s' data-required='%s' />"
    big_input = "<textarea id='%s' class='form-control' name='%s' data-required='%s'></textarea>"

    for i, field in enumerate(schema_fields):
        if field['inputType'] == 'Small input':
            basic_input = small_input
        else:
            basic_input = big_input
        name = field['title']
        required = not field['skippable']
        field_label = label % (name, name)
        input = basic_input % (name, title + "-%s" % i, str(required).lower())
        html_output += field_label + input
    return html_output


def create_workflow_form(schemas, metadata):
    schemas_dict = {schema.title: schema.fields for schema in schemas}
    form = []
    for entry in json.loads(metadata):
        form.append({
            'title': entry['title'],
            'input': schema_fields_to_html(
                schemas_dict[entry['title']],
                entry['title']
            )
        })
    return form


def save_retrospective_form(post_data, workflow):
    for i, schema in enumerate(workflow.entryschemas.all()):
        entry = Entry(schema=schema)
        entry_data = {}
        data_keys = map(lambda x: x['title'], schema.fields)
        fields_data = filter(lambda x: x[0].startswith(workflow.title + "_%s" % i) and x[0] != workflow.title, post_data.items())
        for desired_key, key, entry_text in zip(data_keys, *(zip(*fields_data))):
            if key.startswith(schema.title):
                entry_data[desired_key] = entry_text
        entry.data = entry_data
        entry.save()


@login_required()
def try_workflow(request, title):
    if request.method == 'POST':
        user = request.user
        title = request.POST['title']
        workflow = Workflow.objects.get(creator=user, title=title)
        save_retrospective_form(request.POST, workflow)
        return redirect('/accounts/profile')
    else:
        user = request.user
        workflow = Workflow.objects.get(creator=user, title=title)
        schemas = workflow.entryschemas.all()
        metadata = workflow.entries_metadata
        workflow_form = create_workflow_form(schemas, metadata)
        context = {
            "workflow_title": title,
            "workflow_form": workflow_form,
            "action": '/core/workflow/try/%s/' % title
        }
        return render(request, 'core/workflow_try.html', context)

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
        form = FailedForm(
            initial={'retrospective_id': request.session[
                    'retrospective_id'
                ]
            }
        )

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

