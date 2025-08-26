# 🧪 JUnit 5 - Unit Testing

## 📚 Wprowadzenie
JUnit 5 to najnowsza wersja popularnego framework'a do testowania jednostkowego w Javie. Składa się z trzech podprojektów: JUnit Platform, JUnit Jupiter i JUnit Vintage. Zapewnia zaawansowane możliwości testowania z lepszą integracją z nowoczesnymi narzędziami.

## 🏗️ Podstawowa Struktura

### Setup i Podstawowe Testy
```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.extension.ExtendWith;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {
    
    private Calculator calculator;
    
    @BeforeAll
    static void setUpAll() {
        System.out.println("Setting up test class - wykonuje się raz przed wszystkimi testami");
    }
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
        System.out.println("Setting up before each test");
    }
    
    @AfterEach
    void tearDown() {
        System.out.println("Cleaning up after each test");
        // Cleanup resources
    }
    
    @AfterAll
    static void tearDownAll() {
        System.out.println("Final cleanup - wykonuje się raz po wszystkich testach");
    }
    
    @Test
    @DisplayName("Should add two positive numbers correctly")
    void shouldAddTwoPositiveNumbers() {
        // Given (Arrange)
        double a = 5.0;
        double b = 3.0;
        double expected = 8.0;
        
        // When (Act)
        double result = calculator.add(a, b);
        
        // Then (Assert)
        assertEquals(expected, result, "5.0 + 3.0 should equal 8.0");
    }
    
    @Test
    void shouldThrowExceptionWhenDividingByZero() {
        // Given
        double dividend = 10.0;
        double divisor = 0.0;
        
        // When & Then
        ArithmeticException exception = assertThrows(
            ArithmeticException.class,
            () -> calculator.divide(dividend, divisor),
            "Division by zero should throw ArithmeticException"
        );
        
        assertEquals("Cannot divide by zero", exception.getMessage());
    }
    
    @Test
    void shouldHandleNullInputsGracefully() {
        // Test multiple assertions
        assertAll("Calculator null handling",
            () -> assertThrows(IllegalArgumentException.class, 
                () -> calculator.add(null, 5.0)),
            () -> assertThrows(IllegalArgumentException.class, 
                () -> calculator.add(5.0, null)),
            () -> assertThrows(IllegalArgumentException.class, 
                () -> calculator.multiply(null, null))
        );
    }
}

// Klasa testowana
class Calculator {
    public double add(Double a, Double b) {
        if (a == null || b == null) {
            throw new IllegalArgumentException("Arguments cannot be null");
        }
        return a + b;
    }
    
    public double subtract(double a, double b) {
        return a - b;
    }
    
    public double multiply(Double a, Double b) {
        if (a == null || b == null) {
            throw new IllegalArgumentException("Arguments cannot be null");
        }
        return a * b;
    }
    
    public double divide(double a, double b) {
        if (b == 0) {
            throw new ArithmeticException("Cannot divide by zero");
        }
        return a / b;
    }
}
```

## 🎯 Zaawansowane Asercje

