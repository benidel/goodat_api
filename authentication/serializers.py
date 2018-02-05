from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from core.utils import TokenGenerator

from profiles.serializers import (
	ProfileSerializer,
	DegreeSerializer,
	ProfileSkillSerializer
)
from profiles.models import Skill, ProfileSkill

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

		profile_data = validated_data.pop('profile', {})

		for key, value in validated_data.items():
			setattr(instance, key, value)

		if password is not None:
			instance.set_password(password)
		
		# skills indicate the profile skills
		profile_skills_data = profile_data.pop('skills', [])

		for key, value in profile_data.items():
			setattr(instance.profile, key, value)

		instance_skills = instance.profile.skills
		for profile_skill in profile_skills_data:
			skill = profile_skill.get('skill')
			if skill:
				try:
					instance_skill = instance_skills.get(skill=skill)
					level = profile_skill.get('level')
					if level:
						instance_skill.level = level
						instance_skill.save()
				except ProfileSkill.DoesNotExist:
					p_s = ProfileSkill(
						level=profile_skill.get('level'),
						skill=profile_skill.get('skill')
					)
					p_s.save()
					instance_skills.add(p_s)
		instance.profile.save()
		instance.save()

		return instance

