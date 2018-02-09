from django.urls import path

from .views import (
	OfferRetrieveUpdateDeleteAPIView,
	OfferListCreateAPIView
)

app_name = 'offer'

urlpatterns = [
	path('offer/<int:pk>/', OfferRetrieveUpdateDeleteAPIView.as_view(), name="detail"),
	path('offers/', OfferListCreateAPIView.as_view()),
]