# 🚀 Spring Boot Microservices - Architektura Rozproszona

## 📋 Wprowadzenie do Architektury Mikrousług

Architektura mikrousług to podejście do budowy aplikacji jako zbioru małych, niezależnie wdrażalnych serwisów, które komunikują się ze sobą przez dobrze zdefiniowane API. W przeciwieństwie do monolitycznej architektury, gdzie wszystkie komponenty są ze sobą ściśle powiązane, mikrousługi umożliwiają niezależny rozwój, skalowanie i wdrażanie poszczególnych części systemu.

### Filozofia Mikrousług

**Single Responsibility Principle na poziomie serwisu:**
Każda mikrousługa powinna być odpowiedzialna za jedną konkretną funkcjonalność biznesową lub domenę. To pozwala na:
- Lepsze zrozumienie granic systemu
- Łatwiejsze utrzymanie i rozwój
- Minimalizację wpływu zmian na inne części systemu
- Możliwość używania różnych technologii dla różnych problemów

**Bounded Context z Domain-Driven Design:**
Mikrousługi naturalnie mapują się na bounded contexts z DDD:
- Każdy serwis ma własny model danych
- Jasno zdefiniowane granice między domenami
- Minimalizacja współdzielonych zasobów
- Niezależność w podejmowaniu decyzji technicznych

## 🏗️ Spring Cloud Ecosystem

### Spring Cloud Overview

Spring Cloud to umbrella project dostarczający narzędzi do budowy systemów rozproszonych. Oferuje gotowe rozwiązania dla typowych problemów architektury mikrousług:

**Kluczowe komponenty:**
- **Service Discovery:** Automatyczne wykrywanie i rejestracja serwisów
- **Configuration Management:** Centralizowane zarządzanie konfiguracją
- **Circuit Breaker:** Ochrona przed kaskadowymi awariami
- **API Gateway:** Jednolity punkt wejścia do systemu
- **Distributed Tracing:** Śledzenie requestów przez multiple services
- **Load Balancing:** Inteligentne rozdzielanie ruchu

### Service Discovery

**Teoria Service Discovery:**
W architekturze mikrousług, serwisy muszą znaleźć i komunikować się ze sobą. Service Discovery rozwiązuje problem dynamicznego znajdowania lokalizacji serwisów w środowisku, gdzie instance mogą być tworzone i usuwane dynamicznie.

**Wzorce Service Discovery:**

**Client-Side Discovery:**
- Klient odpowiedzialny za znalezienie dostępnych instancji serwisu
- Klient implementuje logikę load balancing
- Bezpośrednia komunikacja między serwisami
- Przykład: Eureka z Spring Cloud LoadBalancer

**Server-Side Discovery:**
- Load balancer/proxy odpowiedzialny za routing
- Klient wysyła request do load balancera
- Load balancer przekierowuje do właściwej instancji
- Przykład: AWS Application Load Balancer, Kubernetes Service

**Service Registry:**
Centralna baza danych dostępnych serwisów i ich lokalizacji:
- Serwisy rejestrują się przy starcie
- Regularne health checks
- Automatyczne usuwanie niedostępnych instancji
- High availability poprzez replikację

### Netflix Eureka Deep Dive

**Eureka Architecture:**
- **Eureka Server:** Service registry
- **Eureka Client:** Library dla aplikacji rejestrujących się w Eureka
- **Self-Preservation Mode:** Ochrona przed network partitions

**Registration Process:**
1. Service startup i registration w Eureka
2. Heartbeat co 30 sekund (domyślnie)
3. Service discovery przez innych klientów
4. Deregistration przy shutdown

**High Availability:**
- Multiple Eureka servers w cluster
- Peer-to-peer replication
- Client-side caching dla resilience
- Failover mechanisms

## 🌐 API Gateway Pattern

### Teoria API Gateway

API Gateway to jeden z najważniejszych wzorców w architekturze mikrousług. Służy jako single entry point do systemu, agregując wywołania do multiple backend services i dostarczając cross-cutting concerns.

**Główne odpowiedzialności:**
- **Request Routing:** Kierowanie requestów do odpowiednich mikrousług
- **Request/Response Transformation:** Modyfikacja danych w locie
- **Authentication & Authorization:** Centralizacja bezpieczeństwa
- **Rate Limiting:** Ochrona przed nadmiernym obciążeniem
- **Monitoring & Analytics:** Centralne zbieranie metryk
- **Caching:** Optymalizacja wydajności

