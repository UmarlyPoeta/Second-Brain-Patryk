# 🔍 Java - Optional - Najlepsze Praktyki

## 📚 Wprowadzenie
Optional to klasa kontenera wprowadzona w Java 8, która może lub nie musi zawierać wartość non-null. Jest zaprojektowana do eliminacji NullPointerException i czytelniejszego obsługiwania przypadków gdy wartość może być nieobecna.

## 🎯 Podstawowe Użycie

### Tworzenie Optional
```java
import java.util.Optional;

public class OptionalCreation {
    
    public static void demonstrateCreation() {
        // Tworzenie Optional z wartością
        Optional<String> name = Optional.of("Jan Kowalski");
        System.out.println("Optional z wartością: " + name);
        
        // Tworzenie Optional z potencjalnie null wartością
        String nullableValue = getNullableString();
        Optional<String> safeValue = Optional.ofNullable(nullableValue);
        System.out.println("Optional z nullable: " + safeValue);
        
        // Tworzenie pustego Optional
        Optional<String> empty = Optional.empty();
        System.out.println("Pusty Optional: " + empty);
        
        // UWAGA: Optional.of(null) rzuca NullPointerException!
        try {
            Optional<String> invalid = Optional.of(null);
        } catch (NullPointerException e) {
            System.out.println("Optional.of(null) rzuca NPE: " + e.getMessage());
        }
    }
    
    private static String getNullableString() {
        return Math.random() > 0.5 ? "Hello World" : null;
    }
}
```

### Sprawdzanie Obecności Wartości
```java
public class OptionalChecking {
    
    public static void demonstratePresenceChecking() {
        Optional<String> presentValue = Optional.of("Hello");
        Optional<String> emptyValue = Optional.empty();
        
        // isPresent() - sprawdza czy wartość jest obecna
        if (presentValue.isPresent()) {
            System.out.println("Wartość obecna: " + presentValue.get());
        }
        
        if (!emptyValue.isPresent()) {
            System.out.println("Wartość nieobecna");
        }
        
        // isEmpty() (Java 11+) - przeciwność isPresent()
        if (emptyValue.isEmpty()) {
            System.out.println("Optional jest pusty");
        }
        
        // UNIKAJ tego antypattern:
        if (presentValue.isPresent()) {
            String value = presentValue.get(); // Może rzucić NoSuchElementException
            System.out.println(value.toUpperCase());
        }
        
        // LEPIEJ - użyj metod funkcyjnych:
        presentValue.ifPresent(value -> System.out.println(value.toUpperCase()));
        
        // ifPresentOrElse() (Java 9+)
        presentValue.ifPresentOrElse(
            value -> System.out.println("Znaleziono: " + value),
            () -> System.out.println("Nie znaleziono wartości")
        );
    }
}
```

## 🔧 Metody Funkcyjne

### Transformacje z map()
```java
public class OptionalTransformations {
    
    static class Person {
        private String name;
        private Optional<String> email;
        private Optional<Address> address;
        
        public Person(String name, String email, Address address) {
            this.name = name;
            this.email = Optional.ofNullable(email);
            this.address = Optional.ofNullable(address);
        }
        
        // Getters
        public String getName() { return name; }
        public Optional<String> getEmail() { return email; }
        public Optional<Address> getAddress() { return address; }
    }
    
    static class Address {
        private String street;
        private String city;
        private Optional<String> postalCode;
        
        public Address(String street, String city, String postalCode) {
            this.street = street;
            this.city = city;
            this.postalCode = Optional.ofNullable(postalCode);
        }
        
        public String getStreet() { return street; }
        public String getCity() { return city; }
        public Optional<String> getPostalCode() { return postalCode; }
    }
    
    public static void demonstrateMap() {
        Optional<String> name = Optional.of("jan kowalski");
        
        // map() - transformacja wartości jeśli jest obecna
        Optional<String> upperCaseName = name.map(String::toUpperCase);
        Optional<Integer> nameLength = name.map(String::length);
        Optional<String> initials = name.map(n -> {
            String[] parts = n.split(" ");
            return parts[0].charAt(0) + "." + parts[1].charAt(0) + ".";
        });
        
        System.out.println("Oryginalne: " + name.orElse("brak"));
        System.out.println("Wielkie litery: " + upperCaseName.orElse("brak"));
        System.out.println("Długość: " + nameLength.orElse(0));
        System.out.println("Inicjały: " + initials.orElse("brak"));
        
        // Łańcuchowanie transformacji
        Optional<String> processed = name
            .map(String::trim)
            .map(String::toUpperCase)
            .map(s -> s.replace(" ", "_"));
        
        System.out.println("Przetworzone: " + processed.orElse("brak"));
    }
    
    public static void demonstrateFlatMap() {
        Person person = new Person("Jan Kowalski", "jan@example.com", 
            new Address("Marszałkowska 1", "Warszawa", "00-001"));
        
        // flatMap() - dla zagnieżdżonych Optional
        Optional<String> postalCode = Optional.of(person)
            .flatMap(Person::getAddress)
            .flatMap(Address::getPostalCode);
        
        System.out.println("Kod pocztowy: " + postalCode.orElse("nieznany"));
        
        // Przykład bez flatMap (źle)
        Optional<Person> optionalPerson = Optional.of(person);
        // Optional<Optional<String>> nested = optionalPerson.map(Person::getEmail); // Zagnieżdżony Optional!
        
        // Z flatMap (dobrze)
        Optional<String> email = optionalPerson.flatMap(Person::getEmail);
        System.out.println("Email: " + email.orElse("brak"));
        
        // Complex chaining
        String locationInfo = Optional.of(person)
            .flatMap(Person::getAddress)
            .map(addr -> addr.getCity() + ", " + addr.getStreet())
            .map(location -> "Lokalizacja: " + location)
            .orElse("Lokalizacja nieznana");
        
        System.out.println(locationInfo);
    }
}
```

