# 🛡️ CORS i Bezpieczeństwo API

## 🌐 Cross-Origin Resource Sharing (CORS)

### Definicja
**CORS** to mechanizm bezpieczeństwa przeglądarek, który kontroluje jakie domeny mogą wykonywać żądania do Twojego API.

### Same-Origin Policy (SOP)

```
Origin = Protocol + Domain + Port

Przykład: https://example.com:443

Same Origin:
✅ https://example.com:443/api/users
✅ https://example.com:443/page.html

Different Origin (Cross-Origin):
❌ http://example.com (inny protokół)
❌ https://api.example.com (inna subdomena)
❌ https://example.com:8080 (inny port)
❌ https://different.com (inna domena)
```

### Problem CORS

```javascript
// Frontend: http://localhost:3000
fetch('http://localhost:8080/api/users')
  .then(res => res.json())
  .catch(err => {
    // ❌ CORS Error!
    // Access to fetch has been blocked by CORS policy
  });
```

**Bez CORS:**
```
Browser → API Server
         ← Blocked! (Different origin)
```

**Z CORS:**
```
Browser → API Server
         ← Access-Control-Allow-Origin: http://localhost:3000
         ← OK, allowed!
```

## 🔧 CORS Headers

### Request Headers (wysyłane przez przeglądarkę)

```http
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization
```

### Response Headers (zwracane przez serwer)

```http
# Który origin może wykonywać requesty
Access-Control-Allow-Origin: http://localhost:3000

# Jakie metody HTTP są dozwolone
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS

# Jakie headery są dozwolone
Access-Control-Allow-Headers: Content-Type, Authorization, X-API-Key

# Czy wysyłać credentials (cookies, auth headers)
Access-Control-Allow-Credentials: true

# Jak długo cache'ować preflight response
Access-Control-Max-Age: 3600

# Które headery są dostępne w response
Access-Control-Expose-Headers: X-Total-Count, X-Page-Number
```

## ✈️ Preflight Request

Dla "złożonych" requestów przeglądarka wysyła **preflight** (OPTIONS):

```
"Złożone" requesty:
• Metody: PUT, DELETE, PATCH
• Custom headers: Authorization, X-API-Key
• Content-Type: application/json
```

### Flow Preflight

```
1. Browser wysyła OPTIONS:
   ↓
OPTIONS /api/users HTTP/1.1
Origin: http://localhost:3000
Access-Control-Request-Method: POST
Access-Control-Request-Headers: Content-Type, Authorization

2. Server odpowiada:
   ↓
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Methods: POST, GET, OPTIONS
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 3600

3. Jeśli OK, browser wysyła właściwy request:
   ↓
POST /api/users HTTP/1.1
Origin: http://localhost:3000
Authorization: Bearer token...
Content-Type: application/json

4. Server odpowiada z danymi:
   ↓
HTTP/1.1 201 Created
Access-Control-Allow-Origin: http://localhost:3000
```

## 💻 Implementacja CORS

### Spring Boot

```java
// 1. Global Configuration
@Configuration
public class CorsConfig {
    
    @Bean
    public WebMvcConfigurer corsConfigurer() {
        return new WebMvcConfigurer() {
            @Override
            public void addCorsMappings(CorsRegistry registry) {
                registry.addMapping("/api/**")
                    .allowedOrigins("http://localhost:3000", 
                                   "https://myapp.com")
                    .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                    .allowedHeaders("*")
                    .allowCredentials(true)
                    .maxAge(3600);
            }
        };
    }
}

// 2. Controller Level
@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = "http://localhost:3000", 
            methods = {RequestMethod.GET, RequestMethod.POST},
            allowedHeaders = "*",
            allowCredentials = "true")
public class UserController {
    // ...
}

// 3. Method Level
@GetMapping
@CrossOrigin(origins = "http://localhost:3000")
public List<User> getUsers() {
    return userService.findAll();
}
```

