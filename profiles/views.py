from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from core.renderers import CoreJSONRenderer
from .serializers import SkillSerializer
from .models import Skill


class SkillRetrieveAPIView(ListAPIView):
	serializer_class = SkillSerializer
	queryset = Skill.objects.all()
	premissions_classes = (IsAuthenticated, )
	renderers_classes = (CoreJSONRenderer, )










