# 🌱 Spring Boot - Wprowadzenie

## 🚀 Czym jest Spring Boot?

Spring Boot to framework oparty na Spring Framework, który **upraszcza** tworzenie aplikacji Java poprzez:
- **Auto-konfigurację** - automatyczne konfigurowanie komponentów
- **Starter dependencies** - predefiniowane zestawy zależności
- **Embedded server** - wbudowany serwer (Tomcat, Jetty)
- **Production-ready features** - health checks, metrics, monitoring

## 🏗️ Struktura Projektu Spring Boot

```
src/
├── main/
│   ├── java/
│   │   └── com/example/demo/
│   │       ├── DemoApplication.java     # Główna klasa
│   │       ├── controller/              # Kontrolery REST
│   │       ├── service/                 # Logika biznesowa
│   │       ├── repository/              # Dostęp do danych
│   │       └── model/                   # Encje/modele
│   └── resources/
│       ├── application.properties       # Konfiguracja
│       ├── static/                      # Pliki statyczne
│       └── templates/                   # Szablony (Thymeleaf)
└── test/
    └── java/                           # Testy jednostkowe
```

## ⚙️ Kluczowe Adnotacje

### 🎯 Adnotacje Główne

```java
@SpringBootApplication  // = @Configuration + @EnableAutoConfiguration + @ComponentScan
@RestController        // = @Controller + @ResponseBody
@Service              // Klasa serwisu (logika biznesowa)
@Repository           // Klasa dostępu do danych
@Component            // Ogólny komponent Spring
@Configuration        // Klasa konfiguracyjna
```

### 🔧 Przykład Głównej Klasy

```java
@SpringBootApplication
public class DemoApplication {
    
    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
    
    // Bean configuration
    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

## 💉 Dependency Injection (DI)

### 🎯 Rodzaje Wstrzykiwania

```java
@Service
public class UzytkownikService {
    
    // 1. Constructor Injection (ZALECANE)
    private final UzytkownikRepository repository;
    
    public UzytkownikService(UzytkownikRepository repository) {
        this.repository = repository;
    }
    
    // 2. Field Injection (mniej zalecane)
    @Autowired
    private EmailService emailService;
    
    // 3. Setter Injection
    private SmsService smsService;
    
    @Autowired
    public void setSmsService(SmsService smsService) {
        this.smsService = smsService;
    }
}
```

### 🔄 Scopes Bean'ów

```java
@Component
@Scope("singleton")     // Domyślny - jedna instancja
public class SingletonBean { }

@Component  
@Scope("prototype")     // Nowa instancja przy każdym wstrzyknięciu
public class PrototypeBean { }

@Component
@Scope("request")       // Jedna instancja na HTTP request
public class RequestScopedBean { }
```

## 📁 Konfiguracja Application Properties

```properties
# application.properties

# Server configuration
server.port=8080
server.servlet.context-path=/api

# Database configuration
spring.datasource.url=jdbc:mysql://localhost:3306/mydb
spring.datasource.username=root
spring.datasource.password=password
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# JPA/Hibernate
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.format_sql=true

# Logging
logging.level.com.example=DEBUG
logging.level.org.springframework.web=INFO
logging.file.name=logs/application.log

# Profile-specific configuration
spring.profiles.active=dev
```

### 🔧 Konfiguracja YAML (alternatywa)

```yaml
# application.yml
server:
  port: 8080
  servlet:
    context-path: /api

spring:
  datasource:
    url: jdbc:mysql://localhost:3306/mydb
    username: root
    password: password
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    
logging:
  level:
    com.example: DEBUG
    org.springframework.web: INFO
```

## 🏷️ Profile Configuration

### 📄 Różne Profile

```java
@Configuration
@Profile("dev")
public class DevConfiguration {
    
    @Bean
    public DataSource devDataSource() {
        // Konfiguracja dla rozwoju
        return new EmbeddedDatabaseBuilder()
            .setType(EmbeddedDatabaseType.H2)
            .build();
    }
}

@Configuration  
@Profile("prod")
public class ProdConfiguration {
    
    @Bean
    public DataSource prodDataSource() {
        // Konfiguracja produkcyjna
        HikariDataSource dataSource = new HikariDataSource();
        dataSource.setJdbcUrl("jdbc:mysql://prod-server:3306/mydb");
        return dataSource;
    }
}
```

### 🎯 Aktywacja Profili

```java
// Programowo
System.setProperty("spring.profiles.active", "dev");

// VM argument
-Dspring.profiles.active=dev

// Environment variable
export SPRING_PROFILES_ACTIVE=dev
```

## 🔧 Configuration Properties

### 📝 Custom Properties

```java
@ConfigurationProperties(prefix = "app")
@Component
public class AppProperties {
    
    private String name;
    private String version;
    private Database database = new Database();
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public static class Database {
        private String url;
        private int maxConnections = 10;
        
        // Getters and setters
    }
}
```

```properties
# application.properties
app.name=My Application
app.version=1.0.0
app.database.url=jdbc:mysql://localhost:3306/mydb
app.database.max-connections=25
```

### 💡 Używanie Properties

```java
@Service
public class ConfigService {
    
    private final AppProperties appProperties;
    
    public ConfigService(AppProperties appProperties) {
        this.appProperties = appProperties;
    }
    
    public void printConfig() {
        System.out.println("App: " + appProperties.getName());
        System.out.println("Version: " + appProperties.getVersion());
    }
}
```

## 🛠️ Spring Boot Starters

### 📦 Najważniejsze Startory

```xml
<!-- pom.xml -->

<!-- Web aplikacje -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
</dependency>

<!-- Dostęp do danych JPA -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>

<!-- Security -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-security</artifactId>
</dependency>

<!-- Testowanie -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-test</artifactId>
    <scope>test</scope>
</dependency>

<!-- Validation -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-validation</artifactId>
</dependency>
```

## 🔍 Auto-Configuration

### ⚡ Jak Działa Auto-Configuration

```java
// Spring Boot automatycznie konfiguruje beans na podstawie:
// 1. Classpath dependencies
// 2. Existing beans
// 3. Properties configuration

// Przykład custom auto-configuration
@Configuration
@ConditionalOnClass(RestTemplate.class)
@EnableConfigurationProperties(HttpProperties.class)
public class HttpAutoConfiguration {
    
    @Bean
    @ConditionalOnMissingBean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }
}
```

### 🔧 Wyłączanie Auto-Configuration

```java
@SpringBootApplication(exclude = {
    DataSourceAutoConfiguration.class,
    JpaRepositoriesAutoConfiguration.class
})
public class MyApplication {
    // ...
}
```

---

## 🔗 Następny Krok
[[Spring Boot Web|🌐 Spring Boot - Aplikacje Webowe]] - kontrolery, REST API, obsługa HTTP

---
*Czas nauki: ~10 minut*