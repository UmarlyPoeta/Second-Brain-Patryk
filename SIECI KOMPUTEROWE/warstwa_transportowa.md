# 4️⃣ Warstwa Transportowa (Transport Layer)

## 📋 Definicja

Warstwa transportowa zapewnia komunikację end-to-end między aplikacjami na różnych hostach. Odpowiada za segmentację danych, kontrolę przepływu, kontrolę błędów oraz multipleksowanie wielu aplikacji.

## 🔧 Główne Funkcje

### 1. Multipleksowanie/Demultipleksowanie
- Wykorzystanie numerów portów do identyfikacji aplikacji
- Umożliwia wiele połączeń jednocześnie

### 2. Kontrola Przepływu
- Zapobieganie przeciążeniu odbiorcy
- Mechanizmy okien przesuwnych (sliding window)

### 3. Kontrola Błędów
- Wykrywanie i korekcja błędów transmisji
- Retransmisja utraconych segmentów

### 4. Segmentacja i Reassembly
- Dzielenie danych aplikacji na segmenty
- Składanie segmentów w miejscu docelowym

## 🌐 Porty Transportowe

### Zakres Portów
```
Well-known ports:    0 - 1023      (Usługi systemowe)
Registered ports:    1024 - 49151  (Aplikacje użytkownika)
Dynamic/Private:     49152 - 65535 (Tymczasowe, klient)
```

### Popularne Porty
```
TCP:
  20/21  - FTP (data/control)
  22     - SSH
  23     - Telnet
  25     - SMTP
  80     - HTTP
  110    - POP3
  143    - IMAP
  443    - HTTPS
  3389   - RDP (Remote Desktop)

UDP:
  53     - DNS
  67/68  - DHCP (server/client)
  69     - TFTP
  123    - NTP
  161/162- SNMP
  514    - Syslog
```

## 🔄 Protokół TCP (Transmission Control Protocol)

### Charakterystyka
- **Connection-oriented**: Nawiązywanie połączenia przed transmisją
- **Reliable**: Gwarantowana dostarczenie danych
- **Ordered**: Zachowanie kolejności segmentów
- **Flow control**: Kontrola przepływu
- **Error checking**: Detekcja i korekcja błędów

### Struktura Segmentu TCP
```
┌────────────────┬────────────────┬─────────────────┬──────────────┐
│  Source Port   │  Dest Port     │ Sequence Number │              │
│   (16 bit)     │   (16 bit)     │   (32 bit)      │              │
├────────────────┴────────────────┴─────────────────┤              │
│            Acknowledgment Number (32 bit)         │              │
├─────┬──────┬─────────────────────┬────────────────┴──────────────┤
│Offset│Resv │      Flags          │      Window Size              │
│4 bit│6 bit│     (9 bit)         │        (16 bit)               │
├─────┴──────┴─────────────────────┴───────────────────────────────┤
│   Checksum (16 bit)              │  Urgent Pointer (16 bit)      │
├──────────────────────────────────┴───────────────────────────────┤
│                     Options + Padding                             │
├───────────────────────────────────────────────────────────────────┤
│                          Data                                     │
└───────────────────────────────────────────────────────────────────┘
```

### Flagi TCP
```
URG (Urgent):     Priorytetowe dane
ACK (Acknowledgment): Potwierdzenie
PSH (Push):       Natychmiastowe przekazanie do aplikacji
RST (Reset):      Reset połączenia
SYN (Synchronize): Inicjalizacja połączenia
FIN (Finish):     Zakończenie połączenia
```

### Three-Way Handshake (Nawiązywanie Połączenia)
```
Klient                                    Serwer
  │                                          │
  │──────── SYN (seq=100) ──────────────────→│
  │                                          │
  │←─── SYN-ACK (seq=300, ack=101) ─────────│
  │                                          │
  │──────── ACK (seq=101, ack=301) ─────────→│
  │                                          │
  │         POŁĄCZENIE NAWIĄZANE             │
  │                                          │
```

### Four-Way Handshake (Kończenie Połączenia)
```
Klient                                    Serwer
  │                                          │
  │──────── FIN (seq=500) ───────────────────→│
  │                                          │
  │←─────── ACK (ack=501) ───────────────────│
  │                                          │
  │←─────── FIN (seq=700) ───────────────────│
  │                                          │
  │──────── ACK (ack=701) ───────────────────→│
  │                                          │
  │         POŁĄCZENIE ZAMKNIĘTE             │
```

### Kontrola Przepływu TCP
**Sliding Window (Przesuwne Okno)**:
```
Nadawca:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
      ↑───────────↑
      Wysłane    Okno=3

Odbieranie ACK przesuwa okno:
┌───┬───┬───┬───┬───┬───┬───┬───┬───┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │
└───┴───┴───┴───┴───┴───┴───┴───┴───┘
          ↑───────────↑
          Okno przesunięte
```

### Retransmisja TCP
- **Timeout**: Retransmisja po upływie czasu RTO (Retransmission Timeout)
- **Fast Retransmit**: Po 3 duplikatach ACK
- **Selective ACK (SACK)**: Potwierdzanie wybranych segmentów

### Kontrola Przeciążenia (Congestion Control)
```
Algorytmy:
- Slow Start: Wykładniczy wzrost okna
- Congestion Avoidance: Liniowy wzrost
- Fast Recovery: Szybkie odzyskiwanie po utracie

Rozmiar okna:
cwnd (congestion window) ──┐
                           ├─→ Rzeczywiste okno = min(cwnd, rwnd)
rwnd (receiver window) ────┘
```

