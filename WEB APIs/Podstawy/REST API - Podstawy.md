# 🔰 REST API - Podstawy

## 📖 Definicja

**REST** (Representational State Transfer) to styl architektoniczny dla systemów rozproszonych, szczególnie aplikacji webowych. REST API wykorzystuje protokół HTTP do komunikacji między klientem a serwerem.

## 🎯 Kluczowe Zasady REST

### 1. Client-Server (Klient-Serwer)
```
Klient ← HTTP Request/Response → Serwer

Zalety:
✓ Niezależny rozwój
✓ Skalowalność
✓ Możliwość wielokrotnego użycia
```

### 2. Stateless (Bezstanowość)
```
Każde żądanie zawiera wszystkie potrzebne informacje

Request 1: GET /users/123 + Token
Request 2: POST /users + Token + Data
Request 3: DELETE /users/123 + Token

Serwer nie przechowuje stanu sesji!
```

### 3. Cacheable (Możliwość Cachowania)
```http
# Response z możliwością cachowania
HTTP/1.1 200 OK
Cache-Control: max-age=3600
ETag: "abc123"
Last-Modified: Mon, 15 Jan 2024 10:00:00 GMT
```

### 4. Uniform Interface (Jednolity Interfejs)
```
• Identyfikacja zasobów (URI)
• Manipulacja przez reprezentacje (JSON, XML)
• Samodokumentujące się komunikaty
• HATEOAS (Hypermedia As The Engine Of Application State)
```

### 5. Layered System (System Warstwowy)
```
Client → Load Balancer → API Gateway → Service → Database
       ↓               ↓              ↓
    Cache           Auth          Cache
```

### 6. Code on Demand (Opcjonalne)
```
Serwer może wysłać kod wykonywalny:
- JavaScript dla przeglądarki
- Aplets
- Plugins
```

## 🌐 Zasoby i URI

### Struktura URI
```
https://api.example.com/v1/users/123/orders/456

Komponenty:
- Protocol: https://
- Domain: api.example.com
- Version: /v1
- Resource: /users
- ID: /123
- Sub-resource: /orders
- Sub-ID: /456
```

### Dobre Praktyki URI
```
✅ DOBRZE:
GET /users           - lista użytkowników
GET /users/123       - konkretny użytkownik
GET /users/123/posts - posty użytkownika
POST /users          - tworzenie użytkownika

❌ ŹLE:
GET /getUsers
GET /user-123
POST /createNewUser
GET /users/delete/123
```

## 🔄 REST vs CRUD

```
REST Method    SQL Operation    HTTP Status
-----------------------------------------------
POST           INSERT          201 Created
GET            SELECT          200 OK
PUT            UPDATE          200 OK
PATCH          UPDATE          200 OK
DELETE         DELETE          204 No Content
```

## 📦 Reprezentacje Danych

### JSON (Najpopularniejszy)
```json
{
  "id": 123,
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "created_at": "2024-01-15T10:00:00Z",
  "roles": ["user", "admin"]
}
```

### XML
```xml
<?xml version="1.0" encoding="UTF-8"?>
<user>
    <id>123</id>
    <name>Jan Kowalski</name>
    <email>jan@example.com</email>
    <created_at>2024-01-15T10:00:00Z</created_at>
    <roles>
        <role>user</role>
        <role>admin</role>
    </roles>
</user>
```

## 🎨 Content Negotiation

```http
# Request
GET /users/123 HTTP/1.1
Host: api.example.com
Accept: application/json
Accept-Language: pl,en

# Response
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
Content-Language: pl
```

## 📊 Przykład REST API

### Operacje na Użytkownikach
```http
# Lista wszystkich użytkowników
GET /api/v1/users?page=1&limit=20
Response: 200 OK

# Pobranie konkretnego użytkownika
GET /api/v1/users/123
Response: 200 OK

# Utworzenie nowego użytkownika
POST /api/v1/users
Body: {"name": "Jan", "email": "jan@example.com"}
Response: 201 Created

# Pełna aktualizacja użytkownika
PUT /api/v1/users/123
Body: {"name": "Jan Kowalski", "email": "jan@example.com"}
Response: 200 OK

# Częściowa aktualizacja
PATCH /api/v1/users/123
Body: {"email": "newemail@example.com"}
Response: 200 OK

# Usunięcie użytkownika
DELETE /api/v1/users/123
Response: 204 No Content
```

## 🔍 HATEOAS Przykład

```json
{
  "id": 123,
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "_links": {
    "self": {
      "href": "/api/v1/users/123"
    },
    "posts": {
      "href": "/api/v1/users/123/posts"
    },
    "update": {
      "href": "/api/v1/users/123",
      "method": "PUT"
    },
    "delete": {
      "href": "/api/v1/users/123",
      "method": "DELETE"
    }
  }
}
```

## ⚡ Zalety REST API

```
✅ Prostota i czytelność
✅ Skalowalność
✅ Niezależność od platformy
✅ Możliwość cachowania
✅ Bezstanowość (łatwa skalowalność)
✅ Wykorzystanie standardu HTTP
✅ Dobra dokumentacja i tooling
```

## ⚠️ Wady REST API

```
❌ Over-fetching (zbyt dużo danych)
❌ Under-fetching (za mało danych, potrzeba wielu requestów)
❌ Brak standardu dla real-time
❌ Wersjonowanie może być problematyczne
❌ Trudność w reprezentacji złożonych relacji
```

## 🔗 Powiązane Tematy

- [[HTTP Metody i Kody Statusu|📮 HTTP Metody]]
- [[JSON i XML|📄 Formaty Danych]]
- [[REST vs SOAP vs GraphQL|⚖️ Porównanie Protokołów]]
- [[API Gateway Pattern|🚪 API Gateway]]
- [[web_apis_module|🌐 Web APIs - Moduł Główny]]

## 📚 Dalsze Zasoby

```
REST API Tutorial - restfulapi.net
Richardson Maturity Model - Levels 0-3
Roy Fielding's Dissertation - Oryginalna praca o REST
```

---

*Czas czytania: ~10 minut*

#rest #api #http #architecture #web-services
