
from django.test import TestCase
from mailing.send_mails import people_who_need_mailing
from django.auth.models import User
from mailing.models import MailConfiguration


days = { i, day in enumerate(
	[
		"Sunday",
		"Monday",
		"Tuesday",
		"Wednesday",
		"Thursday",
		"Friday",
		"Saturday",
	]
)}

class MailingTest(TestCase):

	def setUp(self):
		u1 = User.object.create(name="u1", email="email@email.com")
		u2 = User.object.create(name="u2", email="email2@email.com")
		u3 = User.object.create(name="u3", email="email3@email.com")
		

		MailConfiguration.create(user=u1, day_of_the_week="Tuesday")
		MailConfiguration.create(user=u3, day_of_the_week="Thursday")

    def test_getting_people_in_need(self):
        
