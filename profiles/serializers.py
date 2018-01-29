from rest_framework import serializers

from .models import (
	Skill,
	Degree,
	ProfileSkill,
	Profile
)


class SkillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Skill
		fields = ('name', )


class DegreeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Degree
		fields = ('title', 'delivery_date')


class ProfileSkillSerializer(serializers.ModelSerializer):
	skill = SkillSerializer()

	class Meta:
		model = ProfileSkill
		fields = ('skill', 'level')

class ProfileSerializer(serializers.ModelSerializer):
	skills = SkillSerializer(many=True)
	degrees = DegreeSerializer(many=True)

	class Meta:
		model = Profile
		fields = ('skills', 'degrees', 'profession')
