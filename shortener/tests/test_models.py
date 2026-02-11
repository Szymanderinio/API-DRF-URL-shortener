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

    def test_short_code_is_unique(self) -> None:
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
        code = generate_short_code()
        assert len(code) == 6

    def test_custom_length(self) -> None:
        code = generate_short_code(length=10)
        assert len(code) == 10

    def test_alphanumeric_only(self) -> None:
        code = generate_short_code()
        assert code.isalnum()

    def test_uniqueness(self) -> None:
        codes = [generate_short_code() for _ in range(100)]
        assert len(set(codes)) == 100
