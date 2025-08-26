# 🌐 Spring Boot - Aplikacje Webowe

## 🎮 REST Controllers

### 🚀 Podstawowy Controller

```java
@RestController
@RequestMapping("/api/users")
@CrossOrigin(origins = "http://localhost:3000") // CORS dla frontend
public class UserController {
    
    private final UserService userService;
    
    // Constructor injection
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    // GET /api/users
    @GetMapping
    public ResponseEntity<List<User>> getAllUsers() {
        List<User> users = userService.findAll();
        return ResponseEntity.ok(users);
    }
    
    // GET /api/users/123
    @GetMapping("/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        User user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
    
    // POST /api/users
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody @Valid User user) {
        User savedUser = userService.save(user);
        return ResponseEntity.status(HttpStatus.CREATED).body(savedUser);
    }
    
    // PUT /api/users/123
    @PutMapping("/{id}")
    public ResponseEntity<User> updateUser(@PathVariable Long id, @RequestBody @Valid User user) {
        User updatedUser = userService.update(id, user);
        return ResponseEntity.ok(updatedUser);
    }
    
    // DELETE /api/users/123
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteUser(@PathVariable Long id) {
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
}
```

## 📝 Request/Response Handling

### 🎯 Request Parameters i Query Parameters

```java
@RestController
@RequestMapping("/api/search")
public class SearchController {
    
    // Query parameters: /api/search?name=Jan&age=25&city=Warsaw
    @GetMapping
    public ResponseEntity<List<User>> searchUsers(
        @RequestParam(value = "name", required = false) String name,
        @RequestParam(value = "age", required = false) Integer age,
        @RequestParam(value = "city", defaultValue = "Unknown") String city,
        @RequestParam Map<String, String> allParams) {
        
        // Logika wyszukiwania
        List<User> results = userService.search(name, age, city);
        return ResponseEntity.ok(results);
    }
    
    // Path variables z regex: /api/search/users/123/posts/456
    @GetMapping("/users/{userId:[0-9]+}/posts/{postId:[0-9]+}")
    public ResponseEntity<Post> getUserPost(
        @PathVariable("userId") Long userId,
        @PathVariable("postId") Long postId) {
        
        Post post = postService.findByUserAndId(userId, postId);
        return ResponseEntity.ok(post);
    }
}
```

### 🔧 Request Body i Validation

```java
// Model z validacją
public class CreateUserRequest {
    
    @NotBlank(message = "Imię jest wymagane")
    @Size(min = 2, max = 50, message = "Imię musi mieć od 2 do 50 znaków")
    private String firstName;
    
    @NotBlank(message = "Nazwisko jest wymagane")
    private String lastName;
    
    @Email(message = "Nieprawidłowy format email")
    @NotBlank(message = "Email jest wymagany")
    private String email;
    
    @Min(value = 18, message = "Wiek musi być większy niż 18")
    @Max(value = 120, message = "Wiek musi być mniejszy niż 120")
    private Integer age;
    
    @Pattern(regexp = "^[0-9]{9}$", message = "Numer telefonu musi mieć 9 cyfr")
    private String phoneNumber;
    
    // Getters and setters
}

@RestController
public class ValidationController {
    
    @PostMapping("/api/users")
    public ResponseEntity<?> createUser(@RequestBody @Valid CreateUserRequest request, 
                                       BindingResult bindingResult) {
        
        // Sprawdzenie błędów walidacji
        if (bindingResult.hasErrors()) {
            Map<String, String> errors = new HashMap<>();
            bindingResult.getFieldErrors().forEach(error -> 
                errors.put(error.getField(), error.getDefaultMessage())
            );
            return ResponseEntity.badRequest().body(errors);
        }
        
        User user = userService.createUser(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(user);
    }
}
```

## 🔥 Exception Handling

### 🛡️ Global Exception Handler

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    
    private static final Logger logger = LoggerFactory.getLogger(GlobalExceptionHandler.class);
    
    // Obsługa wyjątku "nie znaleziono"
    @ExceptionHandler(UserNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleUserNotFound(UserNotFoundException ex) {
        ErrorResponse error = new ErrorResponse(
            "USER_NOT_FOUND", 
            ex.getMessage(), 
            LocalDateTime.now()
        );
        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(error);
    }
    
    // Obsługa błędów walidacji
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ValidationErrorResponse> handleValidationErrors(
            MethodArgumentNotValidException ex) {
        
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error ->
            errors.put(error.getField(), error.getDefaultMessage())
        );
        
        ValidationErrorResponse response = new ValidationErrorResponse(
            "VALIDATION_ERROR",
            "Błędy walidacji",
            errors,
            LocalDateTime.now()
        );
        
        return ResponseEntity.badRequest().body(response);
    }
    
    // Obsługa ogólnych błędów
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneral(Exception ex) {
        logger.error("Nieoczekiwany błąd: ", ex);
        
        ErrorResponse error = new ErrorResponse(
            "INTERNAL_ERROR",
            "Wystąpił nieoczekiwany błąd",
            LocalDateTime.now()
        );
        
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body(error);
    }
}

