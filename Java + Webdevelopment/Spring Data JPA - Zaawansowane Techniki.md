# 🗃️ Spring Data JPA - Zaawansowane Techniki

## 📋 Wprowadzenie do Zaawansowanego JPA

Spring Data JPA to potężny framework, który znacznie wykracza poza podstawowe operacje CRUD. Zaawansowane techniki obejmują optymalizację wydajności, implementację skomplikowanych zapytań, auditing, multitenancy, oraz integrację z cachingiem. Zrozumienie tych konceptów jest kluczowe dla budowania wydajnych aplikacji enterprise obsługujących duże wolumeny danych.

## 🔍 Custom Queries i Specifications

### JPQL vs Native SQL - Kiedy Używać Czego

**JPQL (Java Persistence Query Language):**
JPQL to objektowo-orientowany język zapytań operujący na encjach JPA, a nie bezpośrednio na tabelach bazy danych.

**Zalety JPQL:**
- Database-agnostic - działa z różnymi bazami danych
- Type-safe - kompilator może wykryć błędy składniowe
- Automatyczne mapowanie na obiekty
- Wsparcie dla inheritence mapping
- Integracja z cache pierwszego poziomu

**Kiedy używać JPQL:**
- Standardowe operacje na encjach
- Zapytania korzystające z relacji JPA
- Gdy potrzebujemy przenośności między bazami
- Operacje na hierarchiach dziedziczenia

**Native SQL:**
Bezpośrednie zapytania SQL wykonywane na konkretnej bazie danych.

**Zalety Native SQL:**
- Pełny dostęp do funkcji specyficznych dla bazy
- Optymalna wydajność dla złożonych zapytań
- Możliwość użycia procedur składowanych
- Kontrola nad planami wykonania zapytań

**Kiedy używać Native SQL:**
- Złożone zapytania analityczne z window functions
- Bulk operations wymagające wysokiej wydajności
- Wykorzystanie specyficznych funkcji bazy danych
- Existing legacy queries

### JPA Criteria API

**Teoria:** Criteria API to programowy sposób budowania zapytań JPA w sposób type-safe. Pozwala na dynamiczne konstruowanie zapytań w czasie wykonania aplikacji.

**Komponenty Criteria API:**
- **CriteriaBuilder:** Factory do tworzenia elementów zapytania
- **CriteriaQuery:** Reprezentuje zapytanie SELECT
- **Root:** Punkt startowy dla ścieżek w zapytaniu (FROM clause)
- **Predicate:** Warunki WHERE
- **Path:** Ścieżki do atrybutów encji

**Zalety Criteria API:**
- Type safety - błędy wykrywane w czasie kompilacji
- Dynamiczne budowanie zapytań na podstawie parametrów
- Refactoring-friendly - zmiany w encjach są automatycznie propagowane
- IDE support - autocompletowanie i nawigacja

**Wady:**
- Verbose syntax - więcej kodu niż JPQL
- Steeper learning curve
- Mniej czytelne dla prostych zapytań

### Spring Data Specifications

**Teoria:** Specifications to implementacja wzorca Specification Pattern w Spring Data JPA. Umożliwia komponowanie warunków zapytań w sposób reużywalny i testowalny.

**Specification Interface:**
```java
public interface Specification<T> {
    Predicate toPredicate(Root<T> root, 
                         CriteriaQuery<?> query, 
                         CriteriaBuilder criteriaBuilder);
}
```

**Komponowanie Specifications:**
- **and()** - logiczne AND
- **or()** - logiczne OR  
- **not()** - negacja
- **where()** - punkt startowy dla łańcucha

**Praktyczne zastosowania:**
- Dynamiczne filtry w aplikacjach webowych
- Reużywalne komponenty wyszukiwania
- Business rules jako obiekty
- Complex search functionality

## 📊 Custom Repository Implementations

### Extending Repository Functionality

**Kiedy potrzebujemy custom implementation:**
- Złożone operacje biznesowe wymagające wielu zapytań
- Integracja z zewnętrznymi systemami
- Operacje wymagające bezpośredniego dostępu do EntityManager
- Bulk operations z optymalizacją wydajności

**Wzorzec implementacji:**
1. Definicja custom interface
2. Implementacja z użyciem EntityManager
3. Extension głównego repository
4. Automatyczna detekcja przez Spring Data

### Repository Composition

**Fragment Repositories:**
Spring Data JPA pozwala na komponowanie funkcjonalności poprzez fragment repositories:
- Jeden fragment = jedna odpowiedzialność
- Możliwość mieszania różnych fragmentów
- Lepsze testowanie i utrzymanie
- Separation of concerns

### Auditing

