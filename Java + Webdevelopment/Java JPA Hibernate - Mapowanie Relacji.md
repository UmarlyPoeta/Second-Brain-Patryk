# 💾 Java - JPA/Hibernate - Mapowanie Relacji

## 📚 Wprowadzenie
JPA (Java Persistence API) to specyfikacja Java EE dla mapowania obiektowo-relacyjnego (ORM). Hibernate to najpopularniejsza implementacja JPA. Umożliwia mapowanie obiektów Java na tabele w bazie danych i automatyzuje operacje CRUD.

## 🏗️ Podstawowa Konfiguracja

### Entity i Basic Mapping
```java
import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.math.BigDecimal;
import java.util.*;

@Entity
@Table(name = "users", 
       indexes = {
           @Index(name = "idx_username", columnList = "username"),
           @Index(name = "idx_email", columnList = "email")
       },
       uniqueConstraints = {
           @UniqueConstraint(name = "uk_username", columnNames = "username"),
           @UniqueConstraint(name = "uk_email", columnNames = "email")
       })
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", nullable = false, length = 50)
    private String username;
    
    @Column(name = "email", nullable = false, length = 100)
    private String email;
    
    @Column(name = "password_hash", nullable = false)
    private String passwordHash;
    
    @Column(name = "first_name", length = 50)
    private String firstName;
    
    @Column(name = "last_name", length = 50)
    private String lastName;
    
    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;
    
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @Column(name = "is_active")
    private Boolean isActive = true;
    
    @Column(name = "last_login")
    @Temporal(TemporalType.TIMESTAMP)
    private Date lastLogin;
    
    // Enum mapping
    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private UserStatus status = UserStatus.ACTIVE;
    
    // Large objects
    @Lob
    @Column(name = "profile_picture")
    private byte[] profilePicture;
    
    @Lob
    @Column(name = "bio", columnDefinition = "TEXT")
    private String bio;
    
    // Transient fields (not persisted)
    @Transient
    private String displayName;
    
    // Lifecycle callbacks
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
    // Constructors
    public User() {}
    
    public User(String username, String email, String passwordHash) {
        this.username = username;
        this.email = email;
        this.passwordHash = passwordHash;
    }
    
    // Custom method
    public String getDisplayName() {
        if (displayName == null) {
            displayName = firstName != null && lastName != null 
                ? firstName + " " + lastName 
                : username;
        }
        return displayName;
    }
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    
    // ... other getters and setters
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        User user = (User) o;
        return Objects.equals(id, user.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
    
    @Override
    public String toString() {
        return "User{id=" + id + ", username='" + username + "', email='" + email + "'}";
    }
}

enum UserStatus {
    ACTIVE, SUSPENDED, INACTIVE, DELETED
}
```

### Advanced Column Mappings
```java
@Entity
@Table(name = "products")
public class Product {
    
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "product_seq")
    @SequenceGenerator(name = "product_seq", sequenceName = "product_sequence", 
                       allocationSize = 1, initialValue = 1000)
    private Long id;
    
    @Column(name = "name", nullable = false, length = 200)
    private String name;
    
    // Precision and scale for decimal numbers
    @Column(name = "price", precision = 10, scale = 2, nullable = false)
    private BigDecimal price;
    
    @Column(name = "cost_price", precision = 10, scale = 2)
    private BigDecimal costPrice;
    
    // Custom column definition
    @Column(name = "sku", nullable = false, length = 100, 
            columnDefinition = "VARCHAR(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
    private String sku;
    
    // JSON column (for databases that support it)
    @Column(name = "metadata", columnDefinition = "JSON")
    private String metadata;
    
    // Custom converter
    @Convert(converter = DimensionsConverter.class)
    @Column(name = "dimensions")
    private Dimensions dimensions;
    
    // Embedded object
    @Embedded
    private ProductDetails details;
    
    @Column(name = "created_at", nullable = false)
    @CreationTimestamp
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    @UpdateTimestamp
    private LocalDateTime updatedAt;
    
    // Constructors, getters, setters...
}

// Custom converter
@Converter
public class DimensionsConverter implements AttributeConverter<Dimensions, String> {
    
    @Override
    public String convertToDatabaseColumn(Dimensions dimensions) {
        if (dimensions == null) return null;
        return dimensions.getWidth() + "x" + dimensions.getHeight() + "x" + dimensions.getDepth();
    }
    
    @Override
    public Dimensions convertToEntityAttribute(String dbData) {
        if (dbData == null || dbData.isEmpty()) return null;
        
        String[] parts = dbData.split("x");
        if (parts.length != 3) return null;
        
        try {
            return new Dimensions(
                Double.parseDouble(parts[0]),
                Double.parseDouble(parts[1]),
                Double.parseDouble(parts[2])
            );
        } catch (NumberFormatException e) {
            return null;
        }
    }
}

// Value object
public class Dimensions {
    private double width;
    private double height;
    private double depth;
    
    public Dimensions(double width, double height, double depth) {
        this.width = width;
        this.height = height;
        this.depth = depth;
    }
    
    // Getters, equals, hashCode, toString...
}

// Embeddable class
@Embeddable
public class ProductDetails {
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "weight", precision = 8, scale = 3)
    private BigDecimal weight;
    
    @Column(name = "stock_quantity")
    private Integer stockQuantity = 0;
    
    @Column(name = "min_stock_level")
    private Integer minStockLevel = 0;
    
    @Column(name = "is_active")
    private Boolean active = true;
    
    // Constructors, getters, setters...
}
```

