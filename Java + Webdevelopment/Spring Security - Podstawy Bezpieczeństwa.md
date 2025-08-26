# 🔐 Spring Security - Podstawy Bezpieczeństwa

## 📋 Wprowadzenie do Spring Security

Spring Security to kompleksowy framework bezpieczeństwa dla aplikacji Java, który zapewnia autentykację, autoryzację oraz ochronę przed najczęstszymi atakami bezpieczeństwa. Framework ten został zaprojektowany z myślą o elastyczności i możliwości dostosowania do różnorodnych wymagań bezpieczeństwa w aplikacjach korporacyjnych.

### Dlaczego Bezpieczeństwo jest Kluczowe

W dzisiejszym cyfrowym świecie, aplikacje webowe stają się coraz bardziej narażone na ataki cybernetyczne. Statystyki pokazują, że:
- 43% ataków cybernetycznych jest skierowanych na małe i średnie przedsiębiorstwa
- Średni koszt naruszenia danych wynosi 4.45 miliona dolarów
- 95% udanych ataków jest wynikiem błędów człowieka

Spring Security pomaga deweloperom implementować bezpieczeństwo zgodnie z najlepszymi praktykami branżowymi, redukując ryzyko błędów i luk bezpieczeństwa.

## 🔑 Kluczowe Koncepty Bezpieczeństwa

### Autentykacja vs Autoryzacja

**Autentykacja (Authentication)** to proces weryfikacji tożsamości użytkownika - "Kim jesteś?"
- Sprawdza czy użytkownik jest tym, za kogo się podaje
- Wykorzystuje dane uwierzytelniające (credentials) jak login/hasło, certyfikaty, tokeny
- Jest pierwszym krokiem w procesie zabezpieczeń

**Autoryzacja (Authorization)** to proces określania uprawnień - "Co możesz robić?"
- Sprawdza czy autentykowany użytkownik ma prawo do wykonania konkretnej operacji
- Opiera się na rolach, uprawnieniach lub regułach biznesowych
- Następuje po udanej autentykacji

### Principal, Credentials, Authorities

**Principal** - reprezentuje użytkownika w systemie
- Najczęściej nazwa użytkownika lub obiekt UserDetails
- Unikalnie identyfikuje użytkownika w aplikacji

**Credentials** - dane uwierzytelniające
- Hasło, certyfikat, token JWT
- Są używane do weryfikacji tożsamości
- Powinny być przechowywane bezpiecznie (hashowane)

**Authorities/Roles** - uprawnienia użytkownika
- Określają co użytkownik może robić w systemie
- Role to grupowe uprawnienia (np. ADMIN, USER)
- Authorities to pojedyncze uprawnienia (np. READ_USERS, DELETE_POSTS)

## 🏗️ Architektura Spring Security

### Security Filter Chain

Spring Security działa jako łańcuch filtrów (Filter Chain) w aplikacji webowej. Każde HTTP request przechodzi przez serię filtrów, które sprawdzają różne aspekty bezpieczeństwa:

**1. SecurityContextPersistenceFilter**
- Odtwarza SecurityContext z poprzednich requestów
- Przechowuje kontekst bezpieczeństwa między requestami

**2. AuthenticationFilter (różne implementacje)**
- UsernamePasswordAuthenticationFilter - dla formularzy logowania
- BasicAuthenticationFilter - dla HTTP Basic Auth
- JwtAuthenticationFilter - dla tokenów JWT

**3. AuthorizationFilter**
- Sprawdza uprawnienia do zasobów
- Wykorzystuje konfigurację dostępu (access rules)

### Security Context

SecurityContext to kontener przechowujący informacje o bezpieczeństwie aktualnego wątku. Zawiera:
- Obiekt Authentication (dane uwierzytelnionego użytkownika)
- Informacje o prawach dostępu
- Dodatkowe metadane bezpieczeństwa

