# ⚠️ Java - Wyjątki - Zaawansowane Obsługiwanie

## 📚 Wprowadzenie
System obsługi wyjątków w Javie to mechanizm radzenia sobie z błędami i wyjątkowymi sytuacjami podczas wykonywania programu. Poprawna obsługa wyjątków jest kluczowa dla tworzenia niezawodnych aplikacji.

## 🏗️ Hierarchia Wyjątków

```java
Throwable
├── Error                    // Błędy systemowe (nie obsługiwane przez aplikację)
│   ├── OutOfMemoryError
│   ├── StackOverflowError
│   └── VirtualMachineError
└── Exception               // Wyjątki obsługiwane przez aplikację
    ├── RuntimeException    // Unchecked exceptions
    │   ├── NullPointerException
    │   ├── IllegalArgumentException
    │   ├── IndexOutOfBoundsException
    │   └── ClassCastException
    └── Checked Exceptions  // Checked exceptions
        ├── IOException
        ├── SQLException
        ├── ClassNotFoundException
        └── ParseException
```

## 🎯 Podstawowa Składnia

### Try-Catch-Finally
```java
public class BasicExceptionHandling {
    
    public static void basicTryCatch() {
        try {
            int result = 10 / 0; // ArithmeticException
            System.out.println("Wynik: " + result);
        } catch (ArithmeticException e) {
            System.err.println("Błąd dzielenia przez zero: " + e.getMessage());
        } finally {
            System.out.println("Blok finally zawsze się wykonuje");
        }
    }
    
    public static void multipleCatch() {
        String[] array = {"1", "2", "abc"};
        
        try {
            for (int i = 0; i <= array.length; i++) { // IndexOutOfBoundsException
                int number = Integer.parseInt(array[i]); // NumberFormatException
                int result = 100 / number; // ArithmeticException
                System.out.println("Wynik: " + result);
            }
        } catch (IndexOutOfBoundsException e) {
            System.err.println("Indeks poza zakresem: " + e.getMessage());
        } catch (NumberFormatException e) {
            System.err.println("Nieprawidłowy format liczby: " + e.getMessage());
        } catch (ArithmeticException e) {
            System.err.println("Błąd arytmetyczny: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Nieoczekiwany błąd: " + e.getMessage());
        }
    }
    
    public static void multiCatchBlock() {
        try {
            // Kod, który może rzucić różne wyjątki
            processData("invalid_data");
        } catch (NumberFormatException | IllegalArgumentException e) {
            // Java 7+ - obsługa wielu typów wyjątków w jednym bloku
            System.err.println("Błąd danych wejściowych: " + e.getMessage());
        } catch (Exception e) {
            System.err.println("Ogólny błąd: " + e.getMessage());
        }
    }
    
    private static void processData(String data) {
        if (data == null || data.isEmpty()) {
            throw new IllegalArgumentException("Dane nie mogą być puste");
        }
        // Dalsze przetwarzanie...
    }
}
```

### Try-with-Resources (Java 7+)
```java
import java.io.*;
import java.util.Scanner;

public class TryWithResourcesDemo {
    
    // Automatyczne zamykanie zasobów
    public static void readFileTraditional(String fileName) {
        FileInputStream fis = null;
        try {
            fis = new FileInputStream(fileName);
            // Odczytywanie pliku...
            int data = fis.read();
            System.out.println("Pierwszy bajt: " + data);
        } catch (IOException e) {
            System.err.println("Błąd odczytu pliku: " + e.getMessage());
        } finally {
            if (fis != null) {
                try {
                    fis.close();
                } catch (IOException e) {
                    System.err.println("Błąd zamykania pliku: " + e.getMessage());
                }
            }
        }
    }
    
    // Try-with-resources - automatyczne zamykanie
    public static void readFileModern(String fileName) {
        try (FileInputStream fis = new FileInputStream(fileName);
             BufferedInputStream bis = new BufferedInputStream(fis)) {
            
            int data = bis.read();
            System.out.println("Pierwszy bajt: " + data);
            
        } catch (IOException e) {
            System.err.println("Błąd odczytu pliku: " + e.getMessage());
        }
        // Zasoby są automatycznie zamknięte
    }
    
    // Własna klasa z AutoCloseable
    static class CustomResource implements AutoCloseable {
        private String name;
        
        public CustomResource(String name) {
            this.name = name;
            System.out.println("Otwieranie zasobu: " + name);
        }
        
        public void doSomething() {
            System.out.println("Używanie zasobu: " + name);
        }
        
        @Override
        public void close() {
            System.out.println("Zamykanie zasobu: " + name);
        }
    }
    
    public static void useCustomResource() {
        try (CustomResource resource1 = new CustomResource("Resource1");
             CustomResource resource2 = new CustomResource("Resource2")) {
            
            resource1.doSomething();
            resource2.doSomething();
            
            // Symulacja błędu
            throw new RuntimeException("Coś poszło nie tak!");
            
        } catch (RuntimeException e) {
            System.err.println("Obsługa błędu: " + e.getMessage());
        }
        // Zasoby zostaną zamknięte w odwrotnej kolejności
    }
}
```

