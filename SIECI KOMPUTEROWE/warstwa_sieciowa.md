# 3️⃣ Warstwa Sieciowa (Network Layer)

## 📋 Definicja

Warstwa sieciowa odpowiada za routing pakietów między różnymi sieciami. Zapewnia adresowanie logiczne (IP), wybór najlepszej ścieżki (routing) oraz fragmentację i ponowne składanie pakietów.

## 🔧 Główne Funkcje

### 1. Adresowanie Logiczne (IP)
- Przypisywanie unikalnych adresów IP urządzeniom
- Identyfikacja sieci i hosta
- Hierarchiczna struktura adresów

### 2. Routing (Trasowanie)
- Wybór najlepszej ścieżki do sieci docelowej
- Utrzymywanie tablic routingu
- Przekazywanie pakietów do właściwego następnego przeskoku (next hop)

### 3. Fragmentacja i Reassembly
- Dzielenie dużych pakietów na mniejsze fragmenty (MTU)
- Ponowne składanie fragmentów w miejscu docelowym

### 4. Kontrola Przekazywania
- Określanie czasu życia pakietu (TTL)
- Zapobieganie nieskończonym pętlom

## 📦 Protokół IP (Internet Protocol)

### IPv4
**Format adresu**: 32 bity (4 bajty)
```
Notacja dziesiętna: 192.168.1.100
Notacja binarna: 11000000.10101000.00000001.01100100

Struktura pakietu IPv4:
┌────────┬────────┬─────────┬──────────┬─────────┬─────┬────────┐
│Version │  IHL   │   ToS   │  Total   │   ID    │Flags│Fragment│
│  4 bit │  4 bit │  1 bajt │  Length  │ 2 bajty │3 bit│Offset  │
├────────┴────────┴─────────┴──────────┴─────────┴─────┴────────┤
│         TTL     │Protocol │ Header Checksum │  Src IP Address │
│       1 bajt    │ 1 bajt  │    2 bajty      │    4 bajty      │
├──────────────────────────────────────────────┴─────────────────┤
│                    Dest IP Address (4 bajty)                   │
├────────────────────────────────────────────────────────────────┤
│                    Options + Padding (opcjonalne)              │
├────────────────────────────────────────────────────────────────┤
│                           Data                                 │
└────────────────────────────────────────────────────────────────┘
```

