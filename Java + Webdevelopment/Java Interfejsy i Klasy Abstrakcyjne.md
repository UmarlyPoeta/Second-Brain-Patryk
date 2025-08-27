# 🔌 Java - Interfejsy i Klasy Abstrakcyjne

## 📚 Wprowadzenie
Interfejsy i klasy abstrakcyjne to mechanizmy abstrakcji w Javie, które pozwalają definiować kontrakt dla klas implementujących. Są kluczowe dla osiągnięcia luźnego sprzężenia i wysokiej kohezji w aplikacjach.

## 🎭 Interfejsy (Interfaces)

### Podstawowa Definicja
```java
// Interfejs - kontrakt definiujący co klasa musi umieć robić
public interface Drawable {
    // Metody abstrakcyjne (domyślnie public abstract)
    void draw();
    void setColor(String color);
    String getColor();
    
    // Stałe (domyślnie public static final)
    int MAX_SIZE = 1000;
    String DEFAULT_COLOR = "BLACK";
    
    // Default methods (Java 8+)
    default void reset() {
        setColor(DEFAULT_COLOR);
        System.out.println("Obiekt zresetowany do domyślnych ustawień");
    }
    
    // Static methods (Java 8+)
    static boolean isValidColor(String color) {
        return color != null && !color.trim().isEmpty();
    }
    
    // Private methods (Java 9+) - pomocnicze dla default i static methods
    private void validateColor(String color) {
        if (!isValidColor(color)) {
            throw new IllegalArgumentException("Nieprawidłowy kolor: " + color);
        }
    }
}

// Implementacja interfejsu
public class Circle implements Drawable {
    private double radius;
    private String color = DEFAULT_COLOR;
    
    public Circle(double radius) {
        this.radius = radius;
    }
    
    @Override
    public void draw() {
        System.out.println("Rysowanie koła o promieniu " + radius + 
                          " w kolorze " + color);
    }
    
    @Override
    public void setColor(String color) {
        if (Drawable.isValidColor(color)) {
            this.color = color;
        }
    }
    
    @Override
    public String getColor() {
        return color;
    }
    
    // Dodatkowe metody specyficzne dla Circle
    public double getArea() {
        return Math.PI * radius * radius;
    }
}
```

### Wielokrotne Implementowanie Interfejsów
```java
interface Moveable {
    void move(double x, double y);
    double getSpeed();
}

interface Resizable {
    void resize(double scale);
    double getSize();
}

interface Rotatable {
    void rotate(double degrees);
    double getRotation();
}

// Klasa implementująca wiele interfejsów
public class GameSprite implements Drawable, Moveable, Resizable, Rotatable {
    private double x, y;
    private double size = 1.0;
    private double rotation = 0.0;
    private double speed = 1.0;
    private String color = "WHITE";
    
    @Override
    public void draw() {
        System.out.println("Sprite na pozycji (" + x + "," + y + 
                          "), rozmiar: " + size + ", rotacja: " + rotation);
    }
    
    @Override
    public void move(double x, double y) {
        this.x += x;
        this.y += y;
    }
    
    @Override
    public void resize(double scale) {
        this.size *= scale;
    }
    
    @Override
    public void rotate(double degrees) {
        this.rotation = (this.rotation + degrees) % 360;
    }
    
    // Implementacje getterów i setterów...
    @Override
    public double getSpeed() { return speed; }
    
    @Override
    public double getSize() { return size; }
    
    @Override
    public double getRotation() { return rotation; }
    
    @Override
    public void setColor(String color) { this.color = color; }
    
    @Override
    public String getColor() { return color; }
}
```

