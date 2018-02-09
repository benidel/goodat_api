from django.shortcuts import render, HttpResponse, get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .renderers import OfferJSONRenderer

from .serializers import OfferSerializer
from .models import Offer


class OfferRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
	permission_classes = (IsAuthenticated,)
	renderer_classes = (OfferJSONRenderer,)
	serializer_class = OfferSerializer
	queryset = Offer.objects.all()

	def update(self, request, *args, **kwargs):
		offer_data = request.data.get('offer', {})
		offer = Offer.objects.get(pk=kwargs["pk"])
		serializer_data = {
			'title': offer_data.get('title', offer.title),
			'required_skills': offer_data.get('required_skills', offer.required_skills),
			'service_value': offer_data.get('service_value', offer.service_value),
			'description': offer_data.get('description', offer.description),
			'exp_date': offer_data.get('exp_date', offer.exp_date),
		}

		serializer = self.serializer_class(
			offer, data=serializer_data, partial=True
		)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_200_OK)


class ListCreateOfferAPIView(ListCreateAPIView):
	permission_classes = (IsAuthenticated,)
	renderer_classes = (OfferJSONRenderer,)
	serializer_class = OfferSerializer
	queryset = Offer.objects.all()

	def create(self, request, *args, **kwargs):
		print("AAAA")
		data = request.data.get('data', {})
		offer = data.get('offer', {})
		serializer = self.serializer_class(data=offer)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		return Response(serializer.data, status=status.HTTP_201_CREATED)
