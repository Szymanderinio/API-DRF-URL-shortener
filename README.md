# URL Shortener API

Minimalistyczne API do skracania URLi w Django REST Framework.

## Instalacja

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export SECRET_KEY="your-secret-key"
python manage.py migrate
python manage.py runserver
```

## API

| Metoda | Endpoint | Opis |
|--------|----------|------|
| POST | `/api/shorten/` | Skraca URL |
| GET | `/api/expand/<code>/` | Zwraca oryginalny URL |
| GET | `/s/<code>/` | Przekierowanie 302 |

### Przykład

```bash
# Skrócenie URL
curl -X POST http://localhost:8000/api/shorten/ \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/very/long/url"}'

# Response: {"short_code": "abc123", "original_url": "...", "created_at": "..."}

# Rozwinięcie
curl http://localhost:8000/api/expand/abc123/

# Przekierowanie
curl -L http://localhost:8000/s/abc123/
```

## Testy

```bash
pytest
```
