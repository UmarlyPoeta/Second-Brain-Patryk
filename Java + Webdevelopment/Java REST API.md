# 📡 Java - REST API

## 🌐 REST Architecture Principles

### 📋 Zasady REST
1. **Stateless** - każde żądanie niezależne
2. **Client-Server** - rozdział odpowiedzialności
3. **Cacheable** - odpowiedzi mogą być cachowane
4. **Uniform Interface** - spójny interfejs
5. **Layered System** - architektura warstwowa

### 🎯 HTTP Methods & Status Codes

```java
// HTTP Methods
GET    /api/users        // Pobierz wszystkich użytkowników
GET    /api/users/123    // Pobierz użytkownika o ID 123
POST   /api/users        // Utwórz nowego użytkownika
PUT    /api/users/123    // Zaktualizuj użytkownika o ID 123
PATCH  /api/users/123    // Częściowa aktualizacja użytkownika
DELETE /api/users/123    // Usuń użytkownika o ID 123

// Status Codes
200 OK                   // Sukces
201 Created             // Zasób utworzony
204 No Content          // Sukces bez treści
400 Bad Request         // Błędne żądanie
401 Unauthorized        // Brak autoryzacji
403 Forbidden          // Brak uprawnień
404 Not Found          // Zasób nie znaleziony
409 Conflict           // Konflikt (np. email już istnieje)
422 Unprocessable Entity // Błędy walidacji
500 Internal Server Error // Błąd serwera
```

## 🚀 Kompleksowy REST Controller

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
@Tag(name = "User Management", description = "Operations for managing users")
public class UserRestController {
    
    private final UserService userService;
    private final UserMapper userMapper;
    
    public UserRestController(UserService userService, UserMapper userMapper) {
        this.userService = userService;
        this.userMapper = userMapper;
    }
    
    @GetMapping
    @Operation(summary = "Get all users with pagination and filtering")
    public ResponseEntity<PagedResponse<UserDto>> getAllUsers(
            @Parameter(description = "Page number (0-indexed)") 
            @RequestParam(defaultValue = "0") @Min(0) int page,
            
            @Parameter(description = "Page size")
            @RequestParam(defaultValue = "10") @Min(1) @Max(100) int size,
            
            @Parameter(description = "Sort field")
            @RequestParam(defaultValue = "id") String sortBy,
            
            @Parameter(description = "Sort direction")
            @RequestParam(defaultValue = "ASC") Sort.Direction sortDirection,
            
            @Parameter(description = "Search term")
            @RequestParam(required = false) String search) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortDirection, sortBy));
        Page<User> users = userService.findAll(search, pageable);
        
        PagedResponse<UserDto> response = PagedResponse.<UserDto>builder()
            .content(users.getContent().stream()
                    .map(userMapper::toDto)
                    .collect(Collectors.toList()))
            .page(page)
            .size(size)
            .totalElements(users.getTotalElements())
            .totalPages(users.getTotalPages())
            .first(users.isFirst())
            .last(users.isLast())
            .build();
            
        return ResponseEntity.ok(response);
    }
    
    @GetMapping("/{id}")
    @Operation(summary = "Get user by ID")
    public ResponseEntity<UserDto> getUserById(
            @Parameter(description = "User ID") 
            @PathVariable @Positive Long id) {
        
        User user = userService.findById(id);
        return ResponseEntity.ok(userMapper.toDto(user));
    }
    
    @PostMapping
    @Operation(summary = "Create new user")
    public ResponseEntity<UserDto> createUser(
            @Parameter(description = "User data") 
            @RequestBody @Valid CreateUserRequest request) {
        
        User user = userService.create(request);
        UserDto createdUser = userMapper.toDto(user);
        
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(user.getId())
            .toUri();
            
        return ResponseEntity.created(location).body(createdUser);
    }
    
    @PutMapping("/{id}")
    @Operation(summary = "Update user completely")
    public ResponseEntity<UserDto> updateUser(
            @Parameter(description = "User ID") 
            @PathVariable @Positive Long id,
            
            @Parameter(description = "Updated user data")
            @RequestBody @Valid UpdateUserRequest request) {
        
        User user = userService.update(id, request);
        return ResponseEntity.ok(userMapper.toDto(user));
    }
    
    @PatchMapping("/{id}")
    @Operation(summary = "Partially update user")
    public ResponseEntity<UserDto> patchUser(
            @Parameter(description = "User ID")
            @PathVariable @Positive Long id,
            
            @Parameter(description = "Partial user data")
            @RequestBody PatchUserRequest request) {
        
        User user = userService.patch(id, request);
        return ResponseEntity.ok(userMapper.toDto(user));
    }
    
    @DeleteMapping("/{id}")
    @Operation(summary = "Delete user")
    public ResponseEntity<Void> deleteUser(
            @Parameter(description = "User ID")
            @PathVariable @Positive Long id) {
        
        userService.deleteById(id);
        return ResponseEntity.noContent().build();
    }
    
    // Nested resources
    @GetMapping("/{userId}/posts")
    @Operation(summary = "Get user's posts")
    public ResponseEntity<List<PostDto>> getUserPosts(
            @PathVariable @Positive Long userId) {
        
        List<Post> posts = userService.getUserPosts(userId);
        List<PostDto> postDtos = posts.stream()
            .map(postMapper::toDto)
            .collect(Collectors.toList());
            
        return ResponseEntity.ok(postDtos);
    }
}
```

## 📝 DTOs i Mapping

### 🎯 Request DTOs

```java
// Create request
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class CreateUserRequest {
    
    @NotBlank(message = "Imię nie może być puste")
    @Size(min = 2, max = 50, message = "Imię musi mieć od 2 do 50 znaków")
    private String firstName;
    
    @NotBlank(message = "Nazwisko nie może być puste")
    @Size(min = 2, max = 50, message = "Nazwisko musi mieć od 2 do 50 znaków")
    private String lastName;
    
    @NotBlank(message = "Email nie może być pusty")
    @Email(message = "Nieprawidłowy format email")
    private String email;
    
    @Min(value = 18, message = "Wiek musi być większy niż 18")
    @Max(value = 120, message = "Wiek musi być mniejszy niż 120")
    private Integer age;
    
    @Pattern(regexp = "^[+]?[0-9]{9,15}$", message = "Nieprawidłowy numer telefonu")
    private String phoneNumber;
}