### Różne Typy Asercji
```java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.time.Duration;
import java.util.*;

public class AdvancedAssertionsTest {
    
    @Test
    void testBasicAssertions() {
        // Podstawowe asercje
        assertTrue(5 > 3, "5 should be greater than 3");
        assertFalse(5 < 3, "5 should not be less than 3");
        assertNull(null, "Should be null");
        assertNotNull("not null", "Should not be null");
        
        // Porównywanie obiektów
        String expected = "Hello";
        String actual = "Hello";
        assertEquals(expected, actual, "Strings should be equal");
        assertSame(expected, actual, "Should be same reference"); // Same reference
        
        String different = new String("Hello");
        assertEquals(expected, different, "Should be equal by value");
        assertNotSame(expected, different, "Should not be same reference");
    }
    
    @Test
    void testNumericAssertions() {
        // Liczby zmiennoprzecinkowe z tolerancją
        double result = 0.1 + 0.2;
        assertEquals(0.3, result, 0.0001, "Should be approximately 0.3");
        
        // Zakresy
        int value = 42;
        assertTrue(value >= 40 && value <= 50, "Value should be in range 40-50");
        
        // Custom assertions
        assertThat(value).isBetween(40, 50);
    }
    
    @Test
    void testCollectionAssertions() {
        List<String> actualList = Arrays.asList("apple", "banana", "cherry");
        List<String> expectedList = Arrays.asList("apple", "banana", "cherry");
        
        // Collection equality
        assertEquals(expectedList, actualList, "Lists should be equal");
        
        // Collection content
        assertTrue(actualList.contains("banana"), "Should contain banana");
        assertEquals(3, actualList.size(), "Should have 3 elements");
        
        // Custom collection assertions
        assertIterableEquals(expectedList, actualList, "Iterables should be equal");
        
        // Array assertions
        String[] actualArray = {"a", "b", "c"};
        String[] expectedArray = {"a", "b", "c"};
        assertArrayEquals(expectedArray, actualArray, "Arrays should be equal");
    }
    
    @Test
    void testStringAssertions() {
        String text = "Hello, World!";
        
        // String content
        assertTrue(text.startsWith("Hello"), "Should start with Hello");
        assertTrue(text.endsWith("World!"), "Should end with World!");
        assertTrue(text.contains("World"), "Should contain World");
        
        // String patterns (using custom matchers)
        assertTrue(text.matches("Hello, .*!"), "Should match pattern");
        
        // Case insensitive
        assertEquals("hello, world!", text.toLowerCase(), "Should be equal ignoring case");
    }
    
    @Test
    void testExceptionAssertions() {
        Calculator calc = new Calculator();
        
        // Exception type and message
        Exception exception = assertThrows(ArithmeticException.class, () -> {
            calc.divide(10, 0);
        });
        assertEquals("Cannot divide by zero", exception.getMessage());
        
        // Exception cause
        RuntimeException causedException = new RuntimeException("Cause");
        Exception wrappedException = assertThrows(Exception.class, () -> {
            throw new Exception("Wrapper", causedException);
        });
        assertEquals(causedException, wrappedException.getCause());
        
        // No exception should be thrown
        assertDoesNotThrow(() -> calc.add(5.0, 3.0), "Adding should not throw exception");
    }
    
    @Test
    void testTimeoutAssertions() {
        // Timeout assertions
        assertTimeout(Duration.ofMillis(100), () -> {
            Thread.sleep(50);
            return "Completed within timeout";
        }, "Should complete within 100ms");
        
        // Preemptive timeout (przerwanie wykonania po timeout)
        assertTimeoutPreemptively(Duration.ofMillis(100), () -> {
            Thread.sleep(50);
            return "Completed";
        }, "Should complete within 100ms and be interrupted if not");
    }
    
    // Helper method for custom assertions
    private static AssertionHelper assertThat(int actual) {
        return new AssertionHelper(actual);
    }
    
    private static class AssertionHelper {
        private final int actual;
        
        AssertionHelper(int actual) {
            this.actual = actual;
        }
        
        void isBetween(int min, int max) {
            assertTrue(actual >= min && actual <= max, 
                String.format("Expected %d to be between %d and %d", actual, min, max));
        }
    }
}
```

## 🔄 Parametrized Tests

