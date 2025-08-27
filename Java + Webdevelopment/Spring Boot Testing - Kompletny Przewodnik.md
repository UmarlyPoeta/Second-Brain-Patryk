# 🧪 Spring Boot Testing - Kompletny Przewodnik

## 📋 Wprowadzenie do Testowania w Spring Boot

Testowanie to fundamentalny element profesjonalnego rozwoju oprogramowania, który zapewnia jakość, niezawodność i możliwość bezpiecznego refactoringu aplikacji. Spring Boot wprowadza kompleksową filozofię testowania opartą na Test Slices, która pozwala na wydajne testowanie poszczególnych warstw aplikacji w izolacji, jednocześnie udostępniając narzędzia do testów integracyjnych całego systemu.

## 🏗️ Piramida Testów w Spring Boot

### Teoria Piramidy Testów

**Unit Tests (Podstawa piramidy)**
- Testują pojedyncze komponenty w izolacji
- Szybkie wykonanie (milisekundy)
- Wysokie pokrycie kodu
- Łatwe do pisania i utrzymania
- Nie wymagają Spring Context

**Integration Tests (Środek piramidy)**
- Testują współpracę między komponentami
- Testują rzeczywiste połączenia z bazami danych, API
- Wolniejsze wykonanie (sekundy)
- Mniejsza liczba niż unit tests
- Wykorzystują Spring Test Context

**End-to-End Tests (Szczyt piramidy)**
- Testują cały system od interfejsu użytkownika
- Najwolniejsze (minuty)
- Najmniejsza liczba
- Symulują rzeczywiste scenariusze użytkownika
- Pełna konfiguracja aplikacji

### Zalety Architektury Testowej Spring Boot

**Test Slices:**
Spring Boot wprowadza koncepcję "test slices" - wyspecjalizowanych adnotacji, które konfigurują tylko niezbędne komponenty do testowania konkretnej warstwy:

- Szybsze uruchamianie testów
- Mniejsze zużycie pamięci
- Fokus na konkretnej funkcjonalności
- Lepsza izolacja między testami

## 🔧 Unit Testing

### Testowanie bez Spring Context

**Czysty Unit Testing:**
Testowanie logiki biznesowej bez dependencies na framework Spring. Wykorzystuje pure Java i biblioteki mockujące jak Mockito.

**Zalety:**
- Maksymalna szybkość wykonania
- Brak overhead Spring Context
- Łatwe debugowanie
- Fokus na logice biznesowej

**Kiedy używać:**
- Testowanie algorytmów i business logic
- Utility classes i helper methods
- Domain objects bez Spring dependencies
- Validation logic

### @MockBean vs @Mock

**@Mock (Mockito):**
- Standard Mockito annotation
- Tworzy mock objects bez Spring context
- Używane w czystych unit testach
- Wymaga @ExtendWith(MockitoExtension.class)

**@MockBean (Spring Boot Test):**
- Spring Boot specific annotation
- Integruje mocki ze Spring Application Context
- Automatycznie zastępuje beans w context
- Przydatne w integration tests

**Wskazówki wyboru:**
- @Mock dla pure unit tests bez Spring
- @MockBean gdy potrzebujesz Spring context z mockami

### Testing Service Layer

**Typical Service Test Structure:**
1. **Setup:** Konfiguracja mocks i test data
2. **Exercise:** Wywołanie testowanej metody
3. **Verify:** Sprawdzenie rezultatów i interakcji
4. **Teardown:** Czyszczenie (zazwyczaj automatyczne)

**Mockowanie Dependencies:**
- Repository layer mockowanie
- External API clients
- Complex calculations
- Security context

## 🌐 Web Layer Testing

### @WebMvcTest Deep Dive

**Teoria:** @WebMvcTest to test slice annotation które ładuje tylko web layer komponenty - controllers, filters, security config - bez pełnego Spring context.

**Co jest ładowane:**
- @Controller, @RestController
- @ControllerAdvice, @JsonComponent
- Filter, WebMvcConfigurer
- Security configuration dla web layer

**Co NIE jest ładowane:**
- @Service, @Repository beans
- @Component (ogólne)
- Database connections
- JPA entities

