# ⚖️ REST vs SOAP vs GraphQL

## 📊 Porównanie Ogólne

| Aspekt | REST | SOAP | GraphQL |
|--------|------|------|---------|
| **Protokół** | HTTP | HTTP, SMTP, TCP | HTTP |
| **Format** | JSON, XML | XML | JSON |
| **Architektura** | Architektoniczny styl | Protokół | Query Language |
| **Kompleksowość** | Prosty | Złożony | Średni |
| **Learning Curve** | Łatwy | Trudny | Średni |
| **Wydajność** | Dobra | Wolniejszy | Bardzo dobra |
| **Caching** | Wbudowany (HTTP) | Trudny | Możliwy |
| **Wersjonowanie** | URL/Headers | Namespace | Schema evolution |
| **Popularność** | Bardzo wysoka | Legacy systems | Rosnąca |

## 🔵 REST (Representational State Transfer)

### Charakterystyka
```
• Styl architektoniczny, nie protokół
• Bazuje na HTTP
• Zasoby identyfikowane przez URI
• Stateless
• Wykorzystuje metody HTTP
```

### Przykład REST API
```http
# Pobierz użytkownika
GET /api/v1/users/123 HTTP/1.1
Host: api.example.com
Accept: application/json

Response:
{
  "id": 123,
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "posts": [
    {"id": 1, "title": "First Post"},
    {"id": 2, "title": "Second Post"}
  ]
}

# Utwórz użytkownika
POST /api/v1/users HTTP/1.1
Content-Type: application/json

{
  "name": "Anna Nowak",
  "email": "anna@example.com"
}

Response: 201 Created
{
  "id": 124,
  "name": "Anna Nowak",
  "email": "anna@example.com"
}
```

### Zalety REST
```
✅ Prostota i czytelność
✅ Wbudowane caching (HTTP)
✅ Skalowalność
✅ Niezależność od platformy
✅ Dobry tooling
✅ Świetna dokumentacja
✅ Szeroka adopcja
✅ Lightweight
```

### Wady REST
```
❌ Over-fetching (zbyt dużo danych)
❌ Under-fetching (za mało danych)
❌ Multiple endpoints (N+1 problem)
❌ Brak standardu dla real-time
❌ Wersjonowanie może być trudne
❌ Brak silnej typizacji
```

## 🟢 SOAP (Simple Object Access Protocol)

### Charakterystyka
```
• Protokół (nie styl)
• XML-based
• Silnie typowany (WSDL)
• Wbudowane bezpieczeństwo (WS-Security)
• ACID transactions (WS-AtomicTransaction)
• Enterprise-ready
```

### Przykład SOAP Request
```xml
POST /webservice HTTP/1.1
Host: api.example.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://example.com/GetUser"

<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:web="http://example.com/webservice">
    <soap:Header>
        <web:Authentication>
            <web:Username>user</web:Username>
            <web:Password>pass</web:Password>
        </web:Authentication>
    </soap:Header>
    <soap:Body>
        <web:GetUser>
            <web:UserId>123</web:UserId>
        </web:GetUser>
    </soap:Body>
</soap:Envelope>
```

### Przykład SOAP Response
```xml
<?xml version="1.0" encoding="UTF-8"?>
<soap:Envelope 
    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
    xmlns:web="http://example.com/webservice">
    <soap:Body>
        <web:GetUserResponse>
            <web:User>
                <web:Id>123</web:Id>
                <web:Name>Jan Kowalski</web:Name>
                <web:Email>jan@example.com</web:Email>
            </web:User>
        </web:GetUserResponse>
    </soap:Body>
</soap:Envelope>
```

### WSDL (Web Services Description Language)
```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions name="UserService"
    targetNamespace="http://example.com/userservice"
    xmlns="http://schemas.xmlsoap.org/wsdl/">
    
    <types>
        <schema targetNamespace="http://example.com/types">
            <complexType name="User">
                <sequence>
                    <element name="id" type="int"/>
                    <element name="name" type="string"/>
                    <element name="email" type="string"/>
                </sequence>
            </complexType>
        </schema>
    </types>
    
    <message name="GetUserRequest">
        <part name="userId" type="int"/>
    </message>
    
    <message name="GetUserResponse">
        <part name="user" type="tns:User"/>
    </message>
    
    <portType name="UserServicePortType">
        <operation name="GetUser">
            <input message="tns:GetUserRequest"/>
            <output message="tns:GetUserResponse"/>
        </operation>
    </portType>
    
    <!-- bindings, service... -->
</definitions>
```

### Zalety SOAP
```
✅ Silna typizacja (WSDL)
✅ Wbudowane bezpieczeństwo (WS-Security)
✅ ACID transactions
✅ Reliable messaging (WS-ReliableMessaging)
✅ Wsparcie dla wielu protokołów
✅ Auto-generation tools
✅ Enterprise standards
```

### Wady SOAP
```
❌ Bardzo złożony
❌ Duży overhead (XML)
❌ Wolniejszy
❌ Trudny w debugowaniu
❌ Słabe wsparcie przeglądarek
❌ Steep learning curve
❌ Overkill dla prostych API
```

## 🔴 GraphQL

### Charakterystyka
```
• Query language dla API
• Jeden endpoint
• Client określa strukturę response
• Strongly typed schema
• Real-time subscriptions
• Developed by Facebook
```

