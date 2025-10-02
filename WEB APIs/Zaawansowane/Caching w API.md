# 💾 Caching w API

## 🎯 Po co Cache?

```
✅ Szybsze response times
✅ Mniejsze obciążenie bazy danych
✅ Mniej CPU usage
✅ Skalowalność
✅ Oszczędność kosztów
```

## 📊 Cache Levels

```
1. Browser Cache (Client)
2. CDN Cache
3. API Gateway Cache
4. Application Cache (Redis, Memcached)
5. Database Cache
```

## 🔧 HTTP Caching

### Cache-Control Headers
```http
# Public, cacheable przez wszystkich (CDN, proxy)
Cache-Control: public, max-age=3600

# Private, tylko browser cache
Cache-Control: private, max-age=3600

# No cache - zawsze rewaliduj
Cache-Control: no-cache

# No store - nie cachuj wcale
Cache-Control: no-store

# Kombinacje
Cache-Control: public, max-age=3600, must-revalidate
```

### ETag (Entity Tag)
```http
# Response
GET /api/users/1
Response:
ETag: "abc123"
Cache-Control: max-age=3600

# Subsequent request
GET /api/users/1
If-None-Match: "abc123"

# If not modified
Response: 304 Not Modified

# If modified
Response: 200 OK
ETag: "xyz789"
```

### Last-Modified
```http
# Response
Last-Modified: Mon, 15 Jan 2024 10:00:00 GMT

# Subsequent request
If-Modified-Since: Mon, 15 Jan 2024 10:00:00 GMT

# Response
304 Not Modified or 200 OK
```

## 💻 Application Caching

### Spring Boot + Redis

```java
// Configuration
@Configuration
@EnableCaching
public class CacheConfig {
    
    @Bean
    public RedisCacheManager cacheManager(
            RedisConnectionFactory connectionFactory) {
        
        RedisCacheConfiguration config = RedisCacheConfiguration
            .defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .serializeValuesWith(
                RedisSerializationContext.SerializationPair
                    .fromSerializer(new GenericJackson2JsonRedisSerializer())
            );
        
        return RedisCacheManager.builder(connectionFactory)
            .cacheDefaults(config)
            .build();
    }
}

// Service with caching
@Service
public class UserService {
    
    @Cacheable(value = "users", key = "#id")
    public User findById(Long id) {
        // Wywołane tylko jeśli nie ma w cache
        return userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException());
    }
    
    @CacheEvict(value = "users", key = "#id")
    public void deleteUser(Long id) {
        userRepository.deleteById(id);
    }
    
    @CachePut(value = "users", key = "#user.id")
    public User updateUser(User user) {
        return userRepository.save(user);
    }
    
    @Caching(evict = {
        @CacheEvict(value = "users", key = "#id"),
        @CacheEvict(value = "userList", allEntries = true)
    })
    public void delete(Long id) {
        userRepository.deleteById(id);
    }
}
```

## 🎨 Cache Strategies

### 1. Cache-Aside (Lazy Loading)
```
1. Check cache
2. If miss → load from DB
3. Store in cache
4. Return

Zalety: Tylko używane dane w cache
Wady: Cold start, cache miss penalty
```

### 2. Write-Through
```
1. Write to cache
2. Write to DB
3. Return

Zalety: Cache zawsze aktualny
Wady: Write latency
```

### 3. Write-Behind
```
1. Write to cache
2. Return
3. Async write to DB

Zalety: Szybki write
Wady: Możliwa utrata danych
```

### 4. Refresh-Ahead
```
Automatyczne odświeżanie przed expiry

Zalety: Zawsze fresh data
Wady: Więcej requestów
```

## 🔑 Cache Key Design

```java
// Bad
@Cacheable("users")
public User getUser(Long id) { ... }
// Key: wszystkie users w jednym

// Good
@Cacheable(value = "users", key = "#id")
public User getUser(Long id) { ... }
// Key: user:1, user:2, ...

// Better
@Cacheable(value = "users", 
          key = "T(String).format('user:%d', #id)")
public User getUser(Long id) { ... }
// Key: user:1, user:2, ...

// Complex key
@Cacheable(value = "userOrders",
          key = "#userId + ':' + #status + ':' + #page")
public List<Order> getUserOrders(Long userId, String status, int page) { ... }
// Key: 123:pending:1
```

## 🚀 Advanced Patterns

### Cache Warming
```java
@Component
public class CacheWarmer {
    
    @EventListener(ApplicationReadyEvent.class)
    public void warmCache() {
        // Preload frequently accessed data
        List<Product> popularProducts = 
            productService.getPopularProducts();
        
        popularProducts.forEach(product -> {
            cacheManager.getCache("products")
                .put(product.getId(), product);
        });
    }
}
```

### TTL per Entry
```java
public class CustomRedisCacheWriter {
    
    public void put(String key, Object value, Duration ttl) {
        redisTemplate.opsForValue()
            .set(key, value, ttl);
    }
}

// Usage
@Service
public class ProductService {
    
    public Product getProduct(Long id) {
        Product product = cacheManager.get(id);
        
        if (product == null) {
            product = productRepository.findById(id);
            
            // Hot products: 1 hour TTL
            // Cold products: 10 minutes TTL
            Duration ttl = product.isPopular() 
                ? Duration.ofHours(1)
                : Duration.ofMinutes(10);
            
            cacheWriter.put(id, product, ttl);
        }
        
        return product;
    }
}
```

## ⚠️ Cache Invalidation

```
"There are only two hard things in Computer Science: 
cache invalidation and naming things." - Phil Karlton
```

### Strategies
```java
// 1. Time-based (TTL)
@Cacheable(value = "users", key = "#id", 
          cacheManager = "cacheManagerWith10MinTTL")

// 2. Event-based
@Service
public class UserService {
    
    @Transactional
    public User updateUser(User user) {
        User updated = userRepository.save(user);
        
        // Invalidate cache
        cacheManager.getCache("users")
            .evict(user.getId());
        
        // Publish event
        eventPublisher.publishEvent(
            new UserUpdatedEvent(user.getId())
        );
        
        return updated;
    }
}

// 3. Pattern-based (Redis)
public void invalidateUserCaches(Long userId) {
    Set<String> keys = redisTemplate.keys("user:" + userId + ":*");
    if (keys != null && !keys.isEmpty()) {
        redisTemplate.delete(keys);
    }
}
```

## 🎯 Best Practices

```
✅ Cache immutable data
✅ Set appropriate TTL
✅ Monitor cache hit ratio
✅ Handle cache stampede
✅ Lazy load pattern
✅ Separate cache per data type
✅ Version cache keys
✅ Graceful degradation when cache fails
❌ Don't cache everything
❌ Don't ignore cache eviction
```

## 📊 Monitoring

```java
@Component
public class CacheMonitor {
    
    @Scheduled(fixedRate = 60000)
    public void logCacheStats() {
        Cache cache = cacheManager.getCache("users");
        CacheStatistics stats = cache.getNativeCache().getStatistics();
        
        double hitRatio = stats.getCacheHitRatio();
        log.info("Cache hit ratio: {}%", hitRatio * 100);
        
        if (hitRatio < 0.7) {
            // Alert: Low cache hit ratio
        }
    }
}
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[HTTP Metody i Kody Statusu|📮 HTTP]]
- [[API Gateway Pattern|🚪 API Gateway]]
- [[Microservices i API|🔷 Microservices]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~10 minut*

#caching #performance #redis #http-caching #optimization
