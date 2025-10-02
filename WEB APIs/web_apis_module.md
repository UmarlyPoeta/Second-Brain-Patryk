# 🌐 Web APIs - Moduł Główny

## 📚 Czym są Web APIs?

**Web API** (Application Programming Interface) to zestaw reguł i protokołów, które pozwalają różnym aplikacjom komunikować się ze sobą przez internet. APIs umożliwiają wymianę danych między serwerami a klientami w ustandaryzowany sposób.

## 🗂️ Struktura Modułu

### 🎯 Podstawy Web APIs
- [[REST API - Podstawy|🔰 REST API - Podstawy]] - architektura REST, zasady, koncepcje
- [[HTTP Metody i Kody Statusu|📮 HTTP Metody i Kody Statusu]] - GET, POST, PUT, DELETE, kody odpowiedzi
- [[JSON i XML|📄 JSON i XML - Formaty Danych]] - serializacja, deserializacja, porównanie
- [[Autentykacja i Autoryzacja API|🔐 Autentykacja i Autoryzacja]] - JWT, OAuth, API Keys
- [[CORS i Bezpieczeństwo|🛡️ CORS i Bezpieczeństwo API]] - Cross-Origin Resource Sharing

### 🔄 Protokoły i Standardy
- [[REST vs SOAP vs GraphQL|⚖️ REST vs SOAP vs GraphQL]] - porównanie architektur
- [[OpenAPI i Swagger|📋 OpenAPI i Swagger]] - dokumentacja i specyfikacja
- [[WebSockets|🔌 WebSockets]] - komunikacja dwukierunkowa w czasie rzeczywistym
- [[gRPC Protocol|⚡ gRPC]] - nowoczesny RPC framework
- [[Webhooks|🔔 Webhooks]] - event-driven API

### 🛠️ Narzędzia i Praktyki
- [[Testowanie API|🧪 Testowanie API]] - Postman, curl, automated tests
- [[Rate Limiting i Throttling|⏱️ Rate Limiting]] - ograniczanie liczby żądań
- [[Wersjonowanie API|🔢 Wersjonowanie API]] - strategie wersjonowania
- [[Dokumentacja API|📚 Dokumentacja API]] - best practices
- [[Error Handling API|⚠️ Error Handling]] - obsługa błędów

### 🚀 Tematy Zaawansowane
- [[API Gateway Pattern|🚪 API Gateway]] - centralizacja i routing
- [[Microservices i API|🔷 Microservices]] - architektura rozproszona
- [[Caching w API|💾 Caching Strategies]] - optymalizacja wydajności
- [[API Monitoring|📊 Monitoring i Logging]] - obserwacja i diagnostyka
- [[API Security Best Practices|🔒 Security Best Practices]] - zabezpieczenia
- [[Pagination i Filtering|📑 Pagination]] - zarządzanie dużymi zbiorami danych

## 🔗 Powiązane Tematy

### Java & Spring Boot
- [[JAVA|☕ JAVA - Rozwój Aplikacji Webowych]]
- [[Spring Boot Web|🌐 Spring Boot - Aplikacje Webowe]]
- [[Java REST API|📡 Java - REST API]]
- [[Consuming APIs on the frontend|🖥️ Consuming APIs on Frontend]]

### Sieci Komputerowe
- [[warstwa_prezentacji|6️⃣ Warstwa Prezentacji]]
- [[SIECI KOMPUTEROWE|🌐 Sieci Komputerowe]]

## 📈 Ścieżka Nauki

1. **Fundamenty** (30 min)
   - Zrozumienie REST i HTTP
   - Podstawowe metody i kody statusu
   - Formaty danych JSON/XML

2. **Bezpieczeństwo** (20 min)
   - Autentykacja i autoryzacja
   - CORS
   - API security basics

3. **Protokoły** (25 min)
   - Porównanie REST/SOAP/GraphQL
   - WebSockets
   - gRPC i Webhooks

4. **Praktyka** (30 min)
   - Testowanie API
   - Dokumentacja
   - Error handling
   - Rate limiting

5. **Zaawansowane** (45 min)
   - API Gateway
   - Microservices
   - Caching
   - Monitoring
   - Advanced security

## 💡 Kluczowe Koncepty

### Zasady REST
```
1. Client-Server - Rozdział odpowiedzialności
2. Stateless - Każde żądanie niezależne
3. Cacheable - Możliwość cachowania
4. Uniform Interface - Jednolity interfejs
5. Layered System - Architektura warstwowa
6. Code on Demand (opcjonalne)
```

### HTTP Methods
```
GET    - Pobieranie zasobów
POST   - Tworzenie nowych zasobów
PUT    - Aktualizacja całego zasobu
PATCH  - Częściowa aktualizacja
DELETE - Usuwanie zasobu
HEAD   - Metadane zasobu
OPTIONS - Dostępne metody
```

### Status Codes
```
2xx - Sukces (200 OK, 201 Created, 204 No Content)
3xx - Przekierowanie (301 Moved, 304 Not Modified)
4xx - Błąd klienta (400 Bad Request, 401 Unauthorized, 404 Not Found)
5xx - Błąd serwera (500 Internal Error, 503 Service Unavailable)
```

## 🎯 Praktyczne Zastosowania

- **Frontend-Backend Communication** - SPA, mobile apps
- **Microservices** - Inter-service communication
- **Third-party Integrations** - Payment gateways, social media
- **IoT** - Device management and data collection
- **Mobile Apps** - Native app backends
- **Webhooks** - Event notifications

## 📊 Popularne Web APIs

```
Google APIs - Maps, YouTube, Drive
Facebook Graph API - Social integration
Twitter API - Tweets, users
Stripe API - Payments
GitHub API - Repository management
AWS APIs - Cloud services
```

---

*Czas nauki: ~2.5 godziny | Poziom: Początkujący → Zaawansowany*

#web-api #rest #http #api-design #microservices #api-security