// Klasy odpowiedzi błędów
public class ErrorResponse {
    private String code;
    private String message;
    private LocalDateTime timestamp;
    
    // Constructors, getters, setters
}
```

## 📡 Consuming External APIs

### 🔗 RestTemplate

```java
@Service
public class ExternalApiService {
    
    private final RestTemplate restTemplate;
    
    public ExternalApiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    // GET request
    public User getUserFromExternalApi(Long id) {
        String url = "https://api.external.com/users/" + id;
        return restTemplate.getForObject(url, User.class);
    }
    
    // POST request
    public User createUserInExternalApi(User user) {
        String url = "https://api.external.com/users";
        return restTemplate.postForObject(url, user, User.class);
    }
    
    // With headers
    public ResponseEntity<User> getUserWithHeaders(Long id) {
        HttpHeaders headers = new HttpHeaders();
        headers.set("Authorization", "Bearer token123");
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        HttpEntity<String> entity = new HttpEntity<>(headers);
        
        String url = "https://api.external.com/users/" + id;
        return restTemplate.exchange(url, HttpMethod.GET, entity, User.class);
    }
    
    // Error handling
    public Optional<User> getUserSafely(Long id) {
        try {
            String url = "https://api.external.com/users/" + id;
            User user = restTemplate.getForObject(url, User.class);
            return Optional.ofNullable(user);
        } catch (HttpClientErrorException.NotFound ex) {
            return Optional.empty();
        } catch (RestClientException ex) {
            logger.error("Błąd podczas wywołania API: ", ex);
            throw new ExternalApiException("Nie można pobrać użytkownika", ex);
        }
    }
}
```

### 🚀 WebClient (reaktywny - zalecany)

```java
@Service
public class ReactiveApiService {
    
    private final WebClient webClient;
    
    public ReactiveApiService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder
            .baseUrl("https://api.external.com")
            .defaultHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .build();
    }
    
    // Synchroniczny (blokujący)
    public User getUser(Long id) {
        return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class)
            .block(); // Konwersja na synchroniczny
    }
    
    // Asynchroniczny
    public Mono<User> getUserAsync(Long id) {
        return webClient.get()
            .uri("/users/{id}", id)
            .retrieve()
            .bodyToMono(User.class);
    }
    
    // POST z obsługą błędów
    public Mono<User> createUser(User user) {
        return webClient.post()
            .uri("/users")
            .bodyValue(user)
            .retrieve()
            .onStatus(HttpStatus::is4xxClientError, response -> {
                return Mono.error(new ClientException("Błąd klienta: " + response.statusCode()));
            })
            .onStatus(HttpStatus::is5xxServerError, response -> {
                return Mono.error(new ServerException("Błąd serwera: " + response.statusCode()));
            })
            .bodyToMono(User.class);
    }
}
```

## 🔒 CORS Configuration

```java
@Configuration
public class CorsConfig {
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        
        // Dozwolone origins
        configuration.setAllowedOrigins(Arrays.asList(
            "http://localhost:3000",
            "http://localhost:4200",
            "https://myapp.com"
        ));
        
        // Dozwolone metody HTTP
        configuration.setAllowedMethods(Arrays.asList(
            "GET", "POST", "PUT", "DELETE", "OPTIONS"
        ));
        
        // Dozwolone headers
        configuration.setAllowedHeaders(Arrays.asList("*"));
        
        // Czy wysyłać credentials
        configuration.setAllowCredentials(true);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
}
```

## 📊 JSON Configuration

### 🎯 Custom JSON Serialization

```java
// Konfiguracja Jackson
@Configuration
public class JsonConfig {
    
    @Bean
    @Primary
    public ObjectMapper objectMapper() {
        ObjectMapper mapper = new ObjectMapper();
        
        // Formatowanie dat
        mapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        mapper.registerModule(new JavaTimeModule());
        
        // Ignorowanie nieznanych properties
        mapper.configure(DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
        
        // Naming strategy
        mapper.setPropertyNamingStrategy(PropertyNamingStrategies.SNAKE_CASE);
        
        return mapper;
    }
}

// Custom annotations na modelach
public class User {
    
    @JsonProperty("user_id")
    private Long id;
    
    @JsonFormat(pattern = "yyyy-MM-dd HH:mm:ss")
    private LocalDateTime createdAt;
    
    @JsonIgnore
    private String password;
    
    @JsonInclude(JsonInclude.Include.NON_NULL)
    private String bio;
}
```

---

## 🔗 Następny Krok
[[Java Web MVC|🎨 Java Web - Pattern MVC]] - architektura MVC w aplikacjach webowych

---
*Czas nauki: ~10 minut*