## 🔗 Mapowanie Relacji

### One-to-Many i Many-to-One
```java
// Parent side (One)
@Entity
@Table(name = "categories")
public class Category {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false, length = 100)
    private String name;
    
    @Column(name = "description", columnDefinition = "TEXT")
    private String description;
    
    @Column(name = "slug", nullable = false, length = 100)
    private String slug;
    
    // Self-referencing relationship - parent category
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "parent_category_id", foreignKey = @ForeignKey(name = "fk_category_parent"))
    private Category parentCategory;
    
    // One-to-Many: Category has many subcategories
    @OneToMany(mappedBy = "parentCategory", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Category> subcategories = new ArrayList<>();
    
    // One-to-Many: Category has many products
    @OneToMany(mappedBy = "category", cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    private List<Product> products = new ArrayList<>();
    
    // Constructors
    public Category() {}
    
    public Category(String name, String description, String slug) {
        this.name = name;
        this.description = description;
        this.slug = slug;
    }
    
    // Helper methods for bidirectional relationships
    public void addSubcategory(Category subcategory) {
        subcategories.add(subcategory);
        subcategory.setParentCategory(this);
    }
    
    public void removeSubcategory(Category subcategory) {
        subcategories.remove(subcategory);
        subcategory.setParentCategory(null);
    }
    
    public void addProduct(Product product) {
        products.add(product);
        product.setCategory(this);
    }
    
    public void removeProduct(Product product) {
        products.remove(product);
        product.setCategory(null);
    }
    
    // Getters and setters...
}

// Child side (Many)
@Entity
@Table(name = "products")
public class Product {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false, length = 200)
    private String name;
    
    @Column(name = "price", precision = 10, scale = 2, nullable = false)
    private BigDecimal price;
    
    // Many-to-One: Many products belong to one category
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    @JoinColumn(name = "category_id", nullable = false, 
                foreignKey = @ForeignKey(name = "fk_product_category"))
    private Category category;
    
    // Constructors, getters, setters...
    
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Product product = (Product) o;
        return Objects.equals(id, product.id);
    }
    
    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
```