### Filtrowanie
```java
public class OptionalFiltering {
    
    public static void demonstrateFilter() {
        Optional<String> email = Optional.of("user@example.com");
        Optional<String> invalidEmail = Optional.of("invalid-email");
        
        // filter() - zostaw wartość tylko jeśli spełnia warunek
        Optional<String> validEmail = email.filter(e -> e.contains("@"));
        Optional<String> filteredInvalid = invalidEmail.filter(e -> e.contains("@"));
        
        System.out.println("Poprawny email: " + validEmail.orElse("niepoprawny"));
        System.out.println("Niepoprawny email: " + filteredInvalid.orElse("niepoprawny"));
        
        // Łańcuchowanie filtrów
        Optional<Integer> number = Optional.of(42);
        Optional<Integer> validRange = number
            .filter(n -> n > 0)
            .filter(n -> n < 100)
            .filter(n -> n % 2 == 0);
        
        System.out.println("Liczba w poprawnym zakresie: " + validRange.orElse(-1));
        
        // Filter z complex condition
        Optional<String> password = Optional.of("MyPassword123!");
        Optional<String> strongPassword = password
            .filter(p -> p.length() >= 8)
            .filter(p -> p.matches(".*[A-Z].*"))  // Wielkie litery
            .filter(p -> p.matches(".*[0-9].*"))  // Cyfry
            .filter(p -> p.matches(".*[!@#$%^&*].*")); // Znaki specjalne
        
        strongPassword.ifPresentOrElse(
            p -> System.out.println("Hasło silne: " + p),
            () -> System.out.println("Hasło za słabe")
        );
    }
}
```

## 🎪 Wartości Domyślne i Alternatywy

