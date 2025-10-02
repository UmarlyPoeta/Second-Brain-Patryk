# 📮 HTTP Metody i Kody Statusu

## 🔧 Metody HTTP

### GET - Pobieranie Zasobów
```http
GET /api/users HTTP/1.1
Host: example.com

Cechy:
✓ Idempotentna (wielokrotne wywołanie = ten sam efekt)
✓ Bezpieczna (nie modyfikuje stanu)
✓ Może być cachowana
✓ Parametry w URL (query string)
```

**Przykłady:**
```http
# Lista zasobów
GET /api/users?page=1&limit=20

# Konkretny zasób
GET /api/users/123

# Zagnieżdżone zasoby
GET /api/users/123/posts

# Filtrowanie
GET /api/products?category=electronics&price_min=100
```

### POST - Tworzenie Zasobów
```http
POST /api/users HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "name": "Jan Kowalski",
  "email": "jan@example.com"
}

Cechy:
✗ NIE jest idempotentna (każde wywołanie tworzy nowy zasób)
✗ NIE jest bezpieczna
✗ NIE jest cachowana
✓ Dane w body requestu
```

**Przykłady:**
```http
# Tworzenie użytkownika
POST /api/users
Body: {"name": "Jan", "email": "jan@example.com"}

# Upload pliku
POST /api/files
Content-Type: multipart/form-data

# Operacja niestandardowa
POST /api/users/123/send-email
Body: {"subject": "Welcome", "body": "..."}
```

### PUT - Pełna Aktualizacja
```http
PUT /api/users/123 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "name": "Jan Kowalski",
  "email": "jan.kowalski@example.com",
  "phone": "+48123456789"
}

Cechy:
✓ Idempotentna
✗ NIE jest bezpieczna
✓ Zastępuje cały zasób
```

**Różnica PUT vs POST:**
```http
# PUT - znamy ID, zastępujemy cały zasób
PUT /api/users/123
Body: {całe dane użytkownika}

# POST - tworzymy nowy zasób, ID przydziela serwer
POST /api/users
Body: {dane nowego użytkownika}
```

### PATCH - Częściowa Aktualizacja
```http
PATCH /api/users/123 HTTP/1.1
Host: example.com
Content-Type: application/json

{
  "email": "new.email@example.com"
}

Cechy:
✓ Idempotentna (zazwyczaj)
✗ NIE jest bezpieczna
✓ Aktualizuje tylko podane pola
```

**PUT vs PATCH:**
```json
// Obecny stan użytkownika
{
  "id": 123,
  "name": "Jan",
  "email": "jan@example.com",
  "phone": "+48111222333"
}

// PUT - musimy wysłać WSZYSTKO
PUT /api/users/123
{
  "name": "Jan",
  "email": "newemail@example.com",
  "phone": "+48111222333"
}

// PATCH - tylko zmienione pola
PATCH /api/users/123
{
  "email": "newemail@example.com"
}
```

### DELETE - Usuwanie Zasobów
```http
DELETE /api/users/123 HTTP/1.1
Host: example.com

Cechy:
✓ Idempotentna
✗ NIE jest bezpieczna
✓ Zazwyczaj bez body
```

**Przykłady:**
```http
# Usunięcie pojedynczego zasobu
DELETE /api/users/123

# Usunięcie z warunkiem (w query lub header)
DELETE /api/users/123?confirm=true

# Soft delete (wymaga POST lub PATCH)
PATCH /api/users/123
Body: {"deleted": true}
```

### HEAD - Metadane Zasobu
```http
HEAD /api/users/123 HTTP/1.1
Host: example.com

Response:
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 1234
Last-Modified: Mon, 15 Jan 2024 10:00:00 GMT
ETag: "abc123"

(brak body)

Cechy:
✓ Jak GET ale bez body
✓ Sprawdzenie istnienia zasobu
✓ Pobranie metadanych
```

### OPTIONS - Dostępne Metody
```http
OPTIONS /api/users/123 HTTP/1.1
Host: example.com

Response:
HTTP/1.1 200 OK
Allow: GET, PUT, PATCH, DELETE
Access-Control-Allow-Methods: GET, PUT, PATCH, DELETE
Access-Control-Allow-Origin: *

Cechy:
✓ Preflight request dla CORS
✓ Discovery dostępnych metod
```

## 📊 Kody Statusu HTTP

### 2xx - Sukces

#### 200 OK
```http
GET /api/users/123
Response: 200 OK
Body: {dane użytkownika}

Użycie: Operacja zakończona sukcesem (GET, PUT, PATCH)
```

#### 201 Created
```http
POST /api/users
Response: 201 Created
Location: /api/users/456
Body: {nowo utworzony użytkownik}

Użycie: Zasób został utworzony
```

