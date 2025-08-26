# 🌱 Spring Core - Dependency Injection

## 📚 Wprowadzenie
Spring Core to fundament całego ekosystemu Spring. Główną funkcją jest Dependency Injection (DI) i Inversion of Control (IoC), które pozwalają na tworzenie luźno sprzężonych, testowalnych aplikacji. Spring Container zarządza cyklem życia obiektów i ich zależnościami.

## 🏗️ Podstawy IoC Container

### ApplicationContext i Bean Factory
```java
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

// Service classes
public interface MessageService {
    String getMessage();
}

public class EmailService implements MessageService {
    @Override
    public String getMessage() {
        return "Email message sent!";
    }
}

public class SMSService implements MessageService {
    @Override
    public String getMessage() {
        return "SMS message sent!";
    }
}

public class MessageProcessor {
    private MessageService messageService;
    
    public MessageProcessor(MessageService messageService) {
        this.messageService = messageService;
    }
    
    public void processMessage() {
        System.out.println("Processing: " + messageService.getMessage());
    }
}

// Configuration class
@Configuration
public class AppConfig {
    
    @Bean
    public MessageService messageService() {
        return new EmailService();
    }
    
    @Bean
    public MessageProcessor messageProcessor() {
        return new MessageProcessor(messageService());
    }
    
    // Alternative bean with different name
    @Bean(name = "smsProcessor")
    public MessageProcessor smsMessageProcessor() {
        return new MessageProcessor(new SMSService());
    }
}

// Main application
public class SpringCoreDemo {
    public static void main(String[] args) {
        // Create application context
        ApplicationContext context = new AnnotationConfigApplicationContext(AppConfig.class);
        
        // Get beans from container
        MessageProcessor processor = context.getBean(MessageProcessor.class);
        processor.processMessage();
        
        MessageProcessor smsProcessor = context.getBean("smsProcessor", MessageProcessor.class);
        smsProcessor.processMessage();
        
        // Display all beans
        String[] beanNames = context.getBeanDefinitionNames();
        System.out.println("\nAll beans in context:");
        for (String beanName : beanNames) {
            System.out.println("- " + beanName);
        }
        
        // Close context
        ((AnnotationConfigApplicationContext) context).close();
    }
}
```

## 🔧 Typy Dependency Injection

### Constructor Injection (Zalecane)
```java
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.stereotype.Repository;

@Repository
public class UserRepository {
    public User findById(Long id) {
        // Symulacja znajdowania użytkownika
        return new User(id, "User " + id, "user" + id + "@example.com");
    }
    
    public void save(User user) {
        System.out.println("Saving user: " + user);
    }
}

@Service
public class NotificationService {
    public void sendNotification(String message, String recipient) {
        System.out.println("Sending notification to " + recipient + ": " + message);
    }
}

@Service
public class UserService {
    private final UserRepository userRepository;
    private final NotificationService notificationService;
    
    // Constructor injection - ZALECANE
    public UserService(UserRepository userRepository, NotificationService notificationService) {
        this.userRepository = userRepository;
        this.notificationService = notificationService;
        System.out.println("UserService created with constructor injection");
    }
    
    public User getUserById(Long id) {
        return userRepository.findById(id);
    }
    
    public void createUser(User user) {
        userRepository.save(user);
        notificationService.sendNotification("Welcome!", user.getEmail());
    }
}

// Model class
public class User {
    private Long id;
    private String name;
    private String email;
    
    public User(Long id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    
    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', email='" + email + "'}";
    }
}
```

### Setter Injection
```java
@Service
public class OrderService {
    private PaymentService paymentService;
    private InventoryService inventoryService;
    
    // Setter injection
    @Autowired
    public void setPaymentService(PaymentService paymentService) {
        this.paymentService = paymentService;
        System.out.println("PaymentService injected via setter");
    }
    
    @Autowired
    public void setInventoryService(InventoryService inventoryService) {
        this.inventoryService = inventoryService;
        System.out.println("InventoryService injected via setter");
    }
    
    public void processOrder(Order order) {
        if (inventoryService.isAvailable(order.getProductId())) {
            paymentService.processPayment(order.getAmount());
            System.out.println("Order processed: " + order);
        } else {
            System.out.println("Product not available: " + order.getProductId());
        }
    }
}

@Service
public class PaymentService {
    public void processPayment(double amount) {
        System.out.println("Processing payment: $" + amount);
    }
}

@Service  
public class InventoryService {
    public boolean isAvailable(String productId) {
        return !productId.equals("OUT_OF_STOCK");
    }
}

public class Order {
    private String productId;
    private double amount;
    
    public Order(String productId, double amount) {
        this.productId = productId;
        this.amount = amount;
    }
    
    public String getProductId() { return productId; }
    public double getAmount() { return amount; }
    
    @Override
    public String toString() {
        return "Order{productId='" + productId + "', amount=" + amount + "}";
    }
}
```