### Many-to-Many Relationships
```java
// Simple Many-to-Many
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", nullable = false, unique = true)
    private String username;
    
    // Many-to-Many: User has many roles
    @ManyToMany(fetch = FetchType.LAZY, cascade = {CascadeType.PERSIST, CascadeType.MERGE})
    @JoinTable(
        name = "user_roles",
        joinColumns = @JoinColumn(name = "user_id", foreignKey = @ForeignKey(name = "fk_user_roles_user")),
        inverseJoinColumns = @JoinColumn(name = "role_id", foreignKey = @ForeignKey(name = "fk_user_roles_role"))
    )
    private Set<Role> roles = new HashSet<>();
    
    // Helper methods
    public void addRole(Role role) {
        roles.add(role);
        role.getUsers().add(this);
    }
    
    public void removeRole(Role role) {
        roles.remove(role);
        role.getUsers().remove(this);
    }
    
    // Getters, setters...
}

@Entity
@Table(name = "roles")
public class Role {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "name", nullable = false, unique = true)
    private String name;
    
    @Column(name = "description")
    private String description;
    
    // Many-to-Many: Role belongs to many users
    @ManyToMany(mappedBy = "roles", fetch = FetchType.LAZY)
    private Set<User> users = new HashSet<>();
    
    // Constructors, getters, setters...
}

// Many-to-Many with Join Entity (Association Entity)
@Entity
@Table(name = "order_items")
public class OrderItem {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    // Many-to-One to Order
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "order_id", nullable = false)
    private Order order;
    
    // Many-to-One to Product
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;
    
    // Additional attributes of the relationship
    @Column(name = "quantity", nullable = false)
    private Integer quantity;
    
    @Column(name = "unit_price", precision = 10, scale = 2, nullable = false)
    private BigDecimal unitPrice;
    
    @Column(name = "total_price", precision = 12, scale = 2, nullable = false)
    private BigDecimal totalPrice;
    
    // Calculated field
    @PostLoad
    @PrePersist
    @PreUpdate
    private void calculateTotalPrice() {
        if (quantity != null && unitPrice != null) {
            totalPrice = unitPrice.multiply(BigDecimal.valueOf(quantity));
        }
    }
    
    // Constructors, getters, setters...
}

@Entity
@Table(name = "orders")
public class Order {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "order_number", nullable = false, unique = true)
    private String orderNumber;
    
    // One-to-Many to OrderItem
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, fetch = FetchType.LAZY, orphanRemoval = true)
    private List<OrderItem> orderItems = new ArrayList<>();
    
    // Many-to-One to User
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id", nullable = false)
    private User user;
    
    @Enumerated(EnumType.STRING)
    @Column(name = "status")
    private OrderStatus status = OrderStatus.PENDING;
    
    @Column(name = "order_date", nullable = false)
    private LocalDateTime orderDate;
    
    @Column(name = "total_amount", precision = 12, scale = 2, nullable = false)
    private BigDecimal totalAmount = BigDecimal.ZERO;
    
    // Helper methods
    public void addOrderItem(OrderItem orderItem) {
        orderItems.add(orderItem);
        orderItem.setOrder(this);
        calculateTotalAmount();
    }
    
    public void removeOrderItem(OrderItem orderItem) {
        orderItems.remove(orderItem);
        orderItem.setOrder(null);
        calculateTotalAmount();
    }
    
    private void calculateTotalAmount() {
        totalAmount = orderItems.stream()
            .map(OrderItem::getTotalPrice)
            .filter(Objects::nonNull)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
    
    @PrePersist
    @PreUpdate
    private void updateTotalAmount() {
        calculateTotalAmount();
    }
}

enum OrderStatus {
    PENDING, CONFIRMED, PROCESSING, SHIPPED, DELIVERED, CANCELLED
}
```