**ThreadLocal Storage:** SecurityContext jest przechowywany w ThreadLocal, co oznacza, że każdy wątek ma swój własny kontekst bezpieczeństwa.

## 🔧 Mechanizmy Autentykacji

### Form-Based Authentication

**Teoria:** Tradycyjny mechanizm logowania poprzez formularz HTML. Użytkownik wprowadza dane uwierzytelniające, które są weryfikowane przez serwer.

**Proces:**
1. Użytkownik próbuje uzyskać dostęp do chronionego zasobu
2. System przekierowuje na stronę logowania
3. Po wprowadzeniu danych, następuje weryfikacja
4. W przypadku sukcesu, użytkownik jest przekierowany do oryginalnie żądanego zasobu

**Zalety:**
- Przyjazny dla użytkownika interfejs
- Pełna kontrola nad wyglądem strony logowania
- Możliwość dostosowania do brandingu firmy

**Wady:**
- Wymaga zarządzania sesjami
- Problemy z aplikacjami SPA (Single Page Applications)
- Ograniczona dla API REST

### HTTP Basic Authentication

**Teoria:** Prosty mechanizm autentykacji, gdzie dane uwierzytelniające są przesyłane w nagłówku HTTP w formacie base64.

**Charakterystyka:**
- Stateless - każde żądanie zawiera dane uwierzytelniające
- Prosty w implementacji
- Wspierane przez wszystkie przeglądarki i biblioteki HTTP

**Bezpieczeństwo:**
- Base64 to kodowanie, nie szyfrowanie
- Wymaga HTTPS w środowisku produkcyjnym
- Podatne na ataki man-in-the-middle bez szyfrowania

### Token-Based Authentication (JWT)

**Teoria:** Nowoczesny mechanizm autentykacji wykorzystujący tokeny JSON Web Token (JWT). Token zawiera zakodowane informacje o użytkowniku i jego uprawnieniach.

**Struktura JWT:**
- Header: metadata o tokenie (algorytm szyfrowania)
- Payload: dane o użytkowniku (claims)
- Signature: podpis cyfrowy zapewniający integralność

**Zalety:**
- Stateless - nie wymaga przechowywania sesji po stronie serwera
- Skalowalne w architekturze mikrousług
- Możliwość przechowywania dodatkowych informacji w tokenie
- Crossplatform - działa z aplikacjami mobilnymi, SPA, API

**Wady:**
- Większy rozmiar niż zwykłe session ID
- Trudności z odwołaniem tokenu przed wygaśnięciem
- Wymagana ostrożność przy przechowywaniu w przeglądarce

## 🛡️ Autoryzacja i Kontrola Dostępu

### Role-Based Access Control (RBAC)

**Teoria:** Model autoryzacji oparty na rolach. Użytkownicy są przypisywani do ról, a role mają określone uprawnienia.

**Struktura:**
- User → Role → Permission
- Przykład: Użytkownik "Jan" ma rolę "MANAGER", rola "MANAGER" ma uprawnienie "READ_REPORTS"

**Zalety:**
- Prosty w zrozumieniu i implementacji
- Łatwe zarządzanie uprawnieniami dla grup użytkowników
- Standardowy model w większości organizacji

### Method-Level Security

**Teoria:** Kontrola dostępu na poziomie metod pozwala na precyzyjne określenie, kto może wywołać konkretną metodę w aplikacji.

**Rodzaje:**
- **@PreAuthorize** - sprawdza uprawnienia przed wykonaniem metody
- **@PostAuthorize** - sprawdza uprawnienia po wykonaniu metody (może filtrować wyniki)
- **@RolesAllowed** - prosty mechanizm oparty na rolach

### URL-Based Security

**Teoria:** Konfiguracja bezpieczeństwa na poziomie ścieżek URL. Pozwala na określenie różnych wymagań bezpieczeństwa dla różnych części aplikacji.

