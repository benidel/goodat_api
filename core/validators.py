import os

from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

from goodat.settings import BASE_DIR


class CoreEmailValidator(EmailValidator):

	def __call__(self, value):
		super(CoreEmailValidator, self).__call__(value)

		# check if provider is blacklisted 
		msg = f'The used provider ({value.split("@")[-1]}) is blacklisted, ' \
					'please try another one'
		with open(os.path.join(BASE_DIR, 'forbidden_email_providers.txt'), 'r') as black_list:
			for provider in black_list:
				if provider.strip() in value:
					raise ValidationError(msg, code=self.code)


validate_core_email = CoreEmailValidator()