```java
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.*;
import java.util.stream.Stream;

public class ParameterizedTestsDemo {
    
    @ParameterizedTest
    @ValueSource(strings = {"apple", "banana", "cherry"})
    @DisplayName("Should check that fruit names are not empty")
    void shouldCheckFruitNames(String fruit) {
        assertNotNull(fruit);
        assertFalse(fruit.isEmpty());
        assertTrue(fruit.length() > 2);
    }
    
    @ParameterizedTest
    @ValueSource(ints = {2, 4, 6, 8, 10})
    void shouldCheckEvenNumbers(int number) {
        assertEquals(0, number % 2, () -> number + " should be even");
    }
    
    @ParameterizedTest
    @CsvSource({
        "1, 1, 2",
        "2, 3, 5", 
        "5, 7, 12",
        "-1, 1, 0",
        "0, 0, 0"
    })
    void shouldAddNumbers(int a, int b, int expected) {
        Calculator calculator = new Calculator();
        assertEquals(expected, calculator.add((double)a, (double)b), 0.001);
    }
    
    @ParameterizedTest
    @CsvFileSource(resources = "/test-data.csv", numLinesToSkip = 1)
    void shouldProcessDataFromCsv(String name, int age, String email) {
        User user = new User(name, age, email);
        
        assertNotNull(user.getName());
        assertTrue(user.getAge() > 0);
        assertTrue(user.getEmail().contains("@"));
    }
    
    @ParameterizedTest
    @EnumSource(value = Status.class, names = {"ACTIVE", "PENDING"})
    void shouldHandleActiveStatuses(Status status) {
        assertTrue(status.isProcessable());
    }
    
    @ParameterizedTest
    @EnumSource(value = Status.class, mode = EnumSource.Mode.EXCLUDE, names = {"DELETED"})
    void shouldHandleNonDeletedStatuses(Status status) {
        assertNotEquals(Status.DELETED, status);
    }
    
    @ParameterizedTest
    @MethodSource("provideTestData")
    void shouldProcessComplexTestData(TestData testData) {
        // Test using complex objects
        assertNotNull(testData);
        assertTrue(testData.isValid());
    }
    
    private static Stream<TestData> provideTestData() {
        return Stream.of(
            new TestData("John", 25, "john@test.com"),
            new TestData("Jane", 30, "jane@test.com"),
            new TestData("Bob", 35, "bob@test.com")
        );
    }
    
    @ParameterizedTest
    @ArgumentsSource(CustomArgumentProvider.class)
    void shouldUseCustomArgumentProvider(String input, String expected) {
        assertEquals(expected, input.toUpperCase());
    }
    
    // Custom argument provider
    static class CustomArgumentProvider implements ArgumentsProvider {
        @Override
        public Stream<? extends Arguments> provideArguments(ExtensionContext context) {
            return Stream.of(
                Arguments.of("hello", "HELLO"),
                Arguments.of("world", "WORLD"),
                Arguments.of("java", "JAVA")
            );
        }
    }
    
    // Supporting classes
    enum Status {
        ACTIVE(true), PENDING(true), INACTIVE(false), DELETED(false);
        
        private final boolean processable;
        
        Status(boolean processable) {
            this.processable = processable;
        }
        
        public boolean isProcessable() {
            return processable;
        }
    }
    
    static class User {
        private String name;
        private int age;
        private String email;
        
        public User(String name, int age, String email) {
            this.name = name;
            this.age = age;
            this.email = email;
        }
        
        // Getters
        public String getName() { return name; }
        public int getAge() { return age; }
        public String getEmail() { return email; }
    }
    
    static class TestData {
        private String name;
        private int age;
        private String email;
        
        public TestData(String name, int age, String email) {
            this.name = name;
            this.age = age;
            this.email = email;
        }
        
        public boolean isValid() {
            return name != null && !name.isEmpty() && 
                   age > 0 && age < 150 && 
                   email != null && email.contains("@");
        }
    }
}
```

## 🔧 Test Conditions i Dynamic Tests

