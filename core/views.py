from django.shortcuts import render, redirect
from core.models import Retrospective, User
from core.forms import (
  LearnedForm, FailedForm, SuccessForm, RetrospectiveGeneralForm)


def index(request):
    context = {"info": "Hello!"}
    return render(request, 'core/index.html', context)


def introduction(request):
  return render(request, 'core/introduction.html')


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

 
def finish_creation(request):
    r_id = request.session['retrospective_id']
    retrospective = Retrospective.objects.get(id=r_id)
    context = {"username": "me",
               "retrospective": retrospective}

    return render(request, 'core/finish_creation.html', context)

def thanks(request):
    request.session.pop('retrospective_id')
    return render(request, 'core/thanks.html')