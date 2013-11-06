from core.models import (
	Retrospective, Project, LearnedEntry, SuccessEntry, FailedEntry
)
from collections import Counter


def number_of_retrospectives_per_month(retrospectives):
	number_per_month = Counter()
	for retrospective in retrospectives:
		number_per_month[retrospective.created.month] += 1
	for x in range(12):
		if x not in number_per_month:
			number_per_month[x] = 0

	return number_per_month

def number_of_retrospectives_per_weekday(retrospectives):
	number_per_weekday = Counter()
	for retrospective in retrospectives:
		number_per_weekday[retrospective.created.weekday()] += 1
	for x in range(7):
		if x not in number_per_weekday:
			number_per_weekday[x] = 0
	return number_per_weekday

def get_data_about_retrospective_frequency(user):
	retrospectives = Retrospective.objects.filter(user=user)
	data = {
		"count": retrospectives.count(),
		"number_per_month": number_of_retrospectives_per_month(retrospectives),
		"number_per_weekday": number_of_retrospectives_per_weekday(retrospectives),

	}
	return data

def get_data_about_retrospective_content(user):
	retrospectives = Retrospective.objects.filter(user=user)
	learned_entries = Counter()
	failed_entries = Counter()
	succeeded_entries = Counter()

	for retrospective in retrospectives:
		learned_entries[retrospective.learnedentry_set.count()] += 1
		succeeded_entries[retrospective.successentry_set.count()] += 1
		failed_entries[retrospective.failedentry_set.count()] += 1

	for x in range(5):
		if x not in learned_entries:
			learned_entries[x] = 0

	for x in range(5):
		if x not in failed_entries:
			failed_entries[x] = 0

	for x in range(5):
		if x not in succeeded_entries:
			succeeded_entries[x] = 0

	return {
		"learned": learned_entries,
		"failed": failed_entries,
		"succeeded": succeeded_entries,
	}

def get_data_about_projects(user):
	projects = Project.objects.filter(user=user)
	projects_data = {}
	for project in projects:
		failed = FailedEntry.objects.filter(project=project).count()
		succeeded = SuccessEntry.objects.filter(project=project).count()
		projects_data[project.title] = {
			'failed': failed if failed is not None else 0,
			'succeeded': succeeded if succeeded is not None else 0
		}

	return projects_data

