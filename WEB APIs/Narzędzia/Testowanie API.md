# 🧪 Testowanie API

## 🛠️ Narzędzia do Testowania

### Postman
```
Najpopularniejsze narzędzie do testowania API

Funkcje:
✅ GUI dla tworzenia requestów
✅ Collections (grupy requestów)
✅ Environment variables
✅ Pre-request scripts
✅ Tests (assertions)
✅ Mock servers
✅ Dokumentacja automatyczna
✅ Team collaboration
```

**Przykład Testu w Postman:**
```javascript
// Tests tab
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has user object", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('user');
});

pm.test("User email is valid", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.user.email).to.match(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
});

// Zapisz token do environment
pm.environment.set("auth_token", pm.response.json().token);
```

**Pre-request Script:**
```javascript
// Automatyczne dodanie timestamp
pm.environment.set("timestamp", new Date().toISOString());

// Generowanie signature
const token = pm.environment.get("api_key");
const timestamp = pm.environment.get("timestamp");
const signature = CryptoJS.HmacSHA256(timestamp, token).toString();
pm.environment.set("signature", signature);
```

### curl
```bash
# Podstawowy GET
curl https://api.example.com/users

# Z headerami
curl -H "Authorization: Bearer token123" \
     -H "Content-Type: application/json" \
     https://api.example.com/users

# POST z danymi
curl -X POST https://api.example.com/users \
     -H "Content-Type: application/json" \
     -d '{"name":"Jan","email":"jan@example.com"}'

# Zapisanie response do pliku
curl https://api.example.com/users -o users.json

# Wyświetlenie headerów
curl -i https://api.example.com/users

# Verbose (debug)
curl -v https://api.example.com/users

# Follow redirects
curl -L https://api.example.com/users

# Timeout
curl --max-time 10 https://api.example.com/users

# Upload pliku
curl -F "file=@photo.jpg" https://api.example.com/upload
```

### HTTPie
```bash
# Prostszy syntax niż curl
http GET https://api.example.com/users

# POST z JSON (automatycznie)
http POST https://api.example.com/users name=Jan email=jan@example.com

# Headers
http GET https://api.example.com/users Authorization:"Bearer token123"

# Download pliku
http --download https://api.example.com/file.pdf

# Forms
http --form POST https://api.example.com/upload file@photo.jpg
```

### Insomnia
```
Alternatywa dla Postman

Zalety:
✅ Czysty interface
✅ GraphQL support
✅ gRPC support
✅ Environment variables
✅ Code generation
```

## 🧪 Typy Testów API

### 1. Unit Tests

**JUnit 5 + MockMvc (Spring Boot):**
```java
@WebMvcTest(UserController.class)
class UserControllerTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @MockBean
    private UserService userService;
    
    @Test
    void shouldReturnUser() throws Exception {
        User user = new User(1L, "Jan", "jan@example.com");
        when(userService.findById(1L)).thenReturn(user);
        
        mockMvc.perform(get("/api/users/1"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.id").value(1))
            .andExpect(jsonPath("$.name").value("Jan"))
            .andExpect(jsonPath("$.email").value("jan@example.com"));
    }
    
    @Test
    void shouldCreateUser() throws Exception {
        CreateUserRequest request = new CreateUserRequest("Anna", "anna@example.com");
        User created = new User(2L, "Anna", "anna@example.com");
        
        when(userService.create(any())).thenReturn(created);
        
        mockMvc.perform(post("/api/users")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"name\":\"Anna\",\"email\":\"anna@example.com\"}"))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").value(2))
            .andExpect(jsonPath("$.name").value("Anna"));
    }
    
    @Test
    void shouldReturn404WhenUserNotFound() throws Exception {
        when(userService.findById(999L))
            .thenThrow(new UserNotFoundException());
        
        mockMvc.perform(get("/api/users/999"))
            .andExpect(status().isNotFound());
    }
}
```

### 2. Integration Tests

**Spring Boot:**
```java
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class UserApiIntegrationTest {
    
    @Autowired
    private TestRestTemplate restTemplate;
    
    @Autowired
    private UserRepository userRepository;
    
    @BeforeEach
    void setUp() {
        userRepository.deleteAll();
    }
    
    @Test
    void shouldCreateAndRetrieveUser() {
        // Create
        CreateUserRequest request = new CreateUserRequest("Jan", "jan@example.com");
        ResponseEntity<User> createResponse = restTemplate.postForEntity(
            "/api/users", 
            request, 
            User.class
        );
        
        assertThat(createResponse.getStatusCode()).isEqualTo(HttpStatus.CREATED);
        User created = createResponse.getBody();
        assertThat(created.getId()).isNotNull();
        
        // Retrieve
        ResponseEntity<User> getResponse = restTemplate.getForEntity(
            "/api/users/" + created.getId(), 
            User.class
        );
        
        assertThat(getResponse.getStatusCode()).isEqualTo(HttpStatus.OK);
        assertThat(getResponse.getBody().getName()).isEqualTo("Jan");
    }
    
    @Test
    void shouldReturnPaginatedUsers() {
        // Utwórz 25 użytkowników
        for (int i = 0; i < 25; i++) {
            userRepository.save(new User("User" + i, "user" + i + "@example.com"));
        }
        
        // Test pagination
        ResponseEntity<PagedResponse> response = restTemplate.getForEntity(
            "/api/users?page=1&limit=10", 
            PagedResponse.class
        );
        
        assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
        PagedResponse page = response.getBody();
        assertThat(page.getData()).hasSize(10);
        assertThat(page.getTotal()).isEqualTo(25);
    }
}
```

### 3. Contract Tests