```java
public class OptionalDefaults {
    
    public static void demonstrateDefaults() {
        Optional<String> presentValue = Optional.of("Hello");
        Optional<String> emptyValue = Optional.empty();
        
        // orElse() - wartość domyślna (ZAWSZE ewaluowana)
        String value1 = presentValue.orElse(getDefaultValue());
        String value2 = emptyValue.orElse(getDefaultValue());
        
        System.out.println("Present value: " + value1);
        System.out.println("Empty value: " + value2);
        
        // orElseGet() - supplier (ewaluowany TYLKO gdy potrzebny)
        String value3 = presentValue.orElseGet(() -> getDefaultValue());
        String value4 = emptyValue.orElseGet(() -> getDefaultValue());
        
        System.out.println("Present value (supplier): " + value3);
        System.out.println("Empty value (supplier): " + value4);
        
        // orElseThrow() - rzuć wyjątek jeśli pusta
        try {
            String value5 = presentValue.orElseThrow();
            System.out.println("Present value (no exception): " + value5);
            
            String value6 = emptyValue.orElseThrow(); // NoSuchElementException
        } catch (Exception e) {
            System.out.println("Exception thrown: " + e.getClass().getSimpleName());
        }
        
        // orElseThrow() z custom exception
        try {
            String value7 = emptyValue.orElseThrow(() -> 
                new IllegalStateException("Wartość wymagana!"));
        } catch (IllegalStateException e) {
            System.out.println("Custom exception: " + e.getMessage());
        }
    }
    
    private static String getDefaultValue() {
        System.out.println("Obliczanie wartości domyślnej...");
        return "Default Value";
    }
    
    public static void demonstrateChaining() {
        // or() method (Java 9+) - alternative Optional
        Optional<String> primary = Optional.empty();
        Optional<String> secondary = Optional.of("Secondary");
        Optional<String> tertiary = Optional.of("Tertiary");
        
        Optional<String> result = primary
            .or(() -> secondary)
            .or(() -> tertiary);
        
        System.out.println("Chained result: " + result.orElse("None found"));
        
        // Practical example - try multiple sources
        String config = getConfigFromFile()
            .or(() -> getConfigFromEnvironment())
            .or(() -> getConfigFromDatabase())
            .orElse("default-config");
        
        System.out.println("Configuration: " + config);
    }
    
    private static Optional<String> getConfigFromFile() {
        System.out.println("Próba odczytu z pliku...");
        return Optional.empty(); // Symulacja braku pliku
    }
    
    private static Optional<String> getConfigFromEnvironment() {
        System.out.println("Próba odczytu ze zmiennych środowiskowych...");
        return Optional.of("env-config");
    }
    
    private static Optional<String> getConfigFromDatabase() {
        System.out.println("Próba odczytu z bazy danych...");
        return Optional.of("db-config");
    }
}
```

## 🏗️ Optional w Kolekcjach

```java
import java.util.*;
import java.util.stream.Collectors;

public class OptionalWithCollections {
    
    static class Product {
        private String name;
        private double price;
        private Optional<String> category;
        private boolean available;
        
        public Product(String name, double price, String category, boolean available) {
            this.name = name;
            this.price = price;
            this.category = Optional.ofNullable(category);
            this.available = available;
        }
        
        // Getters
        public String getName() { return name; }
        public double getPrice() { return price; }
        public Optional<String> getCategory() { return category; }
        public boolean isAvailable() { return available; }
        
        @Override
        public String toString() {
            return String.format("Product{name='%s', price=%.2f, category=%s, available=%s}",
                               name, price, category.orElse("None"), available);
        }
    }
    
    public static void demonstrateOptionalInCollections() {
        List<Product> products = Arrays.asList(
            new Product("Laptop", 2500.0, "Electronics", true),
            new Product("Book", 29.99, null, true),
            new Product("Phone", 899.99, "Electronics", false),
            new Product("Pen", 1.99, "Office", true),
            new Product("Monitor", 399.99, null, true)
        );
        
        // Filtrowanie produktów z kategorią
        List<Product> categorizedProducts = products.stream()
            .filter(p -> p.getCategory().isPresent())
            .collect(Collectors.toList());
        
        System.out.println("Produkty z kategorią:");
        categorizedProducts.forEach(System.out::println);
        
        // Mapowanie kategorii do uppercase
        List<String> categories = products.stream()
            .map(Product::getCategory)
            .filter(Optional::isPresent)  // Tylko niepuste Optional
            .map(Optional::get)           // Wyciągnij wartość
            .map(String::toUpperCase)
            .distinct()
            .collect(Collectors.toList());
        
        System.out.println("Kategorie: " + categories);
        
        // Lepszy sposób - flatMap
        List<String> categoriesFlat = products.stream()
            .map(Product::getCategory)
            .flatMap(Optional::stream)    // Java 9+ - zamienia Optional na Stream
            .map(String::toUpperCase)
            .distinct()
            .collect(Collectors.toList());
        
        System.out.println("Kategorie (flatMap): " + categoriesFlat);
        
        // Grupowanie z Optional
        Map<String, List<Product>> productsByCategory = products.stream()
            .collect(Collectors.groupingBy(
                p -> p.getCategory().orElse("Uncategorized")
            ));
        
        System.out.println("Grupowanie po kategoriach:");
        productsByCategory.forEach((category, prods) -> {
            System.out.println("  " + category + ": " + prods.size() + " produktów");
        });
    }
    
    public static void findOperations() {
        List<Product> products = Arrays.asList(
            new Product("Laptop", 2500.0, "Electronics", true),
            new Product("Book", 29.99, "Books", true),
            new Product("Phone", 899.99, "Electronics", false)
        );
        
        // findFirst zwraca Optional
        Optional<Product> firstExpensive = products.stream()
            .filter(p -> p.getPrice() > 1000)
            .findFirst();
        
        firstExpensive.ifPresent(p -> 
            System.out.println("Pierwszy drogi produkt: " + p.getName()));
        
        // findAny zwraca Optional
        Optional<Product> anyAvailable = products.stream()
            .filter(Product::isAvailable)
            .findAny();
        
        anyAvailable.ifPresent(p -> 
            System.out.println("Jakikolwiek dostępny: " + p.getName()));
        
        // max/min zwracają Optional
        Optional<Product> mostExpensive = products.stream()
            .max(Comparator.comparing(Product::getPrice));
        
        mostExpensive.ifPresent(p -> 
            System.out.println("Najdroższy: " + p.getName() + " - " + p.getPrice()));
        
        // reduce zwraca Optional
        Optional<Double> totalValue = products.stream()
            .filter(Product::isAvailable)
            .map(Product::getPrice)
            .reduce(Double::sum);
        
        totalValue.ifPresent(total -> 
            System.out.println("Całkowita wartość dostępnych: " + total));
    }
}
```