## 🔧 Tworzenie Własnych Wyjątków

### Checked Exceptions
```java
// Custom checked exception
public class InsufficientFundsException extends Exception {
    private double balance;
    private double amount;
    
    public InsufficientFundsException(double balance, double amount) {
        super("Niewystarczające środki. Saldo: " + balance + ", wymagane: " + amount);
        this.balance = balance;
        this.amount = amount;
    }
    
    public InsufficientFundsException(String message, double balance, double amount) {
        super(message);
        this.balance = balance;
        this.amount = amount;
    }
    
    public InsufficientFundsException(String message, Throwable cause, double balance, double amount) {
        super(message, cause);
        this.balance = balance;
        this.amount = amount;
    }
    
    public double getBalance() { return balance; }
    public double getAmount() { return amount; }
    public double getDeficit() { return amount - balance; }
}

// Usage example
public class BankAccount {
    private double balance;
    private String accountNumber;
    
    public BankAccount(String accountNumber, double initialBalance) {
        this.accountNumber = accountNumber;
        this.balance = initialBalance;
    }
    
    public void withdraw(double amount) throws InsufficientFundsException {
        if (amount <= 0) {
            throw new IllegalArgumentException("Kwota musi być większa od zera");
        }
        
        if (amount > balance) {
            throw new InsufficientFundsException(balance, amount);
        }
        
        balance -= amount;
        System.out.println("Wypłacono: " + amount + ", nowe saldo: " + balance);
    }
    
    public void deposit(double amount) {
        if (amount <= 0) {
            throw new IllegalArgumentException("Kwota musi być większa od zera");
        }
        balance += amount;
        System.out.println("Wpłacono: " + amount + ", nowe saldo: " + balance);
    }
    
    public double getBalance() { return balance; }
}
```

### Runtime Exceptions
```java
// Custom unchecked exception
public class InvalidEmailException extends RuntimeException {
    private String email;
    
    public InvalidEmailException(String email) {
        super("Nieprawidłowy adres email: " + email);
        this.email = email;
    }
    
    public InvalidEmailException(String email, String reason) {
        super("Nieprawidłowy adres email: " + email + ". Powód: " + reason);
        this.email = email;
    }
    
    public String getEmail() { return email; }
}

public class EmailValidator {
    private static final String EMAIL_PATTERN = 
        "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@" +
        "(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";
    
    public static void validateEmail(String email) {
        if (email == null || email.trim().isEmpty()) {
            throw new InvalidEmailException(email, "Email nie może być pusty");
        }
        
        if (!email.matches(EMAIL_PATTERN)) {
            throw new InvalidEmailException(email, "Niepoprawny format");
        }
        
        if (email.length() > 254) {
            throw new InvalidEmailException(email, "Email za długi (max 254 znaki)");
        }
        
        System.out.println("Email poprawny: " + email);
    }
}
```

## 🔄 Rethrowing i Exception Chaining

