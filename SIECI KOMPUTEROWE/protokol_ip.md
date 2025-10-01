# 🔄 Protokół IP - Internet Protocol

## 📋 Definicja

IP (Internet Protocol) to bezpołączeniowy protokół warstwy sieciowej (warstwa 3), odpowiedzialny za adresowanie i routing pakietów między sieciami. Stanowi podstawę działania Internetu.

## 🌐 IPv4 (Internet Protocol version 4)

### Struktura Pakietu IPv4
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |         Header Checksum       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Options (if IHL > 5)                       |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                            Data                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Pola Nagłówka IPv4

#### Version (4 bity)
```
Wersja protokołu IP
IPv4: 0100 (4)
IPv6: 0110 (6)
```

#### IHL - Internet Header Length (4 bity)
```
Długość nagłówka w 32-bitowych słowach
Wartość: 5-15
Min (bez opcji): 5 × 4 = 20 bajtów
Max (z opcjami): 15 × 4 = 60 bajtów
```

#### Type of Service / DSCP (8 bitów)
```
Klasyfikacja ruchu (QoS)

Stare (ToS):
- Precedence (3 bity): Priorytet
- Delay (1 bit): Niskie opóźnienie
- Throughput (1 bit): Wysoka przepustowość
- Reliability (1 bit): Niezawodność

Nowe (DSCP - Differentiated Services):
- 6 bitów DSCP
- 2 bity ECN (Explicit Congestion Notification)

Przykładowe DSCP:
- EF (Expedited Forwarding): 46 (101110) - VoIP
- AF41: 34 (100010) - Video
- BE (Best Effort): 0 (000000) - Normalny ruch
```

#### Total Length (16 bitów)
```
Całkowita długość pakietu (nagłówek + dane)
Max: 65535 bajtów
Typowo: 1500 bajtów (Ethernet MTU)
```

#### Identification (16 bitów)
```
Unikatowy ID pakietu
Używany do składania fragmentów
Każdy pakiet ma unikalny ID
```

#### Flags (3 bity)
```
Bit 0: Reserved (0)
Bit 1: DF (Don't Fragment)
       1 = Nie fragmentuj (wyślij ICMP if > MTU)
       0 = Można fragmentować
Bit 2: MF (More Fragments)
       1 = Są kolejne fragmenty
       0 = Ostatni fragment (lub nie fragmentowano)
```

#### Fragment Offset (13 bitów)
```
Pozycja fragmentu w oryginalnym pakiecie
Jednostka: 8 bajtów
Zakres: 0-8191 × 8 = 0-65528 bajtów

Przykład:
Fragment 1: Offset=0    (bajty 0-1479)
Fragment 2: Offset=185  (bajty 1480-2959) [1480/8=185]
Fragment 3: Offset=370  (bajty 2960-...)  [2960/8=370]
```

#### TTL - Time to Live (8 bitów)
```
Maksymalna liczba hopów (routerów)
Każdy router dekrementuje TTL o 1
TTL=0 → Router dropuje + ICMP Time Exceeded

Typowe wartości początkowe:
- Windows: 128
- Linux: 64
- Cisco: 255

Zastosowania:
- Zapobieganie pętlom
- traceroute (TTL=1, 2, 3, ...)
```

#### Protocol (8 bitów)
```
Protokół warstwy wyższej

Popularne:
1   - ICMP (Internet Control Message Protocol)
2   - IGMP (Internet Group Management Protocol)
6   - TCP (Transmission Control Protocol)
17  - UDP (User Datagram Protocol)
41  - IPv6 (IPv6 encapsulation)
47  - GRE (Generic Routing Encapsulation)
50  - ESP (Encapsulating Security Payload - IPsec)
51  - AH (Authentication Header - IPsec)
89  - OSPF (Open Shortest Path First)
```

