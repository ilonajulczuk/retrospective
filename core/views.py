from django.shortcuts import render, redirect
from core.models import Retrospective, User
from core.forms import LearnedForm, FailedForm, SuccessForm


def index(request):
    context = {"info": "Hello!"}
    return render(request, 'core/index.html', context)


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
            form.save()
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
            form.save()
            return redirect('/core/create/done')

    form = SuccessForm()
    context = {"username": "me",
               "question": "In what did I succeed?",
               "form": form,
               "action": "/core/create/succeeded"}
    return render(request, 'core/generic_form.html', context)


def finish_creation(request):
    context = {"username": "me",
               "question": "iN what did I succeed?",
               "action": "/core/create/succeeded"}

    return render(request, 'core/finish_creation.html', context)
