# 🎨 Java Web - Pattern MVC

## 🏗️ Model-View-Controller Architecture

### 📋 Komponenty MVC
1. **Model** - dane i logika biznesowa
2. **View** - prezentacja (HTML, JSON)  
3. **Controller** - obsługa żądań HTTP

```
┌─────────────┐    HTTP Request     ┌──────────────┐
│   Browser   │ ───────────────────>│  Controller  │
└─────────────┘                     └──────────────┘
       ▲                                     │
       │                                     ▼
       │            ┌──────────┐    ┌──────────────┐
       │            │   View   │<───│    Model     │
       │            └──────────┘    └──────────────┘
       │                     ▲               │
       └─────────────────────┘               ▼
            HTTP Response              ┌──────────────┐
                                      │   Database   │
                                      └──────────────┘
```

## 📦 Model Layer

### 🎯 Entity Classes (JPA)

```java
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 100)
    private String firstName;
    
    @Column(nullable = false, length = 100)
    private String lastName;
    
    @Column(nullable = false, unique = true)
    private String email;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // Relationships
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Post> posts = new ArrayList<>();
    
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id"),
        inverseJoinColumns = @JoinColumn(name = "role_id")
    )
    private Set<Role> roles = new HashSet<>();
    
    // Constructors, getters, setters
}
```

### 🔧 DTO (Data Transfer Objects)

```java
// Request DTO
public class CreateUserRequest {
    
    @NotBlank(message = "Imię jest wymagane")
    private String firstName;
    
    @NotBlank(message = "Nazwisko jest wymagane")  
    private String lastName;
    
    @Email(message = "Nieprawidłowy format email")
    private String email;
    
    // Constructors, getters, setters
}

// Response DTO
public class UserResponse {
    
    private Long id;
    private String firstName;
    private String lastName;
    private String email;
    private String fullName;
    private LocalDateTime createdAt;
    private List<PostSummary> recentPosts;
    
    // Constructor z Entity
    public UserResponse(User user) {
        this.id = user.getId();
        this.firstName = user.getFirstName();
        this.lastName = user.getLastName();
        this.email = user.getEmail();
        this.fullName = user.getFirstName() + " " + user.getLastName();
        this.createdAt = user.getCreatedAt();
        this.recentPosts = user.getPosts().stream()
            .limit(5)
            .map(PostSummary::new)
            .collect(Collectors.toList());
    }
}
```

### 📊 Repository Layer

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Query methods
    Optional<User> findByEmail(String email);
    List<User> findByFirstNameContainingIgnoreCase(String firstName);
    boolean existsByEmail(String email);
    
    // Custom JPQL queries
    @Query("SELECT u FROM User u WHERE u.createdAt >= :date")
    List<User> findUsersCreatedAfter(@Param("date") LocalDateTime date);
    
    @Query("SELECT u FROM User u JOIN u.posts p WHERE p.title LIKE %:keyword%")
    List<User> findUsersByPostKeyword(@Param("keyword") String keyword);
    
    // Native SQL query
    @Query(value = "SELECT * FROM users WHERE email LIKE %:domain%", nativeQuery = true)
    List<User> findByEmailDomain(@Param("domain") String domain);
    
    // Paging and sorting
    Page<User> findByLastNameStartsWith(String prefix, Pageable pageable);
}
```

## 🎮 Controller Layer

### 🚀 REST Controllers

```java
@RestController
@RequestMapping("/api/v1/users")
@Validated
@CrossOrigin(origins = {"http://localhost:3000", "http://localhost:4200"})
public class UserController {
    
    private final UserService userService;
    
    public UserController(UserService userService) {
        this.userService = userService;
    }
    
    // GET /api/v1/users?page=0&size=10&sort=lastName,asc
    @GetMapping
    public ResponseEntity<Page<UserResponse>> getAllUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(defaultValue = "id") String sortBy,
            @RequestParam(defaultValue = "ASC") Sort.Direction sortDir,
            @RequestParam(required = false) String search) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by(sortDir, sortBy));
        Page<UserResponse> users = userService.findAll(pageable, search);
        return ResponseEntity.ok(users);
    }
    
    @GetMapping("/{id}")
    public ResponseEntity<UserResponse> getUserById(@PathVariable @Min(1) Long id) {
        UserResponse user = userService.findById(id);
        return ResponseEntity.ok(user);
    }
    
    @PostMapping
    public ResponseEntity<UserResponse> createUser(@RequestBody @Valid CreateUserRequest request) {
        UserResponse createdUser = userService.create(request);
        
        URI location = ServletUriComponentsBuilder
            .fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(createdUser.getId())
            .toUri();
            
        return ResponseEntity.created(location).body(createdUser);
    }
}
```

### 🎨 Traditional MVC Controller (z widokami)

```java
@Controller
@RequestMapping("/users")
public class UserViewController {
    
    private final UserService userService;
    
    public UserViewController(UserService userService) {
        this.userService = userService;
    }
    
