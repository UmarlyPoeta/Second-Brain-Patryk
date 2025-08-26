# 🔐 Spring Security - Zaawansowane Techniki

## 📋 Wprowadzenie do Zaawansowanego Bezpieczeństwa

Po opanowaniu podstaw Spring Security, kluczowe staje się zrozumienie zaawansowanych mechanizmów bezpieczeństwa, które są niezbędne w nowoczesnych aplikacjach enterprise. Zaawansowane techniki obejmują integrację z zewnętrznymi providerami tożsamości, implementację protokołów federacyjnych, oraz dostosowywanie mechanizmów bezpieczeństwa do specyficznych wymagań biznesowych.

## 🌐 OAuth 2.0 i OpenID Connect

### Teoria OAuth 2.0

OAuth 2.0 to standard autoryzacji, który umożliwia aplikacjom uzyskiwanie ograniczonego dostępu do zasobów użytkowników bez udostępniania haseł. Protocol ten rozwiązuje problem "password anti-pattern" w aplikacjach trzecich.

**Kluczowe Role w OAuth 2.0:**

**Resource Owner (Właściciel Zasobu)**
- Zazwyczaj końcowy użytkownik
- Ma możliwość udzielenia dostępu do swoich chronionych zasobów
- Może cofnąć uprawnienia w dowolnym momencie

**Client (Klient)**
- Aplikacja żądająca dostępu do chronionych zasobów
- Może być publiczny (aplikacje mobilne, SPA) lub poufny (aplikacje serwerowe)
- Musi być zarejestrowany u Authorization Server

**Authorization Server (Serwer Autoryzacji)**
- Wydaje tokeny dostępu po pomyślnej autentykacji właściciela zasobu
- Zarządza uprawnieniami i zakresami dostępu (scopes)
- Może być zewnętrznym dostawcą (Google, Facebook) lub wewnętrznym systemem

**Resource Server (Serwer Zasobów)**
- Przechowuje chronione zasoby
- Akceptuje i odpowiada na żądania chronionych zasobów przy użyciu tokenów dostępu
- Może być tą samą aplikacją co Authorization Server

### Authorization Code Flow

**Teoria przepływu:**
Authorization Code Flow to najczęściej używany i najbezpieczniejszy flow w OAuth 2.0 dla aplikacji webowych. Wykorzystuje dwuetapowy proces wymiany - najpierw kod autoryzacyjny, potem token dostępu.

**Fazy przepływu:**
1. **Redirect do Authorization Server:** Użytkownik jest przekierowywany do strony logowania providera
2. **Uwierzytelnienie użytkownika:** Użytkownik loguje się i wyraża zgodę na uprawnienia
3. **Authorization Code:** Provider przekierowuje z powrotem z kodem autoryzacyjnym
4. **Token Exchange:** Aplikacja wymienia kod na token dostępu (backend-to-backend)
5. **Dostęp do zasobów:** Aplikacja używa tokenu do dostępu do chronionych zasobów

**Zalety:**
- Wysoki poziom bezpieczeństwa - token nie przechodzi przez frontend
- Możliwość odświeżania tokenów (refresh tokens)
- Wsparcie dla różnych typów klientów

### OpenID Connect (OIDC)

**Teoria:** OpenID Connect to warstwa tożsamości zbudowana na OAuth 2.0, która dodaje funkcjonalność autentykacji do autoryzacji OAuth. Umożliwia klientom weryfikację tożsamości użytkownika końcowego.

**ID Token:**
- JWT zawierający informacje o uwierzytelnionym użytkowniku
- Podpisany przez Identity Provider
- Zawiera claims takie jak `sub` (subject), `email`, `name`

**UserInfo Endpoint:**
- Standardowy endpoint dostarczający dodatkowe informacje o użytkowniku
- Chroniony tokenem dostępu
- Możliwość requestowania różnych zakresów informacji (profile, email, address)

## 🏢 LDAP Integration

### Lightweight Directory Access Protocol

**Teoria:** LDAP to protokół dostępu do usług katalogowych, powszechnie używany w środowiskach korporacyjnych do zarządzania tożsamościami. Active Directory to najpopularniejsza implementacja LDAP w środowiskach Windows.

**Struktura Katalogowa:**
LDAP organizuje dane w hierarchicznej strukturze drzewiastej:
- **Distinguished Name (DN):** Unikalny identyfikator wpisu w drzewie
- **Organizational Unit (OU):** Jednostka organizacyjna grupująca obiekty
- **Common Name (CN):** Nazwa obiektu (użytkownik, grupa)