### One-to-One Relationships
```java
// Shared Primary Key
@Entity
@Table(name = "users")
public class User {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "username", nullable = false, unique = true)
    private String username;
    
    // One-to-One with shared primary key
    @OneToOne(mappedBy = "user", cascade = CascadeType.ALL, fetch = FetchType.LAZY, optional = true)
    @PrimaryKeyJoinColumn
    private UserProfile profile;
    
    // One-to-One with foreign key
    @OneToOne(cascade = CascadeType.ALL, fetch = FetchType.LAZY)
    @JoinColumn(name = "address_id", foreignKey = @ForeignKey(name = "fk_user_address"))
    private Address primaryAddress;
    
    // Helper methods
    public void setProfile(UserProfile profile) {
        this.profile = profile;
        if (profile != null) {
            profile.setUser(this);
        }
    }
    
    // Getters, setters...
}

@Entity
@Table(name = "user_profiles")
public class UserProfile {
    
    // Shared primary key with User
    @Id
    private Long id;
    
    @OneToOne(fetch = FetchType.LAZY)
    @MapsId  // This tells Hibernate to use the User's ID
    @JoinColumn(name = "user_id")
    private User user;
    
    @Column(name = "first_name", length = 50)
    private String firstName;
    
    @Column(name = "last_name", length = 50)
    private String lastName;
    
    @Column(name = "date_of_birth")
    private LocalDate dateOfBirth;
    
    @Column(name = "phone_number", length = 20)
    private String phoneNumber;
    
    @Lob
    @Column(name = "bio", columnDefinition = "TEXT")
    private String bio;
    
    @Column(name = "avatar_url")
    private String avatarUrl;
    
    // Constructors, getters, setters...
}

@Entity
@Table(name = "addresses")
public class Address {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "street_line1", nullable = false, length = 200)
    private String streetLine1;
    
    @Column(name = "street_line2", length = 200)
    private String streetLine2;
    
    @Column(name = "city", nullable = false, length = 100)
    private String city;
    
    @Column(name = "state", length = 100)
    private String state;
    
    @Column(name = "postal_code", nullable = false, length = 20)
    private String postalCode;
    
    @Column(name = "country", nullable = false, length = 100)
    private String country = "Poland";
    
    @Enumerated(EnumType.STRING)
    @Column(name = "type")
    private AddressType type = AddressType.HOME;
    
    // One-to-One back reference (optional)
    @OneToOne(mappedBy = "primaryAddress", fetch = FetchType.LAZY)
    private User user;
    
    // Constructors, getters, setters...
}

enum AddressType {
    HOME, WORK, SHIPPING, BILLING
}
```

## 🔍 Zaawansowane Zapytania

### JPQL (Java Persistence Query Language)
```java
@Repository
public class UserRepositoryImpl {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    // Basic JPQL queries
    public List<User> findActiveUsers() {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.isActive = true", 
            User.class
        ).getResultList();
    }
    
    public List<User> findUsersByRole(String roleName) {
        return entityManager.createQuery(
            "SELECT u FROM User u JOIN u.roles r WHERE r.name = :roleName",
            User.class
        )
        .setParameter("roleName", roleName)
        .getResultList();
    }
    
    // Named parameters
    public User findByUsernameAndEmail(String username, String email) {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.username = :username AND u.email = :email",
            User.class
        )
        .setParameter("username", username)
        .setParameter("email", email)
        .getSingleResult();
    }
    
    // Positional parameters
    public List<User> findUsersCreatedBetween(LocalDateTime start, LocalDateTime end) {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.createdAt BETWEEN ?1 AND ?2 ORDER BY u.createdAt DESC",
            User.class
        )
        .setParameter(1, start)
        .setParameter(2, end)
        .getResultList();
    }
    
    // JOIN queries
    public List<Object[]> findUsersWithOrderCount() {
        return entityManager.createQuery(
            "SELECT u.username, COUNT(o.id) " +
            "FROM User u LEFT JOIN u.orders o " +
            "GROUP BY u.id, u.username " +
            "HAVING COUNT(o.id) > 0 " +
            "ORDER BY COUNT(o.id) DESC",
            Object[].class
        ).getResultList();
    }
    
    // Subqueries
    public List<User> findUsersWithHighValueOrders(BigDecimal minAmount) {
        return entityManager.createQuery(
            "SELECT u FROM User u " +
            "WHERE EXISTS (SELECT o FROM Order o WHERE o.user = u AND o.totalAmount > :minAmount)",
            User.class
        )
        .setParameter("minAmount", minAmount)
        .getResultList();
    }
    
    // Aggregate functions
    public UserStatistics getUserStatistics(Long userId) {
        Object[] result = (Object[]) entityManager.createQuery(
            "SELECT COUNT(o.id), SUM(o.totalAmount), AVG(o.totalAmount), MAX(o.orderDate) " +
            "FROM Order o WHERE o.user.id = :userId"
        )
        .setParameter("userId", userId)
        .getSingleResult();
        
        return new UserStatistics(
            ((Long) result[0]).intValue(),
            (BigDecimal) result[1],
            (BigDecimal) result[2],
            (LocalDateTime) result[3]
        );
    }
    
    // Constructor expressions (DTO projection)
    public List<UserSummaryDTO> findUserSummaries() {
        return entityManager.createQuery(
            "SELECT new com.example.dto.UserSummaryDTO(u.id, u.username, u.email, COUNT(o.id)) " +
            "FROM User u LEFT JOIN u.orders o " +
            "GROUP BY u.id, u.username, u.email",
            UserSummaryDTO.class
        ).getResultList();
    }
    
    // Update queries
    @Transactional
    public int updateUserStatus(UserStatus newStatus, List<Long> userIds) {
        return entityManager.createQuery(
            "UPDATE User u SET u.status = :status, u.updatedAt = :now " +
            "WHERE u.id IN :userIds"
        )
        .setParameter("status", newStatus)
        .setParameter("now", LocalDateTime.now())
        .setParameter("userIds", userIds)
        .executeUpdate();
    }
    
    // Delete queries
    @Transactional
    public int deleteInactiveUsers(LocalDateTime cutoffDate) {
        return entityManager.createQuery(
            "DELETE FROM User u WHERE u.isActive = false AND u.lastLogin < :cutoffDate"
        )
        .setParameter("cutoffDate", cutoffDate)
        .executeUpdate();
    }
}
```