### Field Injection (Unikać w produkcji)
```java
@Service
public class ReportService {
    @Autowired
    private DataService dataService; // Field injection - nie zalecane
    
    @Autowired
    private EmailService emailService;
    
    public void generateAndSendReport() {
        String data = dataService.getData();
        String report = "Report: " + data;
        emailService.sendEmail("admin@company.com", "Daily Report", report);
    }
}

@Service
public class DataService {
    public String getData() {
        return "Sample data from database";
    }
}
```

## 🎯 Qualifiers i Primary

```java
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Primary;

// Multiple implementations of same interface
public interface PaymentProcessor {
    void processPayment(double amount);
}

@Component
@Primary // Default implementation
public class CreditCardProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing credit card payment: $" + amount);
    }
}

@Component
@Qualifier("paypal")
public class PayPalProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing PayPal payment: $" + amount);
    }
}

@Component
@Qualifier("crypto")
public class CryptocurrencyProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing cryptocurrency payment: $" + amount);
    }
}

@Service
public class CheckoutService {
    private final PaymentProcessor defaultProcessor;
    private final PaymentProcessor paypalProcessor;
    private final PaymentProcessor cryptoProcessor;
    
    public CheckoutService(
            PaymentProcessor defaultProcessor, // @Primary bean injected
            @Qualifier("paypal") PaymentProcessor paypalProcessor,
            @Qualifier("crypto") PaymentProcessor cryptoProcessor) {
        this.defaultProcessor = defaultProcessor;
        this.paypalProcessor = paypalProcessor;
        this.cryptoProcessor = cryptoProcessor;
    }
    
    public void processPayment(String method, double amount) {
        switch (method.toLowerCase()) {
            case "paypal":
                paypalProcessor.processPayment(amount);
                break;
            case "crypto":
                cryptoProcessor.processPayment(amount);
                break;
            default:
                defaultProcessor.processPayment(amount);
        }
    }
}

// Custom qualifier annotation
@Qualifier
@Retention(RetentionPolicy.RUNTIME)
@Target({ElementType.FIELD, ElementType.METHOD, ElementType.TYPE, ElementType.PARAMETER})
public @interface PaymentMethod {
    String value();
}

@Component
@PaymentMethod("bank_transfer")
public class BankTransferProcessor implements PaymentProcessor {
    @Override
    public void processPayment(double amount) {
        System.out.println("Processing bank transfer: $" + amount);
    }
}

@Service
public class AdvancedCheckoutService {
    private final PaymentProcessor bankTransferProcessor;
    
    public AdvancedCheckoutService(@PaymentMethod("bank_transfer") PaymentProcessor processor) {
        this.bankTransferProcessor = processor;
    }
    
    public void processBankTransfer(double amount) {
        bankTransferProcessor.processPayment(amount);
    }
}
```

## 🔄 Bean Scopes

