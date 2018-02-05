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
		fields = ('pk', 'name', )
		read_only_fields = ('pk', )


class DegreeSerializer(serializers.ModelSerializer):
	class Meta:
		model = Degree
		fields = ('title', 'delivery_date')


class ProfileSkillSerializer(serializers.ModelSerializer):
	skill = SkillSerializer(read_only=True)
	skill_pk = serializers.PrimaryKeyRelatedField(
		source="skill",
		queryset=Skill.objects.all(),
		write_only=True
	)

	class Meta:
		model = ProfileSkill
		fields = ('skill', 'level', 'skill_pk')


class ProfileSerializer(serializers.ModelSerializer):
	skills = ProfileSkillSerializer(many=True)
	degrees = DegreeSerializer(many=True)

	class Meta:
		model = Profile
		fields = ('skills', 'degrees', 'profession')