**Pact (Consumer-Driven Contracts):**
```java
// Consumer side
@ExtendWith(PactConsumerTestExt.class)
@PactTestFor(providerName = "UserService")
public class UserServiceContractTest {
    
    @Pact(consumer = "FrontendApp")
    public RequestResponsePact getUserPact(PactDslWithProvider builder) {
        return builder
            .given("user 1 exists")
            .uponReceiving("a request for user 1")
            .path("/api/users/1")
            .method("GET")
            .willRespondWith()
            .status(200)
            .body(new PactDslJsonBody()
                .integerType("id", 1)
                .stringType("name", "Jan")
                .stringType("email", "jan@example.com"))
            .toPact();
    }
    
    @Test
    @PactTestFor(pactMethod = "getUserPact")
    void testGetUser(MockServer mockServer) {
        RestTemplate restTemplate = new RestTemplate();
        User user = restTemplate.getForObject(
            mockServer.getUrl() + "/api/users/1", 
            User.class
        );
        
        assertThat(user.getId()).isEqualTo(1);
        assertThat(user.getName()).isEqualTo("Jan");
    }
}
```

### 4. Load Tests

**JMeter:**
```xml
<!-- HTTP Request -->
<HTTPSamplerProxy>
  <stringProp name="HTTPSampler.domain">api.example.com</stringProp>
  <stringProp name="HTTPSampler.path">/api/users</stringProp>
  <stringProp name="HTTPSampler.method">GET</stringProp>
  <elementProp name="HTTPsampler.Arguments">
    <collectionProp name="Arguments.arguments"/>
  </elementProp>
</HTTPSamplerProxy>

<!-- Thread Group -->
<ThreadGroup>
  <intProp name="ThreadGroup.num_threads">100</intProp>
  <intProp name="ThreadGroup.ramp_time">10</intProp>
  <longProp name="ThreadGroup.duration">300</longProp>
</ThreadGroup>
```

**Gatling (Scala):**
```scala
class UserApiLoadTest extends Simulation {
  
  val httpProtocol = http
    .baseUrl("https://api.example.com")
    .acceptHeader("application/json")
  
  val scn = scenario("Load Test")
    .exec(http("Get Users")
      .get("/api/users")
      .check(status.is(200)))
    .pause(1)
    .exec(http("Create User")
      .post("/api/users")
      .body(StringBody("""{"name":"Test","email":"test@example.com"}"""))
      .check(status.is(201)))
  
  setUp(
    scn.inject(
      rampUsers(1000) during (60 seconds)
    )
  ).protocols(httpProtocol)
}
```

**k6 (JavaScript):**
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100, // 100 virtual users
  duration: '5m',
};

export default function() {
  // GET request
  let res = http.get('https://api.example.com/users');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  });
  
  // POST request
  let payload = JSON.stringify({
    name: 'Test User',
    email: 'test@example.com',
  });
  
  let params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  res = http.post('https://api.example.com/users', payload, params);
  check(res, {
    'created successfully': (r) => r.status === 201,
  });
  
  sleep(1);
}
```

## 📊 Assertions i Walidacja

### REST Assured (Java)
```java
@Test
void shouldReturnUserList() {
    given()
        .header("Authorization", "Bearer " + token)
        .param("page", 1)
        .param("limit", 10)
    .when()
        .get("/api/users")
    .then()
        .statusCode(200)
        .contentType(ContentType.JSON)
        .body("data", hasSize(10))
        .body("data[0].id", notNullValue())
        .body("data[0].email", matchesRegex("^[\\w-\\.]+@([\\w-]+\\.)+[\\w-]{2,4}$"))
        .body("pagination.page", equalTo(1))
        .body("pagination.total", greaterThan(0))
        .time(lessThan(2000L)); // Response time < 2s
}

@Test
void shouldValidateJsonSchema() {
    given()
        .get("/api/users/1")
    .then()
        .assertThat()
        .body(matchesJsonSchemaInClasspath("user-schema.json"));
}
```

### Jest (JavaScript/Node.js)
```javascript
describe('User API', () => {
  test('should return user list', async () => {
    const response = await axios.get('http://api.example.com/users');
    
    expect(response.status).toBe(200);
    expect(response.data).toHaveProperty('data');
    expect(Array.isArray(response.data.data)).toBe(true);
    expect(response.data.data.length).toBeGreaterThan(0);
    
    const user = response.data.data[0];
    expect(user).toHaveProperty('id');
    expect(user).toHaveProperty('name');
    expect(user).toHaveProperty('email');
    expect(user.email).toMatch(/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/);
  });
  
  test('should create user', async () => {
    const newUser = {
      name: 'Test User',
      email: 'test@example.com'
    };
    
    const response = await axios.post('http://api.example.com/users', newUser);
    
    expect(response.status).toBe(201);
    expect(response.data.id).toBeDefined();
    expect(response.data.name).toBe(newUser.name);
  });
});
```

## 🎯 Best Practices

```
✅ Test happy path i edge cases
✅ Test wszystkie status codes
✅ Weryfikuj response schema
✅ Test authentication/authorization
✅ Test rate limiting
✅ Test timeout handling
✅ Test error responses
✅ Używaj test data builders
✅ Cleanup po testach
✅ CI/CD integration
✅ Performance benchmarks
✅ Security testing (OWASP)
```

## 🔗 Powiązane Tematy

- [[HTTP Metody i Kody Statusu|📮 HTTP Metody]]
- [[Error Handling API|⚠️ Error Handling]]
- [[API Security Best Practices|🔒 Security]]
- [[Dokumentacja API|📚 Dokumentacja]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~12 minut*

#testing #api-testing #postman #unit-tests #integration-tests