```java
import org.springframework.context.annotation.Scope;
import org.springframework.web.context.WebApplicationContext;

@Component
@Scope("singleton") // Default scope
public class SingletonService {
    private int counter = 0;
    
    public int increment() {
        return ++counter;
    }
    
    public int getCounter() {
        return counter;
    }
}

@Component
@Scope("prototype")
public class PrototypeService {
    private int counter = 0;
    private final String instanceId;
    
    public PrototypeService() {
        this.instanceId = "Instance-" + System.currentTimeMillis();
        System.out.println("Creating new PrototypeService: " + instanceId);
    }
    
    public int increment() {
        return ++counter;
    }
    
    public String getInstanceId() {
        return instanceId;
    }
}

// Web scopes (dostępne tylko w aplikacjach webowych)
@Component
@Scope(WebApplicationContext.SCOPE_REQUEST)
public class RequestScopedService {
    private final String requestId = "Request-" + System.currentTimeMillis();
    
    public String getRequestId() {
        return requestId;
    }
}

@Component
@Scope(WebApplicationContext.SCOPE_SESSION)
public class SessionScopedService {
    private String userId;
    private int pageViews = 0;
    
    public void setUserId(String userId) {
        this.userId = userId;
    }
    
    public String getUserId() {
        return userId;
    }
    
    public int incrementPageViews() {
        return ++pageViews;
    }
}

// Demonstration service
@Service
public class ScopeDemo {
    private final ApplicationContext applicationContext;
    
    public ScopeDemo(ApplicationContext applicationContext) {
        this.applicationContext = applicationContext;
    }
    
    public void demonstrateScopes() {
        System.out.println("=== SINGLETON SCOPE ===");
        SingletonService singleton1 = applicationContext.getBean(SingletonService.class);
        SingletonService singleton2 = applicationContext.getBean(SingletonService.class);
        
        System.out.println("Same instance: " + (singleton1 == singleton2));
        System.out.println("Counter 1: " + singleton1.increment()); // 1
        System.out.println("Counter 2: " + singleton2.getCounter()); // 1 (shared state)
        
        System.out.println("\n=== PROTOTYPE SCOPE ===");
        PrototypeService prototype1 = applicationContext.getBean(PrototypeService.class);
        PrototypeService prototype2 = applicationContext.getBean(PrototypeService.class);
        
        System.out.println("Same instance: " + (prototype1 == prototype2));
        System.out.println("Instance 1 ID: " + prototype1.getInstanceId());
        System.out.println("Instance 2 ID: " + prototype2.getInstanceId());
        System.out.println("Counter 1: " + prototype1.increment()); // 1
        System.out.println("Counter 2: " + prototype2.increment()); // 1 (separate state)
    }
}
```

## 🔧 Bean Lifecycle

```java
import org.springframework.beans.factory.DisposableBean;
import org.springframework.beans.factory.InitializingBean;
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;

@Component
public class LifecycleBean implements InitializingBean, DisposableBean {
    private String name = "LifecycleBean";
    
    // 1. Constructor
    public LifecycleBean() {
        System.out.println("1. Constructor called for " + name);
    }
    
    // 2. Setter methods (if using setter injection)
    public void setName(String name) {
        System.out.println("2. Setter called: " + name);
        this.name = name;
    }
    
    // 3. @PostConstruct annotation
    @PostConstruct
    public void postConstruct() {
        System.out.println("3. @PostConstruct method called for " + name);
        // Initialize resources, validate state, etc.
    }
    
    // 4. InitializingBean.afterPropertiesSet()
    @Override
    public void afterPropertiesSet() throws Exception {
        System.out.println("4. afterPropertiesSet() called for " + name);
        // Additional initialization logic
    }
    
    // Custom init method (configured in @Bean annotation)
    public void customInit() {
        System.out.println("5. Custom init method called for " + name);
    }
    
    public void doWork() {
        System.out.println(name + " is doing work...");
    }
    
    // Destruction methods (called in reverse order)
    @PreDestroy
    public void preDestroy() {
        System.out.println("@PreDestroy method called for " + name);
        // Cleanup resources
    }
    
    @Override
    public void destroy() throws Exception {
        System.out.println("DisposableBean.destroy() called for " + name);
        // Additional cleanup logic
    }
    
    public void customDestroy() {
        System.out.println("Custom destroy method called for " + name);
    }
}

// Configuration with custom init/destroy methods
@Configuration
public class LifecycleConfig {
    
    @Bean(initMethod = "customInit", destroyMethod = "customDestroy")
    public LifecycleBean lifecycleBean() {
        LifecycleBean bean = new LifecycleBean();
        bean.setName("ConfiguredLifecycleBean");
        return bean;
    }
}

// BeanPostProcessor for custom processing
@Component
public class CustomBeanPostProcessor implements BeanPostProcessor {
    
    @Override
    public Object postProcessBeforeInitialization(Object bean, String beanName) throws BeansException {
        if (bean instanceof LifecycleBean) {
            System.out.println("BeanPostProcessor.postProcessBeforeInitialization: " + beanName);
        }
        return bean;
    }
    
    @Override
    public Object postProcessAfterInitialization(Object bean, String beanName) throws BeansException {
        if (bean instanceof LifecycleBean) {
            System.out.println("BeanPostProcessor.postProcessAfterInitialization: " + beanName);
        }
        return bean;
    }
}
```