## 🎯 Przykłady Praktyczne

### Repository Pattern z Optional
```java
import java.util.*;

public class OptionalRepository {
    
    static class User {
        private Long id;
        private String username;
        private String email;
        private boolean active;
        
        public User(Long id, String username, String email, boolean active) {
            this.id = id;
            this.username = username;
            this.email = email;
            this.active = active;
        }
        
        // Getters
        public Long getId() { return id; }
        public String getUsername() { return username; }
        public String getEmail() { return email; }
        public boolean isActive() { return active; }
        
        @Override
        public String toString() {
            return String.format("User{id=%d, username='%s', email='%s', active=%s}",
                               id, username, email, active);
        }
    }
    
    static class UserRepository {
        private Map<Long, User> users = new HashMap<>();
        
        public UserRepository() {
            // Przykładowe dane
            users.put(1L, new User(1L, "john", "john@example.com", true));
            users.put(2L, new User(2L, "jane", "jane@example.com", true));
            users.put(3L, new User(3L, "bob", "bob@example.com", false));
        }
        
        public Optional<User> findById(Long id) {
            return Optional.ofNullable(users.get(id));
        }
        
        public Optional<User> findByUsername(String username) {
            return users.values().stream()
                .filter(user -> user.getUsername().equals(username))
                .findFirst();
        }
        
        public Optional<User> findByEmail(String email) {
            return users.values().stream()
                .filter(user -> user.getEmail().equals(email))
                .findFirst();
        }
        
        public List<User> findActiveUsers() {
            return users.values().stream()
                .filter(User::isActive)
                .collect(Collectors.toList());
        }
        
        public Optional<User> findActiveUserById(Long id) {
            return findById(id)
                .filter(User::isActive);
        }
    }
    
    static class UserService {
        private UserRepository repository = new UserRepository();
        
        public String getUserDisplayName(Long userId) {
            return repository.findById(userId)
                .filter(User::isActive)
                .map(User::getUsername)
                .map(String::toUpperCase)
                .orElse("Unknown User");
        }
        
        public boolean isUserActive(Long userId) {
            return repository.findById(userId)
                .map(User::isActive)
                .orElse(false);
        }
        
        public Optional<String> getUserEmail(String username) {
            return repository.findByUsername(username)
                .filter(User::isActive)
                .map(User::getEmail);
        }
        
        public void processUser(Long userId) {
            repository.findActiveUserById(userId)
                .ifPresentOrElse(
                    user -> {
                        System.out.println("Przetwarzanie użytkownika: " + user);
                        // Logika przetwarzania
                    },
                    () -> System.out.println("Użytkownik o ID " + userId + " nieaktywny lub nie istnieje")
                );
        }
        
        public String generateUserReport(Long userId) {
            return repository.findById(userId)
                .map(user -> {
                    StringBuilder report = new StringBuilder();
                    report.append("=== RAPORT UŻYTKOWNIKA ===\n");
                    report.append("ID: ").append(user.getId()).append("\n");
                    report.append("Username: ").append(user.getUsername()).append("\n");
                    report.append("Email: ").append(user.getEmail()).append("\n");
                    report.append("Status: ").append(user.isActive() ? "AKTYWNY" : "NIEAKTYWNY").append("\n");
                    return report.toString();
                })
                .orElse("Użytkownik nie znaleziony");
        }
    }
    
    public static void demonstrateRepository() {
        UserService service = new UserService();
        
        // Test różnych scenariuszy
        System.out.println("Display name dla ID 1: " + service.getUserDisplayName(1L));
        System.out.println("Display name dla ID 999: " + service.getUserDisplayName(999L));
        
        System.out.println("User 1 aktywny: " + service.isUserActive(1L));
        System.out.println("User 3 aktywny: " + service.isUserActive(3L));
        
        Optional<String> johnEmail = service.getUserEmail("john");
        johnEmail.ifPresent(email -> System.out.println("Email John'a: " + email));
        
        Optional<String> unknownEmail = service.getUserEmail("unknown");
        System.out.println("Email nieznany: " + unknownEmail.orElse("Brak"));
        
        // Przetwarzanie użytkowników
        service.processUser(1L); // Aktywny
        service.processUser(3L); // Nieaktywny
        service.processUser(999L); // Nie istnieje
        
        // Raporty
        System.out.println(service.generateUserReport(1L));
        System.out.println(service.generateUserReport(999L));
    }
}
```

