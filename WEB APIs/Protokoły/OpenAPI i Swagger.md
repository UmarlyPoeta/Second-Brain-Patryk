# 📋 OpenAPI i Swagger

## 📖 Definicje

### OpenAPI Specification (OAS)
```
Standard opisu REST API w formacie JSON/YAML
- Dawniej: Swagger Specification
- Obecnie: OpenAPI 3.x (od 2017)
- Niezależny od języka
- Machine-readable
```

### Swagger
```
Zestaw narzędzi do pracy z OpenAPI:
• Swagger Editor - edytor specyfikacji
• Swagger UI - interaktywna dokumentacja
• Swagger Codegen - generowanie kodu
• SwaggerHub - hosting i współpraca
```

## 📄 Struktura OpenAPI

### Podstawowa Specyfikacja (OpenAPI 3.0)
```yaml
openapi: 3.0.3
info:
  title: User Management API
  description: API do zarządzania użytkownikami
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: http://localhost:8080/v1
    description: Development server

paths:
  /users:
    get:
      summary: Lista wszystkich użytkowników
      description: Zwraca listę użytkowników z paginacją
      operationId: getUsers
      tags:
        - Users
      parameters:
        - name: page
          in: query
          description: Numer strony
          required: false
          schema:
            type: integer
            default: 1
            minimum: 1
        - name: limit
          in: query
          description: Liczba elementów na stronę
          required: false
          schema:
            type: integer
            default: 20
            minimum: 1
            maximum: 100
      responses:
        '200':
          description: Sukces
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          description: Bad Request
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error'
        '401':
          $ref: '#/components/responses/Unauthorized'
    
    post:
      summary: Utwórz nowego użytkownika
      operationId: createUser
      tags:
        - Users
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Użytkownik utworzony
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

  /users/{userId}:
    get:
      summary: Pobierz użytkownika po ID
      operationId: getUserById
      tags:
        - Users
      parameters:
        - name: userId
          in: path
          description: ID użytkownika
          required: true
          schema:
            type: integer
            format: int64
      responses:
        '200':
          description: Sukces
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
    
    put:
      summary: Zaktualizuj użytkownika
      operationId: updateUser
      tags:
        - Users
      security:
        - bearerAuth: []
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
            format: int64
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateUserRequest'
      responses:
        '200':
          description: Użytkownik zaktualizowany
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '404':
          $ref: '#/components/responses/NotFound'
    
    delete:
      summary: Usuń użytkownika
      operationId: deleteUser
      tags:
        - Users
      security:
        - bearerAuth: []
      parameters:
        - name: userId
          in: path
          required: true
          schema:
            type: integer
      responses:
        '204':
          description: Użytkownik usunięty
        '404':
          $ref: '#/components/responses/NotFound'

components:
  schemas:
    User:
      type: object
      required:
        - id
        - name
        - email
      properties:
        id:
          type: integer
          format: int64
          example: 123
        name:
          type: string
          minLength: 2
          maxLength: 50
          example: Jan Kowalski
        email:
          type: string
          format: email
          example: jan@example.com
        createdAt:
          type: string
          format: date-time
          example: 2024-01-15T10:00:00Z
        roles:
          type: array
          items:
            type: string
            enum: [user, admin, moderator]
    
    CreateUserRequest:
      type: object
      required:
        - name
        - email
        - password
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 50
        email:
          type: string
          format: email
        password:
          type: string
          format: password
          minLength: 8
    
    UpdateUserRequest:
      type: object
      properties:
        name:
          type: string
          minLength: 2
          maxLength: 50
        email:
          type: string
          format: email
    
    Pagination:
      type: object
      properties:
        page:
          type: integer
        limit:
          type: integer
        total:
          type: integer
        totalPages:
          type: integer
    
    Error:
      type: object
      required:
        - message
      properties:
        message:
          type: string
        code:
          type: string
        details:
          type: array
          items:
            type: object
            properties:
              field:
                type: string
              message:
                type: string
  
  responses:
    Unauthorized:
      description: Unauthorized
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    BadRequest:
      description: Bad Request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    NotFound:
      description: Not Found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key

tags:
  - name: Users
    description: Operacje na użytkownikach
  - name: Posts
    description: Operacje na postach
```

## 🛠️ Implementacja w Spring Boot

