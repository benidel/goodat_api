from django.contrib.auth import authenticate

from rest_framework import serializers

from profiles.serializers import SkillSerializer

from profiles.models import Skill
from .models import Offer


class OfferSerializer(serializers.ModelSerializer):
	required_skills = SkillSerializer(many=True, read_only=True)
	required_skills_pk = serializers.PrimaryKeyRelatedField(
		source="skill",
		queryset=Skill.objects.all(),
		write_only=True,
		many=True
	)

	class Meta:
		model = Offer
		fields = (
			'title', 
			'required_skills', 
			'required_skills_pk',
			'service_value', 
			'description',
			'exp_date'
		)

	def update(self, instance, validated_data):
		required_skills = validated_data.pop("skill", [])
		instance = super(OfferSerializer, self).update(instance, validated_data)

		instance.required_skills.clear()
		instance.required_skills.add(*required_skills)

		instance.save()

		return instance

	def create(self, validated_data):
		required_skills = validated_data.pop("skill", [])
		instance = super(OfferSerializer, self).create(validated_data)

		instance.required_skills.add(*required_skills)

		instance.save()

		return instance