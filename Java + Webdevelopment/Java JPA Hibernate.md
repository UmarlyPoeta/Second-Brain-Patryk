# 💾 Java - JPA/Hibernate

## 🔗 JPA (Java Persistence API) Podstawy

### 📋 Kluczowe Koncepcje
- **Entity** - klasa Java mapowana na tabelę bazodanową
- **EntityManager** - zarządza cyklem życia encji  
- **Persistence Context** - zbiór zarządzanych encji
- **Repository** - warstwa dostępu do danych
- **JPQL** - język zapytań podobny do SQL

## 🏗️ Entity Configuration

### 🎯 Podstawowa Encja

```java
@Entity
@Table(name = "users", indexes = {
    @Index(name = "idx_users_email", columnList = "email", unique = true),
    @Index(name = "idx_users_created_at", columnList = "created_at")
})
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "first_name", nullable = false, length = 50)
    private String firstName;
    
    @Column(name = "last_name", nullable = false, length = 50) 
    private String lastName;
    
    @Column(name = "email", nullable = false, unique = true, length = 100)
    private String email;
    
    @Column(name = "age")
    @Min(value = 0, message = "Wiek musi być większy niż 0")
    @Max(value = 150, message = "Wiek musi być mniejszy niż 150")
    private Integer age;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status", length = 20)
    private UserStatus status = UserStatus.ACTIVE;
    
    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @Version
    private Long version; // Optimistic locking
    
    // Constructors, getters, setters
}

public enum UserStatus {
    ACTIVE, INACTIVE, SUSPENDED, DELETED
}
```

### 🔗 Relationships (Relacje)

```java
@Entity
@Table(name = "posts")
public class Post {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 200)
    private String title;
    
    @Lob // Large Object dla długich tekstów
    private String content;
    
    // Many-to-One: wiele postów należy do jednego użytkownika
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User author;
    
    // One-to-Many: jeden post ma wiele komentarzy
    @OneToMany(mappedBy = "post", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<Comment> comments = new ArrayList<>();
    
    // Many-to-Many: post może mieć wiele tagów
    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(
        name = "post_tags",
        joinColumns = @JoinColumn(name = "post_id"),
        inverseJoinColumns = @JoinColumn(name = "tag_id")
    )
    private Set<Tag> tags = new HashSet<>();
    
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @UpdateTimestamp
    private LocalDateTime updatedAt;
}

@Entity
@Table(name = "comments")
public class Comment {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, length = 500)
    private String content;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "post_id", nullable = false)
    private Post post;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User author;
    
    @CreationTimestamp
    private LocalDateTime createdAt;
}
```

### 🎯 Advanced Mappings

```java
@Entity
@Table(name = "user_profiles")
public class UserProfile {
    
    @Id
    private Long id;
    
    // One-to-One z shared primary key
    @OneToOne(fetch = FetchType.LAZY)
    @MapsId
    @JoinColumn(name = "user_id")
    private User user;
    
    @Column(length = 1000)
    private String bio;
    
    @Embedded
    private Address address;
    
    // JSON column (PostgreSQL/MySQL 5.7+)
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "json")
    private Map<String, Object> metadata;
}

@Embeddable
public class Address {
    
    @Column(name = "street")
    private String street;
    
    @Column(name = "city")
    private String city;
    
    @Column(name = "postal_code")
    private String postalCode;
    
    @Column(name = "country")
    private String country;
}
```

## 📚 Repository Layer