// Patch request (wszystkie pola opcjonalne)
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PatchUserRequest {
    
    @Size(min = 2, max = 50, message = "Imię musi mieć od 2 do 50 znaków")
    private String firstName;
    
    @Size(min = 2, max = 50, message = "Nazwisko musi mieć od 2 do 50 znaków")
    private String lastName;
    
    @Email(message = "Nieprawidłowy format email")
    private String email;
    
    @Min(value = 18, message = "Wiek musi być większy niż 18")
    @Max(value = 120, message = "Wiek musi być mniejszy niż 120") 
    private Integer age;
    
    @Pattern(regexp = "^[+]?[0-9]{9,15}$", message = "Nieprawidłowy numer telefonu")
    private String phoneNumber;
}
```

### 📤 Response DTOs

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class UserDto {
    
    private Long id;
    
    @JsonProperty("first_name")
    private String firstName;
    
    @JsonProperty("last_name")
    private String lastName;
    
    private String email;
    
    @JsonProperty("full_name")
    private String fullName;
    
    private Integer age;
    
    @JsonProperty("phone_number")
    private String phoneNumber;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @JsonProperty("created_at")
    private LocalDateTime createdAt;
    
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    @JsonProperty("updated_at")
    private LocalDateTime updatedAt;
    
    @JsonProperty("posts_count")
    private int postsCount;
    
    @JsonInclude(JsonInclude.Include.NON_EMPTY)
    private List<PostSummaryDto> recentPosts;
}

// Generic paged response
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PagedResponse<T> {
    
    private List<T> content;
    private int page;
    private int size;
    private long totalElements;
    private int totalPages;
    private boolean first;
    private boolean last;
    
    @JsonProperty("has_previous")
    public boolean getHasPrevious() {
        return !first;
    }
    
    @JsonProperty("has_next") 
    public boolean getHasNext() {
        return !last;
    }
}
```

## 🔄 Mappers (MapStruct)

```java
@Mapper(componentModel = "spring", 
        unmappedTargetPolicy = ReportingPolicy.IGNORE,
        imports = {LocalDateTime.class})
public interface UserMapper {
    
    // Entity -> DTO
    @Mapping(target = "fullName", expression = "java(user.getFirstName() + \" \" + user.getLastName())")
    @Mapping(target = "postsCount", expression = "java(user.getPosts() != null ? user.getPosts().size() : 0)")
    @Mapping(target = "recentPosts", source = "posts", qualifiedByName = "limitPosts")
    UserDto toDto(User user);
    
    // Request -> Entity
    @Mapping(target = "id", ignore = true)
    @Mapping(target = "createdAt", ignore = true)
    @Mapping(target = "updatedAt", ignore = true)
    @Mapping(target = "posts", ignore = true)
    User toEntity(CreateUserRequest request);
    
    // Patch mapping (tylko non-null fields)
    @BeanMapping(nullValuePropertyMappingStrategy = NullValuePropertyMappingStrategy.IGNORE)
    void patchEntity(PatchUserRequest request, @MappingTarget User user);
    
    // Lists
    List<UserDto> toDtoList(List<User> users);
    
    @Named("limitPosts")
    default List<PostSummaryDto> limitPosts(List<Post> posts) {
        if (posts == null || posts.isEmpty()) {
            return Collections.emptyList();
        }
        return posts.stream()
                .limit(3)
                .map(this::toPostSummary)
                .collect(Collectors.toList());
    }
    
    @Mapping(target = "authorName", source = "user.firstName")
    PostSummaryDto toPostSummary(Post post);
}
```

