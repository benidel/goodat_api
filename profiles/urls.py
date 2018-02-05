from django.urls import path

from .views import (
	SkillRetrieveAPIView,
)

app_name = 'profiles'

urlpatterns = [
	path('skills/', SkillRetrieveAPIView.as_view()),
]