### 🚀 JpaRepository

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // Query methods (automatyczne generowanie zapytań)
    Optional<User> findByEmail(String email);
    List<User> findByFirstNameContainingIgnoreCase(String firstName);
    List<User> findByAgeGreaterThan(Integer age);
    List<User> findByStatusAndAgeGreaterThanOrderByCreatedAtDesc(UserStatus status, Integer age);
    
    boolean existsByEmail(String email);
    long countByStatus(UserStatus status);
    
    void deleteByStatus(UserStatus status);
    
    // Paging and sorting
    Page<User> findByStatus(UserStatus status, Pageable pageable);
    Slice<User> findByFirstNameContaining(String firstName, Pageable pageable);
}
```

### 🔍 Custom JPQL Queries

```java
@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    // JPQL Query
    @Query("SELECT u FROM User u WHERE u.email = :email AND u.status = :status")
    Optional<User> findByEmailAndStatus(@Param("email") String email, 
                                       @Param("status") UserStatus status);
    
    @Query("SELECT u FROM User u WHERE u.createdAt >= :fromDate ORDER BY u.createdAt DESC")
    List<User> findUsersCreatedAfter(@Param("fromDate") LocalDateTime fromDate);
    
    // Join query
    @Query("SELECT DISTINCT u FROM User u JOIN u.posts p WHERE p.title LIKE %:keyword%")
    List<User> findUsersByPostTitle(@Param("keyword") String keyword);
    
    // Projection query
    @Query("SELECT new com.example.dto.UserSummary(u.id, u.firstName, u.lastName, u.email) " +
           "FROM User u WHERE u.status = :status")
    List<UserSummary> findUserSummariesByStatus(@Param("status") UserStatus status);
    
    // Count query
    @Query("SELECT COUNT(u) FROM User u WHERE u.status = :status")
    long countUsersByStatus(@Param("status") UserStatus status);
    
    // Native SQL query
    @Query(value = "SELECT * FROM users WHERE email LIKE %:domain% AND created_at > :date", 
           nativeQuery = true)
    List<User> findByEmailDomainNative(@Param("domain") String domain, 
                                      @Param("date") LocalDateTime date);
    
    // Update query
    @Modifying
    @Query("UPDATE User u SET u.status = :newStatus WHERE u.status = :oldStatus")
    int updateUserStatus(@Param("oldStatus") UserStatus oldStatus, 
                         @Param("newStatus") UserStatus newStatus);
    
    // Delete query
    @Modifying
    @Query("DELETE FROM User u WHERE u.status = :status AND u.createdAt < :cutoffDate")
    int deleteInactiveUsers(@Param("status") UserStatus status, 
                           @Param("cutoffDate") LocalDateTime cutoffDate);
}
```

### 🎯 Custom Repository Implementation

```java
public interface UserRepositoryCustom {
    List<User> findUsersByComplexCriteria(UserSearchCriteria criteria);
    Page<User> findUsersWithFilters(UserFilter filter, Pageable pageable);
}

@Repository
public class UserRepositoryImpl implements UserRepositoryCustom {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @Override
    public List<User> findUsersByComplexCriteria(UserSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<User> query = cb.createQuery(User.class);
        Root<User> user = query.from(User.class);
        
        List<Predicate> predicates = new ArrayList<>();
        
        if (criteria.getFirstName() != null) {
            predicates.add(cb.like(cb.lower(user.get("firstName")), 
                                 "%" + criteria.getFirstName().toLowerCase() + "%"));
        }
        
        if (criteria.getEmail() != null) {
            predicates.add(cb.like(user.get("email"), "%" + criteria.getEmail() + "%"));
        }
        
        if (criteria.getMinAge() != null) {
            predicates.add(cb.greaterThanOrEqualTo(user.get("age"), criteria.getMinAge()));
        }
        
        if (criteria.getMaxAge() != null) {
            predicates.add(cb.lessThanOrEqualTo(user.get("age"), criteria.getMaxAge()));
        }
        
        if (criteria.getStatuses() != null && !criteria.getStatuses().isEmpty()) {
            predicates.add(user.get("status").in(criteria.getStatuses()));
        }
        
        query.where(cb.and(predicates.toArray(new Predicate[0])));
        query.orderBy(cb.desc(user.get("createdAt")));
        
        return entityManager.createQuery(query).getResultList();
    }
}
```

## ⚙️ JPA Configuration

### 🔧 Application Properties

```properties
# Database connection
spring.datasource.url=jdbc:postgresql://localhost:5432/myapp
spring.datasource.username=myuser
spring.datasource.password=mypassword
spring.datasource.driver-class-name=org.postgresql.Driver

# HikariCP connection pool
spring.datasource.hikari.maximum-pool-size=20
spring.datasource.hikari.minimum-idle=5
spring.datasource.hikari.idle-timeout=300000
spring.datasource.hikari.connection-timeout=20000

# JPA/Hibernate properties
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.show-sql=false
spring.jpa.properties.hibernate.format_sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
spring.jpa.properties.hibernate.jdbc.batch_size=20
spring.jpa.properties.hibernate.order_inserts=true
spring.jpa.properties.hibernate.order_updates=true
spring.jpa.properties.hibernate.jdbc.batch_versioned_data=true

# Flyway migration
spring.flyway.enabled=true
spring.flyway.locations=classpath:db/migration
spring.flyway.baseline-on-migrate=true
```

### 📊 Auditing Configuration

```java
@Configuration
@EnableJpaAuditing
public class JpaConfig {
    