### Express.js (Node.js)

```javascript
const express = require('express');
const cors = require('cors');

const app = express();

// 1. Simple (allow all)
app.use(cors());

// 2. Specific origins
app.use(cors({
  origin: ['http://localhost:3000', 'https://myapp.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,
  maxAge: 3600
}));

// 3. Dynamic origin
app.use(cors({
  origin: function(origin, callback) {
    const allowedOrigins = process.env.ALLOWED_ORIGINS.split(',');
    if (allowedOrigins.includes(origin) || !origin) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  }
}));

// 4. Route specific
app.get('/api/users', 
  cors({origin: 'http://localhost:3000'}),
  (req, res) => {
    res.json({users: []});
  }
);
```

### Nginx (Reverse Proxy)

```nginx
server {
    listen 80;
    server_name api.example.com;
    
    location /api/ {
        # Preflight
        if ($request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' 
                      'http://localhost:3000' always;
            add_header 'Access-Control-Allow-Methods' 
                      'GET, POST, PUT, DELETE, OPTIONS' always;
            add_header 'Access-Control-Allow-Headers' 
                      'Content-Type, Authorization' always;
            add_header 'Access-Control-Max-Age' 3600 always;
            return 204;
        }
        
        # Actual requests
        add_header 'Access-Control-Allow-Origin' 
                  'http://localhost:3000' always;
        add_header 'Access-Control-Allow-Credentials' 
                  'true' always;
        
        proxy_pass http://localhost:8080;
    }
}
```

## 🔒 Bezpieczeństwo API - Best Practices

### 1. HTTPS Only (TLS/SSL)

```
✅ Zawsze HTTPS w produkcji
✅ Redirect HTTP → HTTPS
✅ HSTS header

Przykład header:
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### 2. Rate Limiting

```javascript
// Express Rate Limit
const rateLimit = require('express-rate-limit');

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minut
  max: 100, // max 100 requestów
  message: 'Too many requests from this IP',
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Różne limity dla różnych endpointów
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // tylko 5 prób logowania
});

app.post('/api/auth/login', authLimiter, loginController);
```

```java
// Spring Boot - Bucket4j
@GetMapping("/api/resource")
public ResponseEntity<?> getResource() {
    Bucket bucket = Bucket4j.builder()
        .addLimit(Bandwidth.classic(10, 
                 Refill.greedy(10, Duration.ofMinutes(1))))
        .build();
    
    if (bucket.tryConsume(1)) {
        return ResponseEntity.ok(resource);
    }
    return ResponseEntity.status(429)
        .body("Rate limit exceeded");
}
```

### 3. Input Validation

```java
// Spring Boot Validation
public class CreateUserRequest {
    
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 50)
    private String name;
    
    @Email(message = "Invalid email format")
    @NotBlank
    private String email;
    
    @Pattern(regexp = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,}$",
            message = "Password must be strong")
    private String password;
}

@PostMapping("/api/users")
public ResponseEntity<?> createUser(
        @Valid @RequestBody CreateUserRequest request) {
    // Walidacja automatyczna przez @Valid
    return ResponseEntity.ok(userService.create(request));
}
```

### 4. SQL Injection Prevention

```java
// ❌ ŹLE - SQL Injection vulnerable
String query = "SELECT * FROM users WHERE email = '" + email + "'";

// ✅ DOBRZE - Prepared statements
String query = "SELECT * FROM users WHERE email = ?";
PreparedStatement stmt = connection.prepareStatement(query);
stmt.setString(1, email);

// ✅ DOBRZE - JPA/Hibernate
@Query("SELECT u FROM User u WHERE u.email = :email")
User findByEmail(@Param("email") String email);

// ✅ DOBRZE - Spring Data JPA
User findByEmail(String email);
```

### 5. XSS Prevention

```javascript
// ❌ ŹLE
document.getElementById('name').innerHTML = userInput;