## 🏭 Bean Factory vs ApplicationContext

```java
import org.springframework.beans.factory.BeanFactory;
import org.springframework.beans.factory.xml.XmlBeanFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.context.support.ClassPathXmlApplicationContext;

public class ContainerComparison {
    
    public static void demonstrateBeanFactory() {
        System.out.println("=== BEAN FACTORY (Lazy Loading) ===");
        
        // BeanFactory - lazy initialization
        BeanFactory factory = new XmlBeanFactory(new ClassPathResource("beans.xml"));
        System.out.println("BeanFactory created - beans not yet instantiated");
        
        // Bean is created only when requested
        System.out.println("Requesting bean...");
        MyService service = (MyService) factory.getBean("myService");
        service.doSomething();
    }
    
    public static void demonstrateApplicationContext() {
        System.out.println("\n=== APPLICATION CONTEXT (Eager Loading) ===");
        
        // ApplicationContext - eager initialization (for singletons)
        ApplicationContext context = new ClassPathXmlApplicationContext("beans.xml");
        System.out.println("ApplicationContext created - singleton beans already instantiated");
        
        // Bean already exists in container
        System.out.println("Requesting bean...");
        MyService service = context.getBean(MyService.class);
        service.doSomething();
        
        // Additional features of ApplicationContext
        System.out.println("\n=== APPLICATION CONTEXT FEATURES ===");
        
        // Event publishing
        context.publishEvent(new CustomEvent("Hello from ApplicationContext"));
        
        // Resource loading
        Resource resource = context.getResource("classpath:application.properties");
        System.out.println("Resource exists: " + resource.exists());
        
        // Internationalization
        String message = context.getMessage("welcome.message", new Object[]{"User"}, Locale.getDefault());
        System.out.println("Localized message: " + message);
        
        ((ClassPathXmlApplicationContext) context).close();
    }
    
    // Event handling
    @Component
    public static class CustomEventListener {
        @EventListener
        public void handleCustomEvent(CustomEvent event) {
            System.out.println("Received event: " + event.getMessage());
        }
    }
    
    public static class CustomEvent {
        private String message;
        
        public CustomEvent(String message) {
            this.message = message;
        }
        
        public String getMessage() {
            return message;
        }
    }
}
```

## 🎯 Configuration Methods

### Java-based Configuration
```java
@Configuration
@ComponentScan(basePackages = "com.example")
@PropertySource("classpath:application.properties")
public class JavaConfig {
    
    @Value("${database.url}")
    private String databaseUrl;
    
    @Value("${database.username}")
    private String databaseUsername;
    
    @Bean
    public DataSource dataSource() {
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl(databaseUrl);
        dataSource.setUsername(databaseUsername);
        dataSource.setMaximumPoolSize(10);
        return dataSource;
    }
    
    @Bean
    @Profile("development")
    public MessageService developmentMessageService() {
        return new ConsoleMessageService();
    }
    
    @Bean
    @Profile("production")
    public MessageService productionMessageService() {
        return new EmailMessageService();
    }
    
    @Bean
    @Conditional(DatabaseCondition.class)
    public DatabaseService databaseService(DataSource dataSource) {
        return new DatabaseServiceImpl(dataSource);
    }
}

// Custom condition
public class DatabaseCondition implements Condition {
    @Override
    public boolean matches(ConditionContext context, AnnotatedTypeMetadata metadata) {
        Environment env = context.getEnvironment();
        return env.getProperty("database.enabled", Boolean.class, false);
    }
}
```

### Annotation-based Configuration
```java
@Configuration
@EnableScheduling
@EnableAsync
public class AnnotationConfig {
    
    // Component scanning automatically detects these
    @Component
    public class TaskService {
        
        @Scheduled(fixedRate = 5000)
        public void periodicTask() {
            System.out.println("Periodic task executed at " + new Date());
        }
        
        @Async
        public CompletableFuture<String> asyncTask() {
            System.out.println("Async task started in thread: " + Thread.currentThread().getName());
            try {
                Thread.sleep(2000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            return CompletableFuture.completedFuture("Async task completed");
        }
    }
    
    @Bean
    public TaskExecutor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(5);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(20);
        executor.setThreadNamePrefix("async-task-");
        executor.initialize();
        return executor;
    }
}
```

