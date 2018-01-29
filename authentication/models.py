import jwt

from datetime import datetime, timedelta

from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager, PermissionsMixin
)

from core.models import TimestampedModel
from core.validators import validate_core_email

from .managers import UserManager
from .utils import jwt_encode_handler


def avatar_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = f'{uuid4()}.{ext.lower()}'
	return os.path.join('profiles/', str(instance.pk), filename)

class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
	email = models.EmailField(
		db_index=True,
		unique=True,
		validators=[validate_core_email]
	)

	first_name = models.CharField(max_length=100, null=True, blank=True)
	last_name = models.CharField(max_length=100, null=True, blank=True)
	
	avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True)

	phone_regex = RegexValidator(
		regex=r'^[0-9]{10}$',
		message="Please insert a valid number"
	)

	gsm = models.CharField(
		"Phone number",
		validators=[phone_regex],
		max_length=10,
		db_index=True,
		null=True,
		blank=True
	)
	
	bio = models.TextField(blank=True)
	address = models.TextField(blank=True)

	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	@property
	def token(self):
		return self._generate_jwt_token()

	def get_full_name(self):
		return f"{self.first_name} {self.last_name}"

	def get_short_name(self):
		return self.first_name

	def _generate_jwt_token(self):
		dt = datetime.now() + timedelta(days=60)
		payload = {
			'id': self.pk,
			'exp': int(dt.strftime('%s'))
		}
		return jwt_encode_handler(payload)