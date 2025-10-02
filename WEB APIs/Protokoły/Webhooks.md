# 🔔 Webhooks - Event-Driven API

## 📖 Definicja

**Webhook** to mechanizm komunikacji, w którym aplikacja wysyła automatyczne powiadomienia HTTP POST do innej aplikacji, gdy następuje określone zdarzenie. Jest to "reverse API" - zamiast pytać o dane (polling), otrzymujesz je automatycznie (push).

## 🔄 Polling vs Webhooks

### Polling (Tradycyjne)
```
Client: "Są nowe dane?"         [Request]
Server: "Nie"                   [Response]

(po 30 sekundach)
Client: "A teraz są nowe dane?" [Request]
Server: "Nie"                   [Response]

(po 30 sekundach)
Client: "A teraz?"              [Request]
Server: "Tak! Oto dane."        [Response]

Wady:
❌ Wiele niepotrzebnych requestów
❌ Opóźnienie w otrzymaniu danych
❌ Marnowanie zasobów
```

### Webhooks (Event-Driven)
```
Server: (event occurs)
Server: POST /webhook → Client  [Natychmiastowe powiadomienie]
Client: "OK, otrzymałem"        [Response]

Zalety:
✅ Real-time
✅ Efektywne
✅ Tylko gdy coś się dzieje
```

## 🎯 Jak Działają Webhooks

### Flow
```
1. Rejestracja Webhooka
   Client → POST /api/webhooks
   {
     "url": "https://myapp.com/webhook",
     "events": ["user.created", "user.deleted"]
   }

2. Zdarzenie Następuje
   User zostaje utworzony na serwerze

3. Webhook Trigger
   Server → POST https://myapp.com/webhook
   {
     "event": "user.created",
     "data": {...}
   }

4. Client Przetwarza
   Client → 200 OK (potwierdzenie otrzymania)

5. Retry (jeśli błąd)
   Jeśli client nie odpowiada → retry po 1min, 5min, 15min...
```

## 💻 Implementacja Provider (Serwer)

### Spring Boot - Webhook Provider

```java
// 1. Model Webhooka
@Entity
public class Webhook {
    @Id
    @GeneratedValue
    private Long id;
    
    private String url;
    
    @ElementCollection
    private Set<String> events;
    
    private String secret; // dla HMAC signature
    
    private boolean active = true;
    
    @Column(name = "retry_count")
    private int retryCount = 0;
    
    @Column(name = "last_triggered")
    private LocalDateTime lastTriggered;
    
    // getters/setters
}

// 2. Webhook Repository
public interface WebhookRepository extends JpaRepository<Webhook, Long> {
    List<Webhook> findByEventsContainingAndActiveTrue(String event);
}

// 3. Webhook Service
@Service
@Slf4j
public class WebhookService {
    
    @Autowired
    private WebhookRepository webhookRepository;
    
    @Autowired
    private RestTemplate restTemplate;
    
    @Async
    public void trigger(String event, Object payload) {
        List<Webhook> webhooks = webhookRepository
            .findByEventsContainingAndActiveTrue(event);
        
        for (Webhook webhook : webhooks) {
            sendWebhook(webhook, event, payload);
        }
    }
    
    private void sendWebhook(Webhook webhook, String event, Object payload) {
        try {
            WebhookPayload webhookPayload = new WebhookPayload(
                UUID.randomUUID().toString(),
                event,
                Instant.now(),
                payload
            );
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            // Dodaj HMAC signature dla bezpieczeństwa
            String signature = generateSignature(
                webhook.getSecret(), 
                webhookPayload
            );
            headers.set("X-Webhook-Signature", signature);
            
            HttpEntity<WebhookPayload> request = 
                new HttpEntity<>(webhookPayload, headers);
            
            ResponseEntity<String> response = restTemplate.postForEntity(
                webhook.getUrl(), 
                request, 
                String.class
            );
            
            if (response.getStatusCode().is2xxSuccessful()) {
                log.info("Webhook sent successfully to {}", webhook.getUrl());
                webhook.setLastTriggered(LocalDateTime.now());
                webhook.setRetryCount(0);
                webhookRepository.save(webhook);
            } else {
                handleFailure(webhook);
            }
            
        } catch (Exception e) {
            log.error("Failed to send webhook to {}", webhook.getUrl(), e);
            handleFailure(webhook);
        }
    }
    
    private void handleFailure(Webhook webhook) {
        webhook.setRetryCount(webhook.getRetryCount() + 1);
        
        // Dezaktywuj po 5 nieudanych próbach
        if (webhook.getRetryCount() >= 5) {
            webhook.setActive(false);
            log.warn("Webhook {} deactivated after 5 failed attempts", 
                    webhook.getUrl());
        }
        
        webhookRepository.save(webhook);
        
        // Zaplanuj retry
        scheduleRetry(webhook);
    }
    
    @Async
    public void scheduleRetry(Webhook webhook) {
        // Exponential backoff: 1min, 5min, 15min, 1h, 24h
        int[] delays = {60, 300, 900, 3600, 86400};
        int retryIndex = Math.min(
            webhook.getRetryCount() - 1, 
            delays.length - 1
        );
        
        try {
            Thread.sleep(delays[retryIndex] * 1000L);
            // Retry webhook
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
    
    private String generateSignature(String secret, Object payload) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKey = new SecretKeySpec(
                secret.getBytes(), 
                "HmacSHA256"
            );
            mac.init(secretKey);
            
            String json = new ObjectMapper().writeValueAsString(payload);
            byte[] hmac = mac.doFinal(json.getBytes());
            
            return Base64.getEncoder().encodeToString(hmac);
        } catch (Exception e) {
            throw new RuntimeException("Failed to generate signature", e);
        }
    }
}

// 4. Webhook Payload
@Data
@AllArgsConstructor
public class WebhookPayload {
    private String id;
    private String event;
    private Instant timestamp;
    private Object data;
}

// 5. Controller dla zarządzania webhookami
@RestController
@RequestMapping("/api/webhooks")
public class WebhookController {
    
    @Autowired
    private WebhookService webhookService;
    
    @Autowired
    private WebhookRepository webhookRepository;
    
    @PostMapping
    public ResponseEntity<Webhook> register(
            @RequestBody CreateWebhookRequest request) {
        
        Webhook webhook = new Webhook();
        webhook.setUrl(request.getUrl());
        webhook.setEvents(request.getEvents());
        webhook.setSecret(generateSecret());
        
        webhook = webhookRepository.save(webhook);
        return ResponseEntity.status(HttpStatus.CREATED).body(webhook);
    }
    
    @GetMapping
    public List<Webhook> list() {
        return webhookRepository.findAll();
    }
    
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {
        webhookRepository.deleteById(id);
        return ResponseEntity.noContent().build();
    }
    
    private String generateSecret() {
        return UUID.randomUUID().toString();
    }
}

// 6. Użycie w serwisie
@Service
public class UserService {
    
    @Autowired
    private WebhookService webhookService;
    
    public User createUser(CreateUserRequest request) {
        User user = userRepository.save(
            new User(request.getName(), request.getEmail())
        );
        
        // Trigger webhook
        webhookService.trigger("user.created", user);
        
        return user;
    }
    
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException());
        
        userRepository.deleteById(id);
        
        // Trigger webhook
        webhookService.trigger("user.deleted", 
            Map.of("id", id, "name", user.getName())
        );
    }
}
```

