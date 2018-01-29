import jwt

from django.conf import settings


def jwt_encode_handler(payload):
	return jwt.encode(
		payload,
		settings.SECRET_KEY,
		algorithm='HS256').decode('utf-8')