```java
import org.junit.jupiter.api.*;
import org.junit.jupiter.api.condition.*;
import java.util.stream.Stream;

public class ConditionalAndDynamicTests {
    
    @Test
    @EnabledOnOs(OS.WINDOWS)
    @DisplayName("Should run only on Windows")
    void shouldRunOnWindows() {
        // Test specific to Windows
        System.out.println("Running on Windows");
    }
    
    @Test
    @EnabledOnOs({OS.LINUX, OS.MAC})
    void shouldRunOnUnix() {
        System.out.println("Running on Unix-like system");
    }
    
    @Test
    @EnabledOnJre(JRE.JAVA_11)
    void shouldRunOnJava11() {
        System.out.println("Running on Java 11");
    }
    
    @Test
    @EnabledOnJre({JRE.JAVA_17, JRE.JAVA_21})
    void shouldRunOnModernJava() {
        System.out.println("Running on modern Java version");
    }
    
    @Test
    @EnabledIfSystemProperty(named = "env", matches = "test")
    void shouldRunInTestEnvironment() {
        System.out.println("Running in test environment");
    }
    
    @Test
    @EnabledIfEnvironmentVariable(named = "DEBUG", matches = "true")
    void shouldRunWhenDebugEnabled() {
        System.out.println("Debug mode enabled");
    }
    
    @Test
    @DisabledIfSystemProperty(named = "skip.integration", matches = "true")
    void shouldSkipWhenIntegrationDisabled() {
        System.out.println("Integration test running");
    }
    
    @Test
    @EnabledIf("customCondition")
    void shouldRunBasedOnCustomCondition() {
        System.out.println("Custom condition met");
    }
    
    boolean customCondition() {
        // Custom logic to determine if test should run
        return System.currentTimeMillis() % 2 == 0;
    }
    
    // Dynamic Tests
    @TestFactory
    @DisplayName("Dynamic tests for mathematical operations")
    Stream<DynamicTest> dynamicTestsForMath() {
        Calculator calculator = new Calculator();
        
        return Stream.of(
            DynamicTest.dynamicTest("Addition: 2 + 3 = 5", 
                () -> assertEquals(5, calculator.add(2.0, 3.0), 0.001)),
            
            DynamicTest.dynamicTest("Subtraction: 5 - 3 = 2", 
                () -> assertEquals(2, calculator.subtract(5.0, 3.0), 0.001)),
            
            DynamicTest.dynamicTest("Multiplication: 4 * 3 = 12", 
                () -> assertEquals(12, calculator.multiply(4.0, 3.0), 0.001)),
            
            DynamicTest.dynamicTest("Division: 10 / 2 = 5", 
                () -> assertEquals(5, calculator.divide(10.0, 2.0), 0.001))
        );
    }
    
    @TestFactory
    @DisplayName("Dynamic tests from data")
    Stream<DynamicTest> dynamicTestsFromData() {
        // Test data
        TestCase[] testCases = {
            new TestCase("positive numbers", 5, 3, 8),
            new TestCase("negative numbers", -2, -3, -5),
            new TestCase("mixed numbers", -4, 6, 2),
            new TestCase("zero", 0, 5, 5)
        };
        
        Calculator calculator = new Calculator();
        
        return Arrays.stream(testCases)
            .map(testCase -> DynamicTest.dynamicTest(
                "Addition test: " + testCase.description,
                () -> {
                    double result = calculator.add(testCase.a, testCase.b);
                    assertEquals(testCase.expected, result, 0.001,
                        () -> String.format("%s: %.1f + %.1f should equal %.1f", 
                            testCase.description, testCase.a, testCase.b, testCase.expected));
                }
            ));
    }
    
    @TestFactory
    @DisplayName("Nested dynamic tests")
    Stream<DynamicNode> nestedDynamicTests() {
        Calculator calculator = new Calculator();
        
        return Stream.of(
            DynamicContainer.dynamicContainer("Addition Tests",
                Stream.of(
                    DynamicTest.dynamicTest("positive", () -> assertEquals(8, calculator.add(5.0, 3.0), 0.001)),
                    DynamicTest.dynamicTest("negative", () -> assertEquals(-8, calculator.add(-5.0, -3.0), 0.001))
                )
            ),
            DynamicContainer.dynamicContainer("Division Tests",
                Stream.of(
                    DynamicTest.dynamicTest("normal division", () -> assertEquals(2, calculator.divide(10.0, 5.0), 0.001)),
                    DynamicTest.dynamicTest("division by zero", 
                        () -> assertThrows(ArithmeticException.class, () -> calculator.divide(10.0, 0.0)))
                )
            )
        );
    }
    
    // Helper class for test data
    static class TestCase {
        final String description;
        final double a;
        final double b;
        final double expected;
        
        TestCase(String description, double a, double b, double expected) {
            this.description = description;
            this.a = a;
            this.b = b;
            this.expected = expected;
        }
    }
}
```

## 🎪 Extensions i Custom Annotations