### Przykład GraphQL Schema
```graphql
type User {
  id: ID!
  name: String!
  email: String!
  posts: [Post!]!
  friends: [User!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
}

type Comment {
  id: ID!
  text: String!
  author: User!
}

type Query {
  user(id: ID!): User
  users(limit: Int): [User!]!
  post(id: ID!): Post
}

type Mutation {
  createUser(name: String!, email: String!): User!
  updateUser(id: ID!, name: String, email: String): User!
  deleteUser(id: ID!): Boolean!
}

type Subscription {
  userAdded: User!
  postUpdated(userId: ID!): Post!
}
```

### Przykład GraphQL Query
```graphql
# Query - dokładnie określamy czego potrzebujemy
query GetUserWithPosts {
  user(id: "123") {
    id
    name
    email
    posts {
      id
      title
      comments {
        id
        text
        author {
          name
        }
      }
    }
  }
}

# Response
{
  "data": {
    "user": {
      "id": "123",
      "name": "Jan Kowalski",
      "email": "jan@example.com",
      "posts": [
        {
          "id": "1",
          "title": "First Post",
          "comments": [
            {
              "id": "10",
              "text": "Great post!",
              "author": {
                "name": "Anna"
              }
            }
          ]
        }
      ]
    }
  }
}
```

### GraphQL Mutations
```graphql
# Tworzenie użytkownika
mutation CreateUser {
  createUser(name: "Anna Nowak", email: "anna@example.com") {
    id
    name
    email
  }
}

# Response
{
  "data": {
    "createUser": {
      "id": "124",
      "name": "Anna Nowak",
      "email": "anna@example.com"
    }
  }
}
```

### GraphQL Subscriptions (Real-time)
```graphql
# WebSocket connection
subscription OnUserAdded {
  userAdded {
    id
    name
    email
  }
}

# Otrzymujesz update gdy nowy user zostanie dodany
```

### Zalety GraphQL
```
✅ Brak over/under-fetching
✅ Jeden endpoint
✅ Silna typizacja
✅ Introspection (auto-documentation)
✅ Real-time (subscriptions)
✅ Efficient (tylko potrzebne dane)
✅ Versionless API
✅ Developer experience
```

### Wady GraphQL
```
❌ Complexity na backendzie
❌ Caching trudniejszy
❌ Learning curve
❌ N+1 query problem (DataLoader wymagany)
❌ Rate limiting trudniejszy
❌ Brak standardowych HTTP status codes
❌ Overkill dla prostych API
❌ File upload trudniejszy
```

## 🎯 Kiedy Używać?

### REST
```
✅ Proste CRUD operations
✅ Public API
✅ Caching jest ważny
✅ Standardowe web services
✅ Microservices
✅ Mobile apps (proste)
✅ Nie potrzebujesz real-time
```

### SOAP
```
✅ Enterprise applications
✅ Banking/Financial services
✅ Wymagane ACID transactions
✅ Strict contracts (WSDL)
✅ High security requirements
✅ Legacy system integration
✅ Multiple transport protocols
```

### GraphQL
```
✅ Frontend-driven API
✅ Complex data requirements
✅ Mobile apps (ograniczony bandwidth)
✅ Real-time features
✅ Rapid prototyping
✅ Microservices aggregation
✅ BFF (Backend for Frontend) pattern
```

## 💻 Przykłady Implementacji

### REST - Spring Boot
```java
@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(@PathVariable Long id) {
        return ResponseEntity.ok(userService.findById(id));
    }
    
    @PostMapping
    public ResponseEntity<User> createUser(@RequestBody User user) {
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(userService.create(user));
    }
}
```

### SOAP - Spring Boot
```java
@Endpoint
public class UserEndpoint {
    
    @PayloadRoot(namespace = NAMESPACE_URI, 
                localPart = "GetUserRequest")
    @ResponsePayload
    public GetUserResponse getUser(@RequestPayload GetUserRequest request) {
        GetUserResponse response = new GetUserResponse();
        response.setUser(userService.findById(request.getUserId()));
        return response;
    }
}
```

### GraphQL - Spring Boot
```java
@Controller
public class UserController {
    
    @QueryMapping
    public User user(@Argument Long id) {
        return userService.findById(id);
    }
    
    @MutationMapping
    public User createUser(@Argument String name, 
                          @Argument String email) {
        return userService.create(new User(name, email));
    }
    
    @SubscriptionMapping
    public Flux<User> userAdded() {
        return userService.getUserAddedStream();
    }
}
```

## 📈 Trendy i Adopcja

```
REST:
├── Dominujący standard (>80% API)
├── Dojrzały ekosystem
└── Nadal rośnie

SOAP:
├── Spadek popularności
├── Głównie legacy systems
└── Enterprise banking/finance

GraphQL:
├── Szybki wzrost
├── Frontend-focused companies
└── Complement do REST (nie replacement)

gRPC:
├── Microservices
├── High-performance
└── Internal APIs
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[gRPC Protocol|⚡ gRPC]]
- [[WebSockets|🔌 WebSockets]]
- [[API Gateway Pattern|🚪 API Gateway]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~15 minut*

#rest #soap #graphql #api-comparison #protocols
