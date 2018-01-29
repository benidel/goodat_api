from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


class TimestampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True
		ordering = ('-created_at', '-updated_at')


class Token(models.Model):
	TOKEN_CHOICES = (
		(1, 'registration'),
	)

	user = models.ForeignKey(
		get_user_model(),
		on_delete=models.CASCADE,
		db_index=True
	)

	token = models.CharField(max_length=100, db_index=True)
	date_end = models.DateTimeField()
	token_type = models.PositiveSmallIntegerField(
		choices=TOKEN_CHOICES,
		default=1
	)

	def get_absolute_url(self):
		if token_type == 1:
			return self.get_registration_url()

	def get_registration_url(self):
		return f'{reverse("authentication:activate")}?token={self.token}'

	def __str__(self):
		return f'{self.user} - {self.date_end}'