```java
// Custom extension
import org.junit.jupiter.api.extension.*;

public class TimingExtension implements BeforeEachCallback, AfterEachCallback {
    
    private static final String START_TIME = "start_time";
    
    @Override
    public void beforeEach(ExtensionContext context) {
        getStore(context).put(START_TIME, System.currentTimeMillis());
    }
    
    @Override
    public void afterEach(ExtensionContext context) {
        long startTime = getStore(context).remove(START_TIME, long.class);
        long duration = System.currentTimeMillis() - startTime;
        
        System.out.printf("Test [%s] took %d ms%n", 
            context.getDisplayName(), duration);
        
        // Fail if test takes too long
        if (duration > 5000) {
            throw new RuntimeException("Test exceeded 5 second limit");
        }
    }
    
    private ExtensionContext.Store getStore(ExtensionContext context) {
        return context.getStore(ExtensionContext.Namespace.create(getClass(), context.getRequiredTestMethod()));
    }
}

// Database cleanup extension
public class DatabaseCleanupExtension implements AfterEachCallback {
    
    @Override
    public void afterEach(ExtensionContext context) throws Exception {
        // Get database connection and clean up
        System.out.println("Cleaning up database after test: " + context.getDisplayName());
        
        // Example cleanup logic
        cleanupTestData();
    }
    
    private void cleanupTestData() {
        // Implementation specific to your database setup
        System.out.println("Database cleanup completed");
    }
}

// Custom composed annotations
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Test
@ExtendWith(TimingExtension.class)
public @interface TimedTest {
    String value() default "";
}

@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Test
@ExtendWith({TimingExtension.class, DatabaseCleanupExtension.class})
public @interface DatabaseTest {
    String value() default "";
}

// Usage of custom extensions and annotations
@ExtendWith(TimingExtension.class)
public class ExtensionDemoTest {
    
    @Test
    @DisplayName("Regular test with timing")
    void regularTest() {
        // This test will be timed
        try {
            Thread.sleep(100);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
        assertTrue(true);
    }
    
    @TimedTest("Custom timed test")
    void customTimedTest() {
        // This test uses the custom @TimedTest annotation
        assertEquals(4, 2 + 2);
    }
    
    @DatabaseTest("Database operation test")
    void databaseTest() {
        // This test will be timed and database will be cleaned up
        System.out.println("Performing database operations...");
        assertTrue(true);
    }
    
    @Test
    @ExtendWith(DatabaseCleanupExtension.class)
    void individualExtensionTest() {
        // Only this test will have database cleanup
        System.out.println("Individual test with cleanup");
    }
}

// Parameter resolver extension
public class RandomNumberExtension implements ParameterResolver {
    
    @Override
    public boolean supportsParameter(ParameterContext parameterContext, ExtensionContext extensionContext) {
        return parameterContext.getParameter().getType() == Integer.class &&
               parameterContext.isAnnotated(RandomNumber.class);
    }
    
    @Override
    public Object resolveParameter(ParameterContext parameterContext, ExtensionContext extensionContext) {
        RandomNumber annotation = parameterContext.findAnnotation(RandomNumber.class).get();
        return new Random().nextInt(annotation.max() - annotation.min()) + annotation.min();
    }
}

@Target(ElementType.PARAMETER)
@Retention(RetentionPolicy.RUNTIME)
public @interface RandomNumber {
    int min() default 0;
    int max() default 100;
}

// Test using parameter resolver
@ExtendWith(RandomNumberExtension.class)
class ParameterResolverTest {
    
    @Test
    void testWithRandomNumber(@RandomNumber(min = 10, max = 50) Integer randomNum) {
        System.out.println("Random number: " + randomNum);
        assertTrue(randomNum >= 10 && randomNum < 50);
    }
    
    @RepeatedTest(5)
    void repeatedTestWithRandomNumber(@RandomNumber(min = 1, max = 10) Integer randomNum) {
        System.out.println("Repeated test with random number: " + randomNum);
        assertTrue(randomNum >= 1 && randomNum < 10);
    }
}
```

## 🧪 Testowanie z Mock Objects (Mockito Integration)

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.InjectMocks;
import org.mockito.junit.jupiter.MockitoExtension;
import static org.mockito.Mockito.*;
import static org.junit.jupiter.api.Assertions.*;