**Backend for Frontend (BFF) Pattern:**
Specjalizacja API Gateway dla różnych typów klientów:
- Mobile BFF - optymalizowane dla urządzeń mobilnych
- Web BFF - dla aplikacji webowych
- Partner BFF - dla external API consumers

### Spring Cloud Gateway

**Reactive Gateway:**
Spring Cloud Gateway zbudowany na Spring WebFlux (reactive programming):
- Non-blocking I/O dla lepszej wydajności
- Backpressure handling
- Functional programming model
- Built-in filters dla common use cases

**Route Configuration:**
- Predicate-based routing
- URI matching patterns
- Header-based routing
- Time-based routing (blue-green deployments)

**Filter Types:**
- **Pre filters:** Executed before routing to backend
- **Post filters:** Executed after backend response
- **Global filters:** Applied to all routes
- **Custom filters:** Business-specific logic

## ⚡ Circuit Breaker Pattern

### Teoria Circuit Breaker

Circuit Breaker to wzorzec projektowy zapobiegający kaskadowym awariom w systemach rozproszonych. Działa podobnie do bezpiecznika elektrycznego - gdy wykryje problemy z downstream service, przerywa połączenia i zwraca fallback response.

**Stany Circuit Breaker:**

**Closed State (Normalny stan):**
- Wszystkie requesty są przekazywane do downstream service
- Monitorowanie success/failure ratio
- Liczenie błędów w sliding window

**Open State (Przerwany obwód):**
- Wszystkie requesty natychmiast zwracają error/fallback
- Downstream service nie jest wywoływany
- Pozwala systemowi na regenerację

**Half-Open State (Stan testowy):**
- Ograniczona liczba requestów jest przekazywana do testowania
- Jeśli succeed - powrót do Closed
- Jeśli fail - powrót do Open

### Resilience4j Integration

**Resilience4j Features:**
- Lightweight library (tylko 2MB)
- Functional programming style
- Multiple resilience patterns w jednej bibliotece
- Rich metrics and monitoring

**Patterns w Resilience4j:**
- **CircuitBreaker:** Failure handling
- **RateLimiter:** Traffic shaping
- **Retry:** Automatic retries with backoff
- **TimeLimiter:** Timeout handling
- **Bulkhead:** Resource isolation

**Configuration Strategies:**
- Annotation-based configuration
- Programmatic configuration
- Application properties configuration
- Dynamic configuration via actuator

## 📨 Inter-Service Communication

### Synchronous Communication

**HTTP/REST:**
Najpopularniejszy sposób komunikacji między mikrousługami:

**Zalety:**
- Prostota implementacji i debugowania
- Szerokie wsparcie toolingowe
- Standard w web development
- Human-readable dla troubleshootingu

**Wady:**
- Blocking I/O model
- Point-to-point coupling
- Network latency
- Cascade failures

**Best Practices:**
- Używaj HTTP/2 dla better performance
- Implement proper timeouts
- Use connection pooling
- Consider compression (gzip)

**gRPC:**
High-performance RPC framework:
- Protocol Buffers jako IDL
- HTTP/2 jako transport layer
- Streaming support (unidirectional i bidirectional)
- Cross-platform compatibility

### Asynchronous Communication

**Message Queues:**
Asynchroniczna komunikacja przez message brokers:

**Zalety:**
- Temporal decoupling - services nie muszą być dostępne jednocześnie
- Better resilience - messages mogą być processed później
- Load leveling - peaks są wygładzane
- Multiple consumers pattern

**Message Patterns:**
- **Point-to-Point:** One producer, one consumer
- **Publish-Subscribe:** One producer, multiple consumers
- **Request-Reply:** Asynchronous request with correlation ID

**Event Sourcing:**
- Events jako single source of truth
- Event store jako persistent log
- CQRS pattern dla read/write separation
- Eventual consistency model

## 🔧 Configuration Management

### Externalized Configuration

**12-Factor App Methodology:**
Konfiguracja powinna być przechowywana w environment variables, oddzielona od kodu:
- Environment-specific settings
- Secrets management
- Feature flags
- Database connections

**Configuration Hierarchy:**
1. Command line arguments (highest priority)
2. JNDI attributes
3. Java system properties
4. Environment variables
5. application.properties/yml
6. Default values (lowest priority)

### Spring Cloud Config

**Centralized Configuration Server:**
Spring Cloud Config Server dostarcza HTTP API do konfiguracji aplikacji:
- Git-based configuration storage
- Environment-specific configurations
- Real-time configuration updates
- Encryption/decryption support

