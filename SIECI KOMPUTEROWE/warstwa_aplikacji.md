# 7️⃣ Warstwa Aplikacji (Application Layer)

## 📋 Definicja

Warstwa aplikacji jest najwyższą warstwą modelu OSI. Zapewnia interfejs między użytkownikiem a siecią, oferując usługi sieciowe bezpośrednio dla aplikacji użytkownika.

## 🔧 Główne Funkcje

### 1. Interfejs Użytkownika
- Bezpośrednia interakcja z aplikacjami
- Udostępnianie usług sieciowych
- Abstrakcja od szczegółów niższych warstw

### 2. Identyfikacja Zasobów
- DNS - tłumaczenie nazw na adresy IP
- URL/URI - identyfikacja zasobów w sieci
- Service discovery

### 3. Synchronizacja Danych
- Email synchronizacja
- File sharing
- Database replication

## 🌐 Protokoły Warstwy Aplikacji

### HTTP/HTTPS (HyperText Transfer Protocol)

#### Podstawy HTTP
```
Port: 80 (HTTP), 443 (HTTPS)
Metody:
  GET     - Pobierz zasób
  POST    - Wyślij dane
  PUT     - Zaktualizuj zasób
  DELETE  - Usuń zasób
  HEAD    - Pobierz nagłówki
  PATCH   - Częściowa aktualizacja
  OPTIONS - Sprawdź dostępne metody
```

#### Request/Response
```http
# Request
GET /index.html HTTP/1.1
Host: www.example.com
User-Agent: Mozilla/5.0
Accept: text/html
Accept-Language: pl,en

# Response
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 1234
Date: Mon, 01 Jan 2024 12:00:00 GMT

<!DOCTYPE html>
<html>...
```

#### Status Codes
```
1xx - Informacyjne
  100 Continue

2xx - Sukces
  200 OK
  201 Created
  204 No Content

3xx - Przekierowanie
  301 Moved Permanently
  302 Found (temporary redirect)
  304 Not Modified

4xx - Błąd klienta
  400 Bad Request
  401 Unauthorized
  403 Forbidden
  404 Not Found

5xx - Błąd serwera
  500 Internal Server Error
  502 Bad Gateway
  503 Service Unavailable
```

#### HTTP/2 i HTTP/3
```
HTTP/2:
- Multiplexing (wiele requestów w jednym połączeniu)
- Server push
- Header compression (HPACK)
- Binary protocol

HTTP/3:
- QUIC zamiast TCP
- Szybsze nawiązywanie połączenia
- Lepsza obsługa packet loss
```

### DNS (Domain Name System)

#### Hierarchia DNS
```
.                           (root)
├── com.                    (TLD - Top Level Domain)
│   ├── google.com.
│   │   ├── www.google.com.
│   │   └── mail.google.com.
│   └── example.com.
├── org.
├── pl.
│   ├── edu.pl.
│   └── gov.pl.
└── ...
```

#### Typy Rekordów DNS
```
A       - Adres IPv4 (example.com → 93.184.216.34)
AAAA    - Adres IPv6 (example.com → 2606:2800:220:1:...)
CNAME   - Alias (www.example.com → example.com)
MX      - Mail server (example.com → mail.example.com, priority)
NS      - Name server (example.com → ns1.example.com)
TXT     - Dowolny tekst (SPF, DKIM, verification)
PTR     - Reverse DNS (IP → nazwa)
SOA     - Start of Authority (informacje o strefie)
SRV     - Service (określa port i priorytet usługi)
```

#### DNS Query
```
1. Klient → Local DNS: Co to jest www.google.com?
2. Local DNS → Root DNS: Kto zarządza .com?
3. Root DNS → Local DNS: ns1.gtld-servers.net
4. Local DNS → TLD DNS (.com): Kto zarządza google.com?
5. TLD DNS → Local DNS: ns1.google.com
6. Local DNS → Authoritative DNS: Jaki IP ma www.google.com?
7. Authoritative → Local DNS: 142.250.185.196
8. Local DNS → Klient: 142.250.185.196
```

#### Narzędzia DNS
```bash
# nslookup
nslookup google.com
nslookup -type=MX google.com

# dig
dig google.com
dig @8.8.8.8 google.com A
dig google.com ANY

# host
host google.com
host -t MX google.com
```

### DHCP (Dynamic Host Configuration Protocol)

#### Proces DHCP (DORA)
```
1. DISCOVER (Client → Broadcast)
   "Szukam serwera DHCP!"
   
2. OFFER (Server → Client)
   "Mam dla Ciebie IP: 192.168.1.100"
   
3. REQUEST (Client → Broadcast)
   "Biorę IP od serwera X"
   
4. ACK (Server → Client)
   "Potwierdzam, IP jest Twój"
```

#### Konfiguracja DHCP
```
IP Address:     192.168.1.100
Subnet Mask:    255.255.255.0
Gateway:        192.168.1.1
DNS Servers:    8.8.8.8, 8.8.4.4
Lease Time:     86400 seconds (24h)
```

### FTP (File Transfer Protocol)

#### Tryby FTP
```
Active Mode:
  Klient: Port command (>1023)
  Serwer: Port 20 (data) → Klient (>1023)
  Problem: Firewall blokuje połączenie z serwera

Passive Mode (PASV):
  Klient: Port command (>1023)
  Serwer: Port command (21) → zwraca port danych
  Klient → Serwer: Port danych
```

#### Komendy FTP
```
USER username   - Nazwa użytkownika
PASS password   - Hasło
LIST            - Lista plików
RETR filename   - Pobierz plik
STOR filename   - Wyślij plik
CWD directory   - Zmień katalog
PWD             - Aktualny katalog
QUIT            - Zakończ
```

