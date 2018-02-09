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
		print("DD", validated_data)
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
		required_skills = validated_data.pop("skill", [])
		instance = super(OfferSerializer, self).create(validated_data)

		instance.required_skills.add(*required_skills)

		instance.save()

		return instance