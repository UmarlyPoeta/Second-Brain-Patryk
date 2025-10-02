# ⏱️ Rate Limiting i Throttling

## 📖 Definicje

### Rate Limiting
```
Ograniczanie liczby żądań od klienta w określonym czasie
Przykład: Max 100 requestów na minutę
```

### Throttling
```
Spowalnianie requestów gdy limit zostanie przekroczony
Zamiast odrzucić - opóźnij
```

## 🎯 Po co?

```
✅ Ochrona przed DDoS
✅ Kontrola kosztów infrastruktury
✅ Zapewnienie fair usage
✅ Ochrona przed botami
✅ SLA dla różnych klientów (free vs paid)
✅ Stabilność systemu
```

## 🔢 Strategie Rate Limiting

### 1. Token Bucket
```
Bucket z tokenami (np. 100)
• Każdy request = 1 token
• Bucket napełnia się stałą szybkością (np. 10/s)
• Brak tokenów = reject

Zalety:
✅ Pozwala na burst traffic
✅ Elastyczny
```

```java
// Guava RateLimiter (Token Bucket)
RateLimiter limiter = RateLimiter.create(10.0); // 10 req/s

if (limiter.tryAcquire()) {
    // Process request
} else {
    throw new RateLimitExceededException();
}
```

### 2. Fixed Window
```
Okno czasowe (np. 1 minuta)
• Counter dla okna
• Reset na początku nowego okna

00:00-01:00 → 100 requestów max
01:00-02:00 → reset, znowu 100

Wada: Burst na granicy okien
00:59 → 100 req
01:00 → 100 req (200 w 2 sekundy!)
```

### 3. Sliding Window
```
Płynnie przesuwające się okno
• Uwzględnia requesty z poprzedniego okna
• Dokładniejsze niż fixed window

Lepsze, ale bardziej złożone
```

### 4. Leaky Bucket
```
Bucket z dziurką na dole
• Requesty wchodzą na górze
• Wychodzą stałą szybkością przez dziurkę
• Przepełnienie = reject

Zalety:
✅ Gładki ruch wyjściowy
✅ Dobry dla backend protection
```

## 💻 Implementacje

### Spring Boot - Bucket4j

```java
// 1. Dependency
<dependency>
    <groupId>com.github.vladimir-bukhtoyarov</groupId>
    <artifactId>bucket4j-core</artifactId>
    <version>8.1.0</version>
</dependency>

// 2. Configuration
@Configuration
public class RateLimitConfig {
    
    @Bean
    public ConcurrentHashMap<String, Bucket> buckets() {
        return new ConcurrentHashMap<>();
    }
    
    public Bucket resolveBucket(String key) {
        return buckets().computeIfAbsent(key, k -> {
            Bandwidth limit = Bandwidth.classic(
                100, // capacity
                Refill.intervally(100, Duration.ofMinutes(1))
            );
            return Bucket.builder()
                .addLimit(limit)
                .build();
        });
    }
}

// 3. Interceptor
@Component
public class RateLimitInterceptor implements HandlerInterceptor {
    
    @Autowired
    private RateLimitConfig rateLimitConfig;
    
    @Override
    public boolean preHandle(HttpServletRequest request,
                            HttpServletResponse response,
                            Object handler) throws Exception {
        
        String key = getClientKey(request); // IP lub API key
        Bucket bucket = rateLimitConfig.resolveBucket(key);
        
        ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);
        
        if (probe.isConsumed()) {
            response.addHeader("X-Rate-Limit-Remaining", 
                String.valueOf(probe.getRemainingTokens()));
            return true;
        } else {
            long waitForRefill = probe.getNanosToWaitForRefill() / 1_000_000_000;
            response.addHeader("X-Rate-Limit-Retry-After-Seconds", 
                String.valueOf(waitForRefill));
            response.sendError(429, "Too many requests");
            return false;
        }
    }
    
    private String getClientKey(HttpServletRequest request) {
        String apiKey = request.getHeader("X-API-Key");
        if (apiKey != null) {
            return apiKey;
        }
        return request.getRemoteAddr(); // IP fallback
    }
}

// 4. Controller z custom limit
@RestController
public class ApiController {
    
    @GetMapping("/api/public")
    @RateLimit(requests = 10, per = "MINUTE")
    public ResponseEntity<?> publicEndpoint() {
        return ResponseEntity.ok("Data");
    }
    
    @GetMapping("/api/premium")
    @RateLimit(requests = 1000, per = "MINUTE")
    public ResponseEntity<?> premiumEndpoint() {
        return ResponseEntity.ok("Premium data");
    }
}
```