### Criteria API
```java
@Repository
public class ProductSearchRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<Product> searchProducts(ProductSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Product> query = cb.createQuery(Product.class);
        Root<Product> product = query.from(Product.class);
        
        List<Predicate> predicates = new ArrayList<>();
        
        // Name filter
        if (criteria.getName() != null && !criteria.getName().isEmpty()) {
            predicates.add(cb.like(cb.lower(product.get("name")), 
                "%" + criteria.getName().toLowerCase() + "%"));
        }
        
        // Price range filter
        if (criteria.getMinPrice() != null) {
            predicates.add(cb.greaterThanOrEqualTo(product.get("price"), criteria.getMinPrice()));
        }
        if (criteria.getMaxPrice() != null) {
            predicates.add(cb.lessThanOrEqualTo(product.get("price"), criteria.getMaxPrice()));
        }
        
        // Category filter
        if (criteria.getCategoryId() != null) {
            Join<Product, Category> categoryJoin = product.join("category");
            predicates.add(cb.equal(categoryJoin.get("id"), criteria.getCategoryId()));
        }
        
        // Active status filter
        if (criteria.getActiveOnly() != null && criteria.getActiveOnly()) {
            predicates.add(cb.equal(product.get("details").get("active"), true));
        }
        
        // In stock filter
        if (criteria.getInStockOnly() != null && criteria.getInStockOnly()) {
            predicates.add(cb.greaterThan(product.get("details").get("stockQuantity"), 0));
        }
        
        // Apply all predicates
        if (!predicates.isEmpty()) {
            query.where(cb.and(predicates.toArray(new Predicate[0])));
        }
        
        // Sorting
        if (criteria.getSortBy() != null) {
            Path<Object> sortPath = product.get(criteria.getSortBy());
            if (criteria.getSortDirection() == SortDirection.DESC) {
                query.orderBy(cb.desc(sortPath));
            } else {
                query.orderBy(cb.asc(sortPath));
            }
        }
        
        TypedQuery<Product> typedQuery = entityManager.createQuery(query);
        
        // Pagination
        if (criteria.getOffset() != null) {
            typedQuery.setFirstResult(criteria.getOffset());
        }
        if (criteria.getLimit() != null) {
            typedQuery.setMaxResults(criteria.getLimit());
        }
        
        return typedQuery.getResultList();
    }
    
    // Count query for pagination
    public Long countProducts(ProductSearchCriteria criteria) {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<Long> query = cb.createQuery(Long.class);
        Root<Product> product = query.from(Product.class);
        
        // Apply same filters as search query
        List<Predicate> predicates = new ArrayList<>();
        // ... (same filter logic as above)
        
        query.select(cb.count(product));
        
        if (!predicates.isEmpty()) {
            query.where(cb.and(predicates.toArray(new Predicate[0])));
        }
        
        return entityManager.createQuery(query).getSingleResult();
    }
    
    // Complex query with multiple joins and aggregations
    public List<CategoryStatistics> getCategoryStatistics() {
        CriteriaBuilder cb = entityManager.getCriteriaBuilder();
        CriteriaQuery<CategoryStatistics> query = cb.createQuery(CategoryStatistics.class);
        
        Root<Category> category = query.from(Category.class);
        Join<Category, Product> productJoin = category.join("products", JoinType.LEFT);
        Join<Product, OrderItem> orderItemJoin = productJoin.join("orderItems", JoinType.LEFT);
        
        query.select(cb.construct(
            CategoryStatistics.class,
            category.get("id"),
            category.get("name"),
            cb.count(productJoin.get("id")).alias("productCount"),
            cb.coalesce(cb.sum(orderItemJoin.get("quantity")), 0L).alias("totalSold"),
            cb.coalesce(cb.sum(orderItemJoin.get("totalPrice")), BigDecimal.ZERO).alias("totalRevenue")
        ));
        
        query.groupBy(category.get("id"), category.get("name"));
        query.orderBy(cb.desc(cb.sum(orderItemJoin.get("totalPrice"))));
        
        return entityManager.createQuery(query).getResultList();
    }
}

// Search criteria class
public class ProductSearchCriteria {
    private String name;
    private BigDecimal minPrice;
    private BigDecimal maxPrice;
    private Long categoryId;
    private Boolean activeOnly;
    private Boolean inStockOnly;
    private String sortBy;
    private SortDirection sortDirection;
    private Integer offset;
    private Integer limit;
    
    // Constructors, getters, setters...
}

enum SortDirection {
    ASC, DESC
}

// Statistics DTO
public class CategoryStatistics {
    private Long categoryId;
    private String categoryName;
    private Long productCount;
    private Long totalSold;
    private BigDecimal totalRevenue;
    
    // Constructor, getters, setters...
}
```