// Service to be tested
class UserService {
    private final UserRepository userRepository;
    private final EmailService emailService;
    
    public UserService(UserRepository userRepository, EmailService emailService) {
        this.userRepository = userRepository;
        this.emailService = emailService;
    }
    
    public User createUser(String username, String email) {
        if (userRepository.existsByUsername(username)) {
            throw new IllegalArgumentException("Username already exists");
        }
        
        User user = new User(username, email);
        User savedUser = userRepository.save(user);
        
        emailService.sendWelcomeEmail(savedUser.getEmail());
        
        return savedUser;
    }
    
    public void deleteUser(Long userId) {
        User user = userRepository.findById(userId)
            .orElseThrow(() -> new IllegalArgumentException("User not found"));
        
        userRepository.delete(user);
        emailService.sendGoodbyeEmail(user.getEmail());
    }
}

// Dependencies
interface UserRepository {
    boolean existsByUsername(String username);
    User save(User user);
    Optional<User> findById(Long id);
    void delete(User user);
}

interface EmailService {
    void sendWelcomeEmail(String email);
    void sendGoodbyeEmail(String email);
}

@ExtendWith(MockitoExtension.class)
class UserServiceTest {
    
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private EmailService emailService;
    
    @InjectMocks
    private UserService userService;
    
    @Test
    @DisplayName("Should create user when username doesn't exist")
    void shouldCreateUserWhenUsernameDoesntExist() {
        // Given
        String username = "john_doe";
        String email = "john@example.com";
        User expectedUser = new User(username, email);
        
        when(userRepository.existsByUsername(username)).thenReturn(false);
        when(userRepository.save(any(User.class))).thenReturn(expectedUser);
        
        // When
        User result = userService.createUser(username, email);
        
        // Then
        assertEquals(expectedUser, result);
        
        // Verify interactions
        verify(userRepository).existsByUsername(username);
        verify(userRepository).save(any(User.class));
        verify(emailService).sendWelcomeEmail(email);
        verifyNoMoreInteractions(userRepository, emailService);
    }
    
    @Test
    @DisplayName("Should throw exception when username already exists")
    void shouldThrowExceptionWhenUsernameExists() {
        // Given
        String username = "existing_user";
        String email = "existing@example.com";
        
        when(userRepository.existsByUsername(username)).thenReturn(true);
        
        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> userService.createUser(username, email)
        );
        
        assertEquals("Username already exists", exception.getMessage());
        
        // Verify that save and email were not called
        verify(userRepository).existsByUsername(username);
        verifyNoInteractions(emailService);
        verify(userRepository, never()).save(any(User.class));
    }
    
    @Test
    @DisplayName("Should delete user and send goodbye email")
    void shouldDeleteUserAndSendGoodbyeEmail() {
        // Given
        Long userId = 1L;
        User existingUser = new User("john_doe", "john@example.com");
        
        when(userRepository.findById(userId)).thenReturn(Optional.of(existingUser));
        
        // When
        userService.deleteUser(userId);
        
        // Then
        verify(userRepository).findById(userId);
        verify(userRepository).delete(existingUser);
        verify(emailService).sendGoodbyeEmail(existingUser.getEmail());
    }
    
    @Test
    @DisplayName("Should throw exception when deleting non-existent user")
    void shouldThrowExceptionWhenDeletingNonExistentUser() {
        // Given
        Long userId = 999L;
        when(userRepository.findById(userId)).thenReturn(Optional.empty());
        
        // When & Then
        IllegalArgumentException exception = assertThrows(
            IllegalArgumentException.class,
            () -> userService.deleteUser(userId)
        );
        
        assertEquals("User not found", exception.getMessage());
        verify(userRepository).findById(userId);
        verify(userRepository, never()).delete(any(User.class));
        verifyNoInteractions(emailService);
    }
}
```

## 📊 Test Organization i Suites

```java
// Test tags for organization
@Tag("unit")
@Tag("fast")
class UnitTests {
    
