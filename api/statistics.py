from core.models import Retrospective
from collections import Counter


def number_of_retrospectives_per_month(retrospectives):
	number_per_month = Counter()
	for retrospective in retrospectives:
		number_per_month[retrospective.created.month] += 1
	for x in xrange(12):
		if x not in number_per_month:
			number_per_month[x] = 0

	return number_per_month

def number_of_retrospectives_per_weekday(retrospectives):
	number_per_weekday = Counter()
	for retrospective in retrospectives:
		number_per_weekday[retrospective.created.weekday()] += 1
	for x in xrange(7):
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
	return {"a": 3}

def get_data_about_projects(user):
	return {
		"project0": {
			"stuff": 1
		}
	}

