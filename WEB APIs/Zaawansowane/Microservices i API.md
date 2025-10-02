# 🔷 Microservices i API

## 📖 Definicja

**Microservices** to architektura, gdzie aplikacja składa się z małych, niezależnych serwisów komunikujących się przez API.

## 🏗️ Architektura

```
Monolith:
┌──────────────────────────┐
│                          │
│  ┌─────┐ ┌──────┐       │
│  │Users│ │Orders│ ...   │
│  └─────┘ └──────┘       │
│                          │
│     Single Database      │
└──────────────────────────┘

Microservices:
┌──────────┐  ┌───────────┐  ┌─────────┐
│  User    │  │  Order    │  │ Payment │
│  Service │  │  Service  │  │ Service │
│          │  │           │  │         │
│  DB      │  │  DB       │  │  DB     │
└────┬─────┘  └─────┬─────┘  └────┬────┘
     │              │              │
     └──────────────┼──────────────┘
              API Calls
```

## 🔄 Inter-Service Communication

### 1. Synchronous (REST/gRPC)
```
User Service → [HTTP] → Order Service
            ← [Response]

Zalety: Prosty, natychmiastowy
Wady: Coupling, cascading failures
```

### 2. Asynchronous (Message Queue)
```
User Service → [Event: UserCreated] → Queue
                                        ↓
                            Order Service otrzymuje event
                            
Zalety: Loose coupling, resilient
Wady: Eventual consistency
```

## 💻 Przykład Implementation

### Service A (User Service)
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @Autowired
    private OrderServiceClient orderClient;
    
    @GetMapping("/{id}/orders")
    public ResponseEntity<UserOrdersResponse> getUserOrders(
            @PathVariable Long id) {
        
        // 1. Get user
        User user = userService.findById(id);
        
        // 2. Call Order Service
        List<Order> orders = orderClient.getOrdersByUserId(id);
        
        // 3. Aggregate response
        return ResponseEntity.ok(
            new UserOrdersResponse(user, orders)
        );
    }
}

// Feign Client
@FeignClient(name = "order-service")
public interface OrderServiceClient {
    
    @GetMapping("/api/orders/user/{userId}")
    List<Order> getOrdersByUserId(@PathVariable Long userId);
}
```

### Service B (Order Service)
```java
@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    @GetMapping("/user/{userId}")
    public List<Order> getOrdersByUserId(@PathVariable Long userId) {
        return orderService.findByUserId(userId);
    }
}
```

## 🎯 Patterns

### 1. API Gateway
```
Client → API Gateway → Services
       (Single entry point)
```

### 2. Service Discovery
```java
// Eureka Server
@SpringBootApplication
@EnableEurekaServer
public class ServiceRegistryApplication {
    // ...
}

// Service registration
@SpringBootApplication
@EnableDiscoveryClient
public class UserServiceApplication {
    // Automatycznie rejestruje się w Eureka
}

// Client lookup
@Autowired
private DiscoveryClient discoveryClient;

List<ServiceInstance> instances = 
    discoveryClient.getInstances("order-service");
```

### 3. Circuit Breaker
```java
@Service
public class OrderServiceClient {
    
    @CircuitBreaker(name = "orderService", 
                   fallbackMethod = "fallback")
    public List<Order> getOrders(Long userId) {
        return restTemplate.getForObject(
            "http://order-service/orders/" + userId,
            List.class
        );
    }
    
    public List<Order> fallback(Long userId, Exception ex) {
        // Fallback logic
        return Collections.emptyList();
    }
}
```

### 4. Saga Pattern (Distributed Transactions)
```
Order Created
  ↓
Reserve Inventory → Success
  ↓
Process Payment → Success
  ↓
Send Notification → Success
  ↓
Order Completed

Jeśli błąd:
  ↓
Compensating transactions (rollback)
```

## ⚡ Zalety i Wady

### Zalety
```
✅ Independent deployment
✅ Technology diversity
✅ Scalability per service
✅ Fault isolation
✅ Team autonomy
```

### Wady
```
❌ Distributed system complexity
❌ Network latency
❌ Data consistency
❌ Testing harder
❌ Monitoring challenge
❌ Operational overhead
```

## 🎯 Best Practices

```
✅ Domain-driven design
✅ Single responsibility
✅ API versioning
✅ Circuit breakers
✅ Health checks
✅ Distributed tracing
✅ Centralized logging
✅ Service mesh (Istio)
✅ Container orchestration (K8s)
```

## 🔗 Powiązane Tematy

- [[API Gateway Pattern|🚪 API Gateway]]
- [[gRPC Protocol|⚡ gRPC]]
- [[REST API - Podstawy|🔰 REST]]
- [[API Monitoring|📊 Monitoring]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~8 minut*

#microservices #distributed-systems #architecture #api
