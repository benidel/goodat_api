from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from profiles.models import Skill

User = get_user_model()

class Offer(models.Model):
	title = models.CharField(max_length = 250)
	required_skills = models.ManyToManyField(Skill, blank=True)
	service_value = models.PositiveSmallIntegerField(default=0)
	description = models.TextField(blank=True, null=True)
	exp_date = models.DateField()

	interested_profiles = models.ManyToManyField(
		User,
		related_name="applied_offers",
		blank=True
	)

	# choosen profile for the service
	choosen_profile = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="approuved_offers",
		blank=True,
		null=True
	)

	def __str__(self):
		return f'{self.title}'

	def get_absolute_url(self):
		return reverse('offer:detail', kwargs={'id':self.id})