    @Bean
    public AuditorAware<String> auditorProvider() {
        return new AuditorAwareImpl();
    }
}

public class AuditorAwareImpl implements AuditorAware<String> {
    
    @Override
    public Optional<String> getCurrentAuditor() {
        // Pobierz aktualnie zalogowanego użytkownika
        Authentication authentication = SecurityContextHolder.getContext().getAuthentication();
        if (authentication == null || !authentication.isAuthenticated() || 
            "anonymousUser".equals(authentication.getPrincipal())) {
            return Optional.empty();
        }
        return Optional.of(authentication.getName());
    }
}

// Entity z auditing
@Entity
@EntityListeners(AuditingEntityListener.class)
public class AuditableEntity {
    
    @CreatedDate
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;
    
    @LastModifiedDate
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @CreatedBy
    @Column(name = "created_by", updatable = false)
    private String createdBy;
    
    @LastModifiedBy
    @Column(name = "updated_by")
    private String updatedBy;
}
```

## 🚀 Service Layer z Transaction Management

```java
@Service
@Transactional(readOnly = true)
public class UserService {
    
    private final UserRepository userRepository;
    private final PostRepository postRepository;
    
    public UserService(UserRepository userRepository, PostRepository postRepository) {
        this.userRepository = userRepository;
        this.postRepository = postRepository;
    }
    
    // Read-only method (dziedziczy z klasy)
    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }
    
    public Page<User> findAll(Pageable pageable) {
        return userRepository.findAll(pageable);
    }
    
    // Write operation - nadpisanie @Transactional
    @Transactional
    public User createUser(CreateUserRequest request) {
        if (userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException("Email już istnieje: " + request.getEmail());
        }
        
        User user = new User();
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail());
        user.setStatus(UserStatus.ACTIVE);
        
        return userRepository.save(user);
    }
    
    @Transactional
    public User updateUser(Long id, UpdateUserRequest request) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
        
        // Sprawdź email conflict tylko jeśli się zmienił
        if (!user.getEmail().equals(request.getEmail()) && 
            userRepository.existsByEmail(request.getEmail())) {
            throw new EmailAlreadyExistsException("Email już istnieje: " + request.getEmail());
        }
        
        user.setFirstName(request.getFirstName());
        user.setLastName(request.getLastName());
        user.setEmail(request.getEmail());
        
        return userRepository.save(user);
    }
    
    @Transactional
    public void deleteUser(Long id) {
        User user = userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException("User not found: " + id));
        
        // Soft delete
        user.setStatus(UserStatus.DELETED);
        userRepository.save(user);
        
        // lub Hard delete
        // userRepository.deleteById(id);
    }
    
    @Transactional
    public void transferUserPosts(Long fromUserId, Long toUserId) {
        User fromUser = userRepository.findById(fromUserId)
            .orElseThrow(() -> new UserNotFoundException("Source user not found"));
        
        User toUser = userRepository.findById(toUserId)
            .orElseThrow(() -> new UserNotFoundException("Target user not found"));
        
        // Batch update w bazie danych
        int updatedPosts = postRepository.transferPostsToUser(fromUserId, toUserId);
        
        log.info("Transferred {} posts from user {} to user {}", 
                updatedPosts, fromUserId, toUserId);
    }
    
    // Propagation examples
    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void createUserWithNewTransaction(CreateUserRequest request) {
        // Ta metoda zawsze działa w nowej transakcji
        createUser(request);
    }
    
    @Transactional(readOnly = true, timeout = 30)
    public List<User> findUsersWithTimeout() {
        // Timeout 30 sekund dla długich operacji read-only
        return userRepository.findAll();
    }
}
```

---

## 🔗 Podsumowanie
To kończy naszą podróż przez Java web development! Masz teraz solidne podstawy do budowania aplikacji webowych z Java i Spring Boot.

### 🎯 Najważniejsze Punkty:
1. **Java OOP** - enkapsulacja, dziedziczenie, polimorfizm
2. **Spring Boot** - auto-konfiguracja, dependency injection
3. **REST API** - HTTP methods, status codes, JSON
4. **JPA/Hibernate** - mapowanie obiektowo-relacyjne, transakcje

### 🚀 Dalsze Kroki:
- Praktyka z projektami
- Spring Security dla autoryzacji
- Spring Boot Testing
- Microservices z Spring Cloud
- Docker i deployment

---
*Czas nauki: ~10 minut | Całkowity czas: ~60 minut*