## 🚀 Protokół UDP (User Datagram Protocol)

### Charakterystyka
- **Connectionless**: Brak nawiązywania połączenia
- **Unreliable**: Brak gwarancji dostarczenia
- **Unordered**: Brak zachowania kolejności
- **Low overhead**: Minimalna liczba nagłówków
- **Fast**: Niskie opóźnienia

### Struktura Datagramu UDP
```
┌────────────────┬────────────────┐
│  Source Port   │  Dest Port     │
│   (16 bit)     │   (16 bit)     │
├────────────────┴────────────────┤
│  Length        │  Checksum      │
│   (16 bit)     │   (16 bit)     │
├─────────────────────────────────┤
│           Data                  │
│                                 │
└─────────────────────────────────┘

Minimalny rozmiar: 8 bajtów (tylko nagłówek)
```

### Zastosowania UDP
- **DNS**: Szybkie zapytania (53/UDP)
- **DHCP**: Konfiguracja IP (67-68/UDP)
- **Streaming**: Wideo/audio (RTSP, RTP)
- **Gaming**: Gry online (niskie opóźnienie)
- **VoIP**: Telefonia internetowa (SIP, RTP)
- **TFTP**: Prosty transfer plików (69/UDP)
- **SNMP**: Monitorowanie sieci (161-162/UDP)

## 🆚 TCP vs UDP - Porównanie

| Cecha               | TCP                          | UDP                        |
|---------------------|------------------------------|----------------------------|
| Połączenie          | Connection-oriented          | Connectionless             |
| Niezawodność        | Gwarantowana                 | Brak gwarancji             |
| Kolejność           | Zachowana                    | Niezachowana               |
| Kontrola przepływu  | Tak (sliding window)         | Nie                        |
| Kontrola błędów     | Retransmisja                 | Tylko checksum             |
| Szybkość            | Wolniejsza                   | Szybsza                    |
| Nagłówek            | 20-60 bajtów                 | 8 bajtów                   |
| Zastosowania        | Web, Email, File transfer    | Streaming, Gaming, DNS     |

## 🔌 Gniazda (Sockets)

### Typy Gniazd
```
Stream Socket (TCP):
- SOCK_STREAM
- Niezawodne, połączeniowe

Datagram Socket (UDP):
- SOCK_DGRAM
- Bez połączenia, szybkie

Raw Socket:
- Bezpośredni dostęp do IP
- Wymaga uprawnień root
```

### Identyfikacja Połączenia
```
Socket = (Protocol, Source IP, Source Port, Dest IP, Dest Port)

Przykład:
(TCP, 192.168.1.100, 50234, 93.184.216.34, 443)
```

## 🔍 Stany Połączenia TCP

```
LISTEN:       Nasłuchiwanie na połączenia
SYN-SENT:     Wysłano SYN, czekanie na SYN-ACK
SYN-RECEIVED: Odebrano SYN, wysłano SYN-ACK
ESTABLISHED:  Połączenie aktywne
FIN-WAIT-1:   Wysłano FIN
FIN-WAIT-2:   Odebrano ACK na FIN
CLOSE-WAIT:   Odebrano FIN, czekanie na zamknięcie aplikacji
CLOSING:      Obydwie strony wysłały FIN
LAST-ACK:     Wysłano FIN, czekanie na ACK
TIME-WAIT:    Czekanie na duplikaty segmentów (2*MSL)
CLOSED:       Połączenie zamknięte
```

## 🛠️ Komendy Diagnostyczne

### Sprawdzenie Połączeń
```bash
# Linux/Mac
netstat -tuln          # Wszystkie porty nasłuchujące
netstat -tun           # Wszystkie aktywne połączenia
ss -tuln               # Nowszy zamiennik netstat
lsof -i :80            # Proces używający portu 80

# Windows
netstat -an            # Wszystkie połączenia
netstat -ano           # Z PID procesu
```

### Testowanie Portów
```bash
# Telnet
telnet example.com 80

# Netcat
nc -zv example.com 80        # Test portu TCP
nc -uzv example.com 53       # Test portu UDP

# Nmap
nmap -p 1-1000 example.com   # Skanowanie portów
```

### Analiza Pakietów
```bash
# tcpdump - TCP
tcpdump -i eth0 tcp port 80

# tcpdump - UDP
tcpdump -i eth0 udp port 53

# Wireshark filtry
tcp.port == 443
udp.port == 53
tcp.flags.syn == 1 && tcp.flags.ack == 0
```

## 🔐 Bezpieczeństwo Warstwy Transportowej

### TLS/SSL (TCP)
- Szyfrowanie połączeń TCP
- Autentykacja serwera/klienta
- HTTPS (HTTP over TLS)

### DTLS (UDP)
- TLS dla UDP
- Używane w VPN (OpenVPN), WebRTC

### Port Security
- Filtrowanie portów (firewall)
- Blokowanie niepotrzebnych usług
- ACL na routerach/switchach

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[warstwa_sesji|Warstwa Sesji]]
- [[protokol_tcp|TCP - Szczegóły]]
- [[protokol_udp|UDP - Szczegóły]]
- [[protokol_http_https|HTTP/HTTPS]]
- [[firewall_zasady|Firewall]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-transportowa #transport-layer #tcp #udp #porty #sockets #osi-layer4
