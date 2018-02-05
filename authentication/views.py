from datetime import datetime
import pytz

from django.shortcuts import HttpResponse, get_object_or_404

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Token

from .serializers import (
	LoginSerializer, RegistrationSerializer, UserSerializer
)
from .renderers import UserJSONRenderer


class RegistrationAPIView(APIView):
	permission_classes = (AllowAny,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = RegistrationSerializer

	def post(self, request):
		user = request.data.get('user', {})
		
		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserActivationAPIView(APIView):
	permission_classes = (AllowAny,)

	def get(self, request):
		token = request.GET.get('token')

		if token is None:
			return HttpResponse("404")

		token = get_object_or_404(Token, token=token)
		user = token.user

		if user.is_active:
			return HttpResponse("Already activate")

		if datetime.now(pytz.UTC) > token.date_end:
			return HttpResponse("Token has expired")

		user.is_active = True
		user.save()

		return HttpResponse("Successfuly activated")


class LoginAPIView(APIView):
	permission_classes = (AllowAny,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = LoginSerializer

	def post(self, request):
		user = request.data.get('user', {})
		if not user:
			user['email'] = request.data.get('email')
			user['password'] = request.data.get('password')

		serializer = self.serializer_class(data=user)
		serializer.is_valid(raise_exception=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
	permission_classes = (IsAuthenticated,)
	renderer_classes = (UserJSONRenderer,)
	serializer_class = UserSerializer

	def retrieve(self, request, *args, **kwargs):
		serializer = self.serializer_class(request.user)

		return Response(serializer.data, status=status.HTTP_200_OK)

	def update(self, request, *args, **kwargs):
		data = request.data.get('data', {})
		user_data = data.get('user', {})

		profile = request.user.profile

		serializer_data = {
			'password': user_data.get('password', request.user.password),
			'first_name': user_data.get('first_name', request.user.first_name),
			'last_name': user_data.get('last_name', request.user.last_name),
			'bio': user_data.get('bio', request.user.bio),
			'gsm': user_data.get('gsm', request.user.gsm),

			'profile': {
				'skills': user_data.get('skills', profile.skills)
			}
		}

		serializer = self.serializer_class(
			request.user, data=serializer_data, partial=True
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)