# 5️⃣ Warstwa Sesji (Session Layer)

## 📋 Definicja

Warstwa sesji odpowiada za nawiązywanie, zarządzanie i kończenie sesji komunikacyjnych między aplikacjami. Umożliwia synchronizację dialogu i zarządzanie wymianą danych.

## 🔧 Główne Funkcje

### 1. Dialog Control (Kontrola Dialogu)
- **Simplex**: Komunikacja jednokierunkowa
- **Half-duplex**: Komunikacja dwukierunkowa na przemian
- **Full-duplex**: Komunikacja dwukierunkowa jednocześnie

### 2. Synchronizacja
- Punkty kontrolne (checkpoints) w przesyłaniu danych
- Możliwość wznowienia transmisji od ostatniego punktu
- Minimalizacja utraty danych przy przerwaniu

### 3. Zarządzanie Tokenami
- Token passing dla koordynacji dostępu
- Zapobieganie jednoczesnym operacjom konfliktowym

## 🔄 Funkcje Sesji

### Nawiązywanie Sesji
```
1. Identyfikacja uczestników
2. Negocjacja parametrów sesji:
   - Tryb transmisji (simplex/half/full-duplex)
   - Szyfrowanie
   - Kompresja
3. Uwierzytelnienie
4. Autoryzacja dostępu
```

### Zarządzanie Sesją
- **Activity Management**: Organizacja danych w logiczne jednostki
- **Exception Handling**: Obsługa wyjątków i błędów
- **Resynchronization**: Możliwość resynchronizacji po błędzie

### Kończenie Sesji
```
1. Orderly release: Normalne zakończenie po zakończeniu transmisji
2. Abrupt release: Nagłe zakończenie (błąd, timeout)
3. Cleanup: Zwolnienie zasobów
```

## 🌐 Protokoły Warstwy Sesji

### NetBIOS (Network Basic Input/Output System)
- Komunikacja w sieciach Windows
- Usługi nazw, sesji i datagramów
- Porty: 137 (name), 138 (datagram), 139 (session)

### RPC (Remote Procedure Call)
- Zdalne wywoływanie procedur
- Umożliwia aplikacjom wywoływanie funkcji na zdalnych systemach
- Używany w NFS, Windows services

### PPTP (Point-to-Point Tunneling Protocol)
- Tworzenie tuneli VPN
- Port 1723 (TCP)
- Używa GRE dla tunelowania danych

### SQL (Session Layer)
- Sesje bazy danych
- Transakcje i blokady
- COMMIT/ROLLBACK

### PAP/CHAP (Authentication Protocols)
- **PAP** (Password Authentication Protocol): Hasło w czystym tekście
- **CHAP** (Challenge Handshake Authentication Protocol): Challenge-response

## 📊 Przykłady Zarządzania Sesjami

### Web Session (HTTP)
```
1. Client → Server: HTTP Request
2. Server tworzy Session ID
3. Server → Client: Set-Cookie: sessionid=xyz123
4. Client przechowuje cookie
5. Kolejne requesty zawierają sessionid
6. Session timeout lub logout kończy sesję
```

### Database Session (SQL)
```sql
-- Rozpoczęcie sesji
CONNECT user@database;

-- Transakcja
BEGIN TRANSACTION;
  UPDATE accounts SET balance = balance - 100 WHERE id = 1;
  UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;  -- lub ROLLBACK w razie błędu

-- Zakończenie sesji
DISCONNECT;
```

### SSH Session
```
1. TCP connection (port 22)
2. SSH protocol version exchange
3. Key exchange (algoritmy kryptograficzne)
4. Authentication (password/key)
5. Session established
6. Interactive shell lub command execution
7. Logout → Session terminated
```

## 🔐 Bezpieczeństwo Sesji

### Session Hijacking (Przechwycenie Sesji)
**Zagrożenia**:
- Kradzież Session ID (XSS, network sniffing)
- Session Fixation
- Man-in-the-Middle

**Obrona**:
```
- HTTPS (szyfrowanie)
- Regeneracja Session ID po logowaniu
- Timeout sesji
- Binding sesji do IP/User-Agent
- Secure i HttpOnly cookies
```

### Session Token Management
```
Best practices:
1. Losowe, nieprzewidywalne tokeny
2. Wystarczająca długość (min. 128 bit)
3. Rotacja tokenów
4. Bezpieczne przechowywanie (encrypted)
5. Timeout nieaktywności
```

## 🛠️ Mechanizmy Sesji w Praktyce

### Cookies (Web)
```http
# Server → Client
Set-Cookie: sessionid=abc123; Secure; HttpOnly; SameSite=Strict

# Client → Server
Cookie: sessionid=abc123
```

### Tokens (API)
```http
# JWT (JSON Web Token)
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# OAuth
Authorization: Bearer ya29.a0AfH6SMBx...
```

### Session Storage
- **Client-side**: Cookies, LocalStorage, SessionStorage
- **Server-side**: Memory, Database, Redis, Memcached

## 🔄 Przykłady Implementacji

### Python - Flask Session
```python
from flask import Flask, session

app = Flask(__name__)
app.secret_key = 'tajny-klucz-sesji'

@app.route('/login', methods=['POST'])
def login():
    # Walidacja użytkownika
    session['user_id'] = user.id
    session['username'] = user.name
    return 'Zalogowano'

@app.route('/logout')
def logout():
    session.clear()
    return 'Wylogowano'
```

### PHP Session
```php
<?php
// Rozpoczęcie sesji
session_start();

// Zapis danych
$_SESSION['user_id'] = 123;
$_SESSION['username'] = 'jan';

// Odczyt danych
echo $_SESSION['username'];

// Zakończenie sesji
session_destroy();
?>
```

### JavaScript - Session Management
```javascript
// LocalStorage (persistent)
localStorage.setItem('sessionToken', token);
const token = localStorage.getItem('sessionToken');

// SessionStorage (until tab close)
sessionStorage.setItem('tempData', data);
const data = sessionStorage.getItem('tempData');
```

## 🔍 Monitoring Sesji

### Session Timeout
```
Idle timeout: 15-30 minut bez aktywności
Absolute timeout: Maksymalny czas sesji (np. 8 godzin)
Concurrent sessions: Limit równoczesnych sesji
```

### Session Tracking
```bash
# Linux - Aktywne sesje SSH
who
w
last

# Web server - Aktywne sesje
# Apache/Nginx access logs
tail -f /var/log/nginx/access.log

# Application monitoring
# Liczba aktywnych sesji
# Średni czas trwania sesji
# Sesje per użytkownik
```

## 📋 Checkpoints i Synchronizacja

### Przykład z FTP
```
1. Rozpoczęcie transferu dużego pliku
2. Checkpoint co 10 MB
3. Przerwanie połączenia
4. Wznowienie od ostatniego checkpointa
   FTP: REST (restart) command
```

### Przykład z bazą danych
```sql
-- Checkpoint w długiej transakcji
BEGIN;
  -- Operacja 1
  SAVEPOINT point1;
  -- Operacja 2
  SAVEPOINT point2;
  -- Błąd - rollback do point2
  ROLLBACK TO point2;
  -- Kontynuacja
COMMIT;
```

## 🔗 Powiązane Tematy

- [[warstwa_transportowa|Warstwa Transportowa]]
- [[warstwa_prezentacji|Warstwa Prezentacji]]
- [[model_osi_overview|Model OSI]]
- [[protokol_http_https|HTTP/HTTPS]]
- [[vpn_tunelowanie|VPN]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-sesji #session-layer #sesje #authentication #osi-layer5