### SMTP/POP3/IMAP (Email Protocols)

#### SMTP (Simple Mail Transfer Protocol)
```
Port: 25 (standard), 587 (submission), 465 (SSL/TLS)

Przykładowa sesja:
C: EHLO client.example.com
S: 250-mail.example.com Hello
C: MAIL FROM:<sender@example.com>
S: 250 OK
C: RCPT TO:<recipient@example.com>
S: 250 OK
C: DATA
S: 354 Start mail input
C: Subject: Test
C: 
C: Treść wiadomości
C: .
S: 250 OK
C: QUIT
```

#### POP3 (Post Office Protocol)
```
Port: 110 (POP3), 995 (POP3S)

Funkcje:
- Pobieranie poczty
- Zazwyczaj usuwa z serwera
- Prosty protokół

Komendy:
USER username
PASS password
LIST         - Lista wiadomości
RETR n       - Pobierz wiadomość n
DELE n       - Usuń wiadomość n
QUIT
```

#### IMAP (Internet Message Access Protocol)
```
Port: 143 (IMAP), 993 (IMAPS)

Funkcje:
- Synchronizacja poczty
- Foldery na serwerze
- Flagi (read, starred, etc.)
- Wyszukiwanie na serwerze

Zalety vs POP3:
- Dostęp z wielu urządzeń
- Zarządzanie folderami
- Częściowe pobieranie wiadomości
```

### SSH (Secure Shell)

#### Funkcje SSH
```
Port: 22

Zastosowania:
- Zdalny terminal
- Bezpieczny transfer plików (SCP, SFTP)
- Tunelowanie portów (port forwarding)
- X11 forwarding
```

#### Autentykacja SSH
```
Password-based:
  ssh user@host

Key-based:
  ssh-keygen -t rsa -b 4096
  ssh-copy-id user@host
  ssh user@host  # Bez hasła
```

#### Port Forwarding
```bash
# Local port forwarding
ssh -L 8080:localhost:80 user@remote

# Remote port forwarding
ssh -R 8080:localhost:80 user@remote

# Dynamic (SOCKS proxy)
ssh -D 1080 user@remote
```

### Telnet
```
Port: 23
Status: Legacy (niezabezpieczone)

Używane do:
- Debugowanie protokołów tekstowych
- Testowanie portów

Przykład:
telnet smtp.gmail.com 25
telnet example.com 80
```

### SNMP (Simple Network Management Protocol)

#### Wersje SNMP
```
SNMPv1: Podstawowa, community string (niezabezpieczone)
SNMPv2c: Bulk operations, nadal community string
SNMPv3: Szyfrowanie i autentykacja
```

#### Operacje SNMP
```
GET     - Pobierz wartość OID
GET-NEXT - Następny OID
SET     - Ustaw wartość
TRAP    - Asynchroniczne powiadomienie
```

#### MIB (Management Information Base)
```
OID (Object Identifier):
1.3.6.1.2.1.1.1.0  - sysDescr
1.3.6.1.2.1.1.3.0  - sysUpTime
1.3.6.1.2.1.2.2.1  - ifTable
```

### LDAP (Lightweight Directory Access Protocol)

#### Struktura LDAP
```
DN (Distinguished Name):
cn=Jan Kowalski,ou=Users,dc=example,dc=com

Komponenty:
cn - Common Name
ou - Organizational Unit
dc - Domain Component
```

#### Zastosowania
- Active Directory (Microsoft)
- OpenLDAP
- Katalogi użytkowników
- Single Sign-On (SSO)

### NTP (Network Time Protocol)

#### Synchronizacja Czasu
```
Port: 123 (UDP)

Stratum:
0 - Reference clock (GPS, atomic)
1 - Primary server (sync to stratum 0)
2 - Secondary server (sync to stratum 1)
...
15 - Max

Komendy:
ntpdate pool.ntp.org        # One-time sync
ntpq -p                      # Query NTP peers
```

## 🔐 Bezpieczeństwo Aplikacji

### SSL/TLS Certificates
```
Typy certyfikatów:
- Domain Validated (DV)
- Organization Validated (OV)
- Extended Validation (EV)

Weryfikacja:
openssl s_client -connect example.com:443
openssl x509 -in cert.pem -text -noout
```

### API Security
```
Metody autentykacji:
- API Keys
- OAuth 2.0
- JWT (JSON Web Tokens)
- mTLS (Mutual TLS)

Best practices:
- HTTPS only
- Rate limiting
- Input validation
- CORS configuration
```

## 🛠️ Narzędzia Diagnostyczne

### cURL
```bash
# GET request
curl https://api.example.com/users

# POST request
curl -X POST -H "Content-Type: application/json" \
     -d '{"name":"Jan"}' https://api.example.com/users

# Verbose output
curl -v https://example.com

# Follow redirects
curl -L https://example.com
```

### Wget
```bash
# Pobierz plik
wget https://example.com/file.pdf

# Rekursywne pobieranie
wget -r -np -k https://example.com/

# Resume download
wget -c https://example.com/largefile.iso
```

### Netcat
```bash
# HTTP request
echo -e "GET / HTTP/1.0\n\n" | nc example.com 80

# Port listening
nc -l -p 8080

# Port scanning
nc -zv example.com 20-100
```

## 🔗 Powiązane Tematy

- [[warstwa_prezentacji|Warstwa Prezentacji]]
- [[model_osi_overview|Model OSI]]
- [[protokol_http_https|HTTP/HTTPS - Szczegóły]]
- [[protokol_dns|DNS - Szczegóły]]
- [[bezpieczenstwo_sieci|Bezpieczeństwo Sieci]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-aplikacji #application-layer #http #dns #dhcp #smtp #ssh #ftp #osi-layer7
