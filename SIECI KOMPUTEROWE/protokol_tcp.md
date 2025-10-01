# 🔌 Protokół TCP - Transmission Control Protocol

## 📋 Definicja

TCP (Transmission Control Protocol) to połączeniowy, niezawodny protokół warstwy transportowej (warstwa 4), zapewniający gwarantowaną dostawę danych w odpowiedniej kolejności między aplikacjami.

## 🔧 Charakterystyka TCP

### Główne Cechy
```
✓ Connection-oriented: Nawiązywanie połączenia przed transmisją
✓ Reliable: Gwarantowana dostawa (retransmisja)
✓ Ordered: Zachowanie kolejności pakietów
✓ Flow control: Kontrola przepływu (sliding window)
✓ Congestion control: Kontrola przeciążenia sieci
✓ Error checking: Detekcja błędów (checksum)
✓ Full-duplex: Dwukierunkowa komunikacja jednocześnie
```

### Zastosowania
```
HTTP/HTTPS - Web browsing
FTP - Transfer plików
SMTP - Email (wysyłanie)
SSH - Zdalny terminal
Telnet - Zdalny terminal (legacy)
SMB - Windows file sharing
Database connections (MySQL, PostgreSQL)
```

## 📦 Struktura Segmentu TCP

### Format Nagłówka (20-60 bajtów)
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|          Source Port          |       Destination Port        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                        Sequence Number                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Acknowledgment Number                      |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
| Offset|Reserv |     Flags     |            Window             |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|           Checksum            |         Urgent Pointer        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (0-40 bytes)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                             Data                              |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Pola Nagłówka

#### Source/Destination Port (16 bit każdy)
```
Porty: 0-65535
- Well-known: 0-1023
- Registered: 1024-49151
- Dynamic: 49152-65535

Przykład:
Source: 50234 (klient)
Destination: 443 (HTTPS server)
```

#### Sequence Number (32 bit)
```
Numer pierwszego bajtu danych w segmencie

Przykład:
Segment 1: SEQ=100 (bajty 100-199)
Segment 2: SEQ=200 (bajty 200-299)
Segment 3: SEQ=300 (bajty 300-399)

ISN (Initial Sequence Number):
- Losowy (security)
- Ustalony w SYN
```

#### Acknowledgment Number (32 bit)
```
Numer następnego oczekiwanego bajtu

Przykład:
Otrzymano bajty 100-199
ACK=200 ("oczekuję bajtu 200")

Cumulative ACK:
ACK=500 potwierdza wszystkie bajty do 499
```

#### Flags (9 bitów)
```
URG: Urgent Pointer valid
ACK: Acknowledgment Number valid
PSH: Push Function (natychmiastowa dostawa do aplikacji)
RST: Reset connection (błąd, odmowa)
SYN: Synchronize (nawiązywanie)
FIN: Finish (zamykanie)

Nowsze (RFC 3168):
ECE: ECN-Echo (Explicit Congestion Notification)
CWR: Congestion Window Reduced
NS:  Nonce Sum (ECN protection)
```

#### Window Size (16 bit)
```
Rozmiar okna odbiorcy (receive window)
Wartość: 0-65535 bajtów

Window Scaling (opcja):
Rzeczywisty rozmiar = Window × 2^Scale
Max: 65535 × 2^14 = 1 GB
```

#### Checksum (16 bit)
```
Weryfikacja integralności:
- Nagłówek TCP
- Dane
- Pseudo-header (IP src/dst)

Algorytm: 16-bit one's complement sum
```

## 🔄 Nawiązywanie Połączenia (Three-Way Handshake)

### Proces
```
Client                                  Server
  │                                       │
  │───────── SYN (SEQ=100) ──────────────→│
  │        (Proszę o połączenie)          │
  │                                       │
  │←─ SYN-ACK (SEQ=300, ACK=101) ────────│
  │   (OK, mój SEQ=300, oczekuję 101)    │
  │                                       │
  │────── ACK (SEQ=101, ACK=301) ────────→│
  │        (Potwierdzam)                  │
  │                                       │
  │         POŁĄCZENIE NAWIĄZANE          │
  │                                       │
```