### Springdoc OpenAPI (Zalecane)

**Dodaj dependency:**
```xml
<dependency>
    <groupId>org.springdoc</groupId>
    <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
    <version>2.2.0</version>
</dependency>
```

**Konfiguracja:**
```java
@Configuration
public class OpenAPIConfig {
    
    @Bean
    public OpenAPI customOpenAPI() {
        return new OpenAPI()
            .info(new Info()
                .title("User Management API")
                .version("1.0.0")
                .description("API do zarządzania użytkownikami")
                .contact(new Contact()
                    .name("API Support")
                    .email("support@example.com"))
                .license(new License()
                    .name("MIT")
                    .url("https://opensource.org/licenses/MIT")))
            .addServersItem(new Server()
                .url("http://localhost:8080")
                .description("Development server"))
            .components(new Components()
                .addSecuritySchemes("bearerAuth",
                    new SecurityScheme()
                        .type(SecurityScheme.Type.HTTP)
                        .scheme("bearer")
                        .bearerFormat("JWT")));
    }
}
```

**Controller z adnotacjami:**
```java
@RestController
@RequestMapping("/api/users")
@Tag(name = "Users", description = "Operacje na użytkownikach")
public class UserController {
    
    @Operation(
        summary = "Pobierz wszystkich użytkowników",
        description = "Zwraca listę wszystkich użytkowników z paginacją"
    )
    @ApiResponses(value = {
        @ApiResponse(
            responseCode = "200",
            description = "Sukces",
            content = @Content(
                mediaType = "application/json",
                schema = @Schema(implementation = UserListResponse.class)
            )
        ),
        @ApiResponse(
            responseCode = "400",
            description = "Bad Request",
            content = @Content(schema = @Schema(implementation = ErrorResponse.class))
        )
    })
    @GetMapping
    public ResponseEntity<UserListResponse> getUsers(
        @Parameter(description = "Numer strony", example = "1")
        @RequestParam(defaultValue = "1") int page,
        
        @Parameter(description = "Liczba elementów", example = "20")
        @RequestParam(defaultValue = "20") int limit
    ) {
        return ResponseEntity.ok(userService.findAll(page, limit));
    }
    
    @Operation(summary = "Utwórz użytkownika")
    @SecurityRequirement(name = "bearerAuth")
    @PostMapping
    public ResponseEntity<User> createUser(
        @io.swagger.v3.oas.annotations.parameters.RequestBody(
            description = "Dane nowego użytkownika",
            required = true,
            content = @Content(
                schema = @Schema(implementation = CreateUserRequest.class)
            )
        )
        @RequestBody @Valid CreateUserRequest request
    ) {
        return ResponseEntity
            .status(HttpStatus.CREATED)
            .body(userService.create(request));
    }
    
    @Operation(summary = "Pobierz użytkownika po ID")
    @GetMapping("/{id}")
    public ResponseEntity<User> getUser(
        @Parameter(description = "ID użytkownika", required = true)
        @PathVariable Long id
    ) {
        return ResponseEntity.ok(userService.findById(id));
    }
}
```

**Model z dokumentacją:**
```java
@Schema(description = "Model użytkownika")
public class User {
    
    @Schema(description = "Unikalny identyfikator", example = "123")
    private Long id;
    
    @Schema(
        description = "Imię i nazwisko użytkownika",
        example = "Jan Kowalski",
        minLength = 2,
        maxLength = 50
    )
    private String name;
    
    @Schema(
        description = "Email użytkownika",
        example = "jan@example.com",
        format = "email"
    )
    private String email;
    
    @Schema(description = "Data utworzenia", example = "2024-01-15T10:00:00Z")
    private LocalDateTime createdAt;
    
    @Schema(description = "Role użytkownika", example = "[\"user\", \"admin\"]")
    private List<String> roles;
    
    // getters/setters
}
```

**application.properties:**
```properties
# Swagger UI path
springdoc.swagger-ui.path=/swagger-ui.html

# OpenAPI JSON path
springdoc.api-docs.path=/api-docs

# Sortowanie
springdoc.swagger-ui.operationsSorter=method

# Grupowanie
springdoc.group-configs[0].group=public
springdoc.group-configs[0].paths-to-match=/api/public/**

springdoc.group-configs[1].group=admin
springdoc.group-configs[1].paths-to-match=/api/admin/**
```