**Configuration Client:**
Applications łączą się z Config Server przy starcie:
- Bootstrap context dla early initialization
- Fail-fast behavior jeśli config server niedostępny
- Refresh scope dla runtime updates
- Health indicators dla monitoring

**Bus Integration:**
Spring Cloud Bus umożliwia propagację configuration changes:
- Event-driven architecture
- RabbitMQ/Kafka jako message broker
- /actuator/bus-refresh endpoint
- Automatic configuration refresh

## 📊 Distributed Tracing

### Teoria Distributed Tracing

W architekturze mikrousług, pojedynczy request może przechodzić przez wiele serwisów. Distributed tracing umożliwia śledzenie kompletnego flow requestu przez cały system:

**Kluczowe koncepty:**
- **Trace:** Kompletna ścieżka requestu przez system
- **Span:** Pojedyncza operacja w ramach trace (np. HTTP call)
- **Trace Context:** Metadata propagowane między serwisami
- **Sampling:** Ograniczenie liczby traces dla performance

### Spring Cloud Sleuth

**Automatic Instrumentation:**
Sleuth automatycznie dodaje tracing do:
- HTTP requests (incoming i outgoing)
- Database calls (JDBC, JPA)
- Message brokers (RabbitMQ, Kafka)
- Async operations (@Async, CompletableFuture)

**Trace Context Propagation:**
- HTTP headers (X-Trace-Id, X-Span-Id)
- MDC (Mapped Diagnostic Context) dla logging
- Baggage dla custom context propagation
- Thread-local storage dla sync operations

**Integration z Zipkin:**
- Zipkin jako centralized tracing system
- HTTP/Kafka/RabbitMQ transport
- Web UI dla trace visualization
- Performance analysis i bottleneck detection

## 🛡️ Security w Mikrousługach

### Distributed Security Challenges

**Security w architekturze rozproszonej:**
- Network security między serwisami
- Identity propagation przez multiple hops
- Token validation i refresh
- Service-to-service authentication

### OAuth2 in Microservices

**JWT Token Strategy:**
- Self-contained tokens z user information
- Stateless authentication
- Token expiration handling
- Public key cryptography dla validation

**Token Relay Pattern:**
Propagacja OAuth2 tokens przez downstream services:
- Authorization header forwarding
- Token refresh handling
- Scoped access per service
- Centralized token management

**mTLS (Mutual TLS):**
Service-to-service authentication:
- Certificate-based authentication
- Network-level security
- Perfect forward secrecy
- Service mesh integration (Istio, Linkerd)

---

## 💼 Praktyczne Scenariusze Enterprise

### E-commerce Microservices Architecture

**Domain Decomposition:**
- **User Service:** Authentication, profiles, preferences
- **Product Catalog:** Product information, inventory
- **Order Service:** Order processing, workflow
- **Payment Service:** Payment processing, billing
- **Shipping Service:** Logistics, tracking
- **Notification Service:** Email, SMS, push notifications

**Cross-Cutting Concerns:**
- **API Gateway:** Single entry point, rate limiting
- **Config Server:** Centralized configuration
- **Service Discovery:** Dynamic service location
- **Distributed Tracing:** Request flow monitoring

### Data Management Strategies

**Database per Service:**
Każda mikrousługa ma własną bazę danych:
- Data isolation i ownership
- Technology diversity (SQL, NoSQL, Graph)
- Independent scaling
- Challenges z consistency

**Saga Pattern:**
Distributed transactions replacement:
- Choreography vs Orchestration
- Compensation actions dla rollbacks
- Event sourcing integration
- Eventual consistency model

### Deployment Strategies

**Container Orchestration:**
- Docker containerization
- Kubernetes dla orchestration
- Service mesh (Istio) dla advanced networking
- GitOps dla declarative deployments

**CI/CD Pipeline:**
- Automated testing pipeline
- Independent deployment per service
- Blue-green deployments
- Canary releases dla risk mitigation

---

## 🔗 Powiązane Tematy

- [[Spring Boot Architecture - Wzorce i Best Practices]] - fundamenty architektury
- [[Spring Security - Zaawansowane Techniki]] - bezpieczeństwo w systemach rozproszonych
- [[Spring Boot Testing - Kompletny Przewodnik]] - testowanie mikrousług
- [[Spring Cloud Config]] - centralizowane zarządzanie konfiguracją
- [[Spring Boot Docker & Deployment]] - wdrażanie mikrousług

---

*Czas nauki: ~50 minut*  
*Poziom: Zaawansowany*  
*Wymagana wiedza: Spring Boot, distributed systems concepts, Docker basics*