```java
public class ExceptionChainingDemo {
    
    public static void processOrder(String orderId) throws OrderProcessingException {
        try {
            validateOrder(orderId);
            processPayment(orderId);
            updateInventory(orderId);
            sendConfirmation(orderId);
        } catch (ValidationException e) {
            // Re-throw jako OrderProcessingException z przyczyna
            throw new OrderProcessingException("Błąd walidacji zamówienia " + orderId, e);
        } catch (PaymentException e) {
            throw new OrderProcessingException("Błąd płatności dla zamówienia " + orderId, e);
        } catch (InventoryException e) {
            throw new OrderProcessingException("Błąd aktualizacji magazynu dla " + orderId, e);
        } catch (Exception e) {
            // Unexpected exception
            throw new OrderProcessingException("Nieoczekiwany błąd przetwarzania zamówienia " + orderId, e);
        }
    }
    
    private static void validateOrder(String orderId) throws ValidationException {
        if (orderId == null || orderId.trim().isEmpty()) {
            throw new ValidationException("ID zamówienia nie może być puste");
        }
        // Dalsza walidacja...
    }
    
    private static void processPayment(String orderId) throws PaymentException {
        try {
            // Symulacja wywołania external API
            callPaymentService(orderId);
        } catch (IOException e) {
            throw new PaymentException("Błąd komunikacji z serwisem płatności", e);
        }
    }
    
    private static void callPaymentService(String orderId) throws IOException {
        // Symulacja błędu sieciowego
        throw new IOException("Connection timeout");
    }
    
    private static void updateInventory(String orderId) throws InventoryException {
        // Symulacja błędu bazy danych
        throw new InventoryException("Błąd aktualizacji bazy danych");
    }
    
    private static void sendConfirmation(String orderId) {
        System.out.println("Wysłano potwierdzenie dla zamówienia: " + orderId);
    }
    
    // Custom exceptions
    static class OrderProcessingException extends Exception {
        public OrderProcessingException(String message, Throwable cause) {
            super(message, cause);
        }
    }
    
    static class ValidationException extends Exception {
        public ValidationException(String message) {
            super(message);
        }
    }
    
    static class PaymentException extends Exception {
        public PaymentException(String message, Throwable cause) {
            super(message, cause);
        }
    }
    
    static class InventoryException extends Exception {
        public InventoryException(String message) {
            super(message);
        }
    }
    
    public static void demonstrateExceptionChaining() {
        try {
            processOrder("ORD001");
        } catch (OrderProcessingException e) {
            System.err.println("Główny błąd: " + e.getMessage());
            
            // Przejdź przez łańcuch przyczyn
            Throwable cause = e.getCause();
            int level = 1;
            while (cause != null) {
                System.err.println("Przyczyna " + level + ": " + cause.getMessage());
                cause = cause.getCause();
                level++;
            }
            
            // Wydrukuj pełny stack trace
            e.printStackTrace();
        }
    }
}
```

## 🛠️ Zaawansowane Techniki

### Exception Suppression (Java 7+)
```java
public class ExceptionSuppressionDemo {
    
    static class ProblematicResource implements AutoCloseable {
        private boolean throwOnClose;
        
        public ProblematicResource(boolean throwOnClose) {
            this.throwOnClose = throwOnClose;
        }
        
        public void doWork() {
            throw new RuntimeException("Błąd podczas pracy");
        }
        
        @Override
        public void close() {
            if (throwOnClose) {
                throw new RuntimeException("Błąd podczas zamykania");
            }
        }
    }
    
    public static void demonstrateSuppression() {
        try (ProblematicResource resource = new ProblematicResource(true)) {
            resource.doWork(); // Rzuca wyjątek
        } catch (Exception e) {
            System.out.println("Główny wyjątek: " + e.getMessage());
            
            // Sprawdź suppressed exceptions
            Throwable[] suppressed = e.getSuppressed();
            for (int i = 0; i < suppressed.length; i++) {
                System.out.println("Wyjątek ukryty " + i + ": " + suppressed[i].getMessage());
            }
        }
    }
    
    // Ręczne dodawanie suppressed exceptions
    public static void manualSuppression() {
        Exception primaryException = new Exception("Główny błąd");
        Exception secondaryException = new Exception("Drugorzędny błąd");
        
        primaryException.addSuppressed(secondaryException);
        
        try {
            throw primaryException;
        } catch (Exception e) {
            System.out.println("Główny: " + e.getMessage());
            for (Throwable suppressed : e.getSuppressed()) {
                System.out.println("Ukryty: " + suppressed.getMessage());
            }
        }
    }
}
```

### Custom Exception Handler
```java
public class GlobalExceptionHandler {
    
    public static void handleException(Exception e, String context) {
        // Log podstawowy
        System.err.println("=== EXCEPTION HANDLER ===");
        System.err.println("Context: " + context);
        System.err.println("Time: " + java.time.LocalDateTime.now());
        System.err.println("Exception Type: " + e.getClass().getSimpleName());
        System.err.println("Message: " + e.getMessage());
        
        // Detailed analysis
        if (e instanceof NullPointerException) {
            System.err.println("ANALIZA: Prawdopodobnie użyto null reference");
            System.err.println("SUGESTIA: Sprawdź inicjalizację obiektów");
        } else if (e instanceof IndexOutOfBoundsException) {
            System.err.println("ANALIZA: Próba dostępu poza zakres kolekcji/tablicy");
            System.err.println("SUGESTIA: Sprawdź warunki pętli i indeksy");
        } else if (e instanceof ClassCastException) {
            System.err.println("ANALIZA: Nieprawidłowe rzutowanie typu");
            System.err.println("SUGESTIA: Użyj instanceof przed rzutowaniem");
        }
        
        // Stack trace analysis
        StackTraceElement[] stackTrace = e.getStackTrace();
        if (stackTrace.length > 0) {
            StackTraceElement topElement = stackTrace[0];
            System.err.println("Lokalizacja błędu:");
            System.err.println("  Klasa: " + topElement.getClassName());
            System.err.println("  Metoda: " + topElement.getMethodName());
            System.err.println("  Linia: " + topElement.getLineNumber());
        }
        
        // Recovery suggestions
        System.err.println("OPCJE NAPRAWY:");
        if (e instanceof IOException) {
            System.err.println("- Sprawdź połączenie sieciowe");
            System.err.println("- Zweryfikuj dostęp do plików");
        } else if (e instanceof SQLException) {
            System.err.println("- Sprawdź połączenie z bazą danych");
            System.err.println("- Zweryfikuj składnię SQL");
        }
        
        System.err.println("========================");
    }
}
```