#### 202 Accepted
```http
POST /api/long-running-task
Response: 202 Accepted
Body: {"status": "processing", "task_id": "abc123"}

Użycie: Żądanie przyjęte do przetwarzania (asynchroniczne)
```

#### 204 No Content
```http
DELETE /api/users/123
Response: 204 No Content

Użycie: Sukces bez zwracanej treści (DELETE, niektóre PUT)
```

### 3xx - Przekierowania

#### 301 Moved Permanently
```http
GET /api/v1/users/123
Response: 301 Moved Permanently
Location: /api/v2/users/123

Użycie: Zasób przeniesiony na stałe
```

#### 304 Not Modified
```http
GET /api/users/123
If-None-Match: "abc123"

Response: 304 Not Modified

Użycie: Zasób nie zmienił się od ostatniego pobrania (cache)
```

### 4xx - Błędy Klienta

#### 400 Bad Request
```http
POST /api/users
Body: {niepoprawne dane}

Response: 400 Bad Request
Body: {
  "error": "Validation failed",
  "details": [
    {"field": "email", "message": "Invalid email format"}
  ]
}

Użycie: Błędna składnia lub walidacja
```

#### 401 Unauthorized
```http
GET /api/users/123

Response: 401 Unauthorized
WWW-Authenticate: Bearer

Body: {"error": "Authentication required"}

Użycie: Brak lub nieprawidłowa autentykacja
```

#### 403 Forbidden
```http
DELETE /api/users/123
Authorization: Bearer {token}

Response: 403 Forbidden
Body: {"error": "Insufficient permissions"}

Użycie: Brak uprawnień (authenticated ale nie authorized)
```

#### 404 Not Found
```http
GET /api/users/999999

Response: 404 Not Found
Body: {"error": "User not found"}

Użycie: Zasób nie istnieje
```

#### 405 Method Not Allowed
```http
POST /api/users/123

Response: 405 Method Not Allowed
Allow: GET, PUT, PATCH, DELETE

Użycie: Metoda HTTP nie jest dozwolona dla tego zasobu
```

#### 409 Conflict
```http
POST /api/users
Body: {"email": "existing@example.com"}

Response: 409 Conflict
Body: {"error": "User with this email already exists"}

Użycie: Konflikt ze stanem zasobu (duplikat)
```

#### 422 Unprocessable Entity
```http
POST /api/users
Body: {"name": "", "email": "invalid"}

Response: 422 Unprocessable Entity
Body: {
  "errors": {
    "name": ["Name is required"],
    "email": ["Email format is invalid"]
  }
}

Użycie: Błędy walidacji biznesowej (poprawny JSON ale niepoprawne dane)
```

#### 429 Too Many Requests
```http
GET /api/users

Response: 429 Too Many Requests
Retry-After: 60

Body: {"error": "Rate limit exceeded. Try again in 60 seconds."}

Użycie: Przekroczony limit żądań (rate limiting)
```

### 5xx - Błędy Serwera

#### 500 Internal Server Error
```http
GET /api/users/123

Response: 500 Internal Server Error
Body: {"error": "An unexpected error occurred"}

Użycie: Nieobsłużony błąd po stronie serwera
```

#### 502 Bad Gateway
```http
GET /api/users/123

Response: 502 Bad Gateway

Użycie: Błąd komunikacji między serwerami (proxy, gateway)
```

#### 503 Service Unavailable
```http
GET /api/users/123

Response: 503 Service Unavailable
Retry-After: 300

Użycie: Serwis tymczasowo niedostępny (maintenance, overload)
```

## 📋 Tabela Metod HTTP

| Metoda  | Idempotentna | Bezpieczna | Cacheable | Typowy Status |
|---------|-------------|-----------|-----------|---------------|
| GET     | ✅          | ✅        | ✅        | 200           |
| POST    | ❌          | ❌        | ❌        | 201           |
| PUT     | ✅          | ❌        | ❌        | 200           |
| PATCH   | ✅*         | ❌        | ❌        | 200           |
| DELETE  | ✅          | ❌        | ❌        | 204           |
| HEAD    | ✅          | ✅        | ✅        | 200           |
| OPTIONS | ✅          | ✅        | ❌        | 200           |

*PATCH może nie być idempotentna w zależności od implementacji

## 🎯 Best Practices

```
✅ Używaj odpowiednich metod HTTP
✅ Zwracaj właściwe kody statusu
✅ GET i HEAD muszą być bezpieczne
✅ PUT, DELETE muszą być idempotentne
✅ Używaj 4xx dla błędów klienta, 5xx dla błędów serwera
✅ Zawsze zwracaj szczegóły błędu w body
✅ Używaj Location header dla 201 Created
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[Error Handling API|⚠️ Error Handling]]
- [[Rate Limiting i Throttling|⏱️ Rate Limiting]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~12 minut*

#http #rest #status-codes #http-methods #api