### Rozszerzanie Interfejsów
```java
interface Vehicle {
    void start();
    void stop();
    int getMaxSpeed();
}

interface ElectricVehicle extends Vehicle {
    void charge();
    int getBatteryLevel();
    int getRange();
    
    // Default method w rozszerzonym interfejsie
    default void showBatteryStatus() {
        System.out.println("Poziom baterii: " + getBatteryLevel() + "%");
        System.out.println("Zasięg: " + getRange() + " km");
    }
}

interface AutonomousVehicle extends Vehicle {
    void enableAutopilot();
    void disableAutopilot();
    boolean isAutopilotActive();
}

// Klasa implementująca interfejs rozszerzony
public class Tesla implements ElectricVehicle, AutonomousVehicle {
    private boolean running = false;
    private int batteryLevel = 100;
    private boolean autopilot = false;
    
    @Override
    public void start() {
        if (batteryLevel > 0) {
            running = true;
            System.out.println("Tesla uruchomiona");
        }
    }
    
    @Override
    public void stop() {
        running = false;
        autopilot = false;
        System.out.println("Tesla zatrzymana");
    }
    
    @Override
    public int getMaxSpeed() {
        return 250; // km/h
    }
    
    @Override
    public void charge() {
        batteryLevel = Math.min(100, batteryLevel + 10);
        System.out.println("Ładowanie... Poziom baterii: " + batteryLevel + "%");
    }
    
    @Override
    public int getBatteryLevel() {
        return batteryLevel;
    }
    
    @Override
    public int getRange() {
        return batteryLevel * 4; // 4km na 1% baterii
    }
    
    @Override
    public void enableAutopilot() {
        if (running) {
            autopilot = true;
            System.out.println("Autopilot włączony");
        }
    }
    
    @Override
    public void disableAutopilot() {
        autopilot = false;
        System.out.println("Autopilot wyłączony");
    }
    
    @Override
    public boolean isAutopilotActive() {
        return autopilot;
    }
}
```

## 🏗️ Klasy Abstrakcyjne

### Podstawowe Użycie
```java
public abstract class DatabaseConnection {
    protected String url;
    protected String username;
    protected String password;
    protected boolean connected = false;
    
    public DatabaseConnection(String url, String username, String password) {
        this.url = url;
        this.username = username;
        this.password = password;
    }
    
    // Metody konkretne - wspólne dla wszystkich implementacji
    public boolean isConnected() {
        return connected;
    }
    
    public String getUrl() {
        return url;
    }
    
    public void printConnectionInfo() {
        System.out.println("URL: " + url + ", User: " + username + 
                          ", Connected: " + connected);
    }
    
    // Metody abstrakcyjne - muszą być zaimplementowane
    public abstract void connect() throws Exception;
    public abstract void disconnect() throws Exception;
    public abstract void executeQuery(String sql) throws Exception;
    
    // Template Method pattern
    public final void performOperation(String sql) {
        try {
            if (!connected) {
                connect();
            }
            executeQuery(sql);
        } catch (Exception e) {
            handleError(e);
        } finally {
            cleanup();
        }
    }
    
    // Hook methods - mogą być nadpisane
    protected void handleError(Exception e) {
        System.err.println("Błąd bazy danych: " + e.getMessage());
    }
    
    protected void cleanup() {
        System.out.println("Czyszczenie zasobów...");
    }
}

// Konkretna implementacja
public class MySQLConnection extends DatabaseConnection {
    private String driverName = "com.mysql.cj.jdbc.Driver";
    
    public MySQLConnection(String url, String username, String password) {
        super(url, username, password);
    }
    
    @Override
    public void connect() throws Exception {
        System.out.println("Łączenie z MySQL: " + url);
        // Logika połączenia z MySQL
        connected = true;
        System.out.println("Połączono z MySQL");
    }
    
    @Override
    public void disconnect() throws Exception {
        System.out.println("Rozłączanie z MySQL");
        connected = false;
        System.out.println("Rozłączono z MySQL");
    }
    
    @Override
    public void executeQuery(String sql) throws Exception {
        if (!connected) {
            throw new Exception("Brak połączenia z bazą danych");
        }
        System.out.println("Wykonywanie zapytania MySQL: " + sql);
        // Logika wykonania zapytania
    }
    
    @Override
    protected void handleError(Exception e) {
        System.err.println("Błąd MySQL: " + e.getMessage());
        // Specjalna obsługa błędów MySQL
    }
    
    // Dodatkowa metoda specyficzna dla MySQL
    public void optimizeTable(String tableName) {
        System.out.println("Optymalizacja tabeli MySQL: " + tableName);
    }
}

public class PostgreSQLConnection extends DatabaseConnection {
    public PostgreSQLConnection(String url, String username, String password) {
        super(url, username, password);
    }
    
    @Override
    public void connect() throws Exception {
        System.out.println("Łączenie z PostgreSQL: " + url);
        connected = true;
        System.out.println("Połączono z PostgreSQL");
    }
    
    @Override
    public void disconnect() throws Exception {
        System.out.println("Rozłączanie z PostgreSQL");
        connected = false;
        System.out.println("Rozłączono z PostgreSQL");
    }
    
    @Override
    public void executeQuery(String sql) throws Exception {
        if (!connected) {
            throw new Exception("Brak połączenia z bazą danych");
        }
        System.out.println("Wykonywanie zapytania PostgreSQL: " + sql);
    }
}
```

