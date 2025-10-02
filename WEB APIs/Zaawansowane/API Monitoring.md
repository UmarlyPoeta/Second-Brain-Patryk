# 📊 API Monitoring i Logging

## 🎯 Po co Monitoring?

```
✅ Wykrywanie problemów
✅ Performance optimization
✅ Capacity planning
✅ SLA tracking
✅ Security incidents
✅ Business metrics
```

## 📈 Kluczowe Metryki

### 1. Golden Signals
```
• Latency - czas odpowiedzi
• Traffic - liczba requestów
• Errors - error rate
• Saturation - wykorzystanie zasobów
```

### 2. RED Method
```
• Rate - requests per second
• Errors - error percentage
• Duration - response time percentiles
```

### 3. USE Method
```
• Utilization - % wykorzystania
• Saturation - queue length
• Errors - error count
```

## 💻 Implementation

### Spring Boot Actuator + Prometheus
```java
// application.properties
management.endpoints.web.exposure.include=*
management.metrics.export.prometheus.enabled=true

// Custom metrics
@Component
public class ApiMetrics {
    
    private final Counter apiCalls;
    private final Timer apiLatency;
    private final Gauge activeUsers;
    
    public ApiMetrics(MeterRegistry registry) {
        this.apiCalls = Counter.builder("api.calls")
            .description("Total API calls")
            .tag("endpoint", "users")
            .register(registry);
        
        this.apiLatency = Timer.builder("api.latency")
            .description("API response time")
            .register(registry);
        
        this.activeUsers = Gauge.builder("api.active.users",
                this::getActiveUserCount)
            .register(registry);
    }
    
    public void recordApiCall(String endpoint) {
        apiCalls.increment();
    }
    
    public void recordLatency(long duration) {
        apiLatency.record(duration, TimeUnit.MILLISECONDS);
    }
}

// Filter
@Component
public class MetricsFilter implements Filter {
    
    @Autowired
    private ApiMetrics metrics;
    
    @Override
    public void doFilter(ServletRequest request, 
                        ServletResponse response,
                        FilterChain chain) {
        long start = System.currentTimeMillis();
        
        try {
            chain.doFilter(request, response);
        } finally {
            long duration = System.currentTimeMillis() - start;
            metrics.recordLatency(duration);
            metrics.recordApiCall(request.getRequestURI());
        }
    }
}
```

## 📝 Structured Logging

```java
@Slf4j
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    public User getUser(@PathVariable Long id) {
        MDC.put("userId", id.toString());
        MDC.put("requestId", UUID.randomUUID().toString());
        
        log.info("Fetching user", 
            kv("userId", id),
            kv("action", "GET_USER"));
        
        try {
            User user = userService.findById(id);
            log.info("User fetched successfully");
            return user;
        } catch (Exception e) {
            log.error("Error fetching user", e);
            throw e;
        } finally {
            MDC.clear();
        }
    }
}
```

## 🔍 Distributed Tracing

### Spring Cloud Sleuth + Zipkin
```java
// Auto-instrumentation
@SpringBootApplication
public class Application {
    // Sleuth automatycznie dodaje trace IDs
}

// Log output:
// [app-name,trace-id,span-id,exportable]
// [user-service,abc123,def456,true] Fetching user
```

## 🚨 Alerting

```yaml
# Prometheus Alert Rules
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(api_errors_total[5m]) > 0.05
        for: 5m
        annotations:
          summary: "High error rate detected"
          
      - alert: SlowAPI
        expr: histogram_quantile(0.95, api_latency) > 1000
        for: 5m
        annotations:
          summary: "P95 latency > 1s"
```

## 🎯 Best Practices

```
✅ Log structured data (JSON)
✅ Include correlation IDs
✅ Monitor 4xx and 5xx separately
✅ Track P50, P95, P99 latencies
✅ Set up SLO/SLA monitoring
✅ Error budgets
✅ Real user monitoring (RUM)
```

## 🔗 Powiązane Tematy

- [[API Gateway Pattern|🚪 API Gateway]]
- [[Microservices i API|🔷 Microservices]]
- [[Error Handling|⚠️ Error Handling]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~6 minut*

#monitoring #logging #observability #metrics #prometheus