## 🎯 Przykład Kompleksowy - System Zarządzania Plikami

```java
import java.io.*;
import java.nio.file.*;
import java.util.zip.*;

public class FileManager {
    
    public static class FileOperationException extends Exception {
        private Path filePath;
        private String operation;
        
        public FileOperationException(String operation, Path filePath, String message, Throwable cause) {
            super(String.format("Operacja '%s' na pliku '%s' nie powiodła się: %s", 
                               operation, filePath, message), cause);
            this.operation = operation;
            this.filePath = filePath;
        }
        
        public Path getFilePath() { return filePath; }
        public String getOperation() { return operation; }
    }
    
    public void copyFileWithBackup(String source, String destination) throws FileOperationException {
        Path sourcePath = Paths.get(source);
        Path destPath = Paths.get(destination);
        Path backupPath = null;
        
        try {
            // Sprawdź czy plik źródłowy istnieje
            if (!Files.exists(sourcePath)) {
                throw new FileOperationException("COPY", sourcePath, 
                    "Plik źródłowy nie istnieje", null);
            }
            
            // Utwórz backup jeśli plik docelowy już istnieje
            if (Files.exists(destPath)) {
                backupPath = createBackup(destPath);
            }
            
            // Kopiuj plik
            Files.copy(sourcePath, destPath, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("Plik skopiowany pomyślnie: " + source + " -> " + destination);
            
        } catch (IOException e) {
            // Przywróć z backup jeśli coś poszło nie tak
            if (backupPath != null) {
                try {
                    Files.move(backupPath, destPath, StandardCopyOption.REPLACE_EXISTING);
                    System.out.println("Przywrócono plik z backup");
                } catch (IOException restoreException) {
                    e.addSuppressed(restoreException);
                }
            }
            
            throw new FileOperationException("COPY", sourcePath, 
                "Błąd podczas kopiowania", e);
        } catch (Exception e) {
            throw new FileOperationException("COPY", sourcePath, 
                "Nieoczekiwany błąd", e);
        }
    }
    
    private Path createBackup(Path filePath) throws IOException {
        Path backupPath = Paths.get(filePath.toString() + ".backup");
        Files.move(filePath, backupPath, StandardCopyOption.REPLACE_EXISTING);
        System.out.println("Utworzono backup: " + backupPath);
        return backupPath;
    }
    
    public void compressFile(String filePath, String zipPath) throws FileOperationException {
        Path sourceFile = Paths.get(filePath);
        
        try (FileInputStream fis = new FileInputStream(sourceFile.toFile());
             FileOutputStream fos = new FileOutputStream(zipPath);
             ZipOutputStream zos = new ZipOutputStream(fos)) {
            
            ZipEntry entry = new ZipEntry(sourceFile.getFileName().toString());
            zos.putNextEntry(entry);
            
            byte[] buffer = new byte[8192];
            int length;
            while ((length = fis.read(buffer)) != -1) {
                zos.write(buffer, 0, length);
            }
            
            zos.closeEntry();
            System.out.println("Plik skompresowany: " + zipPath);
            
        } catch (IOException e) {
            throw new FileOperationException("COMPRESS", sourceFile, 
                "Błąd podczas kompresji", e);
        }
    }
    
    public String readFileWithEncoding(String filePath, String encoding) throws FileOperationException {
        Path file = Paths.get(filePath);
        
        try {
            // Sprawdź czy plik istnieje i czy można go odczytać
            if (!Files.exists(file)) {
                throw new FileOperationException("READ", file, "Plik nie istnieje", null);
            }
            
            if (!Files.isReadable(file)) {
                throw new FileOperationException("READ", file, "Brak uprawnień do odczytu", null);
            }
            
            // Sprawdź rozmiar pliku
            long fileSize = Files.size(file);
            if (fileSize > 50 * 1024 * 1024) { // 50MB limit
                throw new FileOperationException("READ", file, 
                    "Plik za duży (max 50MB): " + fileSize + " bajtów", null);
            }
            
            return Files.readString(file, java.nio.charset.Charset.forName(encoding));
            
        } catch (UnsupportedCharsetException e) {
            throw new FileOperationException("READ", file, 
                "Nieobsługiwane kodowanie: " + encoding, e);
        } catch (IOException e) {
            throw new FileOperationException("READ", file, 
                "Błąd I/O podczas odczytu", e);
        } catch (OutOfMemoryError e) {
            throw new FileOperationException("READ", file, 
                "Brak pamięci do wczytania pliku", e);
        }
    }
    
    public void processMultipleFiles(String[] filePaths) {
        int successful = 0;
        int failed = 0;
        
        for (String filePath : filePaths) {
            try {
                String content = readFileWithEncoding(filePath, "UTF-8");
                System.out.println("Przetworzono plik: " + filePath + 
                                 " (rozmiar: " + content.length() + " znaków)");
                successful++;
                
            } catch (FileOperationException e) {
                System.err.println("Błąd przetwarzania pliku " + filePath + ": " + e.getMessage());
                
                // Loguj szczegóły w zależności od typu błędu
                if (e.getCause() instanceof IOException) {
                    System.err.println("  Typ błędu: I/O");
                } else if (e.getCause() instanceof UnsupportedCharsetException) {
                    System.err.println("  Typ błędu: Kodowanie");
                }
                
                failed++;
            }
        }
        
        System.out.println("\nPodsumowanie:");
        System.out.println("Pomyślne: " + successful);
        System.out.println("Nieudane: " + failed);
        System.out.println("Razem: " + (successful + failed));
    }
    
    public static void main(String[] args) {
        FileManager fm = new FileManager();
        
        try {
            // Test kopiowania z backup
            fm.copyFileWithBackup("source.txt", "destination.txt");
            
            // Test kompresji
            fm.compressFile("test.txt", "test.zip");
            
            // Test odczytu z obsługą błędów
            String content = fm.readFileWithEncoding("example.txt", "UTF-8");
            System.out.println("Zawartość: " + content.substring(0, Math.min(100, content.length())));
            
        } catch (FileOperationException e) {
            System.err.println("Operacja na pliku nie powiodła się:");
            System.err.println("Operacja: " + e.getOperation());
            System.err.println("Plik: " + e.getFilePath());
            System.err.println("Błąd: " + e.getMessage());
            
            if (e.getCause() != null) {
                System.err.println("Przyczyna: " + e.getCause().getMessage());
            }
        }
        
        // Test przetwarzania wielu plików
        String[] files = {"file1.txt", "file2.txt", "nonexistent.txt", "file3.txt"};
        fm.processMultipleFiles(files);
    }
}
```