#### Header Checksum (16 bitów)
```
Suma kontrolna TYLKO nagłówka (nie danych)
Weryfikacja integralności nagłówka

Przeliczany przez każdy router (TTL się zmienia)

Algorytm:
1. Ustaw checksum=0
2. Sumuj 16-bitowe słowa nagłówka
3. One's complement sumy
```

#### Source/Destination Address (32 bity każdy)
```
Adresy IPv4

Format: A.B.C.D (4 oktety)
Przykład:
Source: 192.168.1.10
Destination: 8.8.8.8
```

## 📦 Fragmentacja IPv4

### Proces Fragmentacji
```
Oryginalny pakiet: 3000 bajtów (MTU=1500)

┌─────────────────────────────────────┐
│ IP Header (20) │     Data (2980)    │  Total: 3000B
└─────────────────────────────────────┘

Fragment 1:
┌────────────────────────────────────┐
│ IP (20) │ Data (1480)              │  Total: 1500B
│ ID=123  │ Offset=0, MF=1           │
└────────────────────────────────────┘

Fragment 2:
┌────────────────────────────────────┐
│ IP (20) │ Data (1480)              │  Total: 1500B
│ ID=123  │ Offset=185, MF=1         │
└────────────────────────────────────┘

Fragment 3:
┌────────────────────────────────────┐
│ IP (20) │ Data (20)                │  Total: 40B
│ ID=123  │ Offset=370, MF=0         │
└────────────────────────────────────┘

Wszystkie fragmenty mają ten sam ID=123
```

### Path MTU Discovery (PMTUD)
```
Cel: Znalezienie max MTU w całej ścieżce

Proces:
1. Wyślij pakiet z DF=1 (Don't Fragment)
2. Jeśli MTU za mały → ICMP Fragmentation Needed
3. Zmniejsz MTU i spróbuj ponownie
4. Powtarzaj aż pakiet przejdzie

Problem:
- ICMP często blokowany przez firewalle
- Black hole routing

Rozwiązanie:
- PLPMTUD (Packetization Layer PMTUD)
- TCP MSS clamping
```

## 🌍 IPv6 (Internet Protocol version 6)

### Struktura Pakietu IPv6
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version| Traffic Class |           Flow Label                  |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Payload Length        |  Next Header  |   Hop Limit   |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                                                               +
|                                                               |
+                         Source Address                        +
|                                                               |
+                                                               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                                                               |
+                                                               +
|                                                               |
+                      Destination Address                      +
|                                                               |
+                                                               +
|                                                               |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```

### Główne Różnice IPv6 vs IPv4

#### Stały Rozmiar Nagłówka
```
IPv6: Zawsze 40 bajtów (bez opcji w głównym nagłówku)
IPv4: 20-60 bajtów (z opcjami)

Zaleta: Szybsze przetwarzanie (bez potrzeby IHL)
```

#### Brak Fragmentacji przez Routery
```
IPv6: Tylko host źródłowy fragmentuje
Router: Jeśli pakiet > MTU → ICMPv6 Packet Too Big

Zaleta: Mniej obciążenia routerów
```

#### Brak Checksum
```
IPv6: Brak checksum w nagłówku IP
Powód: Warstwy 2 i 4 mają checksums

Zaleta: Szybsze przetwarzanie
```

#### Extension Headers
```
IPv6 używa rozszerzających nagłówków zamiast opcji:

Next Header wskazuje typ kolejnego nagłówka:
- 6: TCP
- 17: UDP
- 58: ICMPv6
- 0: Hop-by-Hop Options
- 43: Routing
- 44: Fragment
- 50: ESP (IPsec)
- 51: AH (IPsec)
- 60: Destination Options

Chain:
[IPv6][Hop-by-Hop][Routing][Fragment][TCP][Data]
  NH=0      NH=43     NH=44   NH=6
