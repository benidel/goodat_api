from django.contrib.auth import authenticate

from rest_framework import serializers

from profiles.serializers import SkillSerializer

from profiles.models import Skill
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
	required_skills = SkillSerializer(many=True, required=False)

	class Meta:
		model = Offer
		fields = ('title', 'required_skills', 'service_value', 'description', 'exp_date')

	def update(self, instance, validated_data):
		required_skills_data = validated_data.pop("required_skills", [])
		for elem in validated_data:
			if instance._meta.get_field(elem):
				setattr(instance, elem, validated_data[elem])

		for skill in required_skills_data:
			if Skill.objects.filter(name__iexact=skill.name).exist():
				instance.required_skills.add(skill)

		instance.save()

		return instance

	def create(self, validated_data):
		required_skills_data = validated_data.pop("required_skills", [])
		instance = super(OfferSerializer, self).create(validated_data)

		skills = Skill.objects.filter(pk__in = required_skills_data)
		instance.required_skills.add(*skills)

		instance.save()

		return instance