### Configuration Management z Optional
```java
import java.util.Properties;

public class OptionalConfiguration {
    
    static class ConfigurationManager {
        private Properties properties;
        
        public ConfigurationManager() {
            properties = new Properties();
            // Przykładowa konfiguracja
            properties.setProperty("app.name", "MyApplication");
            properties.setProperty("server.port", "8080");
            properties.setProperty("database.url", "jdbc:postgresql://localhost:5432/mydb");
            // database.username nie jest ustawione
            // database.password nie jest ustawione
        }
        
        public Optional<String> getProperty(String key) {
            return Optional.ofNullable(properties.getProperty(key));
        }
        
        public Optional<Integer> getIntProperty(String key) {
            return getProperty(key)
                .filter(value -> value.matches("\\d+"))
                .map(Integer::parseInt);
        }
        
        public Optional<Boolean> getBooleanProperty(String key) {
            return getProperty(key)
                .map(value -> "true".equalsIgnoreCase(value.trim()));
        }
        
        public String getRequiredProperty(String key) {
            return getProperty(key)
                .orElseThrow(() -> new IllegalStateException(
                    "Required property '" + key + "' not found"));
        }
        
        public String getPropertyWithDefault(String key, String defaultValue) {
            return getProperty(key).orElse(defaultValue);
        }
        
        public Optional<DatabaseConfig> getDatabaseConfig() {
            Optional<String> url = getProperty("database.url");
            Optional<String> username = getProperty("database.username");
            Optional<String> password = getProperty("database.password");
            
            // Wszystkie muszą być obecne
            if (url.isPresent() && username.isPresent() && password.isPresent()) {
                return Optional.of(new DatabaseConfig(
                    url.get(), username.get(), password.get()));
            }
            
            return Optional.empty();
        }
        
        public DatabaseConfig getDatabaseConfigWithDefaults() {
            String url = getProperty("database.url")
                .orElse("jdbc:h2:mem:testdb");
            String username = getProperty("database.username")
                .orElse("sa");
            String password = getProperty("database.password")
                .orElse("");
            
            return new DatabaseConfig(url, username, password);
        }
    }
    
    static class DatabaseConfig {
        private String url;
        private String username;
        private String password;
        
        public DatabaseConfig(String url, String username, String password) {
            this.url = url;
            this.username = username;
            this.password = password;
        }
        
        @Override
        public String toString() {
            return String.format("DatabaseConfig{url='%s', username='%s', password='***'}",
                               url, username);
        }
    }
    
    public static void demonstrateConfiguration() {
        ConfigurationManager config = new ConfigurationManager();
        
        // Podstawowe właściwości
        String appName = config.getRequiredProperty("app.name");
        System.out.println("Nazwa aplikacji: " + appName);
        
        // Port z konwersją
        int port = config.getIntProperty("server.port").orElse(3000);
        System.out.println("Port serwera: " + port);
        
        // Właściwość z domyślną wartością
        String logLevel = config.getPropertyWithDefault("log.level", "INFO");
        System.out.println("Poziom logowania: " + logLevel);
        
        // Boolean property
        boolean debugMode = config.getBooleanProperty("debug.enabled").orElse(false);
        System.out.println("Tryb debug: " + debugMode);
        
        // Konfiguracja bazy danych
        Optional<DatabaseConfig> dbConfig = config.getDatabaseConfig();
        dbConfig.ifPresentOrElse(
            db -> System.out.println("Konfiguracja DB: " + db),
            () -> System.out.println("Niekompletna konfiguracja DB, używanie domyślnej")
        );
        
        DatabaseConfig defaultDbConfig = config.getDatabaseConfigWithDefaults();
        System.out.println("Konfiguracja DB z domyślnymi: " + defaultDbConfig);
        
        // Chain operations
        String connectionString = config.getProperty("database.url")
            .filter(url -> url.startsWith("jdbc:"))
            .map(url -> url + "?useSSL=true")
            .orElse("jdbc:h2:mem:testdb");
        
        System.out.println("Connection string: " + connectionString);
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Stream API - Pełny Przewodnik]] - Optional w stream operations
- [[Java Wyjątki - Zaawansowane Obsługiwanie]] - Alternative to exception handling
- [[Java Lambda i Functional Programming]] - Functional style programming
- [[Spring Boot Web]] - Optional w REST API responses

## 💡 Najlepsze Praktyki

### ✅ Dobre Praktyki
1. **Używaj Optional jako return type** dla metod które mogą nie zwrócić wartości
2. **Nigdy nie zwracaj null Optional** - używaj `Optional.empty()`
3. **Preferuj `orElseGet()` nad `orElse()`** gdy default value jest kosztowny do obliczenia
4. **Używaj `ifPresent()` zamiast `isPresent() + get()`**
5. **Łańcuj operacje** używając `map()`, `flatMap()`, `filter()`
6. **Używaj `stream()` method** (Java 9+) dla integration z Stream API

### ❌ Anty-praktyki
```java
public class OptionalAntipatterns {
    