**MockMvc Framework:**
MockMvc to główne narzędzie do testowania Spring MVC applications:
- Symuluje HTTP requests bez uruchamiania serwera
- Pełna kontrola nad request/response cycle
- Możliwość testowania wszystkich aspektów web layer

### Testing REST Controllers

**Request Testing:**
- Path variables validation
- Request parameters handling
- Request body deserialization
- Headers processing

**Response Testing:**
- HTTP status codes
- Response body content
- Response headers
- Content-Type validation

**Error Handling Testing:**
- Exception handling przez @ControllerAdvice
- Validation errors (400 Bad Request)
- Security errors (401, 403)
- Not found scenarios (404)

### Content Negotiation Testing

**Accept Headers:**
Testowanie różnych formatów odpowiedzi:
- application/json
- application/xml
- text/plain
- Custom media types

**Internationalization Testing:**
- Accept-Language headers
- Localized error messages
- Date/time formatting per locale
- Currency formatting

## 🗃️ Data Layer Testing

### @DataJpaTest Explained

**Teoria:** @DataJpaTest konfiguruje infrastrukturę potrzebną wyłącznie do testowania JPA repositories, wykorzystując in-memory database.

**Konfiguracja automatyczna:**
- Embedded database (H2, Derby, HSQLDB)
- JPA EntityManager
- Spring Data JPA repositories
- Transaction management
- SQL logging (opcjonalne)

**TestEntityManager:**
Specialized EntityManager dla testów:
- persistAndFlush() - natychmiastowy zapis do DB
- flush() - wymuszenie wykonania operacji
- clear() - czyszczenie first-level cache

**Testing Custom Queries:**
- @Query annotations testing
- Native queries validation
- Parameters binding verification
- Result mapping testing

### Database Integration Testing

**Test Data Management:**
- @Sql annotation dla setup scripts
- @SqlGroup dla multiple scripts
- @DirtiesContext dla clean state
- Database riders dla complex test data

**Transaction Rollback:**
Spring automatycznie rollbackuje transakcje w testach:
- Zachowuje czysty stan między testami
- Możliwość wyłączenia przez @Commit
- @Transactional na klasie lub metodzie

### Testing Repository Queries

**Query Method Testing:**
- Spring Data query derivation
- Custom implementations testing
- Pagination and sorting
- Specifications testing

**Performance Testing:**
- @Sql timing
- N+1 queries detection
- Index usage verification
- Query execution plans

## 🔗 Integration Testing

### @SpringBootTest Strategies

**Full Integration Testing:**
@SpringBootTest ładuje pełny Spring Application Context:

**WebEnvironment Options:**
- **MOCK:** MockMvc z mocked web environment
- **RANDOM_PORT:** Real HTTP server na random port
- **DEFINED_PORT:** Real HTTP server na konfigurowanym port
- **NONE:** No web environment

**Testing Real HTTP:**
- TestRestTemplate dla real HTTP calls
- WebTestClient dla reactive applications
- Real database connections
- External services integration

### TestContainers Integration

**Teoria:** TestContainers to biblioteka pozwalająca na uruchamianie real databases i zewnętrznych serwisów w Docker containers podczas testów.

**Zalety TestContainers:**
- Real database engines (PostgreSQL, MySQL, MongoDB)
- Identical environment w testach i produkcji
- Isolation między test runs
- Automatic cleanup po testach

**Supported Services:**
- Databases: PostgreSQL, MySQL, MongoDB, Redis
- Message brokers: RabbitMQ, Apache Kafka
- Cloud services: LocalStack (AWS emulation)
- Generic containers: własne Docker images

### Testing External Integrations

**WireMock dla API Testing:**
- Stub external HTTP APIs
- Simulate network failures
- Response delay simulation
- Request verification

**Contract Testing:**
- Spring Cloud Contract
- Consumer-driven contracts
- API compatibility testing
- Microservices integration testing

## 🧰 Advanced Testing Techniques

### Parameterized Tests

**JUnit 5 Parameterized Tests:**
Jedną z najważniejszych funkcji nowoczesnego testowania jest możliwość wykonywania tego samego testu z różnymi zestawami danych.