## 🎪 Profiles i Environment

```java
@Configuration
public class ProfileConfiguration {
    
    @Bean
    @Profile("test")
    public DataSource testDataSource() {
        return new EmbeddedDatabaseBuilder()
                .setType(EmbeddedDatabaseType.H2)
                .build();
    }
    
    @Bean
    @Profile({"development", "staging"})
    public DataSource devDataSource() {
        // Development database configuration
        return new HikariDataSource();
    }
    
    @Bean
    @Profile("production")
    public DataSource prodDataSource() {
        // Production database configuration with connection pooling
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setMaximumPoolSize(50);
        dataSource.setMinimumIdle(10);
        return dataSource;
    }
    
    @Component
    @Profile("!production") // Not production
    public static class DebugService {
        @PostConstruct
        public void init() {
            System.out.println("Debug service initialized - NOT in production");
        }
    }
}

@Service
public class EnvironmentService {
    
    @Autowired
    private Environment environment;
    
    public void printEnvironmentInfo() {
        System.out.println("=== ENVIRONMENT INFO ===");
        System.out.println("Active profiles: " + Arrays.toString(environment.getActiveProfiles()));
        System.out.println("Default profiles: " + Arrays.toString(environment.getDefaultProfiles()));
        
        // Property access
        String appName = environment.getProperty("app.name", "DefaultApp");
        Integer appVersion = environment.getProperty("app.version", Integer.class, 1);
        Boolean debugMode = environment.getProperty("debug.enabled", Boolean.class, false);
        
        System.out.println("App name: " + appName);
        System.out.println("App version: " + appVersion);
        System.out.println("Debug mode: " + debugMode);
        
        // Check if profile is active
        if (environment.acceptsProfiles("development")) {
            System.out.println("Development features enabled");
        }
    }
}
```

## 🧪 Przykład Kompleksowy - E-commerce System

