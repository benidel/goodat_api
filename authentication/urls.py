from django.urls import path

from .views import (
	LoginAPIView,
	RegistrationAPIView,
	UserRetrieveUpdateAPIView,
	UserActivationAPIView,
)

app_name = 'authentication'

urlpatterns = [
	path('user/', UserRetrieveUpdateAPIView.as_view()),

	path('users/', RegistrationAPIView.as_view()),

	path('users/registration/activate/', UserActivationAPIView.as_view(), name="activate"),
	
	path('users/login/', LoginAPIView.as_view()),
]