    public static void demonstrateWhatNotToDo() {
        Optional<String> value = Optional.of("test");
        
        // ❌ NIE: Optional jako field
        // class BadClass {
        //     private Optional<String> name; // ZŁE!
        // }
        
        // ❌ NIE: Optional jako parameter
        // public void badMethod(Optional<String> param) { // ZŁE!
        // }
        
        // ❌ NIE: isPresent() + get()
        if (value.isPresent()) {
            String result = value.get(); // ZŁE! Użyj ifPresent()
        }
        
        // ✅ DOBRZE:
        value.ifPresent(v -> System.out.println(v));
        
        // ❌ NIE: Optional.of(nullable)
        String nullable = null;
        // Optional<String> bad = Optional.of(nullable); // NPE!
        
        // ✅ DOBRZE:
        Optional<String> good = Optional.ofNullable(nullable);
        
        // ❌ NIE: orElse() z expensive operation
        String expensive = value.orElse(expensiveComputation()); // ZAWSZE wykonane!
        
        // ✅ DOBRZE:
        String efficient = value.orElseGet(() -> expensiveComputation()); // Wykonane tylko gdy potrzeba
    }
    
    private static String expensiveComputation() {
        System.out.println("Kosztowne obliczenie wykonane!");
        return "expensive result";
    }
}
```

## 🧪 Testy z Optional

```java
import static org.junit.jupiter.api.Assertions.*;

public class OptionalTesting {
    
    // Przykład testowania metod zwracających Optional
    public class UserService {
        public Optional<User> findByUsername(String username) {
            // Implementation would query database
            if ("john".equals(username)) {
                return Optional.of(new User(1L, "john", "john@example.com", true));
            }
            return Optional.empty();
        }
    }
    
    // @Test
    public void testFindByUsername_ExistingUser() {
        UserService service = new UserService();
        
        Optional<User> result = service.findByUsername("john");
        
        assertTrue(result.isPresent());
        assertEquals("john", result.get().getUsername());
        
        // Lub functional style
        result.ifPresent(user -> {
            assertEquals("john", user.getUsername());
            assertEquals("john@example.com", user.getEmail());
        });
    }
    
    // @Test
    public void testFindByUsername_NonExistingUser() {
        UserService service = new UserService();
        
        Optional<User> result = service.findByUsername("unknown");
        
        assertFalse(result.isPresent());
        assertTrue(result.isEmpty()); // Java 11+
        
        // Test default behavior
        String defaultName = result
            .map(User::getUsername)
            .orElse("Guest");
        
        assertEquals("Guest", defaultName);
    }
}
```

---
*Czas nauki: ~25 minut | Poziom: Średniozaawansowany*