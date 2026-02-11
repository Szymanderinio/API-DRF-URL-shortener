import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shortener.models import ShortenedURL


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.mark.django_db
class TestURLShortenerE2E:
    def test_full_shorten_and_expand_flow(self, api_client: APIClient) -> None:
        original_url = "https://example.com/very/long/path/to/resource?param=value"

        shorten_response = api_client.post(
            reverse('shorten'),
            {'url': original_url},
            format='json'
        )
        assert shorten_response.status_code == status.HTTP_201_CREATED
        short_code = shorten_response.data['short_code']
        assert short_code is not None

        expand_response = api_client.get(
            reverse('expand', kwargs={'short_code': short_code})
        )
        assert expand_response.status_code == status.HTTP_200_OK
        assert expand_response.data['original_url'] == original_url

        redirect_response = api_client.get(
            reverse('redirect', kwargs={'short_code': short_code})
        )
        assert redirect_response.status_code == status.HTTP_302_FOUND
        assert redirect_response.url == original_url

    def test_multiple_urls_independent(self, api_client: APIClient) -> None:
        urls = [
            "https://example.com/page1",
            "https://example.com/page2",
            "https://example.com/page3",
        ]

        short_codes = []
        for url in urls:
            response = api_client.post(
                reverse('shorten'),
                {'url': url},
                format='json'
            )
            assert response.status_code == status.HTTP_201_CREATED
            short_codes.append(response.data['short_code'])

        assert len(set(short_codes)) == len(urls)

        for url, code in zip(urls, short_codes):
            response = api_client.get(
                reverse('expand', kwargs={'short_code': code})
            )
            assert response.data['original_url'] == url

    def test_same_url_returns_same_code(self, api_client: APIClient) -> None:
        url = "https://example.com/same/url"

        response1 = api_client.post(
            reverse('shorten'),
            {'url': url},
            format='json'
        )
        response2 = api_client.post(
            reverse('shorten'),
            {'url': url},
            format='json'
        )

        assert response1.status_code == status.HTTP_201_CREATED
        assert response2.status_code == status.HTTP_201_CREATED
        assert response1.data['short_code'] == response2.data['short_code']

    def test_database_persistence(self, api_client: APIClient) -> None:
        url = "https://example.com/persistent"

        response = api_client.post(
            reverse('shorten'),
            {'url': url},
            format='json'
        )
        short_code = response.data['short_code']

        assert ShortenedURL.objects.filter(short_code=short_code).exists()
        db_entry = ShortenedURL.objects.get(short_code=short_code)
        assert db_entry.original_url == url

    def test_error_handling_invalid_short_code(self, api_client: APIClient) -> None:
        expand_response = api_client.get(
            reverse('expand', kwargs={'short_code': 'INVALID'})
        )
        assert expand_response.status_code == status.HTTP_404_NOT_FOUND

        redirect_response = api_client.get(
            reverse('redirect', kwargs={'short_code': 'INVALID'})
        )
        assert redirect_response.status_code == status.HTTP_404_NOT_FOUND

    def test_special_characters_in_url(self, api_client: APIClient) -> None:
        special_url = "https://example.com/path?query=value&other=123#section"

        response = api_client.post(
            reverse('shorten'),
            {'url': special_url},
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED

        expand_response = api_client.get(
            reverse('expand', kwargs={'short_code': response.data['short_code']})
        )
        assert expand_response.data['original_url'] == special_url