### Szczegóły
```
1. Client → Server: SYN
   SEQ=X (np. 1000)
   SYN flag=1
   
2. Server → Client: SYN-ACK
   SEQ=Y (np. 5000)
   ACK=X+1 (1001)
   SYN flag=1, ACK flag=1
   
3. Client → Server: ACK
   SEQ=X+1 (1001)
   ACK=Y+1 (5001)
   ACK flag=1

Po tym można wysyłać dane
```

### Opcje w SYN
```
MSS (Maximum Segment Size):
- Największy segment danych (bez nagłówków)
- Domyślnie: MTU - 40 (IP+TCP headers)
- Ethernet: 1460 (1500 - 20 - 20)

Window Scale:
- Rozszerzenie window size powyżej 65535

SACK Permitted:
- Selective Acknowledgment support

Timestamps:
- RTT measurement
- PAWS (Protection Against Wrapped Sequences)
```

## 🔚 Zamykanie Połączenia (Four-Way Handshake)

### Graceful Close
```
Client                                  Server
  │                                       │
  │────────── FIN (SEQ=500) ─────────────→│
  │        (Koniec danych z mojej strony) │
  │                                       │
  │←───────── ACK (ACK=501) ──────────────│
  │        (Potwierdzam FIN)              │
  │                                       │
  │←────────── FIN (SEQ=700) ─────────────│
  │        (Koniec danych z mojej strony) │
  │                                       │
  │────────── ACK (ACK=701) ─────────────→│
  │        (Potwierdzam FIN)              │
  │                                       │
  │         POŁĄCZENIE ZAMKNIĘTE          │
  │                                       │
```

### RST (Reset)
```
Nagłe zamknięcie:
- Błąd połączenia
- Port zamknięty
- Odmowa połączenia
- Security (IPS/firewall)

RST flag=1
Brak ACK na RST
```

### Stany Zamykania
```
TIME_WAIT: 2×MSL (Maximum Segment Lifetime)
- Typowo: 2×60s = 120s
- Czeka na opóźnione/zduplikowane pakiety
- Problem: Wyczerpanie portów (many connections)
```

## 🔄 Kontrola Przepływu (Flow Control)

### Sliding Window
```
Nadawca może wysłać tyle, ile pozwala okno odbiorcy

Przykład (Window=3):
┌─────────────────────────────────┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
└─────────────────────────────────┘
  ↑─────────↑
  Wysłane (czeka na ACK)

Po ACK dla 1,2:
┌─────────────────────────────────┐
│ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │
└─────────────────────────────────┘
          ↑─────────↑
          Nowe okno

Może wysłać 4,5 (okno=3, wysłano 3, otrzymano ACK 2)
```

### Zero Window
```
Odbiorca przepełniony → Window=0

Nadawca:
1. Zatrzymuje wysyłanie
2. Okresowo wysyła window probe (sprawdza okno)
3. Czeka na window update (Window > 0)
```

## 📉 Kontrola Przeciążenia (Congestion Control)

### Algorytmy

#### 1. Slow Start
```
Wykładniczy wzrost cwnd (congestion window):

RTT 1: cwnd=1  MSS → Wysłano 1
RTT 2: cwnd=2  MSS → Wysłano 2
RTT 3: cwnd=4  MSS → Wysłano 4
RTT 4: cwnd=8  MSS → Wysłano 8
...

Rośnie do ssthresh (slow start threshold)
```

#### 2. Congestion Avoidance
```
Liniowy wzrost (po przekroczeniu ssthresh):

RTT 1: cwnd=ssthresh
RTT 2: cwnd=ssthresh+1 MSS
RTT 3: cwnd=ssthresh+2 MSS
...

Wzrost powolniejszy, unikanie przeciążenia
```

#### 3. Fast Retransmit
```
3 duplikaty ACK → Retransmituj natychmiast

Przykład:
ACK=100, ACK=100, ACK=100, ACK=100 (4×)
↓
Retransmituj segment 100 (nie czekaj na timeout)
```

