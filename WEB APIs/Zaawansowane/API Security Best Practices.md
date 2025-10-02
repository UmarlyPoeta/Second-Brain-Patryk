# 🔒 API Security Best Practices

## 🛡️ Authentication & Authorization

```
✅ JWT dla stateless auth
✅ OAuth 2.0 dla third-party
✅ API Keys dla server-to-server
✅ MFA dla critical operations
✅ Short-lived tokens
✅ Refresh token rotation
```

## 🔐 Transport Security

```
✅ HTTPS everywhere (TLS 1.3)
✅ HSTS headers
✅ Certificate pinning (mobile)
✅ Disable SSL/TLS older versions
```

## 🚫 Input Validation

```java
@RestController
public class UserController {
    
    @PostMapping("/users")
    public User createUser(@Valid @RequestBody CreateUserRequest request) {
        // Spring Boot auto-validates
        return userService.create(request);
    }
}

@Data
public class CreateUserRequest {
    @NotBlank
    @Size(min = 2, max = 50)
    private String name;
    
    @Email
    @NotBlank
    private String email;
    
    @Pattern(regexp = "^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[@#$%]).{8,}$")
    private String password;
}

// SQL Injection prevention
@Query("SELECT u FROM User u WHERE u.email = :email")
User findByEmail(@Param("email") String email);
```

## 🔑 Sensitive Data

```java
// ❌ ŹLE
public class User {
    private String password;
    private String ssn;
}

// ✅ DOBRZE
public class User {
    @JsonIgnore
    private String password;
    
    @JsonIgnore
    private String ssn;
}

// Lub używaj DTOs
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    // NO password, NO ssn
}
```

## ⏱️ Rate Limiting

```java
@RestController
public class ApiController {
    
    @GetMapping("/public")
    @RateLimit(requests = 100, per = "HOUR")
    public String publicData() { ... }
    
    @PostMapping("/auth/login")
    @RateLimit(requests = 5, per = "MINUTE")
    public String login() { ... }
}
```

## 🔍 Security Headers

```java
@Configuration
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        http.headers()
            .xssProtection()
            .and()
            .contentSecurityPolicy("default-src 'self'")
            .and()
            .frameOptions().deny()
            .and()
            .httpStrictTransportSecurity()
                .maxAgeInSeconds(31536000)
                .includeSubDomains(true);
        
        return http.build();
    }
}
```

## 🎯 OWASP Top 10 API

```
1. Broken Object Level Authorization
2. Broken Authentication
3. Broken Object Property Level Authorization
4. Unrestricted Resource Consumption
5. Broken Function Level Authorization
6. Unrestricted Access to Sensitive Business Flows
7. Server Side Request Forgery (SSRF)
8. Security Misconfiguration
9. Improper Inventory Management
10. Unsafe Consumption of APIs
```

## 🔗 Powiązane Tematy

- [[Autentykacja i Autoryzacja API|🔐 Auth]]
- [[CORS i Bezpieczeństwo|🛡️ CORS]]
- [[Rate Limiting i Throttling|⏱️ Rate Limiting]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~6 minut*

#security #api-security #best-practices #owasp
