import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shortener.models import ShortenedURL


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def shortened_url() -> ShortenedURL:
    return ShortenedURL.objects.create(original_url="https://example.com/test")


@pytest.mark.django_db
class TestShortenURLView:
    def test_shorten_url_success(self, api_client: APIClient) -> None:
        response = api_client.post(
            reverse('shorten'),
            {'url': 'https://example.com/very/long/url'},
            format='json'
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert 'short_code' in response.data
        assert 'original_url' in response.data
        assert response.data['original_url'] == 'https://example.com/very/long/url'
        assert len(response.data['short_code']) == 6

    def test_shorten_url_invalid_url(self, api_client: APIClient) -> None:
        response = api_client.post(
            reverse('shorten'),
            {'url': 'not-a-valid-url'},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_shorten_url_missing_url(self, api_client: APIClient) -> None:
        response = api_client.post(
            reverse('shorten'),
            {},
            format='json'
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
class TestExpandURLView:
    def test_expand_url_success(self, api_client: APIClient, shortened_url: ShortenedURL) -> None:
        response = api_client.get(
            reverse('expand', kwargs={'short_code': shortened_url.short_code})
        )

        assert response.status_code == status.HTTP_200_OK
        assert response.data['original_url'] == 'https://example.com/test'
        assert response.data['short_code'] == shortened_url.short_code

    def test_expand_url_not_found(self, api_client: APIClient) -> None:
        response = api_client.get(
            reverse('expand', kwargs={'short_code': 'nonexistent'})
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
class TestRedirectView:
    def test_redirect_success(self, api_client: APIClient, shortened_url: ShortenedURL) -> None:
        response = api_client.get(
            reverse('redirect', kwargs={'short_code': shortened_url.short_code})
        )

        assert response.status_code == status.HTTP_302_FOUND
        assert response.url == 'https://example.com/test'

    def test_redirect_not_found(self, api_client: APIClient) -> None:
        response = api_client.get(
            reverse('redirect', kwargs={'short_code': 'nonexistent'})
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