#### 4. Fast Recovery
```
Po Fast Retransmit:
1. ssthresh = cwnd / 2
2. cwnd = ssthresh + 3×MSS
3. Congestion Avoidance (nie Slow Start)

Szybsze odzyskanie (bez spadku do 1 MSS)
```

### Wykres Kontroli Przeciążenia
```
cwnd
  │     
  │         ╱╲    Fast Recovery
  │        ╱  ╲╱╲
  │    SS ╱      ╲  CA
  │      ╱        ╲
  │     ╱          ╲    Slow Start
  │    ╱            ╲  ╱
  │   ╱              ╲╱
  └───────────────────────→ time
  
SS = Slow Start
CA = Congestion Avoidance
Spadek = Packet loss (timeout/3×dupACK)
```

## ⏱️ Retransmisja

### RTO (Retransmission Timeout)
```
Dynamiczny timeout na podstawie RTT:

SRTT (Smoothed RTT):
  SRTT = (1-α)×SRTT + α×RTT_sample
  α = 1/8

RTTVAR (RTT Variance):
  RTTVAR = (1-β)×RTTVAR + β×|SRTT - RTT_sample|
  β = 1/4

RTO:
  RTO = SRTT + 4×RTTVAR
  Min: 1 second (RFC)

Exponential Backoff:
  Timeout 1: RTO
  Timeout 2: 2×RTO
  Timeout 3: 4×RTO
  ...
```

### Selective Acknowledgment (SACK)
```
Problem z cumulative ACK:
Otrzymano: 1-100, 201-300 (brak 101-200)
Bez SACK: ACK=101 (tylko do 100)
→ Retransmituj całe 101-300

Z SACK:
ACK=101, SACK 201-300
→ Retransmituj tylko 101-200

Option SACK w nagłówku TCP
```

## 🔍 Stany TCP

### Diagram Stanów
```
CLOSED → LISTEN (server)
       → SYN_SENT (client) → SYN_RECEIVED → ESTABLISHED
                                           ↓
                                     FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED
                                           ↓
                                     CLOSE_WAIT → LAST_ACK → CLOSED

Stany:
CLOSED:       Brak połączenia
LISTEN:       Serwer nasłuchuje
SYN_SENT:     Wysłano SYN, czeka na SYN-ACK
SYN_RECEIVED: Otrzymano SYN, wysłano SYN-ACK
ESTABLISHED:  Połączenie aktywne
FIN_WAIT_1:   Wysłano FIN
FIN_WAIT_2:   Otrzymano ACK na FIN
CLOSE_WAIT:   Otrzymano FIN, aplikacja jeszcze nie zamknęła
CLOSING:      Obie strony FIN jednocześnie
LAST_ACK:     Wysłano FIN, czeka na ACK
TIME_WAIT:    Czeka 2×MSL
```

### Sprawdzanie Stanów
```bash
# Linux
netstat -tan | grep ESTABLISHED
ss -tan state established

# Windows
netstat -ano | findstr ESTABLISHED
```

## 🛠️ TCP Options

### Popularne Opcje
```
MSS (Maximum Segment Size):
- Kind=2, Length=4, MSS=1460

Window Scale:
- Kind=3, Length=3, Shift=7
- Rzeczywisty window = advertised × 2^7

SACK Permitted:
- Kind=4, Length=2

SACK:
- Kind=5, Length=variable
- Bloki odebranych danych

Timestamps:
- Kind=8, Length=10
- TSval, TSecr
- RTT measurement, PAWS

NOP (No Operation):
- Kind=1, Length=1
- Padding/alignment
```

## 🔗 Powiązane Tematy

- [[warstwa_transportowa|Warstwa Transportowa]]
- [[protokol_udp|UDP - User Datagram Protocol]]
- [[protokol_ip|Protokół IP]]
- [[narzedzia_diagnostyczne|Narzędzia Diagnostyczne]]
- [[SIECI KOMPUTEROWE]]

---

#tcp #transmission-control-protocol #three-way-handshake #flow-control #congestion-control #warstwa-transportowa