### Express.js - express-rate-limit

```javascript
const rateLimit = require('express-rate-limit');

// Basic rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // max 100 requests per windowMs
  message: 'Too many requests from this IP',
  standardHeaders: true, // Return rate limit info in headers
  legacyHeaders: false,
});

app.use('/api/', limiter);

// Different limits for different routes
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 login attempts
  skipSuccessfulRequests: true, // Nie licznik successful requests
});

app.post('/api/auth/login', authLimiter, loginController);

// Rate limit by API key
const apiLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: async (req) => {
    const apiKey = req.header('X-API-Key');
    const tier = await getUserTier(apiKey);
    
    return tier === 'premium' ? 1000 : 100;
  },
  keyGenerator: (req) => req.header('X-API-Key'),
});

app.use('/api/', apiLimiter);

// Redis store for distributed apps
const RedisStore = require('rate-limit-redis');
const redis = require('redis');

const redisClient = redis.createClient();

const redisLimiter = rateLimit({
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:',
  }),
  windowMs: 60 * 1000,
  max: 100,
});
```

### Redis-based (Sliding Window)

```java
@Service
public class RedisRateLimiter {
    
    @Autowired
    private StringRedisTemplate redisTemplate;
    
    public boolean isAllowed(String key, int maxRequests, Duration window) {
        String redisKey = "rate_limit:" + key;
        long now = System.currentTimeMillis();
        long windowStart = now - window.toMillis();
        
        // Usuń stare wpisy
        redisTemplate.opsForZSet().removeRangeByScore(redisKey, 0, windowStart);
        
        // Policz obecne requesty
        Long count = redisTemplate.opsForZSet().zCard(redisKey);
        
        if (count != null && count >= maxRequests) {
            return false;
        }
        
        // Dodaj nowy request
        redisTemplate.opsForZSet().add(redisKey, UUID.randomUUID().toString(), now);
        
        // Ustaw expiration
        redisTemplate.expire(redisKey, window);
        
        return true;
    }
}
```

## 📊 Response Headers

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 87
X-RateLimit-Reset: 1234567890

HTTP/1.1 429 Too Many Requests
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1234567890
Retry-After: 60
```

## 🎨 Tier-based Limits

```java
public enum UserTier {
    FREE(100, Duration.ofHours(1)),
    BASIC(1000, Duration.ofHours(1)),
    PREMIUM(10000, Duration.ofHours(1)),
    ENTERPRISE(100000, Duration.ofHours(1));
    
    private final int requests;
    private final Duration window;
    
    UserTier(int requests, Duration window) {
        this.requests = requests;
        this.window = window;
    }
}

@Service
public class TieredRateLimiter {
    
    public boolean isAllowed(User user) {
        UserTier tier = user.getTier();
        return rateLimiter.isAllowed(
            user.getId(),
            tier.getRequests(),
            tier.getWindow()
        );
    }
}
```

## 🔐 Best Practices

```
✅ Różne limity dla różnych endpointów
✅ Wyższe limity dla authenticated users
✅ Tier-based limits (free/paid)
✅ Graceful degradation
✅ Informacyjne error messages
✅ Headers z rate limit info
✅ Monitoring i alerting
✅ Whitelist dla ważnych klientów
✅ Blacklist dla abuse
✅ Distributed rate limiting (Redis)
```

## 🚨 Handling Rate Limit na Kliencie

```javascript
async function apiCallWithRetry(url, options = {}, maxRetries = 3) {
  let retries = 0;
  
  while (retries < maxRetries) {
    try {
      const response = await fetch(url, options);
      
      if (response.status === 429) {
        const retryAfter = response.headers.get('Retry-After');
        const delay = retryAfter ? parseInt(retryAfter) * 1000 : 1000 * Math.pow(2, retries);
        
        console.log(`Rate limited. Retrying after ${delay}ms...`);
        await sleep(delay);
        retries++;
        continue;
      }
      
      return response;
    } catch (error) {
      if (retries === maxRetries - 1) throw error;
      retries++;
    }
  }
  
  throw new Error('Max retries exceeded');
}
```

## 🔗 Powiązane Tematy

- [[CORS i Bezpieczeństwo|🛡️ CORS]]
- [[API Security Best Practices|🔒 Security]]
- [[API Monitoring|📊 Monitoring]]
- [[REST API - Podstawy|🔰 REST API]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~8 minut*

#rate-limiting #throttling #api-protection #security
