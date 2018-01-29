import uuid
from datetime import datetime, timedelta

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string

from .models import Token


class TokenGenerator(object):
	"""
	Generates a token for user registration
	"""

	def generate_token(self, user, token_type=1):
		uuid_token = str(uuid.uuid4())
		date_end = datetime.now() + timedelta(hours=1)
		token = Token(user=user, token=uuid_token,
			date_end=date_end, token_type=token_type)
		token.save()
		return token

	def send_email(self, token, user):
		subject = 'Goodat - Confirmation mail'
		global_conf = settings.GOODAT_APP['global']
		from_email = f"{global_conf['litteral_name']} <{global_conf['email_noreply']}>"

		context = {
			'full_name': user.get_full_name(),
			'url': global_conf['url'] + token.get_registration_url(),
			'site_name': global_conf['litteral_name'],
			'site_url': global_conf['url']
		}
		message_html = render_to_string('email/confirm_registration.html', context)
		message_txt = render_to_string('email/confirm_registration.txt', context)

		msg = EmailMultiAlternatives(subject, message_txt, from_email, [user.email])
		msg.attach_alternative(message_html, 'text/html')
		try:
			msg.send()
		except Exception:
			pass
