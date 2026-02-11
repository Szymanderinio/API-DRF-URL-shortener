import hashlib


def generate_short_code(url: str, length: int = 6) -> str:
    url_hash = hashlib.sha256(url.encode()).hexdigest()
    return url_hash[:length]