## 🔄 Porównanie: Interfejs vs Klasa Abstrakcyjna

```java
// Przykład pokazujący różnice

// INTERFEJS - definiuje "co" obiekt może robić
interface PaymentProcessor {
    void processPayment(double amount);
    boolean validatePayment(double amount);
    String getPaymentMethod();
    
    // Java 8+ features
    default void logTransaction(double amount) {
        System.out.println("Transakcja: " + amount + " PLN przez " + getPaymentMethod());
    }
    
    static boolean isValidAmount(double amount) {
        return amount > 0 && amount <= 1000000;
    }
}

// KLASA ABSTRAKCYJNA - definiuje "jak" coś jest robione (częściowo)
public abstract class BasePaymentProcessor {
    protected String merchantId;
    protected double feeRate;
    
    public BasePaymentProcessor(String merchantId, double feeRate) {
        this.merchantId = merchantId;
        this.feeRate = feeRate;
    }
    
    // Konkretna implementacja wspólna dla wszystkich
    public double calculateFee(double amount) {
        return amount * feeRate;
    }
    
    public void logPayment(double amount, String method) {
        System.out.println("Płatność: " + amount + " PLN, Opłata: " + 
                          calculateFee(amount) + " PLN, Metoda: " + method);
    }
    
    // Abstrakcyjne metody
    public abstract boolean authorize(double amount);
    public abstract String processTransaction(double amount);
}

// Klasa łącząca oba podejścia
public class CreditCardProcessor extends BasePaymentProcessor implements PaymentProcessor {
    private String cardType;
    
    public CreditCardProcessor(String merchantId, double feeRate, String cardType) {
        super(merchantId, feeRate);
        this.cardType = cardType;
    }
    
    // Implementacja z interfejsu
    @Override
    public void processPayment(double amount) {
        if (validatePayment(amount) && authorize(amount)) {
            String result = processTransaction(amount);
            logPayment(amount, getPaymentMethod());
            System.out.println("Wynik: " + result);
        }
    }
    
    @Override
    public boolean validatePayment(double amount) {
        return PaymentProcessor.isValidAmount(amount) && amount >= 1.0;
    }
    
    @Override
    public String getPaymentMethod() {
        return "Credit Card (" + cardType + ")";
    }
    
    // Implementacja z klasy abstrakcyjnej
    @Override
    public boolean authorize(double amount) {
        System.out.println("Autoryzacja karty " + cardType + " na kwotę " + amount);
        return true; // Uproszczona logika
    }
    
    @Override
    public String processTransaction(double amount) {
        return "Transakcja karty kredytowej zakończona sukcesem";
    }
}
```

## 🎯 Funkcjonalne Interfejsy (Java 8+)

```java
// Interfejs funkcjonalny - ma dokładnie jedną abstrakcyjną metodę
@FunctionalInterface
interface Calculator {
    double calculate(double a, double b);
    
    // Default methods are allowed
    default void printResult(double a, double b) {
        System.out.println("Wynik: " + calculate(a, b));
    }
    
    // Static methods are allowed
    static boolean isValidInput(double value) {
        return !Double.isNaN(value) && Double.isFinite(value);
    }
}

public class FunctionalInterfaceDemo {
    public static void main(String[] args) {
        // Lambda expressions
        Calculator addition = (a, b) -> a + b;
        Calculator multiplication = (a, b) -> a * b;
        Calculator division = (a, b) -> b != 0 ? a / b : 0;
        
        // Method references
        Calculator subtraction = Double::sum; // Nie idealne, ale pokazuje składnię
        
        // Użycie
        double x = 10.5, y = 3.2;
        
        System.out.println("Dodawanie: " + addition.calculate(x, y));
        System.out.println("Mnożenie: " + multiplication.calculate(x, y));
        System.out.println("Dzielenie: " + division.calculate(x, y));
        
        addition.printResult(x, y);
        
        // Używanie z metodami wyższego rzędu
        performCalculation(x, y, addition);
        performCalculation(x, y, (a, b) -> Math.pow(a, b));
    }
    
    public static void performCalculation(double a, double b, Calculator calc) {
        if (Calculator.isValidInput(a) && Calculator.isValidInput(b)) {
            calc.printResult(a, b);
        } else {
            System.out.println("Nieprawidłowe dane wejściowe");
        }
    }
}
```

## 🏭 Przykład Kompleksowy - System Notyfikacji

