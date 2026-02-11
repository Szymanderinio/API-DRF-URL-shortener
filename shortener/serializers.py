from rest_framework import serializers

from .models import ShortenedURL


class ShortenURLSerializer(serializers.Serializer):
    url = serializers.URLField()


class ShortenedURLResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['short_code', 'original_url', 'created_at']
        read_only_fields = ['short_code', 'created_at']


class ExpandURLResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ['original_url', 'short_code']
