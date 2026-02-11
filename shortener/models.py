from typing import Any

from django.db import models

from .utils import generate_short_code


class ShortenedURL(models.Model):
    original_url = models.TextField()
    short_code = models.CharField(max_length=8, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args: Any, **kwargs: Any) -> None:
        if not self.short_code:
            self.short_code = generate_short_code()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.short_code} -> {self.original_url[:50]}"
