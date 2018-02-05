from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# from authentication.models import User
from profiles.models import Skill
# Create your models here.

User = get_user_model()

class Offer(models.Model):
	title = models.CharField(max_length = 250)
	required_skills = models.ManyToManyField(Skill, blank=True)
	service_value = models.PositiveSmallIntegerField(default=0)
	description = models.TextField(blank=True, null=True)
	exp_date = models.DateField()

	interested_profiles = models.ManyToManyField(User, blank=True, related_name="applied_offers")

	#choosen profile for the service
	choosen_profile = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="approuved_offers")

	def __str__(self):
		return f'{self.title}'

	def get_absolute_url(self):
		return reverse('offer:detail', kwargs={'id':self.id})


# class Link(models.Model):
#     offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
#     candidate = models.ForeignKey(User, on_delete=models.CASCADE)