# 🔐 Autentykacja i Autoryzacja API

## 🔑 Definicje

### Autentykacja (Authentication)
```
Kim jesteś? → Weryfikacja tożsamości użytkownika

Przykłady:
• Login + hasło
• Token JWT
• API Key
• OAuth
```

### Autoryzacja (Authorization)
```
Co możesz robić? → Sprawdzenie uprawnień

Przykłady:
• User może czytać swoje dane
• Admin może usuwać użytkowników
• Guest może tylko przeglądać
```

### Różnica
```
┌─────────────────┐
│  Autentykacja   │ "Jesteś Jan Kowalski?"
└────────┬────────┘
         │ ✓ TAK
         ↓
┌─────────────────┐
│  Autoryzacja    │ "Czy Jan może usunąć ten zasób?"
└─────────────────┘
```

## 🎫 Metody Autentykacji

### 1. Basic Authentication

**Format:**
```http
GET /api/users HTTP/1.1
Authorization: Basic dXNlcjpwYXNzd29yZA==

# Base64 encode("user:password") → dXNlcjpwYXNzd29yZA==
```

**Implementacja:**
```javascript
// JavaScript
const credentials = btoa('user:password');
fetch('/api/users', {
  headers: {
    'Authorization': `Basic ${credentials}`
  }
});
```

```java
// Java (Spring Security)
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        http.httpBasic()
            .and()
            .authorizeRequests()
            .anyRequest().authenticated();
        return http.build();
    }
}
```

**Wady:**
```
❌ Hasło w każdym requeście
❌ Łatwe do dekodowania (base64)
❌ Wymaga HTTPS
❌ Brak wygaśnięcia sesji
```

### 2. API Keys

**Format:**
```http
GET /api/users HTTP/1.1
X-API-Key: abc123def456ghi789jkl

# Lub w query string (niezalecane)
GET /api/users?api_key=abc123def456ghi789jkl
```

**Najlepsze praktyki:**
```
✅ Używaj custom header (X-API-Key)
✅ Długie, losowe klucze (min. 32 znaki)
✅ Możliwość odwołania
✅ Rate limiting per key
✅ Monitoring użycia
❌ NIE w query string (logi!)
❌ NIE hardcode w kodzie
```

**Przykład użycia:**
```javascript
// JavaScript
fetch('/api/users', {
  headers: {
    'X-API-Key': process.env.API_KEY
  }
});
```

```python
# Python
import os
import requests

headers = {'X-API-Key': os.getenv('API_KEY')}
response = requests.get('/api/users', headers=headers)
```

### 3. Bearer Token (JWT)

**Format:**
```http
GET /api/users HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Struktura JWT:**
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.     ← Header
eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6Ikph.  ← Payload
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c  ← Signature
```

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "sub": "1234567890",
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "roles": ["user", "admin"],
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature:**
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret
)
```

**Flow JWT:**
```
1. Login → POST /api/auth/login
   {username, password}

2. Serwer weryfikuje → zwraca JWT
   {token: "eyJhbGci...", expiresIn: 3600}

3. Klient zapisuje token (localStorage/sessionStorage)

4. Każdy request → Authorization: Bearer {token}

5. Serwer weryfikuje token → dostęp lub 401
```

**Implementacja:**

```javascript
// JavaScript - Login
async function login(username, password) {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({username, password})
  });
  
  const {token} = await response.json();
  localStorage.setItem('token', token);
  return token;
}

// Użycie tokenu
async function getUsers() {
  const token = localStorage.getItem('token');
  const response = await fetch('/api/users', {
    headers: {'Authorization': `Bearer ${token}`}
  });
  return response.json();
}
```

```java
// Java - Generowanie JWT
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;

public String generateToken(User user) {
    return Jwts.builder()
        .setSubject(user.getUsername())
        .claim("roles", user.getRoles())
        .setIssuedAt(new Date())
        .setExpiration(new Date(System.currentTimeMillis() + 3600000))
        .signWith(SignatureAlgorithm.HS512, SECRET_KEY)
        .compact();
}

// Walidacja JWT
public boolean validateToken(String token) {
    try {
        Jwts.parser()
            .setSigningKey(SECRET_KEY)
            .parseClaimsJws(token);
        return true;
    } catch (Exception e) {
        return false;
    }
}
```

**Zalety JWT:**
```
✅ Stateless (server nie przechowuje sesji)
✅ Skalowalność
✅ Cross-domain (CORS-friendly)
✅ Mobile-friendly
✅ Zawiera dane użytkownika (claims)
```

**Wady JWT:**
```
❌ Nie można odwołać (do expiry)
❌ Rozmiar (większy niż session ID)
❌ Wymaga bezpiecznego przechowywania (XSS)
❌ Refresh token pattern wymagany
```

### 4. OAuth 2.0

**Scenariusz:** "Sign in with Google/Facebook"

**Role:**
```
Resource Owner → Użytkownik
Client → Nasza aplikacja
Authorization Server → Google/Facebook
Resource Server → API Google/Facebook
```

**Authorization Code Flow:**
```
1. User klika "Login with Google"
   ↓