## 🛡️ Advanced Exception Handling

```java
@ControllerAdvice
@Slf4j
public class RestExceptionHandler {
    
    @ExceptionHandler(UserNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public ErrorResponse handleUserNotFound(UserNotFoundException ex) {
        log.warn("User not found: {}", ex.getMessage());
        
        return ErrorResponse.builder()
            .status(HttpStatus.NOT_FOUND.value())
            .error("USER_NOT_FOUND")
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .path(getCurrentPath())
            .build();
    }
    
    @ExceptionHandler(EmailAlreadyExistsException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public ErrorResponse handleEmailExists(EmailAlreadyExistsException ex) {
        log.warn("Email conflict: {}", ex.getMessage());
        
        return ErrorResponse.builder()
            .status(HttpStatus.CONFLICT.value())
            .error("EMAIL_ALREADY_EXISTS")
            .message(ex.getMessage())
            .timestamp(LocalDateTime.now())
            .path(getCurrentPath())
            .build();
    }
    
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseStatus(HttpStatus.UNPROCESSABLE_ENTITY)
    public ValidationErrorResponse handleValidation(MethodArgumentNotValidException ex) {
        log.warn("Validation errors: {}", ex.getBindingResult().getAllErrors());
        
        Map<String, List<String>> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error -> {
            String field = error.getField();
            String message = error.getDefaultMessage();
            errors.computeIfAbsent(field, k -> new ArrayList<>()).add(message);
        });
        
        return ValidationErrorResponse.builder()
            .status(HttpStatus.UNPROCESSABLE_ENTITY.value())
            .error("VALIDATION_FAILED")
            .message("Błędy walidacji danych wejściowych")
            .errors(errors)
            .timestamp(LocalDateTime.now())
            .path(getCurrentPath())
            .build();
    }
    
    @ExceptionHandler(ConstraintViolationException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public ValidationErrorResponse handleConstraintViolation(ConstraintViolationException ex) {
        Map<String, List<String>> errors = new HashMap<>();
        
        ex.getConstraintViolations().forEach(violation -> {
            String field = violation.getPropertyPath().toString();
            String message = violation.getMessage();
            errors.computeIfAbsent(field, k -> new ArrayList<>()).add(message);
        });
        
        return ValidationErrorResponse.builder()
            .status(HttpStatus.BAD_REQUEST.value())
            .error("CONSTRAINT_VIOLATION")
            .message("Naruszenie ograniczeń walidacji")
            .errors(errors)
            .timestamp(LocalDateTime.now())
            .path(getCurrentPath())
            .build();
    }
    
    private String getCurrentPath() {
        RequestAttributes requestAttributes = RequestContextHolder.getRequestAttributes();
        if (requestAttributes instanceof ServletRequestAttributes) {
            HttpServletRequest request = ((ServletRequestAttributes) requestAttributes).getRequest();
            return request.getRequestURI();
        }
        return "unknown";
    }
}
```

## 🔧 API Versioning

```java
// URL Versioning
@RestController
@RequestMapping("/api/v1/users")
public class UserV1Controller { ... }

@RestController  
@RequestMapping("/api/v2/users")
public class UserV2Controller { ... }

// Header Versioning
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping(headers = "X-API-Version=1")
    public ResponseEntity<UserDtoV1> getUserV1(@PathVariable Long id) { ... }
    
    @GetMapping(headers = "X-API-Version=2")
    public ResponseEntity<UserDtoV2> getUserV2(@PathVariable Long id) { ... }
}

// Accept Header Versioning
@GetMapping(produces = "application/vnd.myapp.v1+json")
public ResponseEntity<UserDtoV1> getUserV1(@PathVariable Long id) { ... }

@GetMapping(produces = "application/vnd.myapp.v2+json")
public ResponseEntity<UserDtoV2> getUserV2(@PathVariable Long id) { ... }
```

---

## 🔗 Następny Krok
[[Java JPA Hibernate|💾 Java - JPA/Hibernate]] - mapowanie obiektowo-relacyjne i operacje na bazie danych

---
*Czas nauki: ~7 minut*