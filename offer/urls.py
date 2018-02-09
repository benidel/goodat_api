from django.urls import path

from .views import (
	OfferRetrieveUpdateDeleteAPIView,
	ListCreateOfferAPIView
)

app_name = 'offer'

urlpatterns = [
	path('offer/<int:pk>/', OfferRetrieveUpdateDeleteAPIView.as_view(), name="detail"),
	path('offers/', ListCreateOfferAPIView.as_view()),
]