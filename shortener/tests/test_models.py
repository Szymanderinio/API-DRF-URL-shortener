import pytest

from shortener.models import ShortenedURL
from shortener.utils import generate_short_code


@pytest.mark.django_db
class TestShortenedURLModel:
    def test_create_shortened_url(self) -> None:
        url = ShortenedURL.objects.create(original_url="https://example.com/very/long/url")

        assert url.short_code is not None
        assert len(url.short_code) == 6
        assert url.original_url == "https://example.com/very/long/url"

    def test_short_code_is_deterministic(self) -> None:
        url1 = ShortenedURL(original_url="https://example.com/test")
        url1.save()

        expected_code = generate_short_code("https://example.com/test")
        assert url1.short_code == expected_code

    def test_different_urls_get_different_codes(self) -> None:
        url1 = ShortenedURL.objects.create(original_url="https://example.com/1")
        url2 = ShortenedURL.objects.create(original_url="https://example.com/2")

        assert url1.short_code != url2.short_code

    def test_short_code_not_overwritten(self) -> None:
        url = ShortenedURL.objects.create(original_url="https://example.com")
        original_code = url.short_code

        url.original_url = "https://example.com/updated"
        url.save()

        assert url.short_code == original_code

    def test_str_representation(self) -> None:
        url = ShortenedURL.objects.create(original_url="https://example.com/test")

        assert url.short_code in str(url)
        assert "https://example.com/test" in str(url)


class TestGenerateShortCode:
    def test_default_length(self) -> None:
        code = generate_short_code("https://example.com")
        assert len(code) == 6

    def test_custom_length(self) -> None:
        code = generate_short_code("https://example.com", length=10)
        assert len(code) == 10

    def test_deterministic(self) -> None:
        url = "https://example.com/test"
        code1 = generate_short_code(url)
        code2 = generate_short_code(url)
        assert code1 == code2

    def test_different_urls_different_codes(self) -> None:
        code1 = generate_short_code("https://example.com/1")
        code2 = generate_short_code("https://example.com/2")
        assert code1 != code2