**Wzorce matchowania:**
- Ant patterns: `/admin/**`, `/api/*/users`
- Regex patterns: `^/api/v[0-9]+/.*$`
- HTTP methods matching: `POST /api/users`

## 🔒 Ochrona przed Atakami

### CSRF (Cross-Site Request Forgery)

**Teoria ataku:** CSRF to atak, w którym złośliwa strona nakłania uwierzytelnionego użytkownika do wykonania nieautoryzowanej operacji w aplikacji, w której jest zalogowany.

**Mechanizm ochrony:** Spring Security generuje unikalny token CSRF dla każdej sesji. Token musi być dołączony do wszystkich operacji modyfikujących dane (POST, PUT, DELETE).

**Implementacja:** Token może być przesyłany jako:
- Hidden field w formularzach HTML
- Header w requestach AJAX
- Parameter w URL (niezalecane)

### Session Management

**Session Fixation:** Atak polegający na narzuceniu użytkownikowi znanego ID sesji przed logowaniem.

**Ochrona:** Spring Security automatycznie zmienia ID sesji po udanej autentykacji.

**Session Concurrency:** Kontrolowanie liczby jednoczesnych sesji użytkownika:
- Maksymalna liczba sesji
- Strategia przy przekroczeniu limitu (odrzuć nową/zakończ starą)

### Password Security

**Hashowanie haseł:** Spring Security wykorzystuje nowoczesne algorytmy hashowania:
- BCrypt (zalecany) - adaptacyjny, odporny na ataki czasowe
- PBKDF2 - standard NIST
- Argon2 - najnowszy, wygrał konkurs Password Hashing Competition

**Password Policies:** Implementacja zasad dotyczących haseł:
- Minimalna długość
- Wymagane znaki specjalne
- Historia haseł
- Wygasanie haseł

## 📊 Monitoring i Auditing

### Security Events

Spring Security publikuje różne eventy związane z bezpieczeństwem:
- Udane/nieudane próby logowania
- Zmiany uprawnień użytkowników
- Dostęp do chronionych zasobów

### Logging

**Security Logging:** Rejestrowanie wydarzeń bezpieczeństwa dla:
- Compliance i audyt
- Analiza wzorców ataków
- Debugowanie problemów z bezpieczeństwem

**Poziomy logowania:**
- ERROR: Błędy bezpieczeństwa
- WARN: Podejrzane aktywności
- INFO: Normalne operacje bezpieczeństwa
- DEBUG: Szczegółowe informacje deweloperskie

---

## 💼 Praktyczne Zastosowania

### Scenariusze Biznesowe

**1. E-commerce:**
- Różne poziomy dostępu (gość, klient, admin)
- Ochrona danych płatniczych
- Audit trail transakcji

**2. System CRM:**
- Hierarhiczne uprawnienia (sprzedawca → manager → dyrektor)
- Dostęp do danych klientów na podstawie regionu
- Integracja z systemami zewnętrznymi (SSO)

**3. Aplikacje SaaS:**
- Multi-tenant security
- API rate limiting
- OAuth2 dla integracji z zewnętrznymi usługami

### Wybór Strategii Autentykacji

**Kryteria decyzyjne:**
- Typ aplikacji (web, mobile, API)
- Wymagania użytkowe (UX)
- Infrastruktura (single server vs microservices)
- Compliance (GDPR, SOX, HIPAA)

---

## 🔗 Powiązane Tematy

- [[Spring Security - Zaawansowane]] - OAuth2, LDAP, custom providers
- [[Spring Boot Web]] - integracja z kontrolerami
- [[Spring Boot Testing]] - testowanie zabezpieczeń
- [[Spring Boot Microservices]] - bezpieczeństwo w architekturze rozproszonej

---

*Czas nauki: ~25 minut*  
*Poziom: Średniozaawansowany*  
*Wymagana wiedza: Spring Boot podstawy, HTTP, podstawy bezpieczeństwa*