## ⚡ Performance i Optymalizacja

### Fetch Strategies i N+1 Problem
```java
// Demonstrating N+1 problem and solutions
@Repository
public class OptimizedUserRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    // BAD: N+1 problem - causes multiple queries
    public List<User> findUsersWithOrders_Bad() {
        List<User> users = entityManager.createQuery(
            "SELECT u FROM User u", 
            User.class
        ).getResultList();
        
        // This will trigger N additional queries (one for each user's orders)
        for (User user : users) {
            user.getOrders().size(); // Force lazy loading
        }
        
        return users;
    }
    
    // GOOD: Using JOIN FETCH to avoid N+1 problem
    public List<User> findUsersWithOrders_Good() {
        return entityManager.createQuery(
            "SELECT DISTINCT u FROM User u LEFT JOIN FETCH u.orders",
            User.class
        ).getResultList();
    }
    
    // GOOD: Multiple JOIN FETCH for nested relationships
    public List<User> findUsersWithOrdersAndItems() {
        return entityManager.createQuery(
            "SELECT DISTINCT u FROM User u " +
            "LEFT JOIN FETCH u.orders o " +
            "LEFT JOIN FETCH o.orderItems oi " +
            "LEFT JOIN FETCH oi.product",
            User.class
        ).getResultList();
    }
    
    // GOOD: Using entity graphs to control fetching
    @EntityGraph(attributePaths = {"orders", "orders.orderItems", "orders.orderItems.product"})
    public List<User> findUsersWithEntityGraph() {
        return entityManager.createQuery(
            "SELECT u FROM User u",
            User.class
        )
        .setHint("javax.persistence.fetchgraph", 
                entityManager.getEntityGraph("User.withOrdersAndItems"))
        .getResultList();
    }
    
    // Named Entity Graph
    @NamedEntityGraph(
        name = "User.withOrders",
        attributeNodes = {
            @NamedAttributeNode(value = "orders", subgraph = "orders"),
            @NamedAttributeNode("profile")
        },
        subgraphs = {
            @NamedSubgraph(
                name = "orders",
                attributeNodes = {
                    @NamedAttributeNode("orderItems"),
                    @NamedAttributeNode("status")
                }
            )
        }
    )
    public List<User> findUsersWithNamedEntityGraph() {
        return entityManager.createQuery("SELECT u FROM User u", User.class)
            .setHint("javax.persistence.loadgraph", 
                    entityManager.getEntityGraph("User.withOrders"))
            .getResultList();
    }
    
    // Batch fetching configuration
    @BatchSize(size = 10)  // In entity class
    public List<User> findUsersWithBatchFetch() {
        // This will fetch users in batches of 10 when accessing lazy collections
        return entityManager.createQuery("SELECT u FROM User u", User.class)
            .getResultList();
    }
    
    // Pagination for large datasets
    public Page<User> findUsersPageable(int page, int size) {
        // Count query
        Long total = entityManager.createQuery(
            "SELECT COUNT(u) FROM User u", 
            Long.class
        ).getSingleResult();
        
        // Data query with pagination
        List<User> users = entityManager.createQuery(
            "SELECT u FROM User u ORDER BY u.createdAt DESC", 
            User.class
        )
        .setFirstResult(page * size)
        .setMaxResults(size)
        .getResultList();
        
        return new Page<>(users, page, size, total);
    }
}

// Custom Page class
public class Page<T> {
    private List<T> content;
    private int pageNumber;
    private int pageSize;
    private long totalElements;
    private int totalPages;
    
    public Page(List<T> content, int pageNumber, int pageSize, long totalElements) {
        this.content = content;
        this.pageNumber = pageNumber;
        this.pageSize = pageSize;
        this.totalElements = totalElements;
        this.totalPages = (int) Math.ceil((double) totalElements / pageSize);
    }
    
    // Getters and utility methods...
    public boolean hasNext() { return pageNumber < totalPages - 1; }
    public boolean hasPrevious() { return pageNumber > 0; }
    public boolean isEmpty() { return content.isEmpty(); }
    public int getNumberOfElements() { return content.size(); }
}
```