## 🌐 Dostęp do Dokumentacji

```
Swagger UI:
http://localhost:8080/swagger-ui.html

OpenAPI JSON:
http://localhost:8080/api-docs

OpenAPI YAML:
http://localhost:8080/api-docs.yaml
```

## 🎨 Swagger UI Features

```
• Interactive API testing
• Try it out - wykonywanie requestów
• Authentication support
• Schema visualization
• Example values
• Download specification
• Multiple servers
• Deep linking
```

## 🔧 Zaawansowane Funkcje

### Przykłady (Examples)
```java
@Schema(
    description = "User model",
    example = """
        {
            "id": 123,
            "name": "Jan Kowalski",
            "email": "jan@example.com",
            "roles": ["user", "admin"]
        }
        """
)
public class User {
    // ...
}
```

### Polymorphism (OneOf/AnyOf)
```yaml
components:
  schemas:
    Pet:
      oneOf:
        - $ref: '#/components/schemas/Cat'
        - $ref: '#/components/schemas/Dog'
      discriminator:
        propertyName: petType
    
    Cat:
      type: object
      properties:
        petType:
          type: string
        meowVolume:
          type: integer
    
    Dog:
      type: object
      properties:
        petType:
          type: string
        barkVolume:
          type: integer
```

### Callbacks (Webhooks)
```yaml
paths:
  /subscribe:
    post:
      requestBody:
        content:
          application/json:
            schema:
              properties:
                callbackUrl:
                  type: string
      callbacks:
        onEvent:
          '{$request.body#/callbackUrl}':
            post:
              requestBody:
                content:
                  application/json:
                    schema:
                      type: object
                      properties:
                        event:
                          type: string
              responses:
                '200':
                  description: OK
```

## 📚 Best Practices

### Dokumentacja
```
✅ Zawsze dodawaj descriptions
✅ Używaj examples dla każdego schema
✅ Dokumentuj wszystkie response codes
✅ Opisuj parametry i ich walidacje
✅ Grupuj endpointy tagami
✅ Wersjonuj API w URL
✅ Dodaj contact i license info
```

### Security
```
✅ Definiuj security schemes
✅ Używaj @SecurityRequirement dla chronionych endpointów
✅ Dokumentuj wymagane uprawnienia
✅ Nie ujawniaj wrażliwych danych w examples
```

### Maintenance
```
✅ Generuj spec automatycznie (springdoc)
✅ Testuj spec (Swagger Validator)
✅ Wersjonuj spec w Git
✅ CI/CD dla dokumentacji
✅ Synchronizuj z kodem
```

## 🔄 Code Generation

### Generowanie Klienta
```bash
# Instalacja OpenAPI Generator
npm install @openapitools/openapi-generator-cli -g

# Generowanie klienta TypeScript
openapi-generator-cli generate \
  -i openapi.yaml \
  -g typescript-axios \
  -o ./generated-client

# Generowanie klienta Java
openapi-generator-cli generate \
  -i openapi.yaml \
  -g java \
  -o ./generated-client \
  --library resttemplate
```

### Użycie Wygenerowanego Klienta
```typescript
// TypeScript
import { UsersApi, Configuration } from './generated-client';

const config = new Configuration({
  basePath: 'https://api.example.com/v1',
  accessToken: 'your-token'
});

const api = new UsersApi(config);

// Użycie
const users = await api.getUsers(1, 20);
const user = await api.createUser({
  name: 'Jan Kowalski',
  email: 'jan@example.com'
});
```

## 🎯 Narzędzia

```
Edytory:
• Swagger Editor - https://editor.swagger.io
• VS Code - OpenAPI extension
• IntelliJ IDEA - OpenAPI plugin

Validators:
• Swagger Validator
• Spectral (linting)

Hosting:
• SwaggerHub
• Stoplight
• ReadMe.io

Testing:
• Postman (import OpenAPI)
• Insomnia
• Dredd (contract testing)
```

## 🔗 Powiązane Tematy

- [[REST API - Podstawy|🔰 REST API]]
- [[Dokumentacja API|📚 Dokumentacja]]
- [[Testowanie API|🧪 Testowanie]]
- [[Spring Boot Web|🌐 Spring Boot Web]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~12 minut*

#openapi #swagger #api-documentation #specification