## 🔗 Powiązane Tematy
- [[Java Podstawy]] - Podstawy obsługi wyjątków
- [[Java I/O i NIO]] - Wyjątki w operacjach I/O
- [[Java Wielowątkowość - Threading]] - Wyjątki w środowisku wielowątkowym
- [[Spring Boot Web]] - Obsługa wyjątków w aplikacjach web

## 💡 Najlepsze Praktyki

1. **Łap konkretne wyjątki** zamiast `Exception`
2. **Nie ignoruj wyjątków** - zawsze je obsłuż lub przekaż wyżej
3. **Używaj try-with-resources** dla zasobów
4. **Twórz znaczące komunikaty** błędów
5. **Loguj odpowiednie detale** bez ujawniania wrażliwych danych
6. **Nie używaj wyjątków do kontroli przepływu** programu
7. **Dokumentuj rzucane wyjątki** w javadoc
8. **Rozważ fail-fast vs fail-safe** w zależności od kontekstu

## ⚠️ Częste Błędy

1. **Puste bloki catch** - `catch (Exception e) {}`
2. **Zbyt ogólne wyjątki** - łapanie `Exception` zamiast konkretnego typu
3. **Utrata stack trace** - `throw new Exception(e.getMessage())`
4. **Wyjątki w finally** - mogą maskować oryginalne wyjątki
5. **Resource leaks** - nie zamykanie zasobów w finally

---
*Czas nauki: ~30 minut | Poziom: Średniozaawansowany*