    @Test
    @Tag("calculator")
    void calculatorTest() {
        // Fast unit test
    }
    
    @Test
    @Tag("string-utils")
    void stringUtilsTest() {
        // Another fast unit test
    }
}

@Tag("integration")
@Tag("slow")
class IntegrationTests {
    
    @Test
    @Tag("database")
    void databaseIntegrationTest() {
        // Slow integration test with database
    }
    
    @Test
    @Tag("external-api")
    void externalApiTest() {
        // Test calling external services
    }
}

// Test suites using @Suite
@Suite
@SelectPackages("com.example.tests")
class AllTestsSuite {
    // This will run all tests in the package
}

@Suite
@SelectClasses({UnitTests.class, IntegrationTests.class})
class SelectedTestsSuite {
    // This will run specific test classes
}

@Suite
@IncludeTags("fast")
class FastTestsSuite {
    // This will run only tests tagged with "fast"
}

@Suite
@ExcludeTags("slow")
class NonSlowTestsSuite {
    // This will run all tests except those tagged with "slow"
}

// Custom test interface
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
interface ServiceTest {
}

// Nested test organization
@DisplayName("Calculator Tests")
class CalculatorNestedTest {
    
    private Calculator calculator;
    
    @BeforeEach
    void setUp() {
        calculator = new Calculator();
    }
    
    @Nested
    @DisplayName("Addition Tests")
    class AdditionTests {
        
        @Test
        @DisplayName("Should add two positive numbers")
        void shouldAddPositiveNumbers() {
            assertEquals(8, calculator.add(5.0, 3.0), 0.001);
        }
        
        @Test
        @DisplayName("Should add negative numbers")
        void shouldAddNegativeNumbers() {
            assertEquals(-8, calculator.add(-5.0, -3.0), 0.001);
        }
        
        @Nested
        @DisplayName("Edge Cases")
        class EdgeCases {
            
            @Test
            void shouldAddZero() {
                assertEquals(5, calculator.add(5.0, 0.0), 0.001);
            }
            
            @Test
            void shouldAddVeryLargeNumbers() {
                double large1 = Double.MAX_VALUE / 2;
                double large2 = Double.MAX_VALUE / 2;
                assertTrue(calculator.add(large1, large2) > 0);
            }
        }
    }
    
    @Nested
    @DisplayName("Division Tests")
    class DivisionTests {
        
        @Test
        void shouldDivideNormalNumbers() {
            assertEquals(2.5, calculator.divide(5.0, 2.0), 0.001);
        }
        
        @Test
        void shouldThrowExceptionForDivisionByZero() {
            assertThrows(ArithmeticException.class, () -> calculator.divide(5.0, 0.0));
        }
    }
}
```

## 🔗 Powiązane Tematy
- [[Mockito - Mocking Framework]] - Advanced mocking techniques
- [[Spring Boot Testing]] - Integration testing with Spring
- [[Integration Testing w Spring Boot]] - End-to-end testing
- [[Test-Driven Development (TDD)]] - TDD methodology

## 💡 Najlepsze Praktyki

1. **Używaj AAA pattern** - Arrange, Act, Assert
2. **Jednej asercji na test** - każdy test powinien testować jedną rzecz
3. **Opisowe nazwy testów** - `shouldReturnTrueWhenInputIsValid()`
4. **@DisplayName dla czytelności** - szczególnie dla biznesowych wymagań
5. **Grupuj testy logicznie** - używaj `@Nested` dla organizacji
6. **Tag tests** dla różnych kategorii (unit, integration, slow)
7. **Cleanup resources** w `@AfterEach` i `@AfterAll`
8. **Parametrized tests** dla różnych danych wejściowych

## ⚠️ Częste Błędy

1. **Test dependencies** - testy nie powinny zależeć od siebie
2. **Over-mocking** - nie mockuj wszystkiego
3. **Ignored failing tests** - `@Disabled` powinno być tymczasowe
4. **Testing implementation details** zamiast behavior
5. **No assertions** - testy bez asercji nie testują niczego

---
*Czas nauki: ~35 minut | Poziom: Średniozaawansowany*