**Teoria auditing:** Auditing to automatyczne śledzenie zmian w encjach - kto i kiedy utworzył/zmodyfikował rekord. Jest to kluczowy element compliance w aplikacjach biznesowych.

**JPA Auditing annotations:**
- **@CreatedDate:** Data utworzenia
- **@LastModifiedDate:** Data ostatniej modyfikacji
- **@CreatedBy:** Użytkownik tworzący
- **@LastModifiedBy:** Użytkownik modyfikujący

**AuditingEntityListener:**
Listener JPA, który automatycznie wypełnia pola auditing przed persystencją encji.

**AuditorAware Interface:**
Interfejs dostarczający informacje o aktualnym użytkowniku:
```java
public interface AuditorAware<T> {
    Optional<T> getCurrentAuditor();
}
```

**Zalety auditing:**
- Compliance z regulacjami (SOX, GDPR)
- Debugging - śledzenie zmian w danych
- Business intelligence - analiza wzorców użytkowania
- Security - wykrywanie nieautoryzowanych zmian

## ⚡ Performance Optimization

### N+1 Problem i jego rozwiązania

**Teoria N+1 Problem:**
N+1 to częsty problem wydajności, gdy pobranie N encji powoduje wykonanie N+1 zapytań do bazy danych - 1 zapytanie dla głównych encji + N zapytań dla powiązanych danych.

**Przykład problemu:**
```
SELECT * FROM orders;           -- 1 query
SELECT * FROM customers WHERE id = 1;  -- Query for order 1
SELECT * FROM customers WHERE id = 2;  -- Query for order 2
...                             -- N more queries
```

**Rozwiązania:**

**1. Eager Fetching z Join:**
- @Query z JOIN FETCH
- Criteria API z fetch()
- Entity Graphs

**2. Batch Fetching:**
- @BatchSize annotation
- Hibernate-specific optimization
- Ładuje wiele rekordów w jednym zapytaniu

**3. Projection DTOs:**
- Pobranie tylko potrzebnych danych
- Reduced memory footprint
- Custom projections

### Entity Graphs

**Teoria:** Entity Graphs to JPA 2.1 feature umożliwiający deklaratywną kontrolę nad tym, które powiązania mają być załadowane w konkretnym zapytaniu.

**Named Entity Graphs:**
Definiowane na poziomie encji za pomocą adnotacji:
- @NamedEntityGraph
- @NamedAttributeNode
- @NamedSubgraph

**Dynamic Entity Graphs:**
Tworzone programowo w czasie wykonania aplikacji.

**Zalety Entity Graphs:**
- Fine-grained control nad loading strategy
- Możliwość różnych strategii dla różnych use cases
- Performance optimization bez zmian w modelu
- Declarative approach

### Second Level Cache

**Teoria cache'owania:**
Second Level Cache to cache współdzielony między sesjami Hibernate, przechowujący dane na poziomie SessionFactory/EntityManagerFactory.

**Poziomy cache'owania:**
1. **First Level Cache (Session Cache):** Automatyczny, per session
2. **Second Level Cache:** Opcjonalny, współdzielony między sesjami
3. **Query Cache:** Cache dla rezultatów zapytań

**Cache Providers:**
- **Ehcache:** Najpopularniejszy, dobra wydajność
- **Hazelcast:** Distributed cache, cluster support
- **Infinispan:** Red Hat's solution, advanced features
- **Caffeine:** High performance, modern Java

**Cache Strategies:**
- **READ_ONLY:** Dane tylko do odczytu
- **READ_WRITE:** Dane mogą być modyfikowane
- **NONSTRICT_READ_WRITE:** Weak consistency
- **TRANSACTIONAL:** Full transactional support

### Lazy Loading Strategies

**Teoria lazy loading:** Lazy loading to wzorzec ładowania danych na żądanie - powiązane obiekty są ładowane dopiero gdy są potrzebne, a nie podczas głównego zapytania.

**Proxy Objects:**
Hibernate tworzy proxy objects dla lazy relationships:
- Proxy interceptuje wywołania metod
- Inicjalizuje dane przy pierwszym dostępie
- Transparent dla kodu aplikacji

**LazyInitializationException:**
Wyjątek wystepujący przy próbie dostępu do lazy property poza sesją:
- Częsty problem w aplikacjach webowych
- Rozwiązania: @Transactional, Open Session in View, DTOs

**Best Practices:**
- Używaj DTOs dla presentation layer
- Planuj fetch strategies
- Monitor SQL queries w developmencie
- Unikaj Open Session in View w produkcji

## 🔄 Advanced Mapping Techniques

### Inheritance Mapping

**Single Table Strategy:**
Wszystkie klasy hierarchii w jednej tabeli z kolumną dyskryminatora.

