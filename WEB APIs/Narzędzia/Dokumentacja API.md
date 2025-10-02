# 📚 Dokumentacja API

## 🎯 Dlaczego Dokumentacja?

```
✅ Developer experience
✅ Szybsza integracja
✅ Mniej supportu
✅ Adopt API przez więcej devs
✅ Self-service
✅ Consistency
```

## 📝 Co Dokumentować?

### 1. Overview
```
• Cel API
• Use cases
• Authentication
• Base URL
• Rate limits
• Versioning policy
```

### 2. Endpoints
```
• HTTP method
• Path
• Parameters (query, path, body)
• Headers
• Response format
• Status codes
• Error responses
• Examples
```

### 3. Models/Schemas
```
• Data types
• Required fields
• Validations
• Enums
• Relationships
• Examples
```

## 🛠️ Narzędzia

### OpenAPI/Swagger
```yaml
openapi: 3.0.3
info:
  title: User API
  description: |
    Complete API for user management.
    
    ## Authentication
    Use Bearer token in Authorization header.
    
    ## Rate Limiting
    - Free tier: 100 req/hour
    - Premium: 10,000 req/hour
  version: 1.0.0

paths:
  /users:
    get:
      summary: List users
      description: |
        Returns paginated list of users.
        Supports filtering and sorting.
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
          example: 1
      responses:
        '200':
          description: Success
          content:
            application/json:
              example:
                data: [...]
                pagination: {...}
```

### Postman Collections
```
• Auto-generate from OpenAPI
• Executable examples
• Environment variables
• Tests included
```

### README Driven Development
```markdown
# User API

## Quick Start

```bash
# Get all users
curl https://api.example.com/users

# Create user
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Jan","email":"jan@example.com"}'
```

## Authentication
...
```
```

## ✍️ Best Practices

```
✅ Examples dla każdego endpointu
✅ Real examples (nie "string" lub "123")
✅ Error examples
✅ Code samples w różnych językach
✅ Interactive playground (try it out)
✅ Changelog
✅ Migration guides
✅ FAQ
✅ Status page (uptime)
✅ Wersjonowanie dokumentacji
```

## 🔗 Powiązane Tematy

- [[OpenAPI i Swagger|📋 OpenAPI]]
- [[REST API - Podstawy|🔰 REST API]]
- [[Wersjonowanie API|🔢 Wersjonowanie]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~5 minut*

#documentation #api-docs #openapi #developer-experience