```java
// Interfejs główny
interface NotificationSender {
    void send(String message, String recipient);
    boolean isAvailable();
    String getServiceName();
    
    default void sendWithRetry(String message, String recipient, int maxRetries) {
        int attempts = 0;
        while (attempts < maxRetries) {
            try {
                send(message, recipient);
                System.out.println("Wiadomość wysłana za próbą numer " + (attempts + 1));
                break;
            } catch (Exception e) {
                attempts++;
                System.out.println("Próba " + attempts + " nieudana: " + e.getMessage());
                if (attempts == maxRetries) {
                    throw new RuntimeException("Nie udało się wysłać po " + maxRetries + " próbach");
                }
            }
        }
    }
}

// Klasa abstrakcyjna z wspólną logiką
abstract class BaseNotificationService implements NotificationSender {
    protected String serviceId;
    protected boolean enabled;
    protected int dailyLimit;
    protected int sentToday;
    
    public BaseNotificationService(String serviceId, boolean enabled, int dailyLimit) {
        this.serviceId = serviceId;
        this.enabled = enabled;
        this.dailyLimit = dailyLimit;
        this.sentToday = 0;
    }
    
    @Override
    public boolean isAvailable() {
        return enabled && sentToday < dailyLimit && isServiceOnline();
    }
    
    protected abstract boolean isServiceOnline();
    
    protected void incrementCounter() {
        sentToday++;
    }
    
    protected void validateMessage(String message) {
        if (message == null || message.trim().isEmpty()) {
            throw new IllegalArgumentException("Wiadomość nie może być pusta");
        }
    }
    
    protected void validateRecipient(String recipient) {
        if (recipient == null || recipient.trim().isEmpty()) {
            throw new IllegalArgumentException("Odbiorca nie może być pusty");
        }
    }
    
    public void resetDailyCounter() {
        sentToday = 0;
    }
    
    public int getRemainingQuota() {
        return dailyLimit - sentToday;
    }
}

// Konkretne implementacje
class EmailNotificationService extends BaseNotificationService {
    private String smtpServer;
    
    public EmailNotificationService(String smtpServer, int dailyLimit) {
        super("EMAIL", true, dailyLimit);
        this.smtpServer = smtpServer;
    }
    
    @Override
    public void send(String message, String recipient) {
        validateMessage(message);
        validateRecipient(recipient);
        
        if (!isAvailable()) {
            throw new RuntimeException("Usługa email niedostępna");
        }
        
        System.out.println("📧 Wysyłanie email do: " + recipient);
        System.out.println("Treść: " + message);
        System.out.println("Serwer SMTP: " + smtpServer);
        
        incrementCounter();
    }
    
    @Override
    protected boolean isServiceOnline() {
        // Sprawdzenie połączenia z serwerem SMTP
        return true; // Uproszczenie
    }
    
    @Override
    public String getServiceName() {
        return "Email Service (" + smtpServer + ")";
    }
}

class SMSNotificationService extends BaseNotificationService {
    private String apiKey;
    
    public SMSNotificationService(String apiKey, int dailyLimit) {
        super("SMS", true, dailyLimit);
        this.apiKey = apiKey;
    }
    
    @Override
    public void send(String message, String recipient) {
        validateMessage(message);
        validateRecipient(recipient);
        
        if (!isAvailable()) {
            throw new RuntimeException("Usługa SMS niedostępna");
        }
        
        if (message.length() > 160) {
            throw new IllegalArgumentException("Wiadomość SMS za długa (max 160 znaków)");
        }
        
        System.out.println("📱 Wysyłanie SMS do: " + recipient);
        System.out.println("Treść: " + message);
        
        incrementCounter();
    }
    
    @Override
    protected boolean isServiceOnline() {
        // Sprawdzenie API SMS
        return true; // Uproszczenie
    }
    
    @Override
    public String getServiceName() {
        return "SMS Service";
    }
}

class PushNotificationService extends BaseNotificationService {
    private String appId;
    
    public PushNotificationService(String appId, int dailyLimit) {
        super("PUSH", true, dailyLimit);
        this.appId = appId;
    }
    
    @Override
    public void send(String message, String recipient) {
        validateMessage(message);
        validateRecipient(recipient);
        
        if (!isAvailable()) {
            throw new RuntimeException("Usługa push niedostępna");
        }
        
        System.out.println("🔔 Wysyłanie push notification");
        System.out.println("App ID: " + appId);
        System.out.println("Device ID: " + recipient);
        System.out.println("Treść: " + message);
        
        incrementCounter();
    }
    
    @Override
    protected boolean isServiceOnline() {
        // Sprawdzenie usługi push notifications
        return true; // Uproszczenie
    }
    
    @Override
    public String getServiceName() {
        return "Push Notification Service (App: " + appId + ")";
    }
}

// Manager obsługujący wszystkie usługi
class NotificationManager {
    private List<NotificationSender> services;
    
    public NotificationManager() {
        this.services = new ArrayList<>();
    }
    
    public void addService(NotificationSender service) {
        services.add(service);
    }
    
    public void sendNotification(String message, String recipient, String preferredService) {
        NotificationSender selectedService = null;
        
        // Najpierw spróbuj preferowaną usługę
        if (preferredService != null) {
            selectedService = services.stream()
                .filter(s -> s.getServiceName().contains(preferredService))
                .filter(NotificationSender::isAvailable)
                .findFirst()
                .orElse(null);
        }
        
        // Fallback do pierwszej dostępnej usługi
        if (selectedService == null) {
            selectedService = services.stream()
                .filter(NotificationSender::isAvailable)
                .findFirst()
                .orElse(null);
        }
        
        if (selectedService != null) {
            selectedService.send(message, recipient);
            System.out.println("✅ Wiadomość wysłana przez: " + selectedService.getServiceName());
        } else {
            throw new RuntimeException("Żadna usługa notyfikacji nie jest dostępna");
        }
    }
    
    public void broadcastNotification(String message, List<String> recipients) {
        for (String recipient : recipients) {
            try {
                sendNotification(message, recipient, null);
            } catch (Exception e) {
                System.err.println("Błąd wysyłania do " + recipient + ": " + e.getMessage());
            }
        }
    }
    
    public void showServiceStatus() {
        System.out.println("=== STATUS USŁUG NOTYFIKACJI ===");
        for (NotificationSender service : services) {
            String status = service.isAvailable() ? "✅ Dostępna" : "❌ Niedostępna";
            System.out.println(service.getServiceName() + ": " + status);
            
            if (service instanceof BaseNotificationService) {
                BaseNotificationService baseService = (BaseNotificationService) service;
                System.out.println("  Pozostały limit: " + baseService.getRemainingQuota());
            }
        }
    }
}

// Demo usage
public class NotificationSystemDemo {
    public static void main(String[] args) {
        NotificationManager manager = new NotificationManager();
        
        // Dodanie różnych usług
        manager.addService(new EmailNotificationService("smtp.gmail.com", 1000));
        manager.addService(new SMSNotificationService("API_KEY_123", 100));
        manager.addService(new PushNotificationService("app_id_456", 5000));
        
        manager.showServiceStatus();
        
        // Wysyłanie pojedynczych notyfikacji
        manager.sendNotification("Witaj w naszej aplikacji!", "user@email.com", "Email");
        manager.sendNotification("Masz nową wiadomość", "123456789", "SMS");
        
        // Broadcast
        List<String> recipients = Arrays.asList("user1@email.com", "987654321", "device_token_abc");
        manager.broadcastNotification("Ważna aktualizacja systemu!", recipients);
        
        manager.showServiceStatus();
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Dziedziczenie i Polimorfizm]] - Podstawy polimorfizmu
- [[Java Design Patterns]] - Wzorce używające interfejsów
- [[Java Lambda i Functional Programming]] - Interfejsy funkcjonalne
- [[Spring Core - Dependency Injection]] - Interfejsy w DI

## 💡 Najlepsze Praktyki

1. **Preferuj interfejsy nad klasy abstrakcyjne** gdy nie potrzebujesz wspólnej implementacji
2. **Używaj `@FunctionalInterface`** dla interfejsów z jedną metodą abstrakcyjną
3. **Nazywaj interfejsy opisowo** - co reprezentują, nie jak działają
4. **Dziel duże interfejsy** na mniejsze, specjalizowane (Interface Segregation Principle)
5. **Używaj default methods ostrożnie** - mogą łamać kompatybilność wsteczną

## ⚠️ Kiedy Używać Którego?

### Interfejs
- Chcesz definiować kontrakt dla niepowiązanych klas
- Potrzebujesz wielokrotnego dziedziczenia typów
- Planujesz używać lambda expressions
- Skupiasz się na tym "co" obiekt robi

### Klasa Abstrakcyjna  
- Masz wspólny kod do udostępnienia
- Chcesz definiować template methods
- Potrzebujesz nieużywanych konstruktorów
- Skupiasz się na tym "jak" coś jest implementowane

---
*Czas nauki: ~30 minut | Poziom: Średniozaawansowany*