## 📥 Implementacja Consumer (Klient)

### Endpoint do Odbierania Webhooków

```java
@RestController
@RequestMapping("/webhook")
@Slf4j
public class WebhookReceiverController {
    
    private static final String WEBHOOK_SECRET = "your-secret-here";
    
    @PostMapping
    public ResponseEntity<String> handleWebhook(
            @RequestBody WebhookPayload payload,
            @RequestHeader("X-Webhook-Signature") String signature) {
        
        // 1. Weryfikacja signature
        if (!verifySignature(payload, signature)) {
            log.warn("Invalid webhook signature");
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED)
                .body("Invalid signature");
        }
        
        // 2. Idempotency check (zapobieganie duplikatom)
        if (wasAlreadyProcessed(payload.getId())) {
            log.info("Webhook {} already processed", payload.getId());
            return ResponseEntity.ok("Already processed");
        }
        
        // 3. Przetwarzanie asynchroniczne
        processWebhookAsync(payload);
        
        // 4. Szybkie potwierdzenie (< 5s)
        return ResponseEntity.ok("Webhook received");
    }
    
    private boolean verifySignature(WebhookPayload payload, String signature) {
        try {
            Mac mac = Mac.getInstance("HmacSHA256");
            SecretKeySpec secretKey = new SecretKeySpec(
                WEBHOOK_SECRET.getBytes(), 
                "HmacSHA256"
            );
            mac.init(secretKey);
            
            String json = new ObjectMapper().writeValueAsString(payload);
            byte[] hmac = mac.doFinal(json.getBytes());
            String computed = Base64.getEncoder().encodeToString(hmac);
            
            return MessageDigest.isEqual(
                signature.getBytes(), 
                computed.getBytes()
            );
        } catch (Exception e) {
            return false;
        }
    }
    
    private boolean wasAlreadyProcessed(String webhookId) {
        // Sprawdź w bazie czy już przetworzony
        return processedWebhookRepository.existsById(webhookId);
    }
    
    @Async
    public void processWebhookAsync(WebhookPayload payload) {
        try {
            // Zapisz jako przetworzony
            processedWebhookRepository.save(
                new ProcessedWebhook(payload.getId())
            );
            
            // Przetwarzanie w zależności od eventu
            switch (payload.getEvent()) {
                case "user.created":
                    handleUserCreated(payload.getData());
                    break;
                case "user.deleted":
                    handleUserDeleted(payload.getData());
                    break;
                case "payment.succeeded":
                    handlePaymentSucceeded(payload.getData());
                    break;
                default:
                    log.warn("Unknown event: {}", payload.getEvent());
            }
            
        } catch (Exception e) {
            log.error("Error processing webhook", e);
            // Nie rzucaj wyjątku - już odpowiedzieliśmy 200 OK
        }
    }
    
    private void handleUserCreated(Object data) {
        log.info("Processing user.created event: {}", data);
        // Twoja logika biznesowa
    }
}
```

