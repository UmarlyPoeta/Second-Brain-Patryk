# 🔢 Wersjonowanie API

## 🎯 Po co wersjonować?

```
✅ Breaking changes bez przerywania działających klientów
✅ Stopniowa migracja użytkowników
✅ Testowanie nowych features
✅ Zgodność wsteczna (backward compatibility)
✅ Deprecation okresy
```

## 📋 Strategie Wersjonowania

### 1. URL Path Versioning (Najpopularniejsze)

```http
GET /api/v1/users
GET /api/v2/users
GET /api/v3/users

Zalety:
✅ Proste i czytelne
✅ Łatwe caching
✅ Łatwe routing
✅ Browser-friendly

Wady:
❌ Duplikacja kodu
❌ Więcej endpoints
```

**Spring Boot:**
```java
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 {
    
    @GetMapping
    public List<UserV1Dto> getUsers() {
        return userService.findAllV1();
    }
}

@RestController
@RequestMapping("/api/v2/users")
public class UserControllerV2 {
    
    @GetMapping
    public List<UserV2Dto> getUsers() {
        return userService.findAllV2();
    }
}
```

### 2. Query Parameter Versioning

```http
GET /api/users?version=1
GET /api/users?version=2
GET /api/users?v=2

Zalety:
✅ Ten sam URL
✅ Optional (default version)

Wady:
❌ Trudniejsze caching
❌ Może być ignorowane
```

**Spring Boot:**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping
    public ResponseEntity<?> getUsers(
            @RequestParam(defaultValue = "1") int version) {
        
        return switch(version) {
            case 1 -> ResponseEntity.ok(userService.findAllV1());
            case 2 -> ResponseEntity.ok(userService.findAllV2());
            default -> ResponseEntity.badRequest()
                .body("Unsupported version");
        };
    }
}
```

### 3. Header Versioning

```http
GET /api/users
Accept-Version: v2

# lub
GET /api/users
X-API-Version: 2

Zalety:
✅ Czysty URL
✅ Content negotiation

Wady:
❌ Mniej widoczne
❌ Trudniejsze testowanie w przeglądarce
```

**Spring Boot:**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(headers = "X-API-Version=1")
    public List<UserV1Dto> getUsersV1() {
        return userService.findAllV1();
    }
    
    @GetMapping(headers = "X-API-Version=2")
    public List<UserV2Dto> getUsersV2() {
        return userService.findAllV2();
    }
}
```

### 4. Accept Header (Content Negotiation)

```http
GET /api/users
Accept: application/vnd.myapp.v1+json

GET /api/users
Accept: application/vnd.myapp.v2+json

Zalety:
✅ RESTful
✅ Wykorzystuje standard HTTP

Wady:
❌ Najbardziej złożone
❌ Trudniejsze dla developerów
```

**Spring Boot:**
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(produces = "application/vnd.myapp.v1+json")
    public List<UserV1Dto> getUsersV1() {
        return userService.findAllV1();
    }
    
    @GetMapping(produces = "application/vnd.myapp.v2+json")
    public List<UserV2Dto> getUsersV2() {
        return userService.findAllV2();
    }
}
```

## 🔄 Semantic Versioning (SemVer)

```
MAJOR.MINOR.PATCH

v1.0.0 → v1.1.0 → v1.1.1 → v2.0.0

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes
```

## 🎨 Best Practices

### 1. Kiedy tworzyć nową wersję?

```
Breaking Changes (nowa major version):
❌ Usunięcie pola z response
❌ Zmiana typu pola (string → int)
❌ Zmiana nazwy pola
❌ Wymaganie nowego pola w request
❌ Zmiana statusów HTTP
❌ Zmiana znaczenia endpointu

Non-Breaking (ta sama wersja):
✅ Dodanie nowego pola (optional)
✅ Dodanie nowego endpointu
✅ Bug fixes
✅ Performance improvements
✅ Dodanie nowej opcjonalnej walidacji
```

### 2. Deprecation Strategy

```java
@RestController
@RequestMapping("/api/v1/users")
@Deprecated
public class UserControllerV1 {
    