```

### Pola Nagłówka IPv6

#### Version (4 bity)
```
Wartość: 6 (0110)
```

#### Traffic Class (8 bitów)
```
Odpowiednik ToS/DSCP w IPv4
QoS, priorytetyzacja ruchu
```

#### Flow Label (20 bitów)
```
Identyfikacja "flow" (strumienia pakietów)
QoS per-flow
Routing optimization
```

#### Payload Length (16 bitów)
```
Długość payload (bez głównego nagłówka 40B)
Max: 65535 bajtów
Jumbo packets: Extension header (> 65535)
```

#### Next Header (8 bitów)
```
Typ kolejnego nagłówka
Odpowiednik Protocol w IPv4
```

#### Hop Limit (8 bitów)
```
Odpowiednik TTL w IPv4
Każdy router dekrementuje
0 → ICMPv6 Time Exceeded
```

## 🔄 Adresowanie IPv4 vs IPv6

### IPv4
```
32 bity (4 bajty)
Format: 192.168.1.1
Adresy: ~4.3 miliarda
Problem: Wyczerpanie adresów

Rozwiązania:
- NAT (Network Address Translation)
- CIDR (Classless Inter-Domain Routing)
- IPv6
```

### IPv6
```
128 bitów (16 bajtów)
Format: 2001:db8::1
Adresy: 340 undecillion (3.4×10^38)

Zalety:
✓ Ogromna przestrzeń adresowa
✓ Brak potrzeby NAT
✓ Autoconfiguration (SLAAC)
✓ Built-in IPsec
✓ Lepszy multicast
```

## 📊 Typy Adresów

### IPv4
```
Unicast:    Jeden host (192.168.1.10)
Broadcast:  Wszyscy w sieci (255.255.255.255)
Multicast:  Grupa hostów (224.0.0.0/4)
Anycast:    Najbliższy z grupy (implementacja lokalna)
```

### IPv6
```
Unicast:    Jeden host
  - Global:    2000::/3 (Internet)
  - Link-local: fe80::/10
  - Unique local: fc00::/7

Multicast:  Grupa (ff00::/8)
  - ff02::1 (all nodes)
  - ff02::2 (all routers)

Anycast:    Ten sam adres, najbliższy routing
  - Subnet-Router anycast

Brak broadcast! (zastąpiony multicast)
```

## 🛠️ Opcje IPv4

### Record Route
```
Zapisuje adresy IP routerów w ścieżce
Max: 9 adresów (ograniczenie 40B opcji)
```

### Source Routing
```
Strict: Określa dokładną ścieżkę
Loose: Określa niektóre routery w ścieżce

Security risk → często blokowane
```

### Timestamp
```
Rejestruje czas przejścia przez routery
```

## 🔍 Diagnostyka

### IPv4
```bash
# Wyświetl routing
ip route show
route -n

# Test połączenia
ping 8.8.8.8
ping -c 4 -s 1500 8.8.8.8  # Fragmentacja

# Traceroute
traceroute 8.8.8.8
```

### IPv6
```bash
# Wyświetl adresy
ip -6 addr show

# Routing
ip -6 route show

# Test
ping6 2001:4860:4860::8888
traceroute6 google.com
```

### Analiza Pakietów
```bash
# tcpdump
tcpdump -i eth0 ip
tcpdump -i eth0 ip6

# Wireshark filters
ip.addr == 192.168.1.100
ipv6.addr == 2001:db8::1
ip.flags.df == 1        # Don't Fragment
ip.flags.mf == 1        # More Fragments
```

## 🔗 Powiązane Tematy

- [[warstwa_sieciowa|Warstwa Sieciowa]]
- [[adresowanie_ip|Adresowanie IP (IPv4 i IPv6)]]
- [[routing_podstawy|Routing - Podstawy]]
- [[protokol_tcp|TCP]]
- [[SIECI KOMPUTEROWE]]

---

#ip #ipv4 #ipv6 #internet-protocol #warstwa-sieciowa #fragmentacja #routing