**Kluczowe pola**:
- **TTL** (Time To Live): Maksymalna liczba skoków (każdy router dekrementuje)
- **Protocol**: TCP (6), UDP (17), ICMP (1)
- **Flags**: DF (Don't Fragment), MF (More Fragments)

### IPv6
**Format adresu**: 128 bitów (16 bajtów)
```
Notacja: 2001:0db8:85a3:0000:0000:8a2e:0370:7334
Skrócona: 2001:db8:85a3::8a2e:370:7334

Struktura pakietu IPv6:
┌──────────┬────────────┬────────────┬─────────────┐
│ Version  │Traffic Class│ Flow Label │Payload Len │
│  4 bit   │   8 bit    │  20 bit    │  2 bajty   │
├──────────┴────────────┴────────────┴─────────────┤
│  Next Header  │  Hop Limit  │                    │
│    1 bajt     │   1 bajt    │                    │
├───────────────┴─────────────┤                    │
│    Source Address (128 bit / 16 bajtów)          │
│                                                   │
├──────────────────────────────────────────────────┤
│    Destination Address (128 bit / 16 bajtów)     │
│                                                   │
├──────────────────────────────────────────────────┤
│                   Data                           │
└──────────────────────────────────────────────────┘
```

**Zalety IPv6**:
- Ogromna przestrzeń adresowa (2^128)
- Prostsza struktura nagłówka
- Wbudowane IPsec
- Brak konieczności NAT
- Autoconfiguration (SLAAC)

## 🗺️ Klasy Adresów IPv4 (Classful)

```
Klasa A: 0.0.0.0     - 127.255.255.255   (Maska: /8  lub 255.0.0.0)
         Format: 0NNNNNNN.HHHHHHHH.HHHHHHHH.HHHHHHHH
         
Klasa B: 128.0.0.0   - 191.255.255.255   (Maska: /16 lub 255.255.0.0)
         Format: 10NNNNNN.NNNNNNNN.HHHHHHHH.HHHHHHHH
         
Klasa C: 192.0.0.0   - 223.255.255.255   (Maska: /24 lub 255.255.255.0)
         Format: 110NNNNN.NNNNNNNN.NNNNNNNN.HHHHHHHH
         
Klasa D: 224.0.0.0   - 239.255.255.255   (Multicast)
Klasa E: 240.0.0.0   - 255.255.255.255   (Eksperymentalne)

N = Network bits
H = Host bits
```

## 🔀 Routing (Trasowanie)

### Tablica Routingu
```
Destination     Gateway         Genmask         Iface
0.0.0.0         192.168.1.1     0.0.0.0         eth0      # Default route
192.168.1.0     0.0.0.0         255.255.255.0   eth0      # Direct connection
10.0.0.0        192.168.1.254   255.0.0.0       eth0      # Static route
```

### Typy Routingu

#### Static Routing (Statyczny)
- Ręczna konfiguracja tras
- Nie zmienia się automatycznie
- Używany w małych sieciach

```bash
# Linux
ip route add 10.0.0.0/8 via 192.168.1.254

# Windows
route add 10.0.0.0 mask 255.0.0.0 192.168.1.254

# Cisco
ip route 10.0.0.0 255.0.0.0 192.168.1.254
```

#### Dynamic Routing (Dynamiczny)
Protokoły:
- **RIP** (Routing Information Protocol): Distance vector, max 15 hopów
- **OSPF** (Open Shortest Path First): Link state, metryka cost
- **EIGRP** (Enhanced Interior Gateway Routing Protocol): Cisco, hybrid
- **BGP** (Border Gateway Protocol): Routing między AS (Internet)

### Metryki Routingu
- **Hop count**: Liczba routerów (RIP)
- **Bandwidth**: Przepustowość łącza (OSPF, EIGRP)
- **Delay**: Opóźnienie
- **Load**: Obciążenie łącza
- **Reliability**: Niezawodność

## 🔄 Protokoły Pomocnicze

### ICMP (Internet Control Message Protocol)
**Typy komunikatów**:
```
Type 0:  Echo Reply (pong)
Type 3:  Destination Unreachable
Type 5:  Redirect
Type 8:  Echo Request (ping)
Type 11: Time Exceeded (traceroute)
```

**Narzędzia wykorzystujące ICMP**:
- **ping**: Sprawdzenie dostępności hosta
- **traceroute/tracert**: Śledzenie ścieżki pakietu

```bash
# Ping
ping 8.8.8.8
ping6 2001:4860:4860::8888

# Traceroute
traceroute google.com        # Linux/Mac
tracert google.com           # Windows
```

### ARP (Address Resolution Protocol)
- Mapowanie IP → MAC w sieci lokalnej
- Technicznie warstwa 2, ale współpracuje z warstwą 3

### IGMP (Internet Group Management Protocol)
- Zarządzanie grupami multicast
- Pozwala routerowi wiedzieć, które hosty należą do grupy multicast

## 🌐 Adresy Specjalne IPv4

```
0.0.0.0/8           - "This network"
10.0.0.0/8          - Prywatne (RFC 1918)
127.0.0.0/8         - Loopback (localhost)
169.254.0.0/16      - Link-local (APIPA)
172.16.0.0/12       - Prywatne (RFC 1918)
192.168.0.0/16      - Prywatne (RFC 1918)
224.0.0.0/4         - Multicast
255.255.255.255     - Broadcast (limited)
```

## ⚙️ Urządzenia Warstwy Sieciowej

### Router
- **Funkcje**:
  - Routing między różnymi sieciami
  - NAT/PAT
  - Filtrowanie pakietów (ACL)
  - QoS

- **Decyzje routingu**:
```
1. Sprawdź adres docelowy pakietu
2. Przeszukaj tablicę routingu:
   a) Najdłuższe dopasowanie prefiksu (longest prefix match)
   b) Jeśli brak - użyj trasy domyślnej (0.0.0.0/0)
   c) Jeśli brak trasy - odrzuć pakiet (ICMP Unreachable)
3. Przekaż pakiet do interfejsu wyjściowego
4. Zmniejsz TTL o 1
5. Przelicz checksum
```

### Layer 3 Switch
- Switch z funkcjami routingu
- Szybszy routing między VLAN
- Używany w sieciach korporacyjnych

## 🔐 Bezpieczeństwo Warstwy Sieciowej

### IPsec
- Szyfrowanie i autentykacja pakietów IP
- Tryby:
  - **Transport mode**: Tylko dane
  - **Tunnel mode**: Cały pakiet IP

### ACL (Access Control Lists)
```cisco
# Cisco ACL - blokuj ruch z 10.0.0.0/8 do 192.168.1.100
access-list 100 deny ip 10.0.0.0 0.255.255.255 host 192.168.1.100
access-list 100 permit ip any any

interface GigabitEthernet0/0
 ip access-group 100 in
```

## 🛠️ Komendy Diagnostyczne

### Sprawdzenie konfiguracji IP
```bash
# Linux
ip addr show
ip route show

# Windows
ipconfig
route print

# Mac
ifconfig
netstat -nr
```

### Testowanie routingu
```bash
# Ping
ping -c 4 8.8.8.8

# Traceroute
traceroute -n google.com
mtr google.com  # Linux - continuous traceroute
```

### Analiza pakietów
```bash
# tcpdump
tcpdump -i eth0 icmp
tcpdump -i eth0 host 192.168.1.100

# Wireshark (GUI)
# Filtry: ip.addr == 192.168.1.100
#         icmp
```

## 🔗 Powiązane Tematy

- [[warstwa_laczna|Warstwa Łącza Danych]]
- [[warstwa_transportowa|Warstwa Transportowa]]
- [[protokol_ip|Protokół IP]]
- [[adresowanie_ip|Adresowanie IP]]
- [[routing_podstawy|Routing - Podstawy]]
- [[router_dzialanie|Router - Działanie]]
- [[nat_pat|NAT i PAT]]
- [[SIECI KOMPUTEROWE]]

---

#warstwa-sieciowa #network-layer #ip #routing #ipv4 #ipv6 #icmp #osi-layer3
