# 🚪 API Gateway Pattern

## 📖 Definicja

**API Gateway** to single entry point dla wszystkich klientów, który agreguje i routing requests do odpowiednich microservices.

## 🎯 Problemy które rozwiązuje

```
❌ Klient musi znać wiele endpoints
❌ Cross-cutting concerns w każdym serwisie
❌ Różne protokoły dla różnych serwisów
❌ Trudne zarządzanie autentykacją
❌ Rate limiting per service
```

## 🏗️ Architektura

```
┌──────────┐
│  Client  │
└────┬─────┘
     │
     ↓
┌─────────────────┐
│   API Gateway   │  ← Single entry point
│                 │
│ • Routing       │
│ • Auth          │
│ • Rate Limiting │
│ • Caching       │
│ • Monitoring    │
└────┬────────────┘
     │
     ├──→ User Service
     ├──→ Order Service
     ├──→ Payment Service
     └──→ Notification Service
```

## 🎨 Funkcjonalności

### 1. Routing
```
GET /api/users/*      → User Service
GET /api/orders/*     → Order Service
GET /api/payments/*   → Payment Service
```

### 2. Authentication & Authorization
```
Wszystkie requesty przez gateway
↓
Sprawdzenie tokenu
↓
Dodanie user context do requestu
↓
Forward do service
```

### 3. Rate Limiting
```
Centralne zarządzanie limitami:
• Per user
• Per API key
• Per endpoint
```

### 4. Request/Response Transformation
```
Client → JSON → Gateway → gRPC → Service
Client ← JSON ← Gateway ← gRPC ← Service
```

### 5. Aggregation
```
GET /api/user-dashboard

Gateway:
1. Get user data (User Service)
2. Get orders (Order Service)
3. Get recommendations (Recommendation Service)
4. Aggregate & return
```

## 💻 Implementacje

### Spring Cloud Gateway

```java
@Configuration
public class GatewayConfig {
    
    @Bean
    public RouteLocator customRoutes(RouteLocatorBuilder builder) {
        return builder.routes()
            // User Service
            .route("user-service", r -> r
                .path("/api/users/**")
                .filters(f -> f
                    .stripPrefix(2)
                    .addRequestHeader("X-Gateway", "true")
                    .circuitBreaker(c -> c
                        .setName("userServiceCircuitBreaker")
                        .setFallbackUri("forward:/fallback/users"))
                    .retry(config -> config
                        .setRetries(3)
                        .setBackoff(Duration.ofSeconds(1), 
                                   Duration.ofSeconds(5), 
                                   2, true)))
                .uri("lb://user-service"))
            
            // Order Service
            .route("order-service", r -> r
                .path("/api/orders/**")
                .filters(f -> f
                    .stripPrefix(2)
                    .requestRateLimiter(c -> c
                        .setRateLimiter(redisRateLimiter())
                        .setKeyResolver(userKeyResolver())))
                .uri("lb://order-service"))
            
            // Authentication required
            .route("protected", r -> r
                .path("/api/admin/**")
                .filters(f -> f.filter(authenticationFilter()))
                .uri("lb://admin-service"))
            
            .build();
    }
    
    @Bean
    public RedisRateLimiter redisRateLimiter() {
        return new RedisRateLimiter(10, 20); // replenishRate, burstCapacity
    }
}

// Custom Filter
@Component
public class AuthenticationFilter implements GatewayFilter {
    
    @Autowired
    private JwtService jwtService;
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, 
                             GatewayFilterChain chain) {
        
        ServerHttpRequest request = exchange.getRequest();
        
        String token = request.getHeaders()
            .getFirst(HttpHeaders.AUTHORIZATION);
        
        if (token == null || !token.startsWith("Bearer ")) {
            return onError(exchange, "Missing authorization", 
                          HttpStatus.UNAUTHORIZED);
        }
        
        token = token.substring(7);
        
        if (!jwtService.validateToken(token)) {
            return onError(exchange, "Invalid token", 
                          HttpStatus.UNAUTHORIZED);
        }
        
        // Add user context to request
        String userId = jwtService.extractUserId(token);
        ServerHttpRequest modifiedRequest = request.mutate()
            .header("X-User-Id", userId)
            .build();
        
        return chain.filter(exchange.mutate()
            .request(modifiedRequest)
            .build());
    }
}
```

### Kong (Nginx-based)

```yaml
# kong.yml
_format_version: "2.1"

services:
  - name: user-service
    url: http://user-service:8080
    routes:
      - name: user-route
        paths:
          - /api/users
    plugins:
      - name: rate-limiting
        config:
          minute: 100
          hour: 1000
      - name: jwt
      - name: cors

  - name: order-service
    url: http://order-service:8080
    routes:
      - name: order-route
        paths:
          - /api/orders
    plugins:
      - name: key-auth
```

## 🔐 Security Features

```java
@Component
public class SecurityGatewayFilter implements GlobalFilter {
    
    @Override
    public Mono<Void> filter(ServerWebExchange exchange, 
                             GatewayFilterChain chain) {
        
        ServerHttpRequest request = exchange.getRequest();
        
        // 1. CORS
        if (CorsUtils.isPreFlightRequest(request)) {
            return handlePreFlight(exchange);
        }
        
        // 2. Rate Limiting
        if (isRateLimited(request)) {
            return onError(exchange, "Rate limit exceeded", 
                          HttpStatus.TOO_MANY_REQUESTS);
        }
        
        // 3. IP Whitelist/Blacklist
        String ip = request.getRemoteAddress().getAddress()
                          .getHostAddress();
        if (isBlocked(ip)) {
            return onError(exchange, "Access denied", 
                          HttpStatus.FORBIDDEN);
        }
        
        // 4. Request validation
        if (!isValidRequest(request)) {
            return onError(exchange, "Invalid request", 
                          HttpStatus.BAD_REQUEST);
        }
        
        return chain.filter(exchange);
    }
}
```

## ⚖️ Zalety i Wady

### Zalety
```
✅ Single entry point
✅ Centralne zarządzanie auth
✅ Cross-cutting concerns
✅ Protocol translation
✅ Monitoring i logging
✅ Rate limiting
✅ Caching
✅ Load balancing
```

### Wady
```
❌ Single point of failure
❌ Dodatkowy latency
❌ Complexity
❌ Może być bottleneck
```

## 🎯 Best Practices

```
✅ Make it stateless
✅ Circuit breakers
✅ Retry logic
✅ Timeout configuration
✅ Health checks
✅ Monitoring & alerting
✅ Horizontal scaling
✅ Connection pooling
❌ Nie dodawaj business logic
❌ Keep it simple
```

## 🔗 Powiązane Tematy

- [[Microservices i API|🔷 Microservices]]
- [[Rate Limiting i Throttling|⏱️ Rate Limiting]]
- [[API Security Best Practices|🔒 Security]]
- [[Caching w API|💾 Caching]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~8 minut*

#api-gateway #microservices #architecture #routing