**Operacje LDAP:**
- **Bind:** Uwierzytelnienie w katalogu
- **Search:** Wyszukiwanie obiektów na podstawie filtrów
- **Add/Delete/Modify:** Operacje modyfikacji katalogu

### LDAP Authentication Strategies

**Bind Authentication:**
- Użytkownik jest uwierzytelniany poprzez bind operation na serwerze LDAP
- Sprawdza czy podane credentials są poprawne
- Nie wymaga przechowywania haseł w aplikacji

**Password Comparison:**
- Pobiera hash hasła z LDAP i porównuje z podanym
- Wymaga specjalnych uprawnień do odczytu haseł
- Mniej bezpieczne niż bind authentication

### Group-Based Authorization

**Teoria grup LDAP:**
LDAP umożliwia organizowanie użytkowników w grupy, które mogą być mapowane na role aplikacji:
- **Static Groups:** Użytkownicy jawnie przypisani do grup
- **Dynamic Groups:** Członkostwo określane przez filtry LDAP
- **Nested Groups:** Grupy mogące zawierać inne grupy

## 🔧 Custom Authentication Providers

### Authentication Provider Interface

**Teoria:** Authentication Provider to komponent odpowiedzialny za weryfikację credentials i tworzenie objektu Authentication. Spring Security pozwala na implementację własnych providerów dla niestandardowych mechanizmów uwierzytelniania.

**Lifecycle Authentication:**
1. **Authentication Request:** Tworzenie obiektu Authentication z credentials
2. **Provider Selection:** AuthenticationManager wybiera odpowiedniego providera
3. **Authentication Process:** Provider weryfikuje credentials
4. **Authentication Result:** Zwracany jest Authentication object z authorities

### Implementacja Custom Provider

**Scenariusze użycia:**
- Integracja z legacy systemami autentykacji
- Dwuetapowa weryfikacja (2FA)
- Autentykacja oparta na certyfikatach
- Custom business logic w procesie uwierzytelniania

**Komponenty wymagane:**
- **Authentication Object:** Reprezentuje żądanie uwierzytelnienia
- **Authentication Provider:** Logika weryfikacji
- **UserDetailsService:** Ładowanie szczegółów użytkownika
- **PasswordEncoder:** Kodowanie i weryfikacja haseł

## 🛡️ Advanced Authorization

### Attribute-Based Access Control (ABAC)

**Teoria:** ABAC to model autoryzacji, który podejmuje decyzje na podstawie atrybutów podmiotów (subjects), zasobów (resources), operacji (actions) i środowiska (environment).

**Komponenty ABAC:**
- **Policy Administration Point (PAP):** Zarządzanie politykami
- **Policy Decision Point (PDP):** Ewaluacja żądań dostępu
- **Policy Enforcement Point (PEP):** Egzekwowanie decyzji
- **Policy Information Point (PIP):** Dostarczanie atrybutów

**Zalety względem RBAC:**
- Większa granularność kontroli dostępu
- Możliwość uwzględnienia kontekstu (czas, lokalizacja)
- Dynamiczne podejmowanie decyzji
- Lepsze wsparcie dla compliance

### Expression-Based Access Control

**Spring Expression Language (SpEL):**
Spring Security wykorzystuje SpEL do definiowania skomplikowanych reguł autoryzacji:
- Dostęp do informacji o użytkowniku: `authentication.name`
- Porównania: `hasRole('ADMIN') or #username == authentication.name`
- Metody custom: `@securityService.canAccess(#resourceId)`

### Method Security z SpEL

**Pre/Post Processing:**
- **@PreAuthorize:** Sprawdzenie przed wykonaniem metody
- **@PostAuthorize:** Sprawdzenie po wykonaniu (dostęp do return value)
- **@PreFilter:** Filtrowanie parametrów wejściowych
- **@PostFilter:** Filtrowanie rezultatów

## 🔐 JWT i Stateless Security

### JSON Web Token Deep Dive

**Struktura JWT:**
JWT składa się z trzech części oddzielonych kropkami:

**Header (Nagłówek):**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload (Ładunek):**
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "exp": 1516242622
}
```

**Signature (Podpis):**
```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  secret)
```

### JWT Claims

**Standard Claims (RFC 7519):**
- **iss (issuer):** Wystawca tokenu
- **sub (subject):** Podmiot tokenu (zazwyczaj user ID)
- **aud (audience):** Odbiorca tokenu
- **exp (expiration time):** Czas wygaśnięcia
- **nbf (not before):** Token ważny nie wcześniej niż
- **iat (issued at):** Czas wystawienia
- **jti (JWT ID):** Unikalny identyfikator tokenu

**Custom Claims:**
Możliwość dodawania własnych claims z informacjami specyficznymi dla aplikacji:
- Role i uprawnienia użytkownika
- Informacje o sesji
- Metadane biznesowe

### Token Refresh Strategy

**Refresh Token Pattern:**
- **Access Token:** Krótki czas życia (15-30 minut)
- **Refresh Token:** Długi czas życia (dni/tygodnie)
- **Automatyczne odnawianie:** Gdy access token wygasa

**Zalety:**
- Ogranicza okno ryzyka w przypadku kompromitacji access token
- Możliwość odwołania refresh tokenu
- Lepsze user experience (brak częstego logowania)

## 🔒 Multi-Factor Authentication (MFA)

### Teoria MFA

**Czynniki uwierzytelniania:**
1. **Something you know:** Hasło, PIN
2. **Something you have:** Telefon, token hardware'owy
3. **Something you are:** Biometria (odcisk palca, twarz)

**Time-based One-Time Password (TOTP):**
- Algorytm generujący jednorazowe hasła na podstawie czasu
- Standard RFC 6238
- Implementacje: Google Authenticator, Authy

### Implementacja 2FA

**Flow uwierzytelniania:**
1. Pierwotne uwierzytelnienie (login/hasło)
2. Generowanie i wysłanie kodu weryfikacyjnego
3. Weryfikacja kodu wprowadzonego przez użytkownika
4. Kompletna autentykacja z odpowiednimi uprawnieniami

**Strategie dostarczania kodów:**
- **SMS:** Prosty ale mniej bezpieczny
- **Email:** Backup method
- **TOTP Apps:** Najbezpieczniejszy dla użytkowników końcowych
- **Hardware tokens:** Najwyższy poziom bezpieczeństwa

## 🌍 Security Headers i CORS

### HTTP Security Headers

**Strict-Transport-Security (HSTS):**
Wymusza używanie HTTPS przez przeglądarki:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**Content-Security-Policy (CSP):**
Zapobiega atakom XSS poprzez kontrolowanie źródeł zasobów:
```
Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.google.com
```

**X-Frame-Options:**
Zapobiega clickjacking poprzez kontrolowanie embeddingu strony:
```
X-Frame-Options: DENY
```

### Advanced CORS Configuration

**Preflight Requests:**
Dla złożonych żądań CORS, przeglądarka najpierw wysyła OPTIONS request:
- Sprawdza dozwolone metody HTTP
- Weryfikuje dozwolone headers
- Sprawdza credentials policy

**CORS Security Considerations:**
- Nigdy nie używaj wildcard (*) z credentials
- Dokładnie określ dozwolone origins
- Minimalizuj dozwolone headers i metody
- Regularnie audytuj CORS configuration

---

## 💼 Praktyczne Scenariusze

### Enterprise Integration

**Single Sign-On (SSO):**
Implementacja SSO w środowisku korporacyjnym:
- SAML 2.0 dla aplikacji enterprise
- OAuth/OIDC dla aplikacji cloud
- Federacja tożsamości między organizacjami

**Identity and Access Management (IAM):**
- Centralizacja zarządzania tożsamościami
- Automatyczne provisioning/deprovisioning
- Compliance z regulacjami (GDPR, SOX)

### Cloud Native Security

**Service-to-Service Authentication:**
- Mutual TLS (mTLS) między mikrousługami
- Service mesh security (Istio, Linkerd)
- API Gateway authentication

**Secrets Management:**
- Vault integration dla kluczy i haseł
- Kubernetes secrets
- Cloud provider secret services (AWS Secrets Manager)

---

## 🔗 Powiązane Tematy

- [[Spring Security - Podstawy Bezpieczeństwa]] - fundamenty bezpieczeństwa
- [[Spring Boot Microservices]] - bezpieczeństwo w architekturze rozproszonej
- [[Spring Boot Testing]] - testowanie zabezpieczeń
- [[Spring Boot Actuator]] - monitoring bezpieczeństwa

---

*Czas nauki: ~35 minut*  
*Poziom: Zaawansowany*  
*Wymagana wiedza: Spring Security podstawy, HTTP, protokoły sieciowe*