```java
// Domain model
public class Product {
    private Long id;
    private String name;
    private double price;
    private int quantity;
    
    // Constructors, getters, setters...
}

public class Customer {
    private Long id;
    private String name;
    private String email;
    
    // Constructors, getters, setters...
}

// Repository layer
public interface ProductRepository {
    Product findById(Long id);
    List<Product> findAll();
    void save(Product product);
    void updateQuantity(Long productId, int quantity);
}

@Repository
public class InMemoryProductRepository implements ProductRepository {
    private Map<Long, Product> products = new HashMap<>();
    
    @PostConstruct
    public void init() {
        products.put(1L, new Product(1L, "Laptop", 999.99, 10));
        products.put(2L, new Product(2L, "Mouse", 29.99, 50));
        System.out.println("ProductRepository initialized with sample data");
    }
    
    @Override
    public Product findById(Long id) {
        return products.get(id);
    }
    
    @Override
    public List<Product> findAll() {
        return new ArrayList<>(products.values());
    }
    
    @Override
    public void save(Product product) {
        products.put(product.getId(), product);
    }
    
    @Override
    public void updateQuantity(Long productId, int quantity) {
        Product product = products.get(productId);
        if (product != null) {
            product.setQuantity(quantity);
        }
    }
}

// Service layer
@Service
@Transactional
public class ProductService {
    private final ProductRepository productRepository;
    private final NotificationService notificationService;
    
    public ProductService(ProductRepository productRepository, NotificationService notificationService) {
        this.productRepository = productRepository;
        this.notificationService = notificationService;
    }
    
    public List<Product> getAllProducts() {
        return productRepository.findAll();
    }
    
    public Product getProduct(Long id) {
        Product product = productRepository.findById(id);
        if (product == null) {
            throw new ProductNotFoundException("Product not found: " + id);
        }
        return product;
    }
    
    public boolean reserveProduct(Long productId, int quantity) {
        Product product = getProduct(productId);
        
        if (product.getQuantity() >= quantity) {
            productRepository.updateQuantity(productId, product.getQuantity() - quantity);
            
            if (product.getQuantity() - quantity < 5) {
                notificationService.notifyLowStock(product);
            }
            
            return true;
        }
        
        return false;
    }
}

@Service
public class OrderService {
    private final ProductService productService;
    private final PaymentService paymentService;
    private final NotificationService notificationService;
    
    public OrderService(ProductService productService, 
                       PaymentService paymentService, 
                       NotificationService notificationService) {
        this.productService = productService;
        this.paymentService = paymentService;
        this.notificationService = notificationService;
    }
    
    @Transactional
    public Order createOrder(Customer customer, Long productId, int quantity) {
        // Reserve product
        if (!productService.reserveProduct(productId, quantity)) {
            throw new InsufficientStockException("Not enough stock for product: " + productId);
        }
        
        // Calculate total
        Product product = productService.getProduct(productId);
        double total = product.getPrice() * quantity;
        
        // Process payment
        paymentService.processPayment(customer, total);
        
        // Create order
        Order order = new Order(customer, product, quantity, total);
        
        // Send confirmation
        notificationService.sendOrderConfirmation(customer, order);
        
        return order;
    }
}

// Notification service with multiple implementations
public interface NotificationService {
    void sendOrderConfirmation(Customer customer, Order order);
    void notifyLowStock(Product product);
}

@Component
@Primary
@Profile("production")
public class EmailNotificationService implements NotificationService {
    @Override
    public void sendOrderConfirmation(Customer customer, Order order) {
        System.out.println("Sending email confirmation to " + customer.getEmail() + 
                          " for order: " + order.getId());
    }
    
    @Override
    public void notifyLowStock(Product product) {
        System.out.println("Email: Low stock alert for " + product.getName());
    }
}

@Component
@Profile({"development", "test"})
public class ConsoleNotificationService implements NotificationService {
    @Override
    public void sendOrderConfirmation(Customer customer, Order order) {
        System.out.println("CONSOLE: Order confirmation - Customer: " + customer.getName() + 
                          ", Order: " + order.getId());
    }
    
    @Override
    public void notifyLowStock(Product product) {
        System.out.println("CONSOLE: Low stock - " + product.getName() + 
                          " (remaining: " + product.getQuantity() + ")");
    }
}

// Configuration
@Configuration
@ComponentScan(basePackages = "com.example.ecommerce")
@EnableTransactionManagement
public class ECommerceConfig {
    
    @Bean
    @ConditionalOnProperty(name = "payment.mock.enabled", havingValue = "true", matchIfMissing = true)
    public PaymentService mockPaymentService() {
        return new MockPaymentService();
    }
    
    @Bean
    @ConditionalOnProperty(name = "payment.mock.enabled", havingValue = "false")
    public PaymentService realPaymentService() {
        return new RealPaymentService();
    }
}

// Main application
@SpringBootApplication
public class ECommerceApplication {
    public static void main(String[] args) {
        ApplicationContext context = SpringApplication.run(ECommerceApplication.class, args);
        
        // Demo usage
        OrderService orderService = context.getBean(OrderService.class);
        Customer customer = new Customer(1L, "John Doe", "john@example.com");
        
        try {
            Order order = orderService.createOrder(customer, 1L, 2);
            System.out.println("Order created successfully: " + order);
        } catch (Exception e) {
            System.err.println("Order failed: " + e.getMessage());
        }
    }
}
```

## 🔗 Powiązane Tematy
- [[Spring Boot Wprowadzenie]] - Uproszczona konfiguracja Spring
- [[Spring AOP - Aspect Oriented Programming]] - Cross-cutting concerns
- [[Spring Security - Autoryzacja i Autentykacja]] - Security integration
- [[Java Design Patterns]] - IoC i Dependency Injection patterns

## 💡 Najlepsze Praktyki

1. **Preferuj Constructor Injection** - zapewnia immutability i łatwiejsze testowanie
2. **Używaj @Component, @Service, @Repository** - semantic meaning dla warstw
3. **Unikaj circular dependencies** - restructure code lub używaj @Lazy
4. **Używaj @Qualifier** gdy masz multiple implementations
5. **Leverage profiles** do różnych środowisk
6. **Minimize XML configuration** - preferuj Java config
7. **Use @PostConstruct/@PreDestroy** do lifecycle management

## ⚠️ Częste Pułapki

1. **Circular dependencies** - A depends on B, B depends on A
2. **Incorrect bean scopes** - using prototype where singleton needed
3. **Missing @Component** annotations - beans not being detected
4. **Wrong package scanning** - beans outside scanned packages
5. **Field injection in tests** - makes testing harder

---
*Czas nauki: ~30 minut | Poziom: Średniozaawansowany*