    @GetMapping
    @Deprecated
    public ResponseEntity<List<User>> getUsers(HttpServletResponse response) {
        // Dodaj deprecation headers
        response.addHeader("Deprecation", "true");
        response.addHeader("Sunset", "2024-12-31");
        response.addHeader("Link", 
            "</api/v2/users>; rel=\"successor-version\"");
        
        return ResponseEntity.ok(userService.findAll());
    }
}
```

### 3. Komunikacja z Klientami

```
1. Ogłoszenie deprecation (6-12 miesięcy wcześniej)
2. Dodanie Deprecation headers
3. Dokumentacja migration guide
4. Email notifications do użytkowników
5. Grace period
6. Final sunset date
```

## 📊 Zarządzanie Wersjami

```java
// Centralna konfiguracja wersji
@Configuration
public class ApiVersionConfig {
    
    public static final String V1 = "/api/v1";
    public static final String V2 = "/api/v2";
    public static final String V3 = "/api/v3";
    
    public static final String CURRENT_VERSION = V3;
    public static final List<String> SUPPORTED_VERSIONS = 
        List.of(V2, V3);
    public static final List<String> DEPRECATED_VERSIONS = 
        List.of(V1);
}

// Middleware sprawdzający wersję
@Component
public class VersionValidationFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response,
                        FilterChain chain) {
        HttpServletRequest req = (HttpServletRequest) request;
        String path = req.getRequestURI();
        
        if (path.contains("/api/v1/")) {
            HttpServletResponse resp = (HttpServletResponse) response;
            resp.addHeader("X-API-Deprecated", "true");
            resp.addHeader("X-API-Sunset-Date", "2024-12-31");
        }
        
        chain.doFilter(request, response);
    }
}
```

## 🔄 Migration Strategy

### Adapter Pattern

```java
// Stary model (v1)
public class UserV1 {
    private Long id;
    private String fullName;
    private String emailAddress;
}

// Nowy model (v2)
public class UserV2 {
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
}

// Adapter/Mapper
@Component
public class UserVersionAdapter {
    
    public UserV1 toV1(User entity) {
        UserV1 v1 = new UserV1();
        v1.setId(entity.getId());
        v1.setFullName(entity.getFirstName() + " " + entity.getLastName());
        v1.setEmailAddress(entity.getEmail());
        return v1;
    }
    
    public UserV2 toV2(User entity) {
        UserV2 v2 = new UserV2();
        v2.setId(entity.getId());
        v2.setFirstName(entity.getFirstName());
        v2.setLastName(entity.getLastName());
        v2.setEmail(entity.getEmail());
        return v2;
    }
}
```

## 📝 Dokumentacja Wersji

```yaml
# OpenAPI
openapi: 3.0.0
info:
  title: User API
  version: 2.0.0
  description: |
    ## Versions
    - v1 (deprecated, sunset: 2024-12-31)
    - v2 (current)
    
    ## Migration Guide
    v1 → v2 changes:
    - `fullName` split into `firstName` and `lastName`
    - `emailAddress` renamed to `email`
    - New required field: `phoneNumber`

servers:
  - url: https://api.example.com/v2
    description: Current version
  - url: https://api.example.com/v1
    description: Deprecated (sunset 2024-12-31)
```

## 🎯 Recommendations

```
✅ Start with v1, not v0
✅ Use URL versioning dla public APIs
✅ Major version tylko (v1, v2, nie v1.2)
✅ Support minimum 2 versions
✅ Długi deprecation period (6-12 miesięcy)
✅ Clear migration documentation
✅ Komunikacja z klientami
✅ Monitoring usage per version
❌ Nie usuwaj wersji bez warning
❌ Nie zmieniaj behavior w tej samej wersji
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[OpenAPI i Swagger|📋 OpenAPI]]
- [[Dokumentacja API|📚 Dokumentacja]]
- [[HTTP Metody i Kody Statusu|📮 HTTP Metody]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~8 minut*

#api-versioning #backward-compatibility #deprecation #api-design
