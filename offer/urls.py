from django.urls import path

from .views import (
	OfferRetrieveUpdateDeleteAPIView,
	RegisterOfferAPIView
)

app_name = 'offer'

urlpatterns = [
	path('offer/<int:pk>', OfferRetrieveUpdateDeleteAPIView.as_view(), name="detail"),
	path('offers/', RegisterOfferAPIView.as_view()),
]