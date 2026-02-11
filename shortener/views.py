from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import (
    ExpandURLResponseSerializer,
    ShortenedURLResponseSerializer,
    ShortenURLSerializer,
)


class ShortenURLView(APIView):
    def post(self, request: Request) -> Response:
        serializer = ShortenURLSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        shortened_url = ShortenedURL.objects.create(
            original_url=serializer.validated_data['url']
        )

        response_serializer = ShortenedURLResponseSerializer(shortened_url)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class ExpandURLView(APIView):
    def get(self, request: Request, short_code: str) -> Response:
        shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
        serializer = ExpandURLResponseSerializer(shortened_url)
        return Response(serializer.data)


class RedirectView(APIView):
    def get(self, request: Request, short_code: str) -> HttpResponseRedirect:
        shortened_url = get_object_or_404(ShortenedURL, short_code=short_code)
        return redirect(shortened_url.original_url)
