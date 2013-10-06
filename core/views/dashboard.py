from django.shortcuts import render
from core.models import Retrospective, User, Project
from django.contrib.auth.decorators import login_required
from mailing.models import MailConfiguration, BasicMailConfigurationForm



def discard_broken_retrospectives(user):
    for retrospective in Retrospective.objects.filter(user=user):
        if retrospective.is_invalid():
            retrospective.delete()


@login_required()
def profile_dashboard(request):
    if 'retrospective_id' in request.session:
        request.session.pop('retrospective_id')
    user = request.user
    discard_broken_retrospectives(user)
    current_projects = Project.objects.filter(user=user)
    retrospectives = Retrospective.objects.filter(user=user)
    try:
        mailing_configuration = MailConfiguration.objects.get(user=user)
    except MailConfiguration.DoesNotExist:
        mailing_configuration = None

    context = {
        "username": user.username,
        "email": user.email,
        "projects": current_projects,
        "retrospectives": retrospectives,
        "mailing_configuration": mailing_configuration,
    }
    return render(request, 'core/dashboard.html', context)