### Caching Strategies
```java
// Second-level cache configuration
@Entity
@Table(name = "users")
@Cacheable
@org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
public class User {
    // Entity definition...
    
    // Cache the collection as well
    @OneToMany(mappedBy = "user")
    @org.hibernate.annotations.Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
    private List<Order> orders = new ArrayList<>();
}

// Query cache example
@Repository
public class CachedUserRepository {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    public List<User> findActiveUsers() {
        return entityManager.createQuery(
            "SELECT u FROM User u WHERE u.isActive = true",
            User.class
        )
        .setHint("org.hibernate.cacheable", true)  // Enable query cache
        .setHint("org.hibernate.cacheRegion", "activeUsersQuery")
        .getResultList();
    }
    
    // Manual cache management
    @Autowired
    private SessionFactory sessionFactory;
    
    public void evictUserCache(Long userId) {
        SessionFactory sf = entityManager.getEntityManagerFactory()
            .unwrap(SessionFactory.class);
        sf.getCache().evictEntity(User.class, userId);
    }
    
    public void evictAllUserCache() {
        SessionFactory sf = entityManager.getEntityManagerFactory()
            .unwrap(SessionFactory.class);
        sf.getCache().evictEntityData(User.class);
    }
}
```

## 🔗 Powiązane Tematy
- [[Spring Data JPA - Zaawansowane Operacje]] - Repository patterns
- [[SQL - Zaawansowane Zapytania]] - SQL fundamentals
- [[Database Migrations - Flyway/Liquibase]] - Schema versioning
- [[Spring Boot Testing]] - Testing JPA repositories

## 💡 Najlepsze Praktyki

1. **Używaj LAZY loading** jako domyślne dla relacji
2. **Unikaj N+1 problem** - używaj JOIN FETCH lub Entity Graphs  
3. **Optymalizuj queries** - używaj projection dla DTO
4. **Implementuj equals() i hashCode()** poprawnie w encjach
5. **Używaj @Transactional** na poziomie serwisu, nie repository
6. **Konfiguruj connection pooling** odpowiednio
7. **Monitor performance** z Hibernate statistics
8. **Używaj batch operations** dla bulk updates/inserts

## ⚠️ Częste Błędy

1. **Eager loading wszystkiego** - prowadzi do problemów performance
2. **Nieprawidłowe equals/hashCode** w encjach z kolekcjami
3. **Brak @Transactional** przy modify operations
4. **Zapominanie o cascade types** w relacjach
5. **Using entity jako DTO** zamiast projection

---
*Czas nauki: ~45 minut | Poziom: Zaawansowany*