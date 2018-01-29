from django.db import models

from django.contrib.auth import get_user_model

from core.models import TimestampedModel

User = get_user_model()

class Profile(TimestampedModel):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	skills = models.ManyToManyField('ProfileSkill', blank=True)
	degrees = models.ManyToManyField('Degree', blank=True)
	profession = models.CharField(max_length=150, null=True, blank=True)

	@property
	def full_name(self):
		return self.user.get_full_name()

	def __str__(self):
		return self.full_name


class ProfileSkill(TimestampedModel):
	LEVEL_CHOICES = (
		(1, 'Beginner'),
		(2, 'Intermediate'),
		(3, 'Expert')
	)
	skill = models.ForeignKey('Skill', on_delete=models.CASCADE)
	level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES)

	def __str__(self):
		return f"{self.skill} : {self.get_level_display()}"


class Skill(TimestampedModel):
	name = models.CharField(max_length=150)

	def __str__(self):
		return self.name


class Degree(TimestampedModel):
	title = models.CharField(max_length=200)
	delivery_date = models.DateField()

	def __str__(self):
		return f'{self.title} {self.delivery_date}'