// ✅ DOBRZE - escapowanie
document.getElementById('name').textContent = userInput;

// React/Vue automatycznie escapują
<div>{userInput}</div>  // ✅ Bezpieczne

// Dla HTML używaj bibliotek
import DOMPurify from 'dompurify';
const clean = DOMPurify.sanitize(dirtyHTML);
```

### 6. CSRF Protection

```java
// Spring Security - CSRF włączony domyślnie
@Configuration
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        http
            .csrf()
                .csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse())
            .and()
            .authorizeRequests()
                .anyRequest().authenticated();
        return http.build();
    }
}
```

```javascript
// Frontend - wysyłanie CSRF tokenu
fetch('/api/users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRF-TOKEN': getCsrfToken() // z cookie lub meta tag
  },
  body: JSON.stringify(data)
});
```

### 7. Security Headers

```javascript
// Express Helmet
const helmet = require('helmet');
app.use(helmet());

// Ręcznie
app.use((req, res, next) => {
  // XSS Protection
  res.setHeader('X-XSS-Protection', '1; mode=block');
  
  // Prevent MIME type sniffing
  res.setHeader('X-Content-Type-Options', 'nosniff');
  
  // Clickjacking protection
  res.setHeader('X-Frame-Options', 'DENY');
  
  // Content Security Policy
  res.setHeader('Content-Security-Policy', 
    "default-src 'self'; script-src 'self' 'unsafe-inline'");
  
  // HSTS
  res.setHeader('Strict-Transport-Security', 
    'max-age=31536000; includeSubDomains');
  
  next();
});
```

### 8. API Key Rotation

```
Strategia:
1. Generuj nowy klucz
2. Oba klucze działają przez okres przejściowy (np. 30 dni)
3. Powiadom użytkowników
4. Dezaktywuj stary klucz
5. Usuń stary klucz

Automatyzacja:
• Klucze z datą wygaśnięcia
• Email notyfikacje
• Grace period
```

### 9. Logging i Monitoring

```java
@Slf4j
@RestControllerAdvice
public class SecurityLoggingAdvice {
    
    @Around("@annotation(secured)")
    public Object logSecurityEvent(ProceedingJoinPoint joinPoint) {
        String user = SecurityContextHolder.getContext()
            .getAuthentication().getName();
        String method = joinPoint.getSignature().getName();
        
        log.info("Security: User {} accessed {}", user, method);
        
        try {
            return joinPoint.proceed();
        } catch (Exception e) {
            log.warn("Security: Access denied for {} to {}", 
                    user, method);
            throw e;
        }
    }
}
```

### 10. Sensitive Data

```java
// ❌ ŹLE - zwracanie haseł w API
public class User {
    private String password;
    // getters/setters
}

// ✅ DOBRZE - @JsonIgnore
public class User {
    @JsonIgnore
    private String password;
}

// ✅ DOBRZE - DTOs
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    // NIE MA password!
}

// ✅ DOBRZE - maskowanie w logach
log.info("User email: {}", maskEmail(user.getEmail()));
// User email: j***@example.com
```

## 🎯 CORS Best Practices

```
✅ Specyfikuj dokładne origins (nie '*' w produkcji)
✅ Używaj credentials tylko gdy konieczne
✅ Krótki maxAge dla preflight cache
✅ Ograniczaj allowed methods
✅ Waliduj Origin na backendzie
✅ Różne konfiguracje dla dev/prod
❌ NIE używaj '*' z credentials: true
❌ NIE ufaj tylko CORS (waliduj na backendzie)
```

## 🔗 Powiązane Tematy

- [[Autentykacja i Autoryzacja API|🔐 Autentykacja]]
- [[API Security Best Practices|🔒 Security Best Practices]]
- [[Rate Limiting i Throttling|⏱️ Rate Limiting]]
- [[Spring Security - Podstawy Bezpieczeństwa]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~12 minut*

#cors #security #api-security #web-security #https