2. Redirect do Google:
   https://accounts.google.com/oauth/authorize?
     client_id=abc123&
     redirect_uri=https://myapp.com/callback&
     response_type=code&
     scope=email profile

3. User loguje się i wyraża zgodę
   ↓
4. Google redirects z kodem:
   https://myapp.com/callback?code=xyz789

5. Aplikacja wymienia kod na token:
   POST https://oauth2.googleapis.com/token
   {
     grant_type: "authorization_code",
     code: "xyz789",
     client_id: "abc123",
     client_secret: "secret",
     redirect_uri: "https://myapp.com/callback"
   }

6. Google zwraca access_token:
   {
     access_token: "ya29.a0...",
     expires_in: 3600,
     refresh_token: "1//...",
     token_type: "Bearer"
   }

7. Używaj access_token do API:
   GET https://www.googleapis.com/oauth2/v1/userinfo
   Authorization: Bearer ya29.a0...
```

**OAuth Scopes:**
```
• email - dostęp do emaila
• profile - dane profilu
• openid - OpenID Connect
• read:users - czytanie użytkowników
• write:posts - tworzenie postów
```

**Implementacja (Spring Boot):**
```java
@Configuration
@EnableOAuth2Client
public class OAuth2Config {
    
    @Bean
    public OAuth2RestTemplate oauth2RestTemplate() {
        return new OAuth2RestTemplate(
            googleResource(), oauth2ClientContext);
    }
    
    @Bean
    @ConfigurationProperties("google.client")
    public AuthorizationCodeResourceDetails googleResource() {
        return new AuthorizationCodeResourceDetails();
    }
}
```

### 5. OpenID Connect

**OIDC = OAuth 2.0 + Identity Layer**

```
OAuth 2.0: "Daj mi dostęp do API"
OpenID Connect: "Kim jest użytkownik?"
```

**ID Token (JWT):**
```json
{
  "iss": "https://accounts.google.com",
  "sub": "110169484474386276334",
  "azp": "1234.apps.googleusercontent.com",
  "aud": "1234.apps.googleusercontent.com",
  "iat": 1516239022,
  "exp": 1516242622,
  "email": "jan@example.com",
  "email_verified": true,
  "name": "Jan Kowalski",
  "picture": "https://..."
}
```

## 🔐 Autoryzacja

### Role-Based Access Control (RBAC)

```java
// Definicja ról
enum Role {
    GUEST,    // może czytać publiczne
    USER,     // może czytać własne dane
    ADMIN,    // pełny dostęp
    MODERATOR // może moderować
}

// Spring Security
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/users/{id}")
public void deleteUser(@PathVariable Long id) {
    userService.delete(id);
}

@PreAuthorize("hasAnyRole('USER', 'ADMIN')")
@GetMapping("/users/me")
public User getCurrentUser() {
    return userService.getCurrentUser();
}
```

### Permission-Based (Fine-grained)

```java
// Szczegółowe uprawnienia
@PreAuthorize("hasPermission(#userId, 'User', 'DELETE')")
@DeleteMapping("/users/{userId}")
public void deleteUser(@PathVariable Long userId) {
    userService.delete(userId);
}

// Custom permission evaluator
public class CustomPermissionEvaluator 
        implements PermissionEvaluator {
    
    @Override
    public boolean hasPermission(Authentication auth,
            Object targetDomainObject, Object permission) {
        
        User user = (User) auth.getPrincipal();
        String perm = (String) permission;
        
        // Własna logika autoryzacji
        return checkPermission(user, targetDomainObject, perm);
    }
}
```

### Attribute-Based Access Control (ABAC)

```
Decyzja = f(
    Atrybuty użytkownika,
    Atrybuty zasobu,
    Atrybuty środowiska,
    Akcja
)

Przykład:
User.department == Resource.department 
  AND User.clearance >= Resource.classification
  AND Time.now BETWEEN 9:00 AND 17:00
  AND Action == "read"
```

## 🛡️ Best Practices

### Bezpieczeństwo
```
✅ Zawsze HTTPS dla produkcji
✅ Krótki czas wygaśnięcia tokenów (15-60 min)
✅ Refresh token dla długotrwałych sesji
✅ Rate limiting na endpointy auth
✅ Hashowanie haseł (bcrypt, Argon2)
✅ CSRF protection
✅ Logowanie prób uwierzytelniania
```

### Przechowywanie Tokenów
```
✅ httpOnly cookies (najlepsze dla web)
✅ Secure storage (iOS Keychain, Android KeyStore)
✅ sessionStorage dla short-lived
⚠️ localStorage (podatne na XSS)
❌ NIE w URL
❌ NIE hardcode w kodzie
```

### Error Messages
```
❌ ŹLE:
"User 'jan' not found"
"Invalid password for user 'jan'"

✅ DOBRZE:
"Invalid username or password"
"Authentication failed"

Powód: Nie ujawniaj czy user istnieje!
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[CORS i Bezpieczeństwo|🛡️ CORS]]
- [[API Security Best Practices|🔒 Security]]
- [[Spring Security - Podstawy Bezpieczeństwa]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~15 minut*

#authentication #authorization #jwt #oauth #api-security
