# 📑 Pagination i Filtering API

## 🎯 Po co Pagination?

```
✅ Mniejsze response size
✅ Szybsze response time
✅ Mniejsze obciążenie bazy
✅ Lepsza UX (progressive loading)
```

## 📊 Strategie Paginacji

### 1. Offset-based (Page Number)

```http
GET /api/users?page=1&limit=20
GET /api/users?offset=0&limit=20
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

**Spring Boot:**
```java
@GetMapping("/users")
public ResponseEntity<PagedResponse<User>> getUsers(
        @RequestParam(defaultValue = "1") int page,
        @RequestParam(defaultValue = "20") int limit) {
    
    Pageable pageable = PageRequest.of(page - 1, limit);
    Page<User> usersPage = userRepository.findAll(pageable);
    
    PagedResponse<User> response = PagedResponse.builder()
        .data(usersPage.getContent())
        .page(page)
        .limit(limit)
        .total(usersPage.getTotalElements())
        .totalPages(usersPage.getTotalPages())
        .build();
    
    return ResponseEntity.ok(response);
}
```

**Wady:**
```
❌ Problemy z duplikatami gdy dane się zmieniają
❌ Nieefektywne dla dużych offsetów (OFFSET 10000)
```

### 2. Cursor-based (Keyset)

```http
GET /api/users?cursor=abc123&limit=20
```

**Response:**
```json
{
  "data": [...],
  "pagination": {
    "nextCursor": "xyz789",
    "hasMore": true
  }
}
```

**Implementation:**
```java
@GetMapping("/users")
public ResponseEntity<CursorResponse<User>> getUsers(
        @RequestParam(required = false) String cursor,
        @RequestParam(defaultValue = "20") int limit) {
    
    Long lastId = cursor != null ? 
        Long.parseLong(decodeCursor(cursor)) : 0L;
    
    List<User> users = userRepository
        .findByIdGreaterThanOrderById(lastId, limit + 1);
    
    boolean hasMore = users.size() > limit;
    if (hasMore) {
        users = users.subList(0, limit);
    }
    
    String nextCursor = hasMore ? 
        encodeCursor(users.get(users.size() - 1).getId()) : null;
    
    return ResponseEntity.ok(
        new CursorResponse<>(users, nextCursor, hasMore)
    );
}

private String encodeCursor(Long id) {
    return Base64.getEncoder().encodeToString(id.toString().getBytes());
}

private String decodeCursor(String cursor) {
    return new String(Base64.getDecoder().decode(cursor));
}
```

**Zalety:**
```
✅ Consistent results
✅ Wydajne dla dużych zbiorów
✅ Brak skip problems
```

## 🔍 Filtering

### Query Parameters
```http
GET /api/users?status=active&role=admin&age_min=18&age_max=65
```

**Spring Boot:**
```java
@GetMapping("/users")
public List<User> getUsers(
        @RequestParam(required = false) String status,
        @RequestParam(required = false) String role,
        @RequestParam(required = false) Integer ageMin,
        @RequestParam(required = false) Integer ageMax) {
    
    return userService.findByFilters(status, role, ageMin, ageMax);
}

// Service z Specification
public List<User> findByFilters(String status, String role, 
                                Integer ageMin, Integer ageMax) {
    
    Specification<User> spec = Specification.where(null);
    
    if (status != null) {
        spec = spec.and((root, query, cb) -> 
            cb.equal(root.get("status"), status));
    }
    
    if (role != null) {
        spec = spec.and((root, query, cb) -> 
            cb.equal(root.get("role"), role));
    }
    
    if (ageMin != null) {
        spec = spec.and((root, query, cb) -> 
            cb.greaterThanOrEqualTo(root.get("age"), ageMin));
    }
    
    if (ageMax != null) {
        spec = spec.and((root, query, cb) -> 
            cb.lessThanOrEqualTo(root.get("age"), ageMax));
    }
    
    return userRepository.findAll(spec);
}
```

## 📈 Sorting

```http
GET /api/users?sort=name,asc&sort=age,desc
GET /api/users?orderBy=name&order=asc
```

**Spring Boot:**
```java
@GetMapping("/users")
public List<User> getUsers(
        @RequestParam(defaultValue = "id") String sortBy,
        @RequestParam(defaultValue = "asc") String sortOrder) {
    
    Sort sort = Sort.by(
        sortOrder.equals("desc") ? 
            Sort.Direction.DESC : Sort.Direction.ASC,
        sortBy
    );
    
    return userRepository.findAll(sort);
}

// Multiple sort fields
@GetMapping("/users")
public List<User> getUsers(@RequestParam String[] sort) {
    List<Sort.Order> orders = Arrays.stream(sort)
        .map(s -> {
            String[] parts = s.split(",");
            return parts[1].equals("desc") ?
                Sort.Order.desc(parts[0]) :
                Sort.Order.asc(parts[0]);
        })
        .collect(Collectors.toList());
    
    return userRepository.findAll(Sort.by(orders));
}
```

## 🔍 Search

```http
GET /api/users?q=john&fields=name,email
```

**Implementation:**
```java
@GetMapping("/users/search")
public List<User> search(
        @RequestParam String q,
        @RequestParam(defaultValue = "name,email") String fields) {
    
    List<String> searchFields = Arrays.asList(fields.split(","));
    
    return userRepository.search(q, searchFields);
}

// Repository
public interface UserRepository extends JpaRepository<User, Long> {
    
    @Query("SELECT u FROM User u WHERE " +
           "LOWER(u.name) LIKE LOWER(CONCAT('%', :query, '%')) OR " +
           "LOWER(u.email) LIKE LOWER(CONCAT('%', :query, '%'))")
    List<User> search(@Param("query") String query, 
                     @Param("fields") List<String> fields);
}
```

## 🎯 Best Practices

```
✅ Default pagination (max 100 items)
✅ Include total count
✅ Cursor-based dla real-time feeds
✅ Offset-based dla user navigation
✅ Allow field selection (?fields=id,name)
✅ Validate sort fields (whitelist)
✅ Cache filtered results
✅ Index database columns used in filters
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[HTTP Metody i Kody Statusu|📮 HTTP]]
- [[Caching w API|💾 Caching]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~7 minut*

#pagination #filtering #sorting #api-design #performance