### Node.js/Express Example

```javascript
const express = require('express');
const crypto = require('crypto');

const app = express();
app.use(express.json());

const WEBHOOK_SECRET = 'your-secret-here';
const processedWebhooks = new Set();

app.post('/webhook', async (req, res) => {
  const signature = req.headers['x-webhook-signature'];
  const payload = req.body;
  
  // 1. Verify signature
  if (!verifySignature(payload, signature)) {
    return res.status(401).send('Invalid signature');
  }
  
  // 2. Idempotency check
  if (processedWebhooks.has(payload.id)) {
    return res.status(200).send('Already processed');
  }
  
  // 3. Quick acknowledgment
  res.status(200).send('Webhook received');
  
  // 4. Process asynchronously
  processWebhook(payload).catch(err => {
    console.error('Webhook processing error:', err);
  });
});

function verifySignature(payload, signature) {
  const hmac = crypto.createHmac('sha256', WEBHOOK_SECRET);
  hmac.update(JSON.stringify(payload));
  const computed = hmac.digest('base64');
  
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(computed)
  );
}

async function processWebhook(payload) {
  processedWebhooks.add(payload.id);
  
  switch(payload.event) {
    case 'user.created':
      await handleUserCreated(payload.data);
      break;
    case 'user.deleted':
      await handleUserDeleted(payload.data);
      break;
  }
}

app.listen(3000, () => {
  console.log('Webhook receiver listening on port 3000');
});
```

## 🔐 Bezpieczeństwo

### 1. HMAC Signature
```
• Provider generuje signature używając secret key
• Signature wysyłany w headerze
• Receiver weryfikuje signature przed przetworzeniem
```

### 2. HTTPS Only
```
✅ Zawsze używaj HTTPS dla webhooków
❌ NIE używaj HTTP (man-in-the-middle attack)
```

### 3. IP Whitelisting
```java
@Component
public class WebhookSecurityFilter extends OncePerRequestFilter {
    
    private static final Set<String> ALLOWED_IPS = Set.of(
        "192.168.1.100",
        "10.0.0.5"
    );
    
    @Override
    protected void doFilterInternal(HttpServletRequest request,
                                   HttpServletResponse response,
                                   FilterChain filterChain) {
        String ip = request.getRemoteAddr();
        
        if (!ALLOWED_IPS.contains(ip)) {
            response.setStatus(HttpStatus.FORBIDDEN.value());
            return;
        }
        
        filterChain.doFilter(request, response);
    }
}
```

### 4. Idempotency
```
• Zapisuj ID przetworzonych webhooków
• Sprawdzaj przed przetworzeniem
• Zapobiega duplikatom przy retry
```

## 📋 Best Practices

### Provider (Wysyłający)
```
✅ Retry z exponential backoff
✅ Timeout dla requestów (5-10s)
✅ Loguj wszystkie webhooki
✅ Dashboard dla zarządzania
✅ Test endpoint dla developerów
✅ Webhook signing (HMAC)
✅ Rate limiting
✅ Dokumentacja eventów
```

### Consumer (Odbierający)
```
✅ Odpowiadaj szybko (< 5s)
✅ Przetwarzaj asynchronicznie
✅ Weryfikuj signature
✅ Idempotency handling
✅ HTTPS tylko
✅ Loguj wszystkie webhooki
✅ Monitoring i alerting
✅ Graceful degradation
```

## 🎯 Popularne Przypadki Użycia

### Payment Processing
```
Stripe → webhook → Your app
Events:
• payment.succeeded
• payment.failed
• subscription.created
• invoice.paid
```

### CI/CD
```
GitHub → webhook → CI server
Events:
• push
• pull_request
• release
```

### E-commerce
```
Shop → webhook → Shipping service
Events:
• order.created
• order.cancelled
• order.shipped
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[WebSockets|🔌 WebSockets]]
- [[API Security Best Practices|🔒 Security]]
- [[Microservices i API|🔷 Microservices]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~10 minut*

#webhooks #event-driven #real-time #api #push-notifications