**Zalety:**
- Proste joins
- Dobra wydajność dla queries na całej hierarchii
- Brak potrzeby union operations

**Wady:**
- Nullable columns dla subclass properties
- Table może być bardzo szeroka
- Ograniczenia NOT NULL constraints

**Joined Strategy:**
Każda klasa ma własną tabelę połączoną przez foreign key.

**Zalety:**
- Normalized database design
- Wszystkie properties mogą mieć NOT NULL
- Eficient storage

**Wady:**
- Complex joins dla queries
- Performance overhead dla deep hierarchies
- More complex database schema

**Table Per Class Strategy:**
Każda konkretna klasa ma własną tabelę ze wszystkimi properties.

### Embedded Objects

**@Embeddable vs @Embedded:**
Mechanizm kompozycji obiektów w JPA - obiekt nie będący encją może być osadzony w encji.

**Zalety embedded objects:**
- Code reusability - ten sam object w wielu encjach
- Domain modeling - lepsze odzwierciedlenie business domain
- Encapsulation - logiczne grupowanie powiązanych pól

**AttributeOverrides:**
Możliwość zmiany nazw kolumn dla embedded objects:
- Unikanie konfliktów nazw
- Customization dla różnych kontekstów użycia
- Flexibility w database mapping

### Collections Mapping

**Collection Types:**
- **@OneToMany / @ManyToOne:** Parent-child relationships
- **@ManyToMany:** Many-to-many associations
- **@ElementCollection:** Collections of basic types or embeddables

**Fetch Strategies dla Collections:**
- **FetchType.LAZY:** Default dla collections
- **FetchType.EAGER:** Immediate loading
- **@BatchSize:** Optimization dla lazy collections

**Cascade Types:**
- **CascadeType.ALL:** All operations
- **CascadeType.PERSIST:** Only save operations
- **CascadeType.MERGE:** Only merge operations
- **CascadeType.REMOVE:** Only delete operations

## 🧪 Testing JPA

### @DataJpaTest

**Teoria:** @DataJpaTest to specialized test slice annotation w Spring Boot testach, które konfiguruje tylko komponenty potrzebne do testowania JPA repositories.

**Co jest konfigurowane:**
- Embedded test database (H2)
- JPA repositories
- EntityManager
- Transaction management

**Co NIE jest konfigurowane:**
- Web layer (@Controller)
- Service layer (@Service)
- Security configuration

### TestEntityManager

**Alternatywa dla EntityManager w testach:**
- Flush() operations
- Clear() session
- Persist and flush w jednej operacji
- Designed specifically for testing

### Database Migration Testing

**Flyway/Liquibase Integration:**
- Test database schema migrations
- Rollback testing
- Data migration validation
- Cross-database compatibility testing

---

## 💼 Praktyczne Scenariusze Enterprise

### Multi-Tenancy

**Shared Database, Shared Schema:**
- Wszystkie tenants w jednej bazie z discriminator column
- Najprostrza implementacja
- Security przez application logic

**Shared Database, Separate Schemas:**
- Każdy tenant ma własny schemat
- Database-level isolation
- Schema switching w runtime

**Separate Databases:**
- Każdy tenant ma własną bazę danych
- Maksymalna izolacja
- Complex deployment i maintenance

### Soft Deletes

**Teoria:** Soft delete to wzorzec, gdzie rekordy nie są fizycznie usuwane z bazy, ale oznaczane jako usunięte poprzez flagę.

**Implementacja:**
- Boolean deleted flag
- Timestamp deletedAt
- @Where annotation dla automatycznego filtrowania

**Zalety:**
- Data recovery możliwy
- Audit trail preservation
- Referential integrity maintenance

**Wady:**
- Database storage growth
- Complex queries (always filter deleted)
- Index maintenance overhead

### Event Sourcing z JPA

**Teoria:** Event Sourcing to wzorzec, gdzie stan aplikacji jest przechowywany jako sekwencja zdarzeń (events), a nie jako current state.

**Implementacja z JPA:**
- Event Store jako JPA entity
- Aggregate root reconstruction z events
- Snapshots dla performance
- CQRS pattern integration

---

## 🔗 Powiązane Tematy

- [[Java JPA Hibernate]] - podstawy mapowania relacyjnego
- [[SQL - Zaawansowane Zapytania]] - optymalizacja zapytań bazodanowych
- [[Spring Boot Caching]] - strategie cache'owania
- [[Spring Boot Testing]] - testowanie warstwy dostępu do danych
- [[Spring Boot Performance]] - monitorowanie i optymalizacja

---

*Czas nauki: ~40 minut*  
*Poziom: Zaawansowany*  
*Wymagana wiedza: Spring Data JPA podstawy, Hibernate, SQL*