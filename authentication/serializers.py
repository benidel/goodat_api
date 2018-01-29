from django.contrib.auth import authenticate

from rest_framework import serializers

from core.utils import TokenGenerator

from profiles.serializers import (
	ProfileSerializer,
	DegreeSerializer,
	ProfileSkillSerializer
)

from .models import User


class RegistrationSerializer(serializers.ModelSerializer, TokenGenerator):

	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True
	)

	class Meta:
		model = User
		fields = ('email', 'password')

	def create(self, validated_data):
		user = User.objects.create_user(**validated_data)
		# Create registration token and send activation link
		token = self.generate_token(user)
		self.send_email(token, user)
		return user


class LoginSerializer(serializers.Serializer):
	email = serializers.CharField(max_length=255)
	password = serializers.CharField(max_length=128, write_only=True)
	token = serializers.CharField(max_length=255, read_only=True)

	def validate(self, data):
		email = data.get('email', None)
		password = data.get('password', None)

		if email is None:
			raise serializers.ValidationError(
				'An email address is required to log in.'
			)

		if password is None:
			raise serializers.ValidationError(
				'A password is required to log in.'
			)

		user = authenticate(username=email, password=password)

		if user is None:
			raise serializers.ValidationError(
				'A user with this email and password was not found.'
			)

		if not user.is_active:
			raise serializers.ValidationError(
				'This user has been deactivated.'
			)

		return {
			'email': user.email,
			'token': user.token
		}


class UserSerializer(serializers.ModelSerializer):
	profile = ProfileSerializer(write_only=True)
	
	skills = ProfileSkillSerializer(source='profile.skills', many=True)

	password = serializers.CharField(
		max_length=128,
		min_length=8,
		write_only=True
	)

	class Meta:
		model = User
		fields = (
			'password', 'first_name', 'last_name', 
			'bio', 'avatar', 'gsm', 'skills', 'profile'
		)

	def update(self, instance, validated_data):
		password = validated_data.pop('password', None)

		for key, value in validated_data.items():
			setattr(instance, key, value)

		if password is not None:
			instance.set_password(password)

		profile_data = validated_data.pop('profile')
		

		instance.save()

		return instance