**@ParameterizedTest Sources:**
- @ValueSource - proste wartości
- @CsvSource - CSV format data
- @MethodSource - metoda dostarczająca dane
- @ArgumentsSource - custom argument provider

**Dynamic Tests:**
- @TestFactory dla dynamic test generation
- Runtime test creation
- Data-driven test scenarios

### Testing Security

**@WithMockUser:**
- Simulate authenticated users
- Custom roles and authorities
- User properties simulation

**@WithUserDetails:**
- Load user from UserDetailsService
- Real user data testing
- Custom user implementations

**Security Integration Testing:**
- Authentication flows
- Authorization rules
- CSRF protection
- JWT token validation

### Testing Configuration

**@TestConfiguration:**
- Override beans dla testów
- Test-specific configurations
- Mock external dependencies
- Custom test beans

**Profile-Specific Testing:**
- @ActiveProfiles annotation
- Environment-specific configurations
- Database configurations per profile
- Feature flags testing

### Performance Testing

**@Timed Tests:**
JUnit 5 @Timeout annotation:
- Method execution timeout
- Class-level timeouts
- Global timeout configuration

**Load Testing Integration:**
- JMeter integration
- Gatling performance tests
- Memory usage monitoring
- Database connection pooling testing

## 🔍 Testing Best Practices

### Test Naming Conventions

**Given-When-Then Structure:**
Testy powinny jasno opisywać scenariusz:
- Given: Initial state/preconditions
- When: Action being tested
- Then: Expected outcome

**Method Naming:**
- should_ReturnUser_WhenValidIdProvided()
- should_ThrowException_WhenUserNotFound()
- should_SaveUser_WhenValidDataProvided()

### Test Data Management

**Test Data Builders:**
Pattern do tworzenia test objects:
- Fluent API dla object creation
- Default values z możliwością override
- Reusable across multiple tests

**@DirtiesContext Usage:**
Kontrolowane przypadki gdy Spring context musi być odświeżony:
- Po każdej klasie testowej
- Po każdej metodzie testowej
- Po konkretnych metodach

### Assertion Libraries

**AssertJ vs JUnit Assertions:**
AssertJ oferuje bardziej ekspresyjne assertions:
- Fluent API
- Better error messages
- Rich set of assertions for collections, dates, exceptions
- Custom assertions możliwość

**Hamcrest Matchers:**
- Composable matchers
- Readable assertions
- Custom matcher creation
- Integration z MockMvc

### Test Categories i Organization

**Test Suites:**
- @Suite annotation dla JUnit 5
- Grouped test execution
- Category-based test running
- CI/CD pipeline optimization

**Test Profiles:**
- Unit tests profile
- Integration tests profile
- Performance tests profile
- Smoke tests dla production validation

---

## 💼 Scenariusze Biznesowe

### E-commerce Testing Strategy

**User Journey Testing:**
- Product search and filtering
- Cart management
- Checkout process
- Payment integration
- Order fulfillment

**Data Consistency Testing:**
- Inventory management
- Pricing accuracy
- Tax calculations
- Multi-currency support

### API Testing Strategies

**Contract Testing:**
- API specification compliance
- Backward compatibility
- Version management
- Breaking changes detection

**Security Testing:**
- Authentication flows
- Authorization rules
- Input validation
- Rate limiting

### Microservices Testing

**Component Testing:**
- Service isolation
- Dependencies mocking
- Contract verification
- Resilience patterns testing

**End-to-End Testing:**
- Service communication
- Data consistency across services
- Failure scenarios
- Performance across service boundaries

---

## 🔗 Powiązane Tematy

- [[JUnit 5 - Unit Testing]] - szczegóły JUnit 5 features
- [[Spring Boot Architecture - Wzorce i Best Practices]] - architektura wspierająca testowanie
- [[Spring Security - Podstawy Bezpieczeństwa]] - testowanie security
- [[Spring Data JPA - Zaawansowane Techniki]] - testowanie persistence layer
- [[Spring Boot Microservices]] - testowanie architektury rozproszonej

---

*Czas nauki: ~45 minut*  
*Poziom: Średniozaawansowany do Zaawansowanego*  
*Wymagana wiedza: JUnit basics, Spring Boot fundamentals, Mockito*