    // GET /users - lista użytkowników
    @GetMapping
    public String listUsers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            Model model) {
        
        Page<User> users = userService.findAll(PageRequest.of(page, size));
        
        model.addAttribute("users", users);
        model.addAttribute("currentPage", page);
        model.addAttribute("totalPages", users.getTotalPages());
        
        return "users/list"; // templates/users/list.html
    }
    
    // GET /users/new - formularz nowego użytkownika
    @GetMapping("/new")
    public String newUserForm(Model model) {
        model.addAttribute("user", new CreateUserRequest());
        return "users/form";
    }
    
    // POST /users - zapisz nowego użytkownika
    @PostMapping
    public String createUser(@ModelAttribute @Valid CreateUserRequest request, 
                           BindingResult bindingResult,
                           RedirectAttributes redirectAttributes) {
        
        if (bindingResult.hasErrors()) {
            return "users/form";
        }
        
        try {
            UserResponse user = userService.create(request);
            redirectAttributes.addFlashAttribute("message", 
                "Użytkownik " + user.getFullName() + " został utworzony!");
            return "redirect:/users";
        } catch (Exception e) {
            bindingResult.reject("error.general", "Wystąpił błąd podczas zapisu");
            return "users/form";
        }
    }
    
    // GET /users/123/edit - formularz edycji
    @GetMapping("/{id}/edit")
    public String editUserForm(@PathVariable Long id, Model model) {
        UserResponse user = userService.findById(id);
        model.addAttribute("user", user);
        model.addAttribute("isEdit", true);
        return "users/form";
    }
}
```

## 🔧 Service Layer (Business Logic)

```java
@Service
@Transactional(readOnly = true)
public class UserService {
    
    private final UserRepository userRepository;
    private final ModelMapper modelMapper;
    
    public UserService(UserRepository userRepository, ModelMapper modelMapper) {
        this.userRepository = userRepository;
        this.modelMapper = modelMapper;
    }
    
    // Odczyt z paginacją i wyszukiwaniem
    public Page<UserResponse> findAll(Pageable pageable, String search) {
        Page<User> users;
        
        if (search != null && !search.trim().isEmpty()) {
            users = userRepository.findByFirstNameContainingIgnoreCaseOrLastNameContainingIgnoreCase(
                search, search, pageable
            );
        } else {
            users = userRepository.findAll(pageable);
        }
        
        return users.map(UserResponse::new);
    }
    
    public UserResponse findById(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("Użytkownik o ID " + id + " nie istnieje"));
        return new UserResponse(user);
    }
    
    // Zapis (transactional)
    @Transactional
    public UserResponse create(CreateUserRequest request) {
        // Sprawdź czy email już istnieje
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException("Email " + request.getEmail() + " już istnieje");
        }
        
        User user = new User();
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail());
        
        User savedUser = userRepository.save(user);
        
        // Wysłanie emaila powitalnego (asynchronicznie)
        emailService.sendWelcomeEmailAsync(savedUser.getEmail());
        
        return new UserResponse(savedUser);
    }
    
    @Transactional
    public UserResponse update(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("Użytkownik o ID " + id + " nie istnieje"));
        
        // Sprawdź czy email się zmienił i czy nowy email nie jest zajęty
        if (!user.getEmail().equals(request.getEmail()) && 
            userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException("Email " + request.getEmail() + " już istnieje");
        }
        
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail());
        
        User updatedUser = userRepository.save(user);
        return new UserResponse(updatedUser);
    }
    
    @Transactional
    public void deleteById(Long id) {
        if (!userRepository.existsById(id)) {
            throw new UserNotFoundException("Użytkownik o ID " + id + " nie istnieje");
        }
        
        // Soft delete lub hard delete
        userRepository.deleteById(id);
    }
}
```

## 🎯 Configuration & Mapping

### 🔄 Model Mapper Configuration

```java
@Configuration
public class MapperConfig {
    
    @Bean
    public ModelMapper modelMapper() {
        ModelMapper mapper = new ModelMapper();
        
        // Strategia mapowania
        mapper.getConfiguration()
            .setMatchingStrategy(MatchingStrategies.STRICT)
            .setFieldMatchingEnabled(true)
            .setSkipNullEnabled(true);
            
        // Custom mappings
        TypeMap<User, UserResponse> userMapping = mapper.createTypeMap(User.class, UserResponse.class);
        userMapping.addMapping(src -> src.getFirstName() + " " + src.getLastName(), 
                              UserResponse::setFullName);
        
        return mapper;
    }
}
```

### 🛠️ Validation Configuration

```java
@Configuration
public class ValidationConfig {
    
    @Bean
    public LocalValidatorFactoryBean validator() {
        return new LocalValidatorFactoryBean();
    }
    
    @Bean
    public MethodValidationPostProcessor methodValidationPostProcessor() {
        MethodValidationPostProcessor processor = new MethodValidationPostProcessor();
        processor.setValidator(validator());
        return processor;
    }
}

// Custom validator
@Component
public class EmailValidator implements ConstraintValidator<ValidEmail, String> {
    
    private static final String EMAIL_PATTERN = 
        "^[a-zA-Z0-9_+&*-]+(?:\\.[a-zA-Z0-9_+&*-]+)*@(?:[a-zA-Z0-9-]+\\.)+[a-zA-Z]{2,7}$";
    
    private Pattern pattern = Pattern.compile(EMAIL_PATTERN);
    
    @Override
    public boolean isValid(String email, ConstraintValidatorContext context) {
        return email != null && pattern.matcher(email).matches();
    }
}
```

---

## 🔗 Następny Krok
[[Java REST API|📡 Java - REST API]] - szczegóły tworzenia i konsumowania REST API

---
*Czas nauki: ~8 minut*