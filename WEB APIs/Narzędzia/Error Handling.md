# ⚠️ Error Handling API

## 🎯 Zasady

```
✅ Używaj właściwych status codes
✅ Zwracaj szczegóły błędu
✅ Spójny format
✅ Actionable messages
✅ Error codes dla kategoryzacji
✅ Nie ujawniaj wrażliwych danych
```

## 📊 Status Codes

```
400 Bad Request - Błędne dane wejściowe
401 Unauthorized - Brak autentykacji
403 Forbidden - Brak uprawnień
404 Not Found - Zasób nie istnieje
409 Conflict - Konflikt stanu
422 Unprocessable Entity - Walidacja
429 Too Many Requests - Rate limit
500 Internal Server Error - Błąd serwera
503 Service Unavailable - Serwis niedostępny
```

## 📝 Format Błędu

### RFC 7807 (Problem Details)
```json
{
  "type": "https://api.example.com/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "The request contains invalid data",
  "instance": "/api/users",
  "errors": [
    {
      "field": "email",
      "message": "Invalid email format"
    },
    {
      "field": "age",
      "message": "Must be at least 18"
    }
  ]
}
```

### Custom Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Validation failed",
    "details": [
      {
        "field": "email",
        "message": "Invalid email format",
        "code": "INVALID_FORMAT"
      }
    ],
    "timestamp": "2024-01-15T10:00:00Z",
    "path": "/api/users"
  }
}
```

## 💻 Spring Boot Implementation

```java
// Global Exception Handler
@RestControllerAdvice
public class GlobalExceptionHandler {
    
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            ValidationException ex,
            WebRequest request) {
        
        ErrorResponse error = ErrorResponse.builder()
            .code("VALIDATION_ERROR")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .path(request.getDescription(false))
            .details(ex.getErrors())
            .build();
        
        return ResponseEntity
            .status(HttpStatus.UNPROCESSABLE_ENTITY)
            .body(error);
    }
    
    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<ErrorResponse> handleNotFound(
            ResourceNotFoundException ex) {
        
        ErrorResponse error = ErrorResponse.builder()
            .code("NOT_FOUND")
            .message(ex.getMessage())
            .timestamp(Instant.now())
            .build();
        
        return ResponseEntity
            .status(HttpStatus.NOT_FOUND)
            .body(error);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleGeneric(Exception ex) {
        // Nie ujawniaj internal details!
        ErrorResponse error = ErrorResponse.builder()
            .code("INTERNAL_ERROR")
            .message("An unexpected error occurred")
            .timestamp(Instant.now())
            .build();
        
        // Log full exception server-side
        log.error("Unexpected error", ex);
        
        return ResponseEntity
            .status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(error);
    }
}
```

## 🎯 Best Practices

```
✅ Consistent error format
✅ Include error code
✅ Human-readable messages
✅ Validation details
✅ Don't expose stack traces
✅ Don't expose internal paths
✅ Log errors server-side
✅ Correlation IDs
```

## 🔗 Powiązane Tematy

- [[HTTP Metody i Kody Statusu|📮 HTTP]]
- [[REST API - Podstawy|🔰 REST API]]
- [[Testowanie API|🧪 Testing]]
- [[web_apis_module|🌐 Web APIs]]

---

*Czas czytania: ~5 minut*

#error-handling